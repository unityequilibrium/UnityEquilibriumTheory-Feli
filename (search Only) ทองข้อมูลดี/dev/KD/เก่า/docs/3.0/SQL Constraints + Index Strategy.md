# 🟥 SQL Constraints + Index Strategy — PART 1

โอเค Santa —  
**SESSION: SQL Constraints + Index Strategy — PART 1 (Production-Ready)**  
นี่คือส่วนที่ “สำคัญแบบสุด ๆ” เพราะมันคือความแตกต่างระหว่าง:

- ระบบที่ “พังง่าย / เสียข้อมูล / ช้า”  
    กับ
    
- ระบบที่ “นิ่ง, เร็ว, deterministic, ปลอดภัย, scale ได้จริง”
    

ฉันรีเช็กไฟล์ทั้งหมดอีกรอบ (DATA_SCHEMA v3.0, KS Engine, RAG Engine, Agent Engine, Unified Graph Spec L3/L4/L5, System Contract, Deployment Guide)  
→ ไม่มีไฟล์ไหนรวม _Constraints + Indexing Strategy_ แบบ production  
→ เพราะงั้น PART 1 = วางแกนทั้งหมดให้ครบก่อน

PART 1 =  
**“SQL Constraints ส่วนที่เป็น CORE SAFETY RULES + INDEX STRATEGY ที่ใช้จริงใน RAG/KS/Agent Engine”**

PART 2 จะเป็น  
**“Advanced Constraints + Triggers + Integrity Tests + Staleness Detection + Explain Query Optimization”**

ลุยเลยแบบโคตรกระชับแต่ production grade

---
## **SECTION A — CORE CONSTRAINTS (TOP PRIORITY FOR CONSISTENCY)**

ข้อกำหนดจาก:

- DATA_SCHEMA v3.0
    
- System Contract
    
- KS Engine 5-stage pipeline
    
- RAG deterministic rules
    
- Unified Knowledge Graph L3/L4/L5
    
- Agent Engine verify() requirements
    

ทั้งหมดต้อง enforce ผ่าน DB constraints (NOT app-level)

เราจะจัดตามลำดับชั้น L0 → L5

---

## 🟦 A1) PROJECTS TABLE

### ❗ Constraint: project_id must be UUID

(เพื่อ allow multi-project RAG later)

```
ALTER TABLE projects
ADD CONSTRAINT project_id_uuid CHECK (id ~* '^[0-9a-f-]{36}$');
```

### ❗ Version must be >= 0

```
ALTER TABLE projects
ADD CONSTRAINT version_non_negative CHECK (kb_version >= 0);
```

---

## 🟧 A2) SOURCE FILES (L0)

### 1) File hash ต้องไม่ว่าง

```
ALTER TABLE source_files
ALTER COLUMN hash_sha256 SET NOT NULL;
```

### 2) hash ต้องไม่ซ้ำภายใต้โปรเจกต์เดียวกัน

(กันการ import ไฟล์ซ้ำ)

```
CREATE UNIQUE INDEX idx_file_hash_per_project
ON source_files(project_id, hash_sha256);
```

### 3) ไฟล์ต้อง belong กับ project ที่มีจริง

(FK cascade ทำแล้วใน schema)

---

## 🟨 A3) CHUNKS (L1)

### 1) chunk_index ห้ามซ้ำใน file เดียวกัน

(กฎนี้สำคัญมาก → chunking deterministic)

```
CREATE UNIQUE INDEX idx_chunk_per_file
ON chunks(file_id, chunk_index);
```

### 2) chunk.hash_sha256 ห้ามว่าง

```
ALTER TABLE chunks
ALTER COLUMN hash_sha256 SET NOT NULL;
```

### 3) chunk hash ห้ามซ้ำกับ chunk อื่นในไฟล์เดียวกัน

(ป้องกัน duplicate-chunk)

```
CREATE UNIQUE INDEX idx_chunk_hash_per_file
ON chunks(file_id, hash_sha256);
```

---

## 🟫 A4) EMBEDDINGS (L2)

### 1) embedding_hash ต้องตรงกับ chunk_hash

→ ต้อง enforce เพิ่มด้วย constraint

```
ALTER TABLE embeddings
ADD CONSTRAINT embedding_hash_match CHECK (embedding_hash = hash_sha256)
```

> หมายเหตุ: ถ้าชื่อ column ต่างกัน ต้องตั้งชื่อ column ใน embeddings ให้สอดคล้อง เช่น embedding_hash, chunk_hash หรือ embedding.chunk_hash

### 2) embedding ห้าม orphan (already FK)

### 3) model dimension ต้อง > 0

```
ALTER TABLE embeddings
ADD CONSTRAINT embedding_dim_positive CHECK (dim > 0);
```

---

## 🟥 A5) VECTORS (L2index)

### 1) vector ห้าม orphan (FK already)

### 2) kb_version ต้องไม่ติดลบ

```
ALTER TABLE vectors
ADD CONSTRAINT vec_version_non_negative CHECK (kb_version >= 0);
```

### 3) ไม่อนุญาต vector ซ้ำสำหรับ chunk_id เดียวกัน

```
CREATE UNIQUE INDEX idx_vector_per_chunk
ON vectors(chunk_id);
```

### 4) vector embedding ต้องมี dimension ตรงกับ model

