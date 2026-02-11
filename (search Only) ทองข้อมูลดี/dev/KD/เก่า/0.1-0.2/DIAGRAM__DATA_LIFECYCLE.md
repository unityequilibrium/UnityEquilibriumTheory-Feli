# ✅ **2) DIAGRAM__DATA_LIFECYCLE.md**

**นี่คือสิ่งที่สำคัญที่สุดในงานด้าน RAG / Knowledge Architecture**  
ทุกระบบ AI ที่ใช้ไฟล์ต้องมีภาพนี้

---

## **📘 DATA LIFECYCLE — STEP-BY-STEP**

```
1) File Upload (PDF / Docx / MD)
       │
       ▼
2) Validate File (type, size)
       │
       ▼
3) Store Original File → SourceFile table
       │
       ▼
4) Extract Text (parser)
       │
       ▼
5) Chunking (split by semantics)
       │
       ▼
6) Embedding → pgvector
       │
       ▼
7) Save Chunks + Vectors
       │
       ▼
8) Index Build / Update Graph
       │
       ▼
9) Retrieval when AI is called
       │
       ▼
10) LLM Response (with context)
       │
       ▼
11) Feedback or Correction
       │
       ▼
12) Version Update (manual sync)
```

---

## **📘 DATA LIFECYCLE (Diagram Block Version)**

```
┌──────────────┐
│   UPLOAD      │
└──────┬────────┘
       │
       ▼
┌──────────────┐
│   PARSE TEXT  │
└──────┬────────┘
       │
       ▼
┌──────────────┐
│   CHUNKING    │
└──────┬────────┘
       │
       ▼
┌──────────────┐
│  EMBEDDING    │  ← AI แปลงเป็นเวกเตอร์
└──────┬────────┘
       │
       ▼
┌──────────────┐
│ VECTOR STORE  │ ← PostgreSQL + pgvector
└──────┬────────┘
       │
       ▼
┌──────────────┐
│   GRAPH EDGE  │ ← link relations
└──────┬────────┘
       │
       ▼
┌──────────────┐
│   RETRIEVAL   │ ← used in Chat/Studio
└──────┬────────┘
       │
       ▼
┌──────────────┐
│ LLM RESPONSE  │
└──────────────┘
```

---
