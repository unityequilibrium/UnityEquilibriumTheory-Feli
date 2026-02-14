# 🔍 UET RAG Engine (v5.0 — THE AXIOMATIC RETRIEVER)

The RAG Engine v5.0 is the "Evidence Filter" of the Unity Mega-Platform. It transcends simple vector search by providing a multi-layered, version-aware retrieval pipeline that guarantees high-fidelity context for Agent reasoning.

---

## 🏗️ 1. The Retrieval Pipeline (Macro Flow)
1.  **QUERY NORMALIZATION**: Deterministic cleaning and Thai-script normalization.
2.  **ROUTING & EMBEDDING**: Choosing the optimal embedding model based on task complexity.
3.  **VECTOR SEARCH (L2)**: High-speed similarity search within Postgres `pgvector`.
4.  **VERSION SAFETY FILTER**: Immediate rejection of any chunk where `kb_version` != `registry.kb_version`.
5.  **EVIDENCE SCORING (v5)**: Multi-factor ranking (Similarity + Recency + Semantic Weight).
6.  **EVIDENCE FUSION**: Removing redundant chunks and clustering by Semantic Node (L3).

---

## 💎 2. Unified Scoring Model (v5.0)
Every retrieved chunk is scored using the following weighted logic:
- **Cosine Similarity (40%)**: Mathematical proximity in vector space.
- **$\Omega$-Gap Score (30%)**: Physical validity and axiomatic strength.
- **Semantic Relevance (20%)**: Alignment with the User's Intent Profile.
- **Recency/Version (10%)**: Proximity to the latest Knowledge Sync event.

---

## 🛡️ 3. Zero-Stale Enforcement Policy
The RAG Engine acts as a gatekeeper for knowledge freshness:
- **Immediate Invalidation**: Any `KB_VERSION_UPDATED` event from the Event Bus triggers a total purge of the RAG Cache.
- **Stale Block**: If a vector search returns data from a prior version, the system raises a `STALE_DATA_CRITICAL` error and halts the Agent.

---

## 📥 4. Input/Output Contract

### **Input Request**
```json
{
  "query": "String",
  "project_context": "UUID",
  "depth": "Fast | Deep | Axiomatic",
  "top_k": 10
}
```

### **Output (EvidenceSet v5.0)**
```json
{
  "query_intent": "String",
  "evidence_chunks": "Chunk[]",
  "contradiction_flags": "Boolean",
  "kb_version": "Integer"
}
```

---

> [!TIP]
> **Axiomatic Search**: In "Axiomatic" mode, the RAG Engine only returns chunks with an $\Omega$-score > 0.95, ensuring the highest level of scientific rigor.