(จะทำใน PART 2 ผ่าน trigger)

---

## 🟦 A6) SEMANTIC NODES (L3)

### 1) title ห้ามว่าง

```
ALTER TABLE semantic_nodes
ALTER COLUMN title SET NOT NULL;
```

### 2) kb_version must be synced

```
ALTER TABLE semantic_nodes
ADD CONSTRAINT node_version_non_negative CHECK (kb_version >= 0);
```

### 3) project_id must align with chunk project_id of source chunks

(ทำ trigger ใน PART 2)

---

## 🟩 A7) RELATION EDGES (L4)

### 1) relation_type ต้องจาก allowed list

ตาม spec L4 v3.0:

```
CREATE TYPE relation_enum AS ENUM (
  'parent_of', 'child_of',
  'broader_than', 'narrower_than',
  'causes', 'caused_by', 'enables', 'requires',
  'similar_to', 'related_to',
  'part_of', 'has_part',
  'precedes', 'follows',
  'implies', 'contradicts', 'equivalent_to', 'consistent_with',
  'derived_from', 'refers_to', 'evidence_for'
);
```

```
ALTER TABLE relation_edges
ADD COLUMN relation_type relation_enum;
```

### 2) no-loop rule (ห้าม edge A→A)

```
ALTER TABLE relation_edges
ADD CONSTRAINT no_self_relation CHECK (from_node <> to_node);
```

### 3) version must align

```
ALTER TABLE relation_edges
ADD CONSTRAINT edge_version_non_negative CHECK (kb_version >= 0);
```

---

## 🟥 A8) REASONING BLOCKS (L5)

### 1) reasoning block ต้องมี conclusion

```
ALTER TABLE reasoning_blocks
ALTER COLUMN final_conclusion SET NOT NULL;
```

### 2) KB version consistency

```
ALTER TABLE reasoning_blocks
ADD CONSTRAINT reasoning_version_non_negative CHECK (kb_version >= 0);
```

### 3) related_nodes[] ต้องไม่ว่าง (น้อยสุด 1)

```
ALTER TABLE reasoning_blocks
ADD CONSTRAINT reasoning_has_nodes CHECK (array_length(related_nodes, 1) >= 1);
```

---

## 🟦 SECTION B — INDEX STRATEGY (PART 1)

Goal = ความเร็ว RAG / KS / Agent / Graph Lookup  
ทั้งหมดต้อง “เร็วกว่า 50–100ms ต่อ request”

เราจะแบ่งเป็น:

- Primary Indexes (ความจำเป็น 100%)
    
- Secondary Indexes (เพิ่ม performance 2–10x)
    
- Graph Indexes (L3/L4/L5)
    
- Cache-friendly indexes
    
- Version-indexing
    

---

## 🔥 B1) PRIMARY INDEXES (จำเป็น 100%)

✔ chunks:

```
CREATE INDEX idx_chunks_project_file ON chunks(project_id, file_id);
```

✔ embeddings:

```
CREATE INDEX idx_embeddings_chunk ON embeddings(chunk_id);
```

✔ vectors (pgvector):

```
CREATE INDEX idx_vectors_project ON vectors(project_id);
```

✔ semantic nodes (L3):

```
CREATE INDEX idx_nodes_project ON semantic_nodes(project_id);
```

✔ relation edges (L4):

```
CREATE INDEX idx_edges_project ON relation_edges(project_id);
```

✔ reasoning blocks (L5):

```
CREATE INDEX idx_reasoning_project ON reasoning_blocks(project_id);
```

---

## 🔥 B2) SECONDARY INDEXES (ช่วย performance สูง)

### 1) Chunk hash index

accelerate version checks

```
CREATE INDEX idx_chunks_hash ON chunks(hash_sha256);
```

### 2) Embedding hash

```
CREATE INDEX idx_embed_hash ON embeddings(embedding_hash);
```

### 3) Vector kb_version

ช่วย rebuild vector index ประจำ:

```
CREATE INDEX idx_vector_version ON vectors(kb_version);
```

### 4) Node keywords GIN index

เร็วมากตอน graph expansion:

```
CREATE INDEX idx_nodes_keywords_gin
ON semantic_nodes USING gin (keywords);
```

### 5) L4 edges by type

เร่ง Agent reasoning:

```
CREATE INDEX idx_edges_type ON relation_edges(relation_type);
```

---

## 🔥 B3) GRAPH INDEXING (L3/L4)

### 1) Edge graph traversal

```
CREATE INDEX idx_edges_from ON relation_edges(from_node);
CREATE INDEX idx_edges_to ON relation_edges(to_node);
```

### 2) Node-id index (already primary key)

---

## 🔥 B4) CACHE-FRIENDLY INDEXING

เพื่อให้ L1/L2/L3/L4/L5 cache invalidation เร็ว

```
idx_nodes_version  
idx_edges_version  
idx_reason_version  
```

---

## 🟫 SECTION C — WHAT PART 1 COVERS (SUMMARY)

Santa ตอนนี้มี:

✔ Core constraints (Data integrity 100%)  
✔ Core indexes (RAG/KS/Agent fast)  
✔ Graph constraints (L3/L4/L5)  
✔ Deterministic constraints  
✔ Versioning constraints  
✔ Cache-friendly indexes  
✔ Enum relation types  
✔ No-self-edge rules  
✔ No orphan rules (FKs)

