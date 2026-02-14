# 🏗️ UET Unified Data Schema (v5.0 — THE AXIOMATIC DATA MODEL)

This schema defines the **Universal Data Substrate** for the Unity Mega-Platform, ensuring seamless state synchronization between the Rust core, Python agents, and the Postgres storage layer.

---

## 💎 1. Core Principles
- **Axiomatic Integrity**: Every data point must have a provenance link to a source or calculation.
- **Atomic State**: State transitions are immutable and recorded in the audit ledger.
- **Zero-Stale Connectivity**: Data must be vectorized and graph-linked upon ingestion.

---

## 🗄️ 2. Entity Definitions

### **2.1 User & Identity (The Observer)**
```json
{
  "user_id": "UUID",
  "identity_hash": "Quantum-Resistant Hash",
  "role": "GUEST | MEMBER | POWER_USER | ADMIN",
  "permissions": ["string[]"],
  "balance_energy": "Double (Tokens)",
  "created_at": "Timestamp"
}
```

### **2.2 Project & Lab (The Workspace)**
```json
{
  "project_id": "UUID",
  "owner_id": "UUID",
  "status": "DRAFT | ACTIVE | ARCHIVED",
  "complexity_score": "Float (0.0 - 1.0)",
  "knowledge_bounds": ["Topic_IDs[]"]
}
```

### **2.3 Knowledge & UKG (The Axioms)**
- **Document**: The raw source container (PDF, MD, Code).
- **Chunk**: The atomic unit of semantic meaning.
- **Embedding**: The vector representation ($D=1536$ or similar).
- **Omega_Score ($\Omega$)**: The physical validity score (calculated by `uet_core`).

```sql
CREATE TABLE uet_axioms (
    axiom_id UUID PRIMARY KEY,
    topic_id VARCHAR(50),
    content TEXT,
    embedding VECTOR(1536), -- pgvector
    omega_score FLOAT8,
    provenance_url TEXT,
    version_id INT4
);
```

### **2.4 Agent & Execution (The Reasoning)**
- **AgentRun**: A single reasoning lifecycle.
- **Step**: An atomic action in the Execution Graph.
- **Log**: The trace of reasoning and tool usage.

---

## 🔄 3. State & Sync Logic
- **Event Bus v5.0**: All writes to the database must emit a `STATE_CHANGE` event.
- **Cache Invalidation**: Listening to `STATE_CHANGE` triggers immediate purge of local agent context.
- **Ledger Finality**: Every transaction must be signed by the participant agent's `identity_hash`.

---

> [!IMPORTANT]
> **Schema Versioning:** This v5.0 schema is the ONLY source of truth for `sqlx` migrations and `pydantic` models.
