# 🔄 UET Knowledge Sync (v5.0 — THE AXIOMATIC REGISTRY)

The Knowledge Sync (KS) Engine v5.0 is the "Truth Harmonizer" of the Unity Mega-Platform. It serves as the bridge between raw data, the high-performance Rust core, and the Agent's reasoning context, ensuring 100% version integrity.

---

## 🏛️ 1. The 5-Layer Sync Pipeline (Axiomatic)
1.  **DIFF LAYER**: Real-time detection of changes between raw sources (L0) and existing chunks (L1).
2.  **CHUNK LAYER**: Deterministic, semantic-boundary splitting to ensure stable vector addressing.
3.  **EMBEDDING LAYER**: Batch Processing via the **Model Routing** engine for low-latency vectorization.
4.  **VECTOR LAYER**: Atomic upserts to Postgres `pgvector`, tagged with the new `kb_version`.
5.  **REGISTRY LAYER**: Final commitment to the **Unity Ledger** and global broadcast of the sync event.

---

## 💎 2. Zero-Stale Deployment Rules
- **Atomic Commits**: No chunk is visible to the RAG Engine until the entire document sync is finalized.
- **Version Monotonicity**: Rejection of any sync attempt that would result in a lower KB version than currently active.
- **Registry Lock**: During the final L5 write phase, the **Flow Control** locks the Agent Engine to prevent race conditions.

---

## 🛡️ 3. Failure Mode Recovery
- **Sync Timeout**: Partial syncs are automatically rolled back using the last stable Ledger entry.
- **Hash Mismatch**: If chunk hashes drift from source hashes, the system triggers a full **Axiomatic Rebuild**.
- **Vector Orphanage**: Detection of vectors without registry entries triggers immediate garbage collection.

---

## 📥 4. Input/Output Manifest

### **Sync Request (L0 Ingest)**
```json
{
  "project_id": "UUID",
  "document_type": "MD | PDF | CODE",
  "sync_mode": "Incremental | Rebuild",
  "priority": "High"
}
```

### **Registry Update Output**
```json
{
  "new_kb_version": 42,
  "chunk_count": 1560,
  "sync_duration_ms": 120,
  "registry_status": "LOCKED | VERIFIED"
}
```

---

> [!IMPORTANT]
> **Rust Performance**: The core sync logic (Diff & Chunking) is executed in the `uet_core` Rust module to guarantee millisecond-level responsiveness even for million-chunk projects.