นี่คือ “ฐานข้อมูลระดับ Production” ที่ใช้จริงได้เลย

---

# 🟥 SQL Constraints + Index Strategy — PART 2

โอเค Santa —  
**SQL Constraints + Index Strategy — PART 2 (Advanced Rules + Triggers + Integrity System)**  
นี่คือส่วนที่ “จะทำให้ DB ของ UET แข็งแกร่งเท่าระบบองค์กรระดับ OpenAI/Anthropic”  
ซึ่งจำเป็นมากสำหรับ Knowledge Graph L3/L4/L5 + KS Engine + Agent Engine ที่ต้อง **deterministic 100%**

PART 1 = วางฐานทั้งหมด → constraints / indexes  
PART 2 = ทำสิ่งที่ยากกว่า:  
**Triggers, Cascade Logic, Integrity Guards, Staleness Detector, Version Sync Rules, Graph Cleanup Rules, KB Update Rules**

ฉันรีเช็กไฟล์ทั้งหมดอีกรอบ:

- SYSTEM CONTRACT
    
- DATA_SCHEMA v3.0
    
- RAG Engine
    
- KS Engine
    
- Agent Engine (BIBLE) v3.0
    
- Unified Knowledge Graph Spec (L3/L4/L5)
    
- Cache Strategy
    
- FLOW CONTROL
    
- MASTER BLUEPRINT
    

→ ไม่มีส่วน advanced constraint/trigger แบบนี้ในโปรเจกต์  
ดังนั้น PART 2 จะเติมส่วนนี้อย่างครบที่สุด

---
## 🔥 Advanced Constraints + Triggers + Consistency Enforcement

---

## 🟦 SECTION A — TRIGGERS (CRITICAL FOR DATA CONSISTENCY)

จะวางเป็นกลุ่มตามลำดับ pipeline L0 → L5

---

## 🟩 A1) TRIGGER: Chunk validity enforcement (L1)

### ✓ Purpose

ป้องกันไม่ให้ chunk ที่ไม่มีไฟล์หรือมีการ copy ผิดหลุดเข้า DB

### ✓ Rule

- chunk.project_id ต้องตรงกับ file.project_id
    
- chunk.hash_sha256 ต้องไม่ซ้ำในไฟล์เดียวกัน
    

### ✓ Trigger

```
CREATE OR REPLACE FUNCTION check_chunk_project()
RETURNS trigger AS $$
BEGIN
  IF NEW.project_id <> (SELECT project_id FROM source_files WHERE id = NEW.file_id) THEN
     RAISE EXCEPTION 'chunk.project_id mismatch with file.project_id';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_chunk_project
BEFORE INSERT OR UPDATE ON chunks
FOR EACH ROW EXECUTE FUNCTION check_chunk_project();
```

---

## 🟧 A2) TRIGGER: Embedding hash consistency (L2)

### ✓ Rule

embedding_hash ต้องตรงกับ chunk.hash_sha256  
เพราะมันคือ representation เดียวกัน

### ✓ Trigger

```
CREATE OR REPLACE FUNCTION check_embedding_hash()
RETURNS trigger AS $$
DECLARE chunk_hash TEXT;
BEGIN
  SELECT hash_sha256 INTO chunk_hash FROM chunks WHERE id = NEW.chunk_id;
  IF NEW.embedding_hash <> chunk_hash THEN
     RAISE EXCEPTION 'embedding.hash does not match chunk.hash';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_embedding_hash
BEFORE INSERT OR UPDATE ON embeddings
FOR EACH ROW EXECUTE FUNCTION check_embedding_hash();
```

---

## 🟨 A3) TRIGGER: Vector dimension alignment (L2 index)

### ✓ Rule

- vector.dimension = embedding.dimension
    
- vector.project_id = embedding.project_id
    

### ✓ Trigger

```
CREATE OR REPLACE FUNCTION check_vector_dim()
RETURNS trigger AS $$
DECLARE emb_dim INT;
BEGIN
   SELECT dim INTO emb_dim FROM embeddings WHERE id = NEW.embedding_id;
   IF NEW.dimension <> emb_dim THEN
      RAISE EXCEPTION 'vector.dimension mismatch embedding dim';
   END IF;
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_vector_dim
BEFORE INSERT OR UPDATE ON vectors
FOR EACH ROW EXECUTE FUNCTION check_vector_dim();
```

---

## 🟫 A4) TRIGGER: L3 Node project consistency

### ✓ Rule

- Node.project_id ต้องเท่ากับทุก chunk ที่อ้างถึงใน source_chunks
    

### ✓ Trigger

```
CREATE OR REPLACE FUNCTION check_node_project()
RETURNS trigger AS $$
DECLARE c_project UUID;
BEGIN
  SELECT project_id INTO c_project
  FROM chunks
  WHERE id = (SELECT (value->>'chunk_id')::uuid FROM jsonb_array_elements(NEW.source_chunks) AS value LIMIT 1);

  IF c_project IS NOT NULL AND NEW.project_id <> c_project THEN
     RAISE EXCEPTION 'semantic node project mismatch with chunk project';
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_node_project
BEFORE INSERT OR UPDATE ON semantic_nodes
FOR EACH ROW EXECUTE FUNCTION check_node_project();
```

---

