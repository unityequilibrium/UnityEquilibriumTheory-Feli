# UET Multi-Agent RAG — Implementation Plan

## Background

Comprehensive plan for building the UET Multi-Agent RAG system, synthesized from:
- [architecture_analysis.md.resolved](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/v/architecture_analysis.md.resolved) — Full architecture report
- [embeddings_and_models_analysis.md.resolved](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/v/embeddings_and_models_analysis.md.resolved) — Embedding & model strategy
- [01.md](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/v/01.md) — UET Tensorizer design guide
- [00.md](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/v/00.md) — Previous failure lessons

**Disk:** 12.9 GB free ✅ | **Target:** Python first → Rust migration

---

## User Review Required

> [!IMPORTANT]
> **API Key Management:** User requested per-key, per-agent cost tracking structure.
> Each OpenRouter call will be tagged with `agent_id` and logged to track costs per function.

> [!WARNING]
> **API Key Needed:** User must register at [openrouter.ai](https://openrouter.ai) and create API key(s) before Phase 2.
> The plan below includes a key management system so user can see exactly which agent spends what.

---

---

## Implemented Architecture (Status: Completed)

### Phase 1: Foundation — Project Structure & Config (Completed ✅)

#### [EXISTING] [config.toml](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/knowledge_base/config.toml)

#### [NEW] [config.toml](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/knowledge_base/config.toml)

Central config — all API keys, model assignments, cost budgets in one place:

```toml
[openrouter]
base_url = "https://openrouter.ai/api/v1"

# === API Keys — แยกตาม function ===
[openrouter.keys]
# ถ้าใช้ key เดียว ใส่ที่ default แล้ว agent อ้าง key นี้
default = "sk-or-v1-xxxx"     # <-- ใส่ key ตรงนี้

# ถ้าอยากแยก key ต่อ agent (optional — เพื่อ track cost แยก)
# embedding = "sk-or-v1-embed-xxxx"
# orchestrator = "sk-or-v1-orch-xxxx"

# === Model Assignment ต่อ Agent ===
[agents.orchestrator]
model = "qwen/qwen3-coder-next"
key_name = "default"                  # ใช้ key ไหน
max_tokens_per_call = 4096
daily_budget_usd = 0.50               # budget limit

[agents.local_data]
model = "zhipu/glm-4.7-flash"
key_name = "default"
max_tokens_per_call = 2048
daily_budget_usd = 0.20

[agents.web_research]
model = "deepseek/deepseek-v3.2"
key_name = "default"
max_tokens_per_call = 4096
daily_budget_usd = 0.30

[agents.equation_expert]
model = "qwen/qwen3-30b-a3b:free"    # Free tier first
key_name = "default"
max_tokens_per_call = 4096
daily_budget_usd = 0.00

[agents.embedding]
model = "qwen/qwen3-embedding-8b"
key_name = "default"
daily_budget_usd = 0.50               # สำหรับ batch embed

# === Vector DB ===
[vector_db]
engine = "lancedb"                    # lancedb | sqlite_vss | qdrant
path = "./knowledge_base/vectors"
embedding_dim = 1024

# === Cost Tracking ===
[cost_tracking]
log_file = "./knowledge_base/cost_log.jsonl"
alert_threshold_usd = 1.00            # แจ้งเตือนเมื่อใช้เกิน
```

#### [NEW] [__init__.py](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/knowledge_base/__init__.py)

Package init — ว่าง

#### [NEW] [api_client.py](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/knowledge_base/api_client.py)

OpenRouter API client พร้อม **cost tracking per agent**:

```python
class CostTracker:
    """Track API costs per agent, per model, per day"""
    # Logs every call to cost_log.jsonl:
    # {"timestamp", "agent_id", "model", "input_tokens", "output_tokens",
    #  "cost_usd", "cumulative_daily_usd"}
    
class OpenRouterClient:
    """Unified OpenRouter client with agent-aware routing"""
    def embed(self, texts: list[str]) -> list[list[float]]
    def chat(self, agent_id: str, messages: list[dict]) -> str
    # Each call auto-logs to CostTracker
    # Respects daily_budget_usd per agent — raises BudgetExceeded if over
```

---

### Phase 2: UET Tensorizer — Physics-derived Embeddings (Completed ✅)

#### [NEW] [tensorizer.py](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/knowledge_base/tensorizer.py)

Per [01.md](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/v/01.md) design, using real UET engine:

```python
@dataclass
class UetVector:
    """Rust-compatible, serde-compatible"""
    omega: float          # จาก uet_master_equation.compute_omega()
    kappa: float          # จาก uet_parameters
    beta: float           # coupling strength
    entropy: float        # Shannon H ของเนื้อหา
    axiom_signature: list[bool]  # len=12
    topic_id: str
    content_hash: bytes   # sha256, 32 bytes

class UetTensorizer:
    """Convert research files → UetVector using real UET engine"""
    def __init__(self):
        self.engine = UETMasterEquation(...)  # import from core
    
    def tensorize_file(self, filepath: Path) -> UetVector:
        # 1. Read file content
        # 2. Compute Ω, κ, β via uet_master_equation.py
        # 3. Compute Shannon entropy H
        # 4. Detect axiom references → 12-bit signature
        # 5. Return UetVector
```

---

### Phase 3: Hybrid Vector Store (Completed: SQLite+UET) ✅

#### [NEW] [vector_store.py](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/knowledge_base/vector_store.py)

LanceDB embedded store:

```python
class HybridVectorStore:
    """Semantic + UET physics vectors in LanceDB"""
    
    # Schema per record:
    # | semantic_vec (1024d) | uet_vec (~20d) | metadata JSON |
    
    def insert(self, file_path, semantic_embed, uet_vector, metadata)
    def search_semantic(self, query_embed, top_k=10)
    def search_omega(self, target_omega_range, top_k=10)  # Ω-Search
    def search_hybrid(self, query_embed, uet_params, alpha=0.7, top_k=10)
```

#### [NEW] [omega_search.py](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/knowledge_base/omega_search.py)

UET Ω-minimization search engine:

```python
class OmegaSearchEngine:
    """Physics-informed similarity search"""
    def compute_relevance(self, query_field, result_field) -> float:
        omega_gap = self.engine.compute_omega(query_field, result_field)
        return 1.0 / (1.0 + omega_gap)
    
    def search(self, query, filters=None) -> list[SearchResult]
```

---

### Phase 4: Ingestion Pipeline (Completed ✅)

#### [NEW] [ingest.py](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/knowledge_base/ingest.py)

Scan → tensorize → embed → store:

```python
class IngestionPipeline:
    """Process research_uet/topics/ → LanceDB"""
    def ingest_topic(self, topic_path: Path) -> int  # returns count
    def ingest_all(self, dry_run=False) -> dict       # returns stats
    # Supports: .py, .md, data_logs/*
    # Chunks large files → multiple vectors
```

---

### Phase 5: Cost Dashboard & Monitoring (Completed ✅)

#### [NEW] [cost_dashboard.py](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/knowledge_base/cost_dashboard.py)

CLI tool to view costs:

```
$ python -m research_uet.knowledge_base.cost_dashboard

╔══════════════════════════════════════════════════════════╗
║              API Cost Report — 2026-02-11               ║
╠══════════════════════════════════════════════════════════╣
║ Agent          │ Model              │ Calls │ Cost USD  ║
║────────────────┼────────────────────┼───────┼───────────║
║ embedding      │ qwen3-embedding-8b │  450  │ $0.09     ║
║ orchestrator   │ qwen3-coder-next   │   12  │ $0.03     ║
║ local_data     │ glm-4.7-flash      │   28  │ $0.02     ║
║ web_research   │ deepseek-v3.2      │    3  │ $0.04     ║
║ equation_expert│ qwen3-30b (free)   │    8  │ $0.00     ║
║────────────────┼────────────────────┼───────┼───────────║
║ TOTAL          │                    │  501  │ $0.18     ║
╚══════════════════════════════════════════════════════════╝
```

---

## File Structure Summary

```
research_uet/knowledge_base/           # ← NEW directory
├── __init__.py                         # Package init
├── config.toml                         # API keys, models, budgets
├── api_client.py                       # OpenRouter client + CostTracker
├── tensorizer.py                       # UET physics → vectors
├── vector_store.py                     # LanceDB hybrid store
├── omega_search.py                     # Ω-minimization search
├── ingest.py                           # Bulk ingestion pipeline
├── cost_dashboard.py                   # Cost tracking CLI
├── vectors/                            # LanceDB data (auto-created)
└── cost_log.jsonl                      # Per-call cost log (auto-created)
```

---

## Build Order (ทำทีละ module → test → discuss → ต่อ)

| # | Module | Dependencies | Test Method |
|:--|:-------|:-------------|:------------|
| 1 | `config.toml` + [__init__.py](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/__init__.py) | None | Load & validate config |
| 2 | `api_client.py` + `CostTracker` | config.toml | Unit test: mock API, verify cost log |
| 3 | `tensorizer.py` | [core/uet_master_equation.py](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/core/uet_master_equation.py) | **Test with 1 file first → discuss** |
| 4 | `vector_store.py` | lancedb (pip install) | CRUD test with 10 vectors |
| 5 | `omega_search.py` | tensorizer + vector_store | Search test: "find κ > 0.5" |
| 6 | `ingest.py` | all above | **Dry-run → report stats → discuss** |
| 7 | `cost_dashboard.py` | cost_log.jsonl | Visual verification |

> [!IMPORTANT]
> **Rule from 00.md:** ทำทีละขั้น — สร้าง 1 module → ทดสอบ → คุย → แล้วค่อยต่อ

---

## Verification Plan

### Automated Tests

Each module gets a test file in `research_uet/knowledge_base/tests/`:

1. **`test_api_client.py`** — Mock OpenRouter API, verify:
   - Cost tracking writes correct JSONL
   - Budget limits raise `BudgetExceeded`
   - Agent routing uses correct model
   ```
   python -m pytest research_uet/knowledge_base/tests/test_api_client.py -v
   ```

2. **`test_tensorizer.py`** — Verify against real UET engine:
   - Tensorize 1 file from `0.0_Grand_Unification/`
   - Check Ω, κ, β are non-zero floats (not NaN)
   - Check axiom_signature is 12-bit
   - Check output is JSON-serializable (Rust-compatible)
   ```
   python -m pytest research_uet/knowledge_base/tests/test_tensorizer.py -v
   ```

3. **`test_vector_store.py`** — LanceDB CRUD:
   - Insert 10 test vectors → search → verify ranking
   - Hybrid search: semantic + Ω combined
   ```
   python -m pytest research_uet/knowledge_base/tests/test_vector_store.py -v
   ```

### Manual Verification (After Phase 6 ingestion)

1. **Run cost dashboard** — User visually confirms per-agent cost breakdown
2. **Test search** — User queries "find all topics related to Grand Unification" and verifies results make physics sense
3. **Check cost_log.jsonl** — User opens file to verify each API call is logged with agent_id and cost

### Pre-existing Tests

Existing tests in [research_uet/core/test/](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/core/test/) confirm the UET engine works correctly:
```
python -m pytest research_uet/core/test/ -v
```
These must pass before tensorizer can delegate to the engine.

---

## Phase 11: Data Ingestion & Preservation Strategy (Active)

### Goal
Organize disperse data sources into a unified, searchable archive without damaging original research or history.

### 1. `research_uet` (Active Research)
- **Policy:** **Stable/Index-Only**.
- **Action:** No restructuring. Agents will index this directory "in-place".
- **Role:** The primary source of truth for current UET development.

### 2. `(search Only) ทองข้อมูลดี` (Work History Archive)
- **Policy:** **Clean & Restructure**.
- **Action:**
    - Create top-level `history/` directory.
    - **Filter out junk:** Remove/Move to `trash_waiting/` redundant `.html` logs, obsolete `.ps1` scripts, and `.tmp` files.
    - **Categorize:** Move valuable history into:
        - `history/documents/` (PDfs, Master Blueprints)
        - `history/old_code/` (Historical scripts)
        - `history/archives/` (ZIP files)
- **Role:** Historical context for the UET project.

### 3. Ingestion into `uet_kb`
- Both sources will be ingested into the Rust Knowledge Base with metadata tags:
    - `{ "source": "research_active" }`
    - `{ "source": "work_history" }`
- This ensures the `uet_agents` can distinguish between what is "current" and what is "historical".

---

## Final Verification Checklist
- [ ] Dry-run ingestion on `research_uet`
- [ ] Propose specific "Delete List" for `ทองข้อมูลดี` junk files
- [ ] User approval for `history/` restructuring
- [ ] Execution of move/clean-up command
- [ ] Build final `uet_kb` index
