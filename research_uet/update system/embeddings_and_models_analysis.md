# UET Embeddings & AI Model Strategy

**Date:** 2026-02-11 | **Status:** Research Complete

---

## 1. UET-Based Embeddings — สิ่งที่มีอยู่แล้ว

### 1.1 UET Tensorizer Design ([walkthrough.md](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/v/walkthrough.md))

> [!IMPORTANT]
> โปรเจกต์มี design ที่ดีมากสำหรับ physics-informed embeddings อยู่แล้ว — ต้อง implement ตาม design นี้

แต่ละเอกสาร/ไฟล์จะถูก embed เป็น **UET Vector** ที่มาจากสมการจริง:

| Feature | Source | Meaning |
|:--------|:-------|:--------|
| **Ω (Omega)** | `Ω = ∫(C−I)² dx` | Gap reality↔information |
| **κ (Kappa)** | [uet_parameters.py](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/core/uet_parameters.py) | Information diffusion rate |
| **β (Beta)** | Coupling strength | C↔I linkage |
| **Shannon H** | `H = −Σ pᵢ log₂ pᵢ` | Information density |
| **Axiom Sig** | 12-bit binary | Which axioms referenced |
| **Topic Coupling** | βᵢⱼ matrix | Cross-topic connections |

### 1.2 Ω-Search (Similarity via Physics)

```python
# ❌ Generic: cosine(a, b)
# ✅ UET: minimize Ω-gap
Ω_gap = compute_omega(query_field, result_field)
relevance = 1.0 / (1.0 + Ω_gap)
```

### 1.3 Living Code ([Developmental_Agent.py](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/topics/0.24_Artificial_Intelligence/Code/05_Developmental_AI/Developmental_Agent.py))

Agent ที่ **เรียนรู้ผ่าน UET dynamics จริงๆ**:
- Text → Information Field `I(x,y)` via semantic hashing
- Learning = minimizing Ω between Mind (`C`) and Knowledge (`I`)
- Parameters evolve: Infant (high temp, low β) → Adult (low temp, high β)

### 1.4 UET NanoGPT ([Research_NanoGPT_UET.py](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/topics/0.24_Artificial_Intelligence/Code/03_Research/Research_NanoGPT_UET.py))