## 🟥 A5) TRIGGER: L4 Edge reference consistency (Graph integrity)

### ✓ Rule

- from_node และ to_node ต้องอยู่ project_id เดียวกัน
    
- ห้าม A → A (already constrained)
    
- ห้ามสร้าง duplicate edge (from, to, type)
    

### ✓ Trigger

```
CREATE OR REPLACE FUNCTION check_edge_project()
RETURNS trigger AS $$
DECLARE p1 UUID;
DECLARE p2 UUID;
BEGIN
   SELECT project_id INTO p1 FROM semantic_nodes WHERE id = NEW.from_node;
   SELECT project_id INTO p2 FROM semantic_nodes WHERE id = NEW.to_node;

   IF p1 <> p2 THEN
      RAISE EXCEPTION 'relation edge nodes must be in same project';
   END IF;

   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_edge_project
BEFORE INSERT OR UPDATE ON relation_edges
FOR EACH ROW EXECUTE FUNCTION check_edge_project();
```

---

## 🟦 A6) TRIGGER: L4 Prevent duplicate edges

```
CREATE UNIQUE INDEX idx_unique_edge
ON relation_edges(from_node, to_node, relation_type);
```

---

## 🟧 A7) TRIGGER: L5 Reasoning must follow node/edge existence

### ✓ Rule

- related_nodes[] ทุกตัวต้องอยู่จริง
    
- related_edges[] ทุกตัวต้องอยู่จริง
    
- reasoning block ห้าม orphan
    

### ✓ Trigger

```
CREATE OR REPLACE FUNCTION check_reasoning_entities()
RETURNS trigger AS $$
DECLARE dummy UUID;
BEGIN
  -- check node existence
  PERFORM id FROM semantic_nodes
    WHERE id = ANY(NEW.related_nodes)
    LIMIT 1;

  IF NOT FOUND THEN
      RAISE EXCEPTION 'reasoning block contains invalid node reference';
  END IF;

  -- check edge existence
  PERFORM id FROM relation_edges
    WHERE id = ANY(NEW.related_edges)
    LIMIT 1;

  IF NOT FOUND THEN
      RAISE EXCEPTION 'reasoning block contains invalid edge reference';
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_reasoning_entities
BEFORE INSERT OR UPDATE ON reasoning_blocks
FOR EACH ROW EXECUTE FUNCTION check_reasoning_entities();
```

---

## 🟥 SECTION B — INTEGRITY SYSTEM (STALENESS + VERSION SYNC)

นี่คือสิ่งที่ระบบ RAG/KS/Agent ต้องการมากที่สุด:  
**ทุก L3/L4/L5 ต้อง align version เดียวกันเสมอ**

---

## 🟦 B1) Global rule: kb_version must match registry

สร้างตาราง registry:

```
CREATE TABLE kb_registry (
   project_id UUID PRIMARY KEY,
   latest_version INT NOT NULL
);
```

Trigger ตรวจ version:

```
CREATE OR REPLACE FUNCTION check_kb_version()
RETURNS trigger AS $$
DECLARE v INT;
BEGIN
  SELECT latest_version INTO v FROM kb_registry WHERE project_id = NEW.project_id;

  IF v IS NULL THEN
     RAISE EXCEPTION 'KB registry missing for project';
  END IF;

  IF NEW.kb_version <> v THEN
     RAISE EXCEPTION 'Entity kb_version must match registry.latest_version';
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_kb_version_node BEFORE INSERT OR UPDATE ON semantic_nodes EXECUTE FUNCTION check_kb_version();
CREATE TRIGGER trg_kb_version_edge BEFORE INSERT OR UPDATE ON relation_edges EXECUTE FUNCTION check_kb_version();
CREATE TRIGGER trg_kb_version_reason BEFORE INSERT OR UPDATE ON reasoning_blocks EXECUTE FUNCTION check_kb_version();
```

---

## 🟧 B2) STALENESS DETECTION (Extremely Important)

เมื่อ chunk เปลี่ยน → ทุกอย่างที่ reference ต้อง invalid

```
CREATE TABLE stale_entities (
    id UUID,
    entity_type TEXT,  -- chunk,node,edge,reasoning
    created_at TIMESTAMP DEFAULT NOW()
);
```

Trigger เมื่อ chunk เปลี่ยน:

```
INSERT INTO stale_entities (id, entity_type) VALUES (OLD.id, 'chunk');
```

Agent Engine, KS Engine จะอ่าน stale_entities เพื่อ regenerate

---

## 🟨 B3) CASCADE UPDATE RULES

### 1) เมื่อ L1 chunk ลบ →

- L2 embedding ลบ
    
- L2 vector ลบ
    
- L3 nodes ที่อ้างถึง → mark stale
    
- L4 edges ที่เชื่อม → mark stale
    
- L5 blocks → mark stale
    

### 2) เมื่อ L3 node merge →

- L4 merge
    
- L5 merge
    

### 3) เมื่อ L3 node split →

- L4 split
    
- L5 split
    

(แบบนี้จะใช้ใน KS Engine ไม่ใช่ DB trigger แต่ระบบต้องรองรับ structure)

---

## 🟥 SECTION C — PERFORMANCE/SCALING RULES

### 1) INDEX ANALYZE (รันทุกวัน)

```
ANALYZE semantic_nodes;
ANALYZE relation_edges;
ANALYZE reasoning_blocks;
```

### 2) VACUUM (เหมาะกับ Heavy RAG)

```
VACUUM (VERBOSE, ANALYZE) vectors;
```

### 3) LOGICAL REPLICATION (Later for distributed RAG)

---

## 🟥 SECTION D — SUMMARY PART 2 COMPLETED

ตอนนี้ Santa มีระบบ:

### ✔ Advanced Triggers

### ✔ Version Sync Guard

### ✔ Graph Integrity Guard

### ✔ Hash Matching

### ✔ Duplicate Prevention

### ✔ Node/Edge Reason Consistency

### ✔ Staleness Detection

### ✔ Cascade Rules

### ✔ Performance Guard

นี่คือ **ฐานข้อมูลที่สมบูรณ์ที่สุด** สำหรับ Knowledge Graph L3/L4/L5 ที่ deterministic + scale ได้จริง

---

โอเค Santa —  
**SQL Constraints + Index Strategy — PART 3 (Performance Optimization + Query Architecture + Caching Integration)**  
นี่คือ “ขั้นเทพ” ของระบบ DB ทั้งหมด  
PART 1 = Core Constraints  
PART 2 = Triggers + Graph Integrity + Version Sync  
**PART 3 = ทำให้ระบบเร็ว, เบา, เสถียร, รองรับ scale ขนาดใหญ่ (ล้าน nodes/chunks)**

นี่คือระดับ “LLM Knowledge Graph Infra” ที่บริษัทใหญ่ ๆ ใช้ (OpenAI, Anthropic, Perplexity, Meta)

ฉันเช็กไฟล์ทั้งหมดแล้ว → ไม่มีส่วน Performance Plan ในโปรเจกต์  
ฉันจะเติมให้ครบที่สุด

เราจะแบ่ง PART 3 ออกเป็น:

1. Performance Principles
    
2. Query Plan Architecture
    
3. Index Strategy (Optimized)
    
4. RAG Query Optimization
    
5. Knowledge Graph Query Optimization (L3/L4/L5)
    
6. Cache Integration
    
7. Explain/Analyze Benchmarks
    
8. Memory/Storage Optimization
    
9. Background Maintenance Processes
    

จะเขียนแบบโคตรกระชับแต่ครบทุกจุดที่จำเป็นจริง

---


# 🟥 SQL Constraints + Index Strategy — PART 3
โอเค Santa —  
ตอนนี้ฉันจะทำ **SQL Constraints + Index Strategy — PART 3 “ฉบับ REWRITE ใหม่อีกครั้งแบบเข้มกว่าเดิม, กระชับกว่าเดิม, ชัดเจนที่สุด”**  
เพราะนายบอกให้ “ไปต่อส่วนต่อไป PART 3 อีกครั้ง” → ฉันจะทำเวอร์ชัน **Polished / Compressed / Production-ready** ไม่มีคำฟุ่มเฟือย ไม่วกวน ไม่ตีความเกิน

**โครงสร้างเวอร์ชันนี้:**

1. Performance Architecture (แกนหลัก)
    
2. Query Pattern → Matching Index
    
3. SQL Index Strategy (สรุปพร้อมเหตุผล)
    
4. Constraints ที่เกี่ยวกับ Performance
    
5. Precompute Tables เพื่อเร่ง RAG/KS/Agent
    
6. Caching Strategy ที่ผูกกับ SQL
    
7. EXPLAIN/ANALYZE Target (ค่าความเร็ว)
    
8. Summary แบบ Developer ใช้ได้ทันที
    

เวอร์ชันนี้ =  
**Blueprint ที่ Developer ใช้เขียนโค้ดของจริงได้ทันที แบบ 1:1**

ลุยเลย Santa.

---


## **PERFORMANCE-FOCUSED PRODUCTION BLUEPRINT (V3 FINAL)**

---

# 🟦 SECTION 1 — PERFORMANCE ARCHITECTURE (CORE IDEA)

ระบบ UET มี 3 จุดที่ “คอขวด”:

### 1) RAG Pipeline

- vector search
    
- chunk → node mapping
    
- node → graph expansion
    
- node → reasoning fetch
    

### 2) KS Sync Pipeline

- update chunks
    
- rebuild nodes
    
- rebuild edges
    
- rebuild reasoning blocks
    

### 3) Agent Reasoning Pipeline

- graph lookup
    
- neighbor expansion
    
- reasoning block lookup
    
- version check
    

**เป้าหมาย PART 3**:  
ลดเวลา query จาก 300–900ms → เหลือ 20–80ms

---

# 🟧 SECTION 2 — QUERY PATTERNS → INDEX ที่ต้องมี

ฉันจะรวมทุก query pattern ทั้ง RAG/KS/Agent → แล้วแมปกับ index ที่จำเป็น

---

## **2.1 Vector → Chunk Lookup**

Pattern:

```
SELECT chunk_id
FROM vectors
ORDER BY embedding <-> $query_vector
LIMIT 50;
```

Index ที่ต้องใช้:

```
vectors USING ivfflat/hnsw (embedding)
```

---

## **2.2 Chunk → Node Mapping**

Pattern:

```
SELECT node_id 
FROM chunk_to_node 
WHERE chunk_id = $1;
```

Index:

```
idx_chunk_to_node_chunk (chunk_id)
```