[UETLanguageManifold](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/research_uet/topics/0.24_Artificial_Intelligence/Code/03_Research/Research_NanoGPT_UET.py#32-175) — N-gram language model ที่ใช้ **Holographic Associative Memory** concepts

---

## 2. Hybrid Embedding Strategy — แนะนำ

ออกแบบ embedding เป็น 2 layers:

### Layer 1: Semantic Embeddings (จาก AI Model)
ใช้สำหรับ **text search** — เข้าใจ "ความหมาย" ของเอกสาร

### Layer 2: UET Physics Embeddings (จาก Master Equation)
ใช้สำหรับ **physics-informed search** — Ω, κ, β, axiom signatures

### Combined Vector

```
Final Vector = [Semantic_Embed (768-1024d) | UET_Vector (~20d)]
```

Search = `α × semantic_similarity + (1-α) × Ω_relevance` — ถ่วงน้ำหนักได้

---

## 3. OpenRouter.ai Model Recommendations

### 3.1 Embedding Models (สำหรับ Vector DB)

| Model | Dimensions | Context | Price (input/M) | แนะนำ |
|:------|:-----------|:--------|:-----------------|:------|
| **Qwen3 Embedding 8B** | — | 32K | $0.01 | ⭐ **Best value** — multilingual, code-aware |
| **BAAI bge-m3** | 1024d | 8K | $0.01 | ⭐ Multilingual, proven |
| **Gemini Embedding 001** | — | 20K | $0.15 | Premium, MTEB #1 |
| **OpenAI text-embedding-3-small** | — | 8K | $0.02 | Budget-friendly |
| **OpenAI text-embedding-3-large** | — | 8K | $0.13 | Best OpenAI |
| Mistral Embed 2312 | 1024d | 8K | $0.10 | RAG-optimized |
| Mistral Codestral Embed | — | 8K | $0.15 | **Code-specific** |

> [!TIP]
> **แนะนำ: Qwen3 Embedding 8B** — ราคาถูกสุด ($0.01/M), context ยาว 32K, รองรับ multilingual ทั้ง EN/TH, ดีสำหรับ code+text

**Cost Estimate** (9,144 files × avg 2K tokens):
- Qwen3 8B: ~18M tokens → **$0.18** total ✅
- Gemini: ~18M tokens → **$2.70** total
- OpenAI small: ~18M tokens → **$0.36** total

---

### 3.2 Agent LLMs (สำหรับ Multi-Agent RAG)

#### 🆓 Free Tier (เริ่มต้น)

| Model | Context | Use Case |
|:------|:--------|:---------|
| **Aurora Alpha** | 128K | General agent — $0 |
| **Pony Alpha** | 200K | Coding + agentic — $0, #10 Programming |
| **StepFun Step 3.5 Flash** | 256K | Reasoning MoE — $0 |
| **Arcee Trinity Large** | 131K | Tech + Programming — $0 |
| **Arcee Trinity Mini** | 131K | Lightweight agent — $0 |
| **NVIDIA Nemotron Nano** | 256K | MoE agentic — $0 |

#### 💰 Budget ($0.05-0.30/M — แนะนำสำหรับ production)

| Model | Context | Price In/Out | Why |
|:------|:--------|:-------------|:----|
| **Qwen3 Coder Next** | 262K | $0.07/$0.30 | ⭐ **Best for MCP agent** — coding-focused, 80B MoE/3B active |
| **DeepSeek V3.2** | 164K | $0.25/$0.38 | ⭐ Reasoning + tool-use, IMO/IOI gold |
| **Mistral Devstral 2** | 262K | $0.05/$0.22 | ⭐ Agentic coding, open-source 123B |
| **Xiaomi MiMo V2 Flash** | 262K | $0.09/$0.29 | SWE-bench #1 open-source |
| **GLM 4.7 Flash** | 203K | $0.06/$0.40 | Agentic coding, 30B SOTA |
| **MiniMax M2.1** | 197K | $0.27/$0.95 | #2 Programming, 10B active |

#### 🧠 Multi-Agent Role Assignment

| Agent Role | Recommended Model | Why |
|:-----------|:------------------|:----|
| **Orchestrator** (Agent 0) | Qwen3 Coder Next | 262K context, cheap, agentic |
| **Local Data** (Agent 1) | GLM 4.7 Flash | Fast, tool-calling |
| **Web Research** (Agent 2) | DeepSeek V3.2 | Deep reasoning |
| **Equation Expert** (Agent 3) | Qwen3 30B Thinking | Math + reasoning, $0.05/$0.34 |
| **Embeddings** | Qwen3 Embedding 8B | Cheapest, multilingual |

---

## 4. Architecture Diagram — Hybrid Embedding + Multi-Agent

```
┌─────────────────────────────────────────────────────────┐
│                    User Query                           │
│            "Find research related to κ > 0.5"           │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│              Agent 0: Orchestrator                       │
│              (Qwen3 Coder Next via OpenRouter)           │
│              Parses intent → routes to agents            │
└───┬─────────────┬─────────────┬─────────────────────────┘
    │             │             │
    ▼             ▼             ▼
┌────────┐  ┌──────────┐  ┌──────────┐
│Agent 1 │  │ Agent 2  │  │ Agent 3  │
│Local   │  │ Web      │  │ Equation │
│Data    │  │ Research │  │ Expert   │
│(MCP)   │  │          │  │          │
└───┬────┘  └──────────┘  └──────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│                    Rust MCP Server                       │
│  ┌─────────────────┐  ┌────────────────────┐            │
│  │ Semantic Search  │  │ UET Physics Search │            │
│  │ (Qwen3 Embed)   │  │ (Ω-minimization)   │            │
│  │ via OpenRouter   │  │ via Master Equation│            │
│  └────────┬────────┘  └────────┬───────────┘            │
│           │                    │                         │
│           ▼                    ▼                         │
│  ┌─────────────────────────────────────┐                 │
│  │         LanceDB (Embedded)          │                 │
│  │  [semantic_vec | uet_vec | metadata]│                 │
│  └─────────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────┘
```

---

## 5. Implementation Priority

| # | Task | Cost | Time |
|:--|:-----|:-----|:-----|
| 1 | ตั้งค่า OpenRouter API key | $0 | 5 min |
| 2 | สร้าง UET Tensorizer (Python) | $0 | 2-3 hrs |
| 3 | Embed 9K files ด้วย Qwen3 Embedding | ~$0.18 | 1 hr |
| 4 | สร้าง LanceDB store | $0 | 2 hrs |
| 5 | สร้าง Ω-Search Engine | $0 | 2-3 hrs |
| 6 | Wire up Agent 0 (Orchestrator) | ~$0.10/day | 3 hrs |
| 7 | Port to Rust MCP Server | $0 | 1-2 weeks |

**Total API cost to bootstrap: ~$0.30** ✅

---

## 6. Open Questions

1. **OpenRouter API key** — มีพร้อมใช้แล้วหรือยัง? ต้องการ key สำหรับ embedding + agent models
2. **Disk space** — ยังเหลือ ~2.5 MB บน C: ต้องย้ายก่อนเริ่ม implement
3. **เลือก embedding model** — Qwen3 Embedding 8B ($0.01/M) vs Gemini Embedding 001 ($0.15/M)?
4. **เริ่มจาก agent ไหน** — Tensorizer + LanceDB ก่อน? หรือ MCP Server ก่อน?