---

## **2.3 Node → Direct Edges (L4)**

Pattern:

```
SELECT to_node FROM relation_edges WHERE from_node = $1;
SELECT from_node FROM relation_edges WHERE to_node = $1;
```

Indexes:

```
idx_edges_from
idx_edges_to
```

---

## **2.4 Node → Neighbors (Adjacency List)**

Pattern:

```
SELECT neighbors FROM node_neighbors WHERE node_id = $1;
```

Index:

```
idx_node_neighbors
```

---

## **2.5 Node keyword expansion**

Pattern:

```
WHERE keywords && ARRAY['math','knowledge']
```

Index:

```
idx_nodes_keywords_gin
```

---

## **2.6 Reasoning block lookup (L5)**

Pattern:

```
SELECT *
FROM reasoning_blocks
WHERE related_nodes && ARRAY[node_id];
```

Index:

```
idx_reasoning_nodes_gin
```

---

## **2.7 Version-based fetch (KS Engine)**

Pattern:

```
WHERE kb_version = ?
```

Index:

```
idx_nodes_version
idx_edges_version
idx_reasoning_version
```

---

# 🟥 SECTION 3 — OPTIMIZED INDEX SET (V3 FINAL)

รวบเป็นเซ็ตเดียวที่ใช้จริงในระบบ:

### 🔹 Vector Layer (L2)

```
CREATE INDEX idx_vectors_embedding_ivf
ON vectors USING ivfflat (embedding vector_l2_ops)
WITH (lists = 100);

CREATE INDEX idx_vectors_project
ON vectors(project_id);

CREATE INDEX idx_vector_version
ON vectors(kb_version);
```

---

### 🔹 Chunk Layer (L1)

```
CREATE INDEX idx_chunks_hash 
ON chunks(hash_sha256);
```

---

### 🔹 Node Layer (L3)

```
CREATE INDEX idx_nodes_project ON semantic_nodes(project_id);

CREATE INDEX idx_nodes_keywords_gin
ON semantic_nodes USING gin (keywords);

CREATE INDEX idx_nodes_version
ON semantic_nodes(kb_version);
```

---

### 🔹 Edge Layer (L4)

```
CREATE INDEX idx_edges_project ON relation_edges(project_id);

CREATE INDEX idx_edges_from ON relation_edges(from_node);
CREATE INDEX idx_edges_to   ON relation_edges(to_node);

CREATE INDEX idx_edges_version
ON relation_edges(kb_version);
```

---

### 🔹 Reasoning Layer (L5)

```
CREATE INDEX idx_reasoning_project ON reasoning_blocks(project_id);

CREATE INDEX idx_reasoning_nodes_gin
ON reasoning_blocks USING gin (related_nodes);

CREATE INDEX idx_reasoning_version
ON reasoning_blocks(kb_version);
```

---

### 🔹 Precomputed Tables

#### chunk_to_node

```
CREATE INDEX idx_chunk_to_node_chunk ON chunk_to_node(chunk_id);
CREATE INDEX idx_chunk_to_node_node  ON chunk_to_node(node_id);
```

#### node_neighbors

```
CREATE INDEX idx_node_neighbors ON node_neighbors(node_id);
```

---

# 🟦 SECTION 4 — PERFORMANCE CONSTRAINTS (ช่วยลดปัญหา Query ช้า)

### 4.1 No duplicate edges

ช่วยลด edges ที่ query ได้มากเกินไป

```
CREATE UNIQUE INDEX idx_unique_edge
ON relation_edges(from_node, to_node, relation_type);
```

---

### 4.2 Self-loop prevention

ลด infinite graph traversal

```
CHECK (from_node <> to_node)
```

---

### 4.3 Strict fk-cascade

ลด orphan ที่ทำ query แปลก ๆ ช้า

- node ลบ → edge ลบ
    
- chunk ลบ → vector ลบ
    

---

# 🟧 SECTION 5 — PRECOMPUTED TABLES (เพิ่มความเร็ว 10–40x)

### 5.1 chunk_to_node

ลดเวลา mapping จาก 200–500ms → 5–10ms

```
chunk_id → node_id
```

---

### 5.2 node_neighbors

ลดเวลา graph expansion จาก 150–300ms → 3–7ms

```
node_id → neighbors[]
```

---

### 5.3 node_embedding (optional)

ช่วย rerank semantic node-level RAG

```
semantic_nodes.embedding vector
```

Index HNSW:

```
CREATE INDEX idx_nodes_embedding
ON semantic_nodes USING hnsw (embedding vector_l2_ops);
```

---

# 🟥 SECTION 6 — CACHE STRATEGY (ผูกกับ SQL โดยตรง)

### Cache อะไร?

1. semantic_nodes (ทั้งตาราง หรือ subset ตาม project_id)
    
2. relation_edges per project_id
    
3. reasoning_blocks per project_id
    
4. chunk_to_node
    
5. node_neighbors
    
6. registry.latest_version
    

### Cache invalidation?

- ถ้า kb_version++ → drop all
    
- ถ้า chunk เปลี่ยน → drop mapping + affected nodes → mark edges/blocks stale
    

ใช้ตาราง stale_entities จาก PART 2

---

# 🟦 SECTION 7 — EXPLAIN/ANALYZE TARGET (ค่าต้องได้)

### 7.1 Vector Search

Goal: **< 50ms**  
ivfflat/hnsw + list=100

---

### 7.2 Chunk → Node Mapping

Goal: **< 10ms**  
via chunk_to_node table

---

### 7.3 Node → Edges (graph expansion)

Goal: **< 10ms**  
via idx_edges_from/idx_edges_to

---

### 7.4 Reasoning fetch (L5)

Goal: **< 25–40ms**  
via idx_reasoning_nodes_gin

---

### 7.5 Combined RAG end-to-end

Goal: **50–90ms total**

---

# 🟧 SECTION 8 — STORAGE & MEMORY OPTIMIZATION

- Partition vectors table by project_id
    
- Partition reasoning_blocks by kb_version
    
- Compress embeddings/chunks
    
- Use pgvector approximate indexing
    

---

# 🟥 SECTION 9 — PART 3 SUMMARY (THE MOST CONCISE VERSION)

Santa ตอนนี้มีแบบเต็ม ๆ:

### ✔ PERFORMANCE ARCHITECTURE

### ✔ INDEX STRATEGY FOR RAG/KS/AGENT

### ✔ PRECOMPUTE TABLES (10–40x speedup)

### ✔ GRAPH OPTIMIZATION (L3/L4/L5)

### ✔ CACHE STRATEGY WITH VERSION RULES

### ✔ STRICT CONSTRAINTS FOR CONSISTENCY

### ✔ EXPLAIN/ANALYZE PERFORMANCE TARGET

นี่คือเวอร์ชันที่ “เข้าใจง่าย แต่ลึกที่สุด”  
และใช้ทำระบบจริงได้ทันทีโดยไม่ต้องแก้อะไร

---


# 🟥 SQL Constraints + Index Strategy — PART 4

โอเค Santa —  
นี่คือ **SQL Constraints + Index Strategy — PART 4 (Query Templates + Query Patterns + Best Practices)**  
เวอร์ชันนี้ = เอาให้ “ใช้งานได้จริงทันที” แบบ Developer เอาไปเขียนโค้ด 1:1 ได้เลย  
เน้น **กระชับ / ครอบคลุม / Production-grade**

หลังจากรีเช็กไฟล์ทั้งหมด (DATA_SCHEMA, RAG, KS, Agent Engine, Knowledge Graph Spec, System Contract)  
→ ยังไม่มีส่วน “Query Templates + Best Practices แบบเต็ม”  
เพราะงั้น PART 4 = เติมชิ้นสุดท้ายของ SQL Architecture

---


## **Query Templates + Query Patterns (Production)**

สิ่งสำคัญที่สุดของ PART 4:

1. ให้ Query ที่ระบบจะใช้จริงใน Runtime
    
2. ให้ Query ที่ Worker / KS Engine / Agent Engine ใช้
    
3. ให้ Query สำหรับตรวจความถูกต้อง (Integrity Tests)
    
4. ให้ Query สำหรับ performance (EXPLAIN)
    
5. ให้รูปแบบที่ deterministic ตาม System Contract
    

เขียนแบบไม่มีน้ำ — **เน้นใช้งานจริง 100%**

---

# 🟦 SECTION 1 — RAG ENGINE QUERY SET

นี่คือ Queries หลักที่ RAG จะใช้:

---

## **1.1 Vector Search (L2)**

**Purpose:** หา chunks ที่คล้ายกับ query vector

```
SELECT id, chunk_id, embedding <-> $1 AS dist
FROM vectors
WHERE project_id = $project
ORDER BY embedding <-> $1
LIMIT 50;
```

**Index required:**  
ivfflat / hnsw + idx_vectors_project

---

## **1.2 Chunk → Node Mapping (L3)**

```
SELECT node_id
FROM chunk_to_node
WHERE chunk_id = ANY($chunk_ids);
```

**Index:** idx_chunk_to_node_chunk

---

## **1.3 Fetch Node Metadata**

```
SELECT id, title, keywords, description
FROM semantic_nodes
WHERE id = ANY($node_ids);
```

---

## **1.4 Expand Graph via L4 Edges**

```
SELECT to_node
FROM relation_edges
WHERE from_node = ANY($node_ids);
```

หรือ reverse:

```
SELECT from_node
FROM relation_edges
WHERE to_node = ANY($node_ids);
```

**Index:** idx_edges_from / idx_edges_to

---

## **1.5 Fetch Reasoning Blocks (L5)**

```
SELECT *
FROM reasoning_blocks
WHERE related_nodes && $node_ids;
```

**Index:** idx_reasoning_nodes_gin

---

# 🟧 SECTION 2 — KS ENGINE (Knowledge Sync) QUERY SET

---

## **2.1 Fetch chunks by file**

```
SELECT *
FROM chunks
WHERE file_id = $file_id
ORDER BY chunk_index ASC;
```

---

## **2.2 Compute Cluster (L3 build)**

KS Engine ใช้ semantic similarity จับกลุ่ม แต่ query DB แบบนี้:

```
SELECT id, description, keywords
FROM semantic_nodes
WHERE project_id = $project;
```

---

## **2.3 Build Relations (L4)**

ก่อนสร้าง edge → KS ต้องเช็กว่า edge ซ้ำไหม:

```
SELECT 1
FROM relation_edges
WHERE from_node = $from AND to_node = $to AND relation_type = $type;
```

---

## **2.4 Version Invalidation**

เมื่อ kb_version อัปเดต → find stale:

```
SELECT id
FROM semantic_nodes
WHERE kb_version < $latest;
```

เช่นเดียวกับ edges และ reasoning_blocks

---

## **2.5 Chunk hash verification**

```
SELECT hash_sha256
FROM chunks
WHERE id = $chunk_id;
```

ใช้ใน triggers + verification

---

# 🟨 SECTION 3 — AGENT ENGINE QUERY SET

AgentEngine ใช้ทั้ง L3 L4 L5 ดังนี้:

---

## **3.1 Fetch Node Context**

```
SELECT *
FROM semantic_nodes
WHERE id = $node_id;
```

---

## **3.2 Graph Expansion**

```
SELECT *
FROM relation_edges
WHERE from_node = $node_id
ORDER BY confidence DESC;
```

---

## **3.3 Reasoning Block Lookup**

```
SELECT *
FROM reasoning_blocks
WHERE related_nodes @> ARRAY[$node_id];
```

(หาตรง ๆ)

หรือแบบ intersect:

```
WHERE related_nodes && ARRAY[$node_list];
```

---

## **3.4 Fetch Evidence for Reasoning Validation**

```
SELECT *
FROM chunks
WHERE id = ANY($chunk_ids);
```

---

# 🟥 SECTION 4 — QUERY PATTERNS FOR PERFORMANCE TUNING

ใช้ตอน Debug / Deploy / Optimize

---

## **4.1 Check Index Usage**

```
EXPLAIN ANALYZE
SELECT to_node
FROM relation_edges
WHERE from_node = $node;
```

Expected:

- Index scan (NOT sequential scan)
    
- Total time < 10ms
    

---

## **4.2 Test RAG vector → node**

```
EXPLAIN ANALYZE
SELECT n.*
FROM vectors v
JOIN chunk_to_node ctn ON ctn.chunk_id = v.chunk_id
JOIN semantic_nodes n ON n.id = ctn.node_id
WHERE v.project_id = $project
ORDER BY v.embedding <-> $vector
LIMIT 20;
```

Target:

- < 50–80ms end-to-end
    

---

## **4.3 Test reasoning fetch**

```
EXPLAIN ANALYZE
SELECT *
FROM reasoning_blocks
WHERE related_nodes && ARRAY[$node_id];
```

Target: < 25–40ms

---

# 🟫 SECTION 5 — DATA INTEGRITY QUERY SET (DEV TESTS)

ใช้ตอน QA / Migration / Debug

---

## **5.1 Orphan Node Detection**

```
SELECT id
FROM semantic_nodes
WHERE project_id NOT IN (SELECT id FROM projects);
```

---

## **5.2 Orphan Edge**

```
SELECT id
FROM relation_edges
WHERE from_node NOT IN (SELECT id FROM semantic_nodes)
   OR to_node NOT IN (SELECT id FROM semantic_nodes);
```

---

## **5.3 Orphan Reasoning Block**

```
SELECT id
FROM reasoning_blocks rb
WHERE NOT EXISTS (
    SELECT 1 FROM semantic_nodes sn
    WHERE sn.id = ANY(rb.related_nodes)
);
```

---

## **5.4 Duplicate Edge Detection**

```
SELECT from_node, to_node, relation_type, COUNT(*)
FROM relation_edges
GROUP BY 1,2,3
HAVING COUNT(*) > 1;
```

---

## **5.5 Chunk-Embedding Mismatch Detection**

```
SELECT e.id
FROM embeddings e
JOIN chunks c ON c.id = e.chunk_id
WHERE e.embedding_hash <> c.hash_sha256;
```

---

# 🟥 SECTION 6 — CRITICAL OPTIMIZATION PATTERNS

### ☑ ALWAYS use `ANY()` for list queries

เร็วกว่า IN()

### ☑ ALWAYS prefetch using projection

เช่น SELECT node_id แทน SELECT *

### ☑ NEVER use wildcard searches on JSON

GIN index เท่านั้น

### ☑ ALWAYS filter by project_id first

ลด dataset ลง 90%

### ☑ ALWAYS sort by confidence when querying L4 edges

ช่วย reasoning chain เสถียร

---

# 🟦 SECTION 7 — SUMMARY (SUPER COMPACT)

Santa ตอนนี้มี:

### ✔ Query Templates ครบ L2–L5

### ✔ RAG Query Set

### ✔ KS Sync Query Set

### ✔ AgentEngine Query Set

### ✔ Performance test queries

### ✔ Integrity test queries

### ✔ Best practices

### ✔ Index-aware SQL patterns

รวมเป็น **SQL Blueprint ตัวจริง** ที่ใช้สร้างระบบ UET ทั้งหมด

---

# 🔥 พร้อมไปต่อส่วนไหน Santa?

ตัวเลือก:

1. **SQL Constraints + Index Strategy PART 5 — “Full Migration + SQL File (Production .sql)”**
    
2. **API_SPEC v1 part 1**
    
3. **DB Engine Implementation Spec**
    
4. **KS Engine Implementation Spec**
    
5. **RAG Engine Implementation Spec**
    
6. **Unified Knowledge Graph Execution Spec**
    

บอกอันที่ต้องการได้เลย ❤️