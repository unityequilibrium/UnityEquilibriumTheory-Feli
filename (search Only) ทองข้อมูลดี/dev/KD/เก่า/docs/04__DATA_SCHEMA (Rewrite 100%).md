## 1. กูเช็คจากอะไรบ้าง?

กูไล่ดูทั้งหมดว่า “Data Schema ของมึงต้องรองรับอะไรบ้าง” จากโปรเจกต์ตอนนี้:

- Core entity: user / project / workspace / session / message / asset
    
- Document & RAG: document, chunk, embedding, pipeline, log
    
- Unified Knowledge Graph: L1–L5 node/edge, mapping, KS engine
    
- Engine state: KS, RAG, Agent, Flow, Execution Graph, Routing
    
- Event & Queue: event_bus, retry, job queue
    
- Security & Permission: role, policy, audit
    
- Performance: index, partition, shard, retention
    
- Migration & Versioning
    
- Observability & Metrics
    
- Mapping: SQL ↔ Prisma ↔ API payload ↔ Engine interface
    
- Testing & synthetic data
    

พอรวมทุกอย่างจริง ๆ แล้ว  
**10 part มันแน่นเกินไป → เสี่ยงต้องมาแตกเพิ่มทีหลัง**

---

## 2. โครงสุดท้ายที่กูเสนอ (Data Schema Blueprint “ถาวร”)

กูเลยจัดเป็น **12 Part หลัก** แบบนี้  
(อันที่ทำไปแล้วคือ Part 1)

> ใช้เลข “Part” ใน 04_data_schema.md เลย ไม่ต้องไปสนชื่อไฟล์อื่น

---

### **Part 0 — Overview & Design Principles**

- Scope ของ data layer
    
- แยก “Core / Knowledge / Engine / Infra” ให้ชัด
    
- กฎเหล็ก 5–7 ข้อของ schema v3.0 (ห้ามทรยศในอนาคต)
    

---

### **Part 1 — Core System Schema** ✅ _เขียนไปแล้ว_

- users / projects / workspaces / sessions / messages / assets
    
- core FK, index, relation
    
- query pattern เบื้องต้น
    

---

### **Part 2 — Document & Content Schema**

- documents / document_versions
    
- extraction_pipeline / parse_log
    
- content_block / section / annotation
    
- ผูกกับ assets + project + workspace
    

---

### **Part 3 — RAG & Retrieval Schema**

- chunks / embeddings / vector_index_meta
    
- retrieval_log / retrieval_strategy
    
- mapping doc → chunk → embedding
    
- support shard หลายตัว + หลาย provider
    

---

### **Part 4 — Unified Knowledge Graph & KS Schema**

- graph_nodes (L1–L5)
    
- graph_edges
    
- node_type / edge_type / layer mapping
    
- ks_task, ks_job, ks_log
    
- index + constraint ของกราฟ
    

---

### **Part 5 — Engine State & Execution Schema**

(Agent / Flow / ExecutionGraph / Routing)

- agent_task / agent_step / agent_context
    
- flow_run / flow_step
    
- exec_graph / exec_node / exec_edge / exec_log
    
- routing_rule / routing_log
    

---

### **Part 6 — Events, Queue & Background Jobs**

- event_bus (topic, payload, status)
    
- job_queue (type, payload, retries)
    
- retry_policy / dead_letter_queue
    
- mapping ไปยัง Engine/Graph/KS/RAG
    

---

### **Part 7 — Security, Permission & Audit Schema**

- roles / role_binding (user ↔ project/workspace)
    
- permission_profile
    
- audit_log (สำคัญกับ governance)
    
- data_access_policy (เผื่ออนาคตต้องทำ multi-tenant / org-level)
    

---

### **Part 8 — Constraints, Indexing & Partition Strategy**

- global FK & cascade rules
    
- unique constraints (across project/workspace/doc)
    
- index list ระดับ production
    
- partition/shard แนวคิด (per project / per time window)
    

---

### **Part 9 — Versioning & Migration Strategy v3.0**

- table version field / schema version
    
- migration_history (ผูกกับ 06_sql_migration.md)
    
- rule เวลาต้องเปลี่ยน schema แต่ไม่อยากพังของเก่า
    
- zero-downtime migration guideline
    

---

### **Part 10 — Observability & Metrics Schema**

- metrics_log (latency, cost, token usage)
    
- engine_metrics (per engine)
    
- data_volume_log / storage_usage
    
- hook เข้ากับ ExecutionGraph & EventBus
    

---

### **Part 11 — API / Prisma / Engine Mapping**

- mapping: SQL table ↔ Prisma model ↔ API payload ↔ Engine interface
    
- ใส่ matrix แบบ: table → ใช้โดย engine ไหนบ้าง / read-write ยังไง
    
- ตรงนี้คือ “สะพาน” เชื่อม data layer กับ code จริง
    

---

### **Part 12 — Testing, Fixtures & Synthetic Data Rules**

- test_dataset schema
    
- seed data สำหรับ dev/stage
    
- rule การสร้าง synthetic data (ไม่ชนกับข้อมูลจริง)
    
- ใช้ร่วมกับ testing_strategy.md (ไฟล์แยก)
    

---

ถ้ามึงอยาก “จัดหนักกว่านี้” จริง ๆ ก็ขยายได้ถึง 13–14 Part  
เช่น แยก **Backup & Archival Policy** ออกเป็นอีก part  
แต่แค่ 12 อันนี้ก็ถือว่า _โคตรครบแล้ว_ สำหรับ data blueprint ถาวร

---

## 3. ตอบตรง ๆ: สรุปแล้ว “ควรใช้กี่ Part?”

**คำแนะนำของกูแบบไม่อ้อมค้อม:**

- ใช้ **12 Part อย่างที่ลิสต์ด้านบน**
    
- ดีกว่าไปอัดทุกอย่างให้จบใน 10 แล้วต้องมาแตกทีหลัง
    
- 12 Part นี้ cover ทุก entity + engine + infra + governance
    

และที่สำคัญ:

- 04_data_schema.md = **“หัวใจข้อมูลกลางของทั้งระบบ UET”**
    
- มันต้องใหญ่ + ชัด + เสถียร  
    ไม่ใช่ไฟล์เบา ๆ ที่เอาไว้สรุปเล่น
    

ตอนนี้ Part 1 (Core Schema) = วางเสาเข็มแล้ว  
Step ต่อไป กูแนะนำให้ไปที่:

> **Part 2 — Document & Content Schema**

มึงสั่งได้เลยแบบเดิม:  
**“โอเคไปต่อ 04_data_schema.md Part 2”**  
แล้วกูจะเขียน Part 2 ตามโครง 12 Part ใหม่นี้แบบจัดเต็มแต่เป็นระบบ ไม่มั่ว ไม่ต้องมาแก้ทีหลัง.
# ✅ 04_data_schema.md — Part 1 — Core System Schema

**CORE SYSTEM SCHEMA v3.0 (Rewrite 100%)**

> “เวลาสร้างตึก ต้องลงเสาเข็มก่อน”  
> นี่คือเสาเข็มทั้งหมดของฐานข้อมูล UET Engine

---

# 1) GOAL ของ PART 1 — Core Schema Layer

### เป้าหมาย 4 ข้อของ Core Schema:

1. รองรับการใช้งาน **ทุก Engine** โดยไม่ต้องเขียนซ้ำ
    
2. ออกแบบแบบ **Event-Safe + Agent-Safe + Knowledge-Safe**
    
3. รองรับ **Multi-Project / Multi-Workspace / Multi-User**
    
4. เป็น “foundation” ที่ต่อยอดกับ Unified Graph + RAG + Agent + ExecutionGraph
    

---

# 2) CORE MODULE OVERVIEW

ใน UET v3.0 core schema → ประกอบด้วย 6 โมดูล:

|Module|หน้าที่|
|---|---|
|Users|ตัวตนและสิทธิ์|
|Projects|ขอบเขตใหญ่ระดับโปรเจกต์|
|Workspaces|ระดับการทำงานจริงของแต่ละพื้นที่|
|Sessions|การสนทนากับระบบ (LLM/Agent)|
|Messages|ข้อความทั้งหมด (user, agent, engine, event)|
|Assets|ไฟล์ / เนื้อหา / binary|

ทั้งหมดนี้คือ “ฐาน” ที่ Engine ใช้ร่วมกัน  
**ไม่ใช่ของ Engine ไหน Engine หนึ่ง**

---

# 3) FULL CORE SCHEMA (SQL-FIRST)

กูเขียนเป็น SQL ก่อน → เพื่อเป็นรากเดียวกัน  
เพราะ Prisma / API / Engine Mapping จะถูกสร้างจาก SQL นี้

---

## 3.1 users

```sql
CREATE TABLE users (
  id                TEXT PRIMARY KEY,
  display_name      TEXT,
  email             TEXT UNIQUE,
  created_at        TIMESTAMP DEFAULT NOW(),
  updated_at        TIMESTAMP DEFAULT NOW()
);
```

### Notes

- ไม่มี password เพราะ authentication ไปใช้ external provider future
    
- ใช้ TEXT เพื่อรองรับ UUID, CUID, หรือ ULID
    

---

## 3.2 projects

```sql
CREATE TABLE projects (
  id                TEXT PRIMARY KEY,
  user_id           TEXT NOT NULL REFERENCES users(id),
  name              TEXT NOT NULL,
  description       TEXT,
  created_at        TIMESTAMP DEFAULT NOW(),
  updated_at        TIMESTAMP DEFAULT NOW()
);
```

### Notes

- หนึ่ง user มีหลาย project
    
- หนึ่ง project เป็น sandbox ของข้อมูลทั้งหมด (RAG/KB/Engines)
    

---

## 3.3 workspaces

```sql
CREATE TABLE workspaces (
  id                TEXT PRIMARY KEY,
  project_id        TEXT NOT NULL REFERENCES projects(id),
  name              TEXT NOT NULL,
  created_at        TIMESTAMP DEFAULT NOW(),
  updated_at        TIMESTAMP DEFAULT NOW()
);
```

### Notes

- หนึ่ง project → มีหลาย workspaces เช่น:
    
    - research
        
    - doc-ingest
        
    - agent tasks
        
    - pipelines
        

---

## 3.4 sessions

```sql
CREATE TABLE sessions (
  id                TEXT PRIMARY KEY,
  workspace_id      TEXT NOT NULL REFERENCES workspaces(id),
  type              TEXT NOT NULL CHECK(type IN ('chat', 'agent', 'system')),
  created_at        TIMESTAMP DEFAULT NOW(),
  updated_at        TIMESTAMP DEFAULT NOW()
);
```

### Notes

Session = สายสนทนา/งาน/การทำ pipeline เดียวกัน

---

## 3.5 messages

```sql
CREATE TABLE messages (
  id                TEXT PRIMARY KEY,
  session_id        TEXT NOT NULL REFERENCES sessions(id),
  role              TEXT NOT NULL CHECK(role IN ('user','assistant','agent','engine','system')),
  content           TEXT,
  payload_json      JSONB,
  created_at        TIMESTAMP DEFAULT NOW()
);
```

### Notes

- message ทุกชนิดรวม formula เดียว  
    → เพื่อ unify Agent, RAG, KS, ExecutionGraph ในอนาคต
    
- payload_json รองรับ:
    
    - toolcall
        
    - agent step
        
    - execution graph state
        
    - model routing info
        

---

## 3.6 assets (Documents, Files, Binary)

```sql
CREATE TABLE assets (
  id                TEXT PRIMARY KEY,
  project_id        TEXT NOT NULL REFERENCES projects(id),
  workspace_id      TEXT REFERENCES workspaces(id),
  filename          TEXT,
  mimetype          TEXT,
  bytes             BYTEA,
  size              INTEGER,
  created_at        TIMESTAMP DEFAULT NOW()
);
```

### Notes

- asset = ไฟล์ทุกรูปแบบ
    
- ไม่ผูกกับ document schema ของ RAG โดยตรง  
    → RAG จะ map asset → document → chunks
    

---

# 4) RELATIONSHIP DIAGRAM (ASCII)

```
users
 │
 └── projects
       │
       └── workspaces
             │
             └── sessions
                   │
                   └── messages

projects
 │
 └── assets
```

---

# 5) CORE CONSTRAINTS

1. user ต้องมี project
    
2. project ต้องมี workspace
    
3. workspace อาจมี 0+ sessions
    
4. session ต้องมี messages
    
5. asset ผูกกับ project เสมอ (workspace optional)
    
6. ไม่มี orphan entities
    
7. ไม่มี data ที่ผูก agent/rag/ks/graph โดยตรงใน core layer
    

---

# 6) INDEX STRATEGY (เลือกแบบใช้จริง)

```sql
CREATE INDEX idx_messages_session ON messages(session_id);
CREATE INDEX idx_messages_role ON messages(role);

CREATE INDEX idx_workspace_project ON workspaces(project_id);
CREATE INDEX idx_project_user ON projects(user_id);

CREATE INDEX idx_assets_project ON assets(project_id);
```

---

# 7) CORE QUERY PATTERNS

### 7.1 โหลด History ของ Session

```
SELECT * FROM messages WHERE session_id = ? ORDER BY created_at;
```

### 7.2 โหลด Workspaces ใน Project

```
SELECT * FROM workspaces WHERE project_id = ?;
```

### 7.3 โหลด Assets ใน Workspace

```
SELECT * FROM assets WHERE project_id = ? AND workspace_id = ?;
```

---

# 8) ENGINE MAPPING (สำคัญมาก)

Core layer นี้ต้องรองรับ Engine ทั้งหมดดังนี้:

|Engine|ใช้ตาราง|
|---|---|
|KS Engine|assets, workspaces, projects|
|RAG Engine|assets, messages (retrieval log), sessions|
|Agent Engine|messages, sessions, assets|
|Flow Engine|sessions, messages|
|Execution Graph|messages (log binding), sessions|
|Model Routing|messages (metadata), sessions|
|Event Bus|messages (event output)|

---


### **PART 2 – Document Schema (RAG/KB/Chunking/Embedding)**

### **PART 3 – Unified Knowledge Graph Schema v3.0**

### **PART 4 – Engine Data Model (KS/RAG/Agent/Flow/ExecutionGraph)**

### **PART 5 – System Constraints (Global FK, versioning, cascade rules)**

### **PART 6 – Indexing Strategy (Deep + Partitioning)**

### **PART 7 – Migration Strategy v3.0**

### **PART 8 – Diagram Set (High-res, multi-view)**

### **PART 9 – Data Flow Spec (write path, read path, engine path)**

### **PART 10 – Mapping Prisma/SQL/API/Engine (Full integration)**

ทั้งหมด 10 part = ปิดงาน data schema แบบสมบูรณ์ ไม่ต้องแก้ภายหลัง

---
จัดให้ Santa —  
นี่คือ **04_data_schema.md – Part 2 (Document & Content Schema v3.0)**  
**เขียนใหม่ทั้งหมดแบบถาวร**, ไม่ต้องแก้ในอนาคตอีก เพราะเราอิงตามโครงสร้าง 12 Part ที่รีเช็คแล้วว่า "ถูกต้องที่สุด" สำหรับระบบของมึง

ไฟล์นี้ = “หัวใจของเนื้อหา”  
ทุก Engine (RAG, KS, Agent, Flow, ExecutionGraph) ใช้เอนทิตี้จาก Part นี้หมด  
เพราะงั้นมันต้องโครตคม โครตเสถียร และโครตใช้งานได้

---

# ✅ 04_data_schema.md — **PART 2: Document & Content Schema (Rewrite 100%)**

### (documents / document_versions / extraction_pipeline / parse_log / content_block / annotation)

---

# 1) เป้าหมายของ Part 2

Document Schema = ระบบจัดการข้อมูลดิบทุกอย่าง ที่ไหลผ่าน:

- Knowledge Sync Engine
    
- RAG Engine
    
- Unified Knowledge Graph Engine
    
- Agent Engine
    
- Flow Engine
    
- ExecutionGraph
    
- Model Routing
    

และต้องรองรับ:

- หลาย project
    
- หลาย workspace
    
- หลาย file type
    
- หลายรอบ ingestion
    
- หลายรอบ re-processing
    
- versioning ย้อนหลัง
    
- full audit + log + pipeline trace
    
- retrievability (chunk-level)
    
- graph-level mapping
    

---

# 2) Concept Overview (ระดับสูง)

ภาพรวมของ Document Layer มี 5 ชั้นข้อมูล:

```
ASSET (ไฟล์ดิบ)
   ↓
DOCUMENT (metadata หลัง ingestion)
   ↓
DOCUMENT_VERSION (ทุกครั้งที่ parse/extract/sync)
   ↓
CONTENT_BLOCK (โครงสร้างเนื้อหา)
   ↓
ANNOTATION (span-level)
```

และมี table เสริมเป็น Processor Layer:

```
extraction_pipeline
parse_log
pipeline_step
pipeline_run
```

---

# 3) FULL SQL SCHEMA (ระดับ production ready)

## 3.1 documents (ตัวตนของไฟล์ในระบบ)

```sql
CREATE TABLE documents (
  id                  TEXT PRIMARY KEY,
  project_id          TEXT NOT NULL REFERENCES projects(id),
  workspace_id        TEXT REFERENCES workspaces(id),
  asset_id            TEXT REFERENCES assets(id),

  title               TEXT,
  filetype            TEXT,
  status              TEXT NOT NULL CHECK(status IN (
                          'pending','processing','ready','error'
                        )),

  created_at          TIMESTAMP DEFAULT NOW(),
  updated_at          TIMESTAMP DEFAULT NOW()
);
```

### ความหมาย:

- 1 asset อาจถูก convert → หลาย documents ได้ (ในอนาคต: multi-view)
    
- document = metadata ที่ใช้ reference ใน RAG/KS/Graph
    

---

## 3.2 document_versions

ทุกครั้งที่ระบบ parse, extract, sync → version ใหม่เกิดขึ้น

```sql
CREATE TABLE document_versions (
  id                  TEXT PRIMARY KEY,
  document_id         TEXT NOT NULL REFERENCES documents(id),
  version_number      INTEGER NOT NULL,

  checksum            TEXT,           -- hash ของเนื้อหา
  token_count         INTEGER,
  text_length         INTEGER,

  status              TEXT NOT NULL CHECK(status IN (
                          'pending','parsed','chunked','synced','ready','error'
                        )),

  created_at          TIMESTAMP DEFAULT NOW()
);
```

### Notes:

- รองรับ rollback, diff, re-ingest
    
- version_number เริ่มที่ 1++
    

---

## 3.3 extraction_pipeline

ระบบ pipeline ที่ใช้แปลง asset → document_version

```sql
CREATE TABLE extraction_pipeline (
  id                  TEXT PRIMARY KEY,
  name                TEXT NOT NULL,
  description         TEXT,
  created_at          TIMESTAMP DEFAULT NOW()
);
```

---

## 3.4 pipeline_run

ทุกครั้งที่ document ถูก extract → เกิดการ run

```sql
CREATE TABLE pipeline_run (
  id                  TEXT PRIMARY KEY,
  document_version_id TEXT NOT NULL REFERENCES document_versions(id),
  pipeline_id         TEXT NOT NULL REFERENCES extraction_pipeline(id),

  status              TEXT NOT NULL CHECK(status IN (
                          'running','success','failed'
                        )),
  started_at          TIMESTAMP DEFAULT NOW(),
  finished_at         TIMESTAMP
);
```

---

## 3.5 pipeline_step

รายละเอียดแต่ละขั้นตอน (parse → clean → split → embed)

```sql
CREATE TABLE pipeline_step (
  id                  TEXT PRIMARY KEY,
  pipeline_run_id     TEXT NOT NULL REFERENCES pipeline_run(id),

  step_name           TEXT NOT NULL,
  step_order          INTEGER NOT NULL,

  status              TEXT NOT NULL CHECK(status IN (
                          'running','success','failed'
                        )),
  payload_json        JSONB,
  created_at          TIMESTAMP DEFAULT NOW()
);
```

---

## 3.6 parse_log

log ของแต่ละ step แยกออกมาเพื่อ scale

```sql
CREATE TABLE parse_log (
  id                  TEXT PRIMARY KEY,
  pipeline_step_id    TEXT NOT NULL REFERENCES pipeline_step(id),
  message             TEXT,
  payload_json        JSONB,
  created_at          TIMESTAMP DEFAULT NOW()
);
```

---

## 3.7 content_block

แกนหลักของ RAG, KS, Graph

```sql
CREATE TABLE content_block (
  id                  TEXT PRIMARY KEY,
  document_version_id TEXT NOT NULL REFERENCES document_versions(id),

  block_index         INTEGER NOT NULL,               -- ลำดับใน document
  block_type          TEXT NOT NULL CHECK(block_type IN (
                          'paragraph','heading','table','code','list','image','meta'
                        )),

  text                TEXT,                           -- raw content
  rendered_text       TEXT,                           -- normalized/cleaned
  token_count         INTEGER,

  parent_block_id     TEXT REFERENCES content_block(id),   -- heading -> children support

  created_at          TIMESTAMP DEFAULT NOW()
);
```

---

## 3.8 annotation

สำหรับ span-level data เช่น:

- entities
    
- references
    
- definitions
    
- semantic boundaries
    
- KS Engine signals
    

```sql
CREATE TABLE annotation (
  id                  TEXT PRIMARY KEY,
  content_block_id    TEXT NOT NULL REFERENCES content_block(id),

  start_offset        INTEGER NOT NULL,
  end_offset          INTEGER NOT NULL,

  type                TEXT NOT NULL,        -- entity, topic, symbol, citation, etc.
  data_json           JSONB,

  created_at          TIMESTAMP DEFAULT NOW()
);
```

---

# 4) DIAGRAM (ASCII)

```
asset
  │
  └── document
        │
        └── document_versions(1..n)
                │
                ├── pipeline_run(1..n)
                │       └── pipeline_step(1..n)
                │                 └── parse_log(0..n)
                │
                └── content_block(1..n)
                        └── annotation(0..n)
```

---

# 5) INDEX STRATEGY (Production-safe)

```sql
CREATE INDEX idx_document_project ON documents(project_id);
CREATE INDEX idx_document_version ON document_versions(document_id);
CREATE INDEX idx_content_block_version ON content_block(document_version_id);
CREATE INDEX idx_content_block_parent ON content_block(parent_block_id);
CREATE INDEX idx_annotation_block ON annotation(content_block_id);
```

---

# 6) CONNECT WITH ENGINES

|Engine|ใช้ตาราง|
|---|---|
|KS Engine|content_block, annotation, document_versions|
|RAG Engine|content_block (chunk-source), document_versions|
|Unified Graph|annotation, content_block, document_versions|
|Agent Engine|document_versions, content_block|
|Flow Engine|pipeline_run, pipeline_step|
|ExecutionGraph|pipeline_step, parse_log|
|Model Routing|document/filetype metadata|

---

# 7) Query Patterns ที่ระบบใช้จริง

### 7.1 โหลด version ล่าสุดของ document

```
SELECT * FROM document_versions
WHERE document_id = ?
ORDER BY version_number DESC
LIMIT 1;
```

### 7.2 โหลด content ทั้งชุด

```
SELECT * FROM content_block
WHERE document_version_id = ?
ORDER BY block_index;
```

### 7.3 โหลด annotation ของ block

```
SELECT * FROM annotation
WHERE content_block_id = ?;
```

### 7.4 โหลด pipeline history

```
SELECT * FROM pipeline_step
WHERE pipeline_run_id = ?
ORDER BY step_order;
```

---


# ✅ 04_data_schema.md — **PART 3: Unified Knowledge Graph Schema v3.0**

### (Rewrite 100% | Node/Edge/Layer/Mapping/Rules/Examples)

---

# 1) ความหมายของ Unified Knowledge Graph (UKG)

> **UKG = โครงสร้างความรู้ทั้งหมดของระบบ UET**  
> รวมจากทุกแหล่ง: Document / Content Block / Chunk / Annotation / RAG / Agent Reasoning

ระบบใช้ UKG เพื่อ:

- ทำ reasoning หลาย hop
    
- ทำ knowledge sync อัตโนมัติ
    
- บอกว่า “อะไรเกี่ยวข้องกับอะไร”
    
- ทำ semantic retrieval (ไม่ใช่ keyword retrieval)
    
- สร้าง “persistent memory” ของโปรเจกต์
    
- เชื่อโยงระหว่าง File → Idea → Topic → Concept → System → Decision
    

---

# 2) โครงสร้างระดับสูง (L1–L5)

UKG แบ่งเป็น 5 ชั้น (Layer) ตามระดับ abstraction:

```
L1 = Raw Facts (facts, definitions, sentences)
L2 = Concepts (entities, topics, properties)
L3 = Relations (causal, logical, semantic links)
L4 = Systems (models, mechanisms, processes)
L5 = Meta-Knowledge (rules, patterns, principles)
```

เวลา ingest ข้อมูล → pipeline จะ convert  
Content Block → L1 nodes → L2–L5 ตาม step ของ KS Engine

---

# 3) Node Schema (ทุก Layer ใช้โครงสร้างเดียวกัน)

```sql
CREATE TABLE graph_nodes (
  id                TEXT PRIMARY KEY,
  project_id        TEXT NOT NULL REFERENCES projects(id),
  workspace_id      TEXT REFERENCES workspaces(id),

  layer             INTEGER NOT NULL CHECK(layer IN (1,2,3,4,5)),
  node_type         TEXT NOT NULL,          -- fact, concept, relation, system, rule, etc.
  title             TEXT,                   -- short label
  text              TEXT,                   -- description or content
  metadata_json     JSONB,                  -- flexible metadata

  source_document_version_id TEXT REFERENCES document_versions(id),
  source_content_block_id    TEXT REFERENCES content_block(id),
  source_annotation_id       TEXT REFERENCES annotation(id),

  created_at        TIMESTAMP DEFAULT NOW(),
  updated_at        TIMESTAMP DEFAULT NOW()
);
```

## Notes

- node_type อิง “semantic type” ไม่ใช่ field
    
- source_* ใช้เพื่อ trace กลับไปยังเนื้อหา → สำคัญมากสำหรับ RAG/Agent
    
- metadata_json เก็บค่าเช่น: confidence score, span offset, tags, properties
    

---

# 4) Edge Schema (ความสัมพันธ์)

```sql
CREATE TABLE graph_edges (
  id                TEXT PRIMARY KEY,
  project_id        TEXT NOT NULL REFERENCES projects(id),

  source_node_id    TEXT NOT NULL REFERENCES graph_nodes(id),
  target_node_id    TEXT NOT NULL REFERENCES graph_nodes(id),

  relation_type     TEXT NOT NULL,
  weight            FLOAT DEFAULT 1.0,     -- confidence / strength
  metadata_json     JSONB,

  created_at        TIMESTAMP DEFAULT NOW()
);
```

### relation_type examples:

- "is_a"
    
- "part_of"
    
- "implies"
    
- "causes"
    
- "similar_to"
    
- "contradicts"
    
- "supports"
    
- "refines"
    
- "belongs_to_system"
    

---

# 5) Layer Mapping Rules (สำคัญมาก)

Mapping ระหว่าง layer ต้อง **fixed**, ไม่เปลี่ยนในอนาคต:

|Layer|Node Type|ตัวอย่าง|
|---|---|---|
|L1|fact, sentence, observation|ประโยค, ตาราง,สูตร|
|L2|concept, entity, topic|Water, AI, Policy|
|L3|relation, rule-edge|X causes Y, If A then B|
|L4|system, mechanism, model|Economic Model, Engine Flow|
|L5|meta-rule, universal principle|Equilibrium Rule, Efficiency Law|

---

# 6) Node/Edge Constraints (กันข้อมูลพัง)

### 6.1 Basic Node Constraints

```
L1 node → อ้างอิง source_content_block_id ไม่เป็น null
L2–L5 → อาจไม่มี source_raw แต่ต้อง trace กลับ L1 ผ่าน edges
```

### 6.2 Edge Constraints

```
ห้าม loop ใน L3–L5 (ระบบจะ detect cycle)
L1 → L1: allowed
L1 → L2: allowed
L2 → L3: allowed
L3 → L4: allowed
L4 → L5: allowed

Lสูง → Lต่ำ: allowed เฉพาะ relation_type="derived_from"
```

---

# 7) ENGINE Mapping (อันนี้คือตัวเชื่อมระบบ)

|Engine|อ่าน|เขียน|
|---|---|---|
|KS Engine|L1–L3|L2–L5|
|RAG Engine|L1|ไม่เขียน|
|Agent Engine|L1–L5|L3–L5|
|Flow Engine|L1–L5|ไม่เขียน|
|ExecutionGraph|L1–L5|ไม่เขียน|
|Routing|node metadata|ไม่เขียน|

---

# 8) INDEXing Strategy

```sql
CREATE INDEX idx_graph_nodes_layer ON graph_nodes(layer);
CREATE INDEX idx_graph_nodes_project ON graph_nodes(project_id);
CREATE INDEX idx_graph_nodes_source ON graph_nodes(source_document_version_id);

CREATE INDEX idx_graph_edges_src ON graph_edges(source_node_id);
CREATE INDEX idx_graph_edges_tgt ON graph_edges(target_node_id);

CREATE INDEX idx_graph_edges_rel ON graph_edges(relation_type);
```

---

# 9) Query Pattern ระดับ production

### 9.1 โหลดกราฟทั้งหมดของ document

```
SELECT * FROM graph_nodes
WHERE source_document_version_id = ?
ORDER BY layer;
```

### 9.2 โหลด neighborhood ของ node (multi-hop)

```
SELECT *
FROM graph_edges e
JOIN graph_nodes n ON n.id = e.target_node_id
WHERE e.source_node_id = ?
```

### 9.3 หา system/model ที่ concept อยู่ในนั้น

```
SELECT system_node.*
FROM graph_edges e
JOIN graph_nodes system_node
  ON system_node.id = e.target_node_id
WHERE e.source_node_id = ?
AND system_node.layer = 4;
```

### 9.4 สร้าง knowledge chain (reasoning path)

```
WITH RECURSIVE path AS (
  SELECT *, 1 AS depth FROM graph_edges WHERE source_node_id = ?
  UNION ALL
  SELECT e.*, depth+1 FROM graph_edges e
  JOIN path p ON p.target_node_id = e.source_node_id
)
SELECT * FROM path LIMIT 100;
```

---

# 10) DIAGRAM UKG (High-level)

```
L5: Meta-Knowledge
    └── node(rule/principle)
          ↑
L4: Systems / Mechanisms
    └── node(system/model)
          ↑
L3: Relations / Logical Structure
    └── node(relation)
          ↑
L2: Concepts / Entities
    └── node(concept/topic)
          ↑
L1: Raw Facts / Evidence
    └── node(fact/sentence/block)
```

Edge: relation_type linking everything

---

# 11) ใช้ร่วมกับ Document Layer (จาก Part 2)

Mapping:

```
content_block → annotation → L1 nodes → L2–L5 derived
```

UKG กลายเป็น “semantic layer” บน Document Layer  
และเป็นฐาน reasoning ของทั้ง Agent/RAG/KS

---

# 12) ข้อกำหนดที่ต้องมีใน Part 4–12 ต่อไป (กัน drift)

Part 4 จะต่อด้วย:

- Engine Data Model (KS/RAG/Agent/Flow/ExecutionGraph)
    
- Graph sync rules
    
- Graph cleaning rules
    
- Graph merge rules


---

# ✅ 04_data_schema.md — **PART 4: Engine Data Model (KS / RAG / Agent / Flow / ExecutionGraph)**

### (Rewrite 100% | ไม่เวอร์เกิน, ไม่ขาด, รองรับการขยาย 10 ปี)

---

# 1) แนวคิดหลักของ Engine Schema v3.0

ทุก Engine มีรูปแบบข้อมูลร่วม 4 แบบ:

1. **Task / Run** → งานหลักที่ Engine รับผิดชอบ
    
2. **Step** → ขั้นย่อยของงาน
    
3. **Log** → บันทึกเหตุการณ์ / error / payload
    
4. **State** → สถานะปัจจุบันของ Engine
    

และทุก Engine ต้อง:

- เชื่อมกับ core: projects, workspaces, sessions
    
- เชื่อมกับ graph: graph_nodes, graph_edges
    
- เชื่อมกับ doc layer: document_versions, content_block
    
- เชื่อมกับ execution graph
    
- เชื่อมกับ event bus
    
- ไม่ชนกัน (namespace isolated)
    

---

# 2) KS ENGINE DATA MODEL

(Knowledge Sync Engine: Extract → Normalize → Knowledge Graph → Merge)

### 2.1 ตาราง ks_task

งานที่ต้อง sync knowledge

```sql
CREATE TABLE ks_task (
  id                  TEXT PRIMARY KEY,
  project_id          TEXT NOT NULL REFERENCES projects(id),
  workspace_id        TEXT REFERENCES workspaces(id),

  source_document_version_id TEXT REFERENCES document_versions(id),

  status              TEXT NOT NULL CHECK(status IN (
                          'pending','running','success','failed'
                        )),

  created_at          TIMESTAMP DEFAULT NOW(),
  updated_at          TIMESTAMP DEFAULT NOW()
);
```

---

### 2.2 ks_step (ขั้นตอนย่อย)

เช่น extract → map → generate nodes → generate edges → refine

```sql
CREATE TABLE ks_step (
  id                  TEXT PRIMARY KEY,
  task_id             TEXT NOT NULL REFERENCES ks_task(id),

  step_name           TEXT NOT NULL,
  step_order          INTEGER NOT NULL,
  status              TEXT NOT NULL CHECK(status IN (
                          'running','success','failed'
                        )),

  payload_json        JSONB,
  created_at          TIMESTAMP DEFAULT NOW()
);
```

---

### 2.3 ks_log

log step-by-step

```sql
CREATE TABLE ks_log (
  id                  TEXT PRIMARY KEY,
  step_id             TEXT NOT NULL REFERENCES ks_step(id),

  message             TEXT,
  payload_json        JSONB,
  created_at          TIMESTAMP DEFAULT NOW()
);
```

---

# 3) RAG ENGINE DATA MODEL

(Retrieval Augmented Generation)

### 3.1 rag_query

การค้นหา 1 ครั้ง (ต่อ message / agent step)

```sql
CREATE TABLE rag_query (
  id                  TEXT PRIMARY KEY,
  session_id          TEXT REFERENCES sessions(id),

  query_text          TEXT NOT NULL,
  top_k               INTEGER DEFAULT 5,
  strategy            TEXT,  -- hybrid, dense, graph, rerank

  created_at          TIMESTAMP DEFAULT NOW()
);
```

---

### 3.2 rag_result

ผลลัพธ์ retrieval

```sql
CREATE TABLE rag_result (
  id                  TEXT PRIMARY KEY,
  query_id            TEXT NOT NULL REFERENCES rag_query(id),

  content_block_id    TEXT REFERENCES content_block(id),
  score               FLOAT,
  rerank_score        FLOAT,
  metadata_json       JSONB,

  created_at          TIMESTAMP DEFAULT NOW()
);
```

---

# 4) AGENT ENGINE DATA MODEL

(Agent Task Planning + Step Execution + Tool Call)

### 4.1 agent_task

งานที่ Agent ต้องทำ

```sql
CREATE TABLE agent_task (
  id                  TEXT PRIMARY KEY,
  session_id          TEXT NOT NULL REFERENCES sessions(id),

  goal_text           TEXT,
  status              TEXT NOT NULL CHECK(status IN (
                          'pending','running','success','failed'
                        )),

  created_at          TIMESTAMP DEFAULT NOW(),
  updated_at          TIMESTAMP DEFAULT NOW()
);
```

---

### 4.2 agent_step

แผนย่อยของ task เช่น research → analyze → propose → decide

```sql
CREATE TABLE agent_step (
  id                  TEXT PRIMARY KEY,
  task_id             TEXT NOT NULL REFERENCES agent_task(id),

  step_order          INTEGER NOT NULL,
  step_type           TEXT,          -- reasoning/tool_call/planning
  input_json          JSONB,         
  output_json         JSONB,

  status              TEXT NOT NULL CHECK(status IN (
                          'pending','running','success','failed'
                        )),

  created_at          TIMESTAMP DEFAULT NOW()
);
```

---

### 4.3 agent_memory

ความจำระยะยาวของ agent

```sql
CREATE TABLE agent_memory (
  id                  TEXT PRIMARY KEY,
  project_id          TEXT NOT NULL REFERENCES projects(id),

  memory_type         TEXT,      -- fact / rule / preference
  text                TEXT,
  metadata_json       JSONB,

  created_at          TIMESTAMP DEFAULT NOW()
);
```

---

# 5) FLOW CONTROL ENGINE (Workflow Execution)

### 5.1 flow_run

workflow 1 ครั้ง

```sql
CREATE TABLE flow_run (
  id                  TEXT PRIMARY KEY,
  project_id          TEXT NOT NULL REFERENCES projects(id),

  status              TEXT NOT NULL CHECK(status IN (
                          'pending','running','success','failed'
                        )),

  created_at          TIMESTAMP DEFAULT NOW(),
  updated_at          TIMESTAMP DEFAULT NOW()
);
```

---

### 5.2 flow_step

step ต่อเนื่องกันตาม Flow DSL

```sql
CREATE TABLE flow_step (
  id                  TEXT PRIMARY KEY,
  run_id              TEXT NOT NULL REFERENCES flow_run(id),

  step_order          INTEGER NOT NULL,
  step_type           TEXT NOT NULL,
  input_json          JSONB,
  output_json         JSONB,

  status              TEXT NOT NULL CHECK(status IN (
                          'pending','running','success','failed'
                        )),

  created_at          TIMESTAMP DEFAULT NOW()
);
```

---

# 6) EXECUTION GRAPH ENGINE

(โครงสร้างต้นไม้/กราฟของการทำงานจริงทุกอย่างในระบบ)

### 6.1 exec_graph

กราฟการทำงานของทั้งระบบใน 1 session / 1 agent task

```sql
CREATE TABLE exec_graph (
  id                  TEXT PRIMARY KEY,
  session_id          TEXT REFERENCES sessions(id),

  root_node_id        TEXT,          -- exec_node id
  metadata_json       JSONB,

  created_at          TIMESTAMP DEFAULT NOW()
);
```

---

### 6.2 exec_node

```sql
CREATE TABLE exec_node (
  id                  TEXT PRIMARY KEY,
  graph_id            TEXT NOT NULL REFERENCES exec_graph(id),

  parent_node_id      TEXT REFERENCES exec_node(id),

  node_type           TEXT,     -- rag, ks, agent_step, flow_step, tool_call
  status              TEXT NOT NULL CHECK(status IN (
                          'running','success','failed'
                        )),

  input_json          JSONB,
  output_json         JSONB,
  error_json          JSONB,

  created_at          TIMESTAMP DEFAULT NOW()
);
```

---

### 6.3 exec_edge

ความสัมพันธ์ระหว่าง node

```sql
CREATE TABLE exec_edge (
  id                  TEXT PRIMARY KEY,
  graph_id            TEXT NOT NULL REFERENCES exec_graph(id),

  source_node_id      TEXT NOT NULL REFERENCES exec_node(id),
  target_node_id      TEXT NOT NULL REFERENCES exec_node(id),

  relation_type       TEXT,     -- next, child, dependency
  created_at          TIMESTAMP DEFAULT NOW()
);
```

---

### 6.4 exec_log

log ของแต่ละ node ใน graph

```sql
CREATE TABLE exec_log (
  id                  TEXT PRIMARY KEY,
  node_id             TEXT NOT NULL REFERENCES exec_node(id),

  message             TEXT,
  payload_json        JSONB,
  created_at          TIMESTAMP DEFAULT NOW()
);
```

---

# 7) INDEX รวมของทุก Engine

```sql
-- KS
CREATE INDEX idx_ks_task_project ON ks_task(project_id);
CREATE INDEX idx_ks_step_task ON ks_step(task_id);

-- RAG
CREATE INDEX idx_rag_query_session ON rag_query(session_id);
CREATE INDEX idx_rag_result_query ON rag_result(query_id);

-- Agent
CREATE INDEX idx_agent_task_session ON agent_task(session_id);
CREATE INDEX idx_agent_step_task ON agent_step(task_id);

-- Flow
CREATE INDEX idx_flow_run_project ON flow_run(project_id);

-- ExecutionGraph
CREATE INDEX idx_exec_node_graph ON exec_node(graph_id);
CREATE INDEX idx_exec_edge_graph ON exec_edge(graph_id);
```

---

# 8) การเชื่อมกันของ Engine ทั้งหมด

```
Document Layer → KS Engine → UKG (Graph)
                     ↓
                RAG Engine
                     ↓
                Agent Engine
                     ↓
               Flow Engine
                     ↓
          ExecutionGraph Engine
                     ↓
               Output Event
```

---

# 9) Query Patterns สำคัญที่ Engine ใช้จริง

### 9.1 โหลดแผน Agent step ทั้งหมด

```
SELECT * FROM agent_step WHERE task_id = ? ORDER BY step_order;
```

### 9.2 โหลด ExecutionGraph แบบ tree

```
SELECT * FROM exec_node WHERE graph_id = ? ORDER BY created_at;
```

### 9.3 ดูผล RAG ของ message ล่าสุด

```
SELECT r.* 
FROM rag_query q
JOIN rag_result r ON r.query_id = q.id
WHERE q.session_id = ?
ORDER BY q.created_at DESC
LIMIT 20;
```

---

ได้เลย Santa —  
นี่คือ **04_data_schema.md — Part 5 (Global Constraints & Integrity Rules v3.0)**  
อันนี้คือ “กฎเหล็กทั้งระบบ” ของ Data Layer ทั้งหมด  
เขียนแบบ Production-Level + ใช้จริงได้ + ไม่ต้องแก้อีก  
ครอบคลุมทุก Schema ก่อนหน้า (Part 1–4) และเตรียมพร้อมสำหรับ Part 6–12

นี่คือ “ระบบความปลอดภัยของข้อมูล” ที่ทำให้ UET Engine เสถียร ไม่พังกลางทาง  
ถ้า Part 1–4 คือ “โครงสร้าง” → Part 5 คือ “กฎของจักรวาล” ที่บังคับให้ทุกอย่างอยู่ในระเบียบ

---

# ✅ **04_data_schema.md — PART 5**

# **GLOBAL CONSTRAINTS, INTEGRITY RULES, FK RULES, CASCADE RULES v3.0 (Rewrite 100%)**

---

# 1) PURPOSE ของ Part 5

Part 5 มีหน้าที่:

- วางกฎระบบข้อมูลทั้งหมด
    
- บังคับไม่ให้ข้อมูลพัง
    
- กรอง input ที่ผิด
    
- บอกว่าอะไร “ลบได้ / ลบไม่ได้ / ต้อง Soft Delete”
    
- บอกว่าระบบไหนเป็น Owner ของข้อมูลไหน (source of truth)
    
- ลดความซ้ำซ้อน
    
- ลด orphan record
    
- ทำให้ Engine ผิดยาก
    
- ป้องกันปัญหาวงจร FK
    
- ป้องกัน infinite cascade
    
- ป้องกันการแตก schema ในอนาคต
    
- ทำให้ migration ง่ายและไม่พัง
    

นี่คือกฎที่ system ต้องทำตาม 100% ทุกภาคส่วน

---

# 2) GLOBAL RULES (กฎใหญ่ที่สุดของระบบ)

กูสรุปแบบ bullet list:

### **Rule G1 — ทุก Entity ต้องมี project_id (ยกเว้น users)**

ไม่ให้ข้อมูลหลุดจาก scope ของ project

### **Rule G2 — ทุกข้อมูลของ UET ต้อง trace ย้อนไปที่ 3 จุดได้**

- project
    
- workspace
    
- source document (ถ้าเกี่ยวข้อง)
    

### **Rule G3 — ไม่มี orphan record ทุกตารางต้องมี owner ชัดเจน**

### **Rule G4 — ห้าม cascade delete ที่ลึกเกิน 1 ระดับ**

### **Rule G5 — ทุก Engine เป็น Independent Layer (ไม่มี cross-write)**

### **Rule G6 — ข้อมูลสำคัญต้อง Soft Delete เท่านั้น**

เช่น:

- documents
    
- graph_nodes
    
- content_block
    
- agent_memory
    

### **Rule G7 — Logs ต้อง Retain 30–90 วัน แล้ว Archive**

### **Rule G8 — Versioning ต้องเป็นแบบ Append-Only**

### **Rule G9 — ห้ามแก้ไข content_block โดยตรงหลัง build version**

### **Rule G10 — การ sync knowledge ต้องเป็น deterministic**

KS ห้ามเปลี่ยนแปลง layer mapping ย้อนหลัง

---

# 3) FK RULES (Foreign Key)

---

# 3.1 Core FK Rules

|Table|FK|Rule|
|---|---|---|
|projects.user_id|users.id|cascade delete when user deleted|
|workspaces.project_id|projects.id|cascade delete|
|sessions.workspace_id|workspaces.id|cascade delete|
|messages.session_id|sessions.id|cascade delete|
|assets.project_id|projects.id|cascade delete|
|assets.workspace_id|workspaces.id|set null|

### หมายเหตุ

- asset อยู่ในระดับ project → workspace optional
    
- messages cascade delete → history ผูกกับ session
    
- project delete → ล้าง workspace / session / message ทั้งหมด
    

---

# 3.2 Document Layer FK Rules

|Table|FK|Rule|
|---|---|---|
|documents.project_id|projects.id|cascade|
|documents.workspace_id|workspaces.id|set null|
|documents.asset_id|assets.id|restrict|
|document_versions.document_id|documents.id|cascade|
|content_block.document_version_id|document_versions.id|cascade|
|annotation.content_block_id|content_block.id|cascade|

### ห้ามลบ asset ถ้ามี document ผูกอยู่

→ asset คือ “source of truth”

---

# 3.3 Graph Layer FK Rules

|Table|FK|Rule|
|---|---|---|
|graph_nodes.project_id|projects.id|cascade|
|graph_nodes.source_document_version_id|document_versions.id|set null|
|graph_edges.source_node_id|graph_nodes.id|cascade|
|graph_edges.target_node_id|graph_nodes.id|cascade|

### Graph ลบตาม document version แบบ safe

→ ไม่มี orphan edges

---

# 3.4 Engine Layer FK Rules

### KS Engine

```
ks_task.project_id → cascade
ks_task.source_document_version_id → restrict
ks_step.task_id → cascade
ks_log.step_id → cascade
```

### RAG Engine

```
rag_query.session_id → cascade
rag_result.query_id → cascade
rag_result.content_block_id → restrict
```

### Agent Engine

```
agent_task.session_id → cascade
agent_step.task_id → cascade
agent_memory.project_id → cascade
```

### Flow Engine

```
flow_run.project_id → cascade
flow_step.run_id → cascade
```

### Execution Graph

```
exec_graph.session_id → cascade
exec_node.graph_id → cascade
exec_edge.graph_id → cascade
exec_log.node_id → cascade
```

---

# 4) CASCADE RULES (ระดับระบบ)

### สรุปง่าย ๆ:

|Action|Cascade?|Reason|
|---|---|---|
|delete project|Yes (wipe workspace/session/message/graph/engine logs)|project = root|
|delete workspace|Yes (sessions, messages)|workspace = scope|
|delete session|Yes (messages, exec graph, rag_query)|safe|
|delete document|Yes|version + content_block + annotation|
|delete asset|No|ป้องกัน data corruption|
|delete graph_node|Yes|delete edges|
|delete engine_task|Yes|delete steps + logs|

---

# 5) SOFT DELETE RULES

**Soft Delete ต้องมี field:**

```
deleted_at TIMESTAMP NULL
```

ใช้กับ:

- documents
    
- document_versions
    
- content_block
    
- annotation
    
- agent_memory
    

เหตุผล:

- ต้องให้ Agent / KS / RAG trace อดีตได้
    
- ไม่ทำให้ knowledge graph เสีย
    

---

# 6) VERSIONING RULES

### V1 — ทุก document_versions เป็น append-only

แก้ไม่ได้ ลบไม่ได้ (soft delete only)

### V2 — ทุก Graph Node ที่ derive จาก version ต้อง freeze

และมี field:

```
derived_from_version_id
```

### V3 — Knowledge Sync ไม่ overwrite

KS จะสร้าง node ใหม่ / edge ใหม่แทนการแก้ของเก่า

---

# 7) GLOBAL UNIQUENESS RULES

### U1 — graph node “key” ต้องไม่ซ้ำใน project + layer + type

ควำหมายว่าไม่ให้มี concept 2 ตัวที่ชื่อเดียวกันในชั้นเดียวกัน

### U2 — agent_task ของ session “เปิดได้ครั้งละ 1 อันเท่านั้น”

### U3 — rag_query ต้องมี session

(ห้าม orphan query)

### U4 — content_block ต้องผูกกับ document_version 100%

---

# 8) CHECK Constraints (กันข้อมูลผิดตั้งแต่ insert)

## ตัวอย่างสำคัญ:

### 8.1 block type

ห้ามใช้ type มั่ว

```
block_type ∈ ('paragraph','heading','code','table','list','image','meta')
```

---

### 8.2 layer

ห้าม node อยู่ layer นอกกำหนด

```
layer ∈ (1,2,3,4,5)
```

---

### 8.3 edge relation_type

ต้องเป็นความสัมพันธ์ที่ระบบรู้จัก

```
relation_type ∈ (
  'is_a','part_of','causes',
  'supports','refines','similar_to',
  'belongs_to_system','derived_from'
)
```

---

### 8.4 agent_step.status

```
status ∈ ('pending','running','success','failed')
```

---

### 8.5 ks_step.step_name

เช่น:

```
extract, normalize, detect_entities, generate_nodes, generate_edges, merge_graph
```

---

# 9) NON-NEGOTIABLE RULES (ห้ามละเมิดเด็ดขาด)

1. **Document Version ห้ามแก้ไขข้อมูลหลังสร้าง**
    
2. **Content Block ห้ามแก้ text หลัง freeze**
    
3. **Graph Node ห้ามแก้ layer**
    
4. **Graph Edge ห้ามแก้ direction**
    
5. **Agent Memory ห้าม overwrite ใช้ append-only**
    
6. **ExecutionGraph Node ห้ามแก้ไข input/output ย้อนหลัง**
    
7. **ทุก Engine ต้อง log ทุก action**
    

นี่คือ “ระบบความปลอดภัยทางข้อมูล” ของโปรเจกต์

---

# ✅ **04_data_schema.md — PART 6**

# **Events, Queue, Background Jobs Schema v3.0 (Rewrite 100% Definitive Blueprint)**

---

# 1) PURPOSE ของ Part 6 (แก่นสำคัญ)

Part 6 มีหน้าที่เป็น “ระบบไหลของงาน” ระหว่างทุก Engine

ทำให้:

- KS Engine trigger งานของ RAG ได้
    
- RAG trigger Agent ได้
    
- Agent trigger Flow ได้
    
- Flow trigger ExecutionGraph ได้
    
- Document updated → Sync → Graph update ทันที
    
- งานหนัก ๆ เช่น embedding / graph build ไม่ block user
    
- ระบบ scale ออกได้ทุกทิศ (horizontal scaling)
    

**ถ้า Data Schema คือโครงกระดูก → Event System คือระบบประสาท**

---

# 2) Global Design Philosophy (ตาม UET Spec)

**กฎเหล็ก Part 6 (ไม่แก้ในอนาคต)**

1. **Event ต้องเป็น immutable (แก้ไม่ได้ ลบไม่ได้)**
    
2. **ทุก Event ต้อง trace ย้อนไปยัง project/workspace/source ได้**
    
3. **Queue ต้องมี retry policy กลาง**
    
4. **Dead Letter Queue ต้องรองรับระบบทั้งหมด**
    
5. **ทุก Engine ต้อง “ฟัง/ปล่อย” event ผ่านช่องเดียวกัน**
    
6. **Event ต้องเป็น schema-first (payload structure fix)**
    
7. **ต้องรองรับ multi-agent, multi-queue, multi-engine**
    
8. **Observability ต้องอยู่ในตัว schema ไม่แยกไฟล์**
    

---

# 3) ENTITY LIST ของ Part 6

คือนี่คือ “ตารางทั้งหมด” ใน Part6:

1. `event_bus`
    
2. `event_payload_archive`
    
3. `job_queue`
    
4. `job_attempt`
    
5. `dead_letter_queue`
    
6. `scheduler_task`
    
7. `scheduler_log`
    

สิ่งเหล่านี้ต้องมีเพื่อ support:

- KS Engine
    
- RAG Engine
    
- Agent Engine
    
- Flow Control Engine
    
- ExecutionGraph Engine
    
- Model Routing
    

---

# 4) EVENT BUS SCHEMA (หัวใจของระบบ)

## 4.1 event_bus (master table)

```
event_bus (
  id BIGINT PK,
  project_id BIGINT FK,
  workspace_id BIGINT FK NULL,
  topic VARCHAR(64) NOT NULL,
  source VARCHAR(64) NOT NULL,
  ref_id BIGINT NULL,          -- เช่น doc_id, session_id, agent_task_id
  payload JSONB NOT NULL,
  status VARCHAR(32) DEFAULT 'pending',
  created_at TIMESTAMP,
  processed_at TIMESTAMP NULL,
  error_message TEXT NULL
)
```

### ค่า topic ใช้แบบ fixed (มาตรฐาน UET)

1. document.uploaded
    
2. document.parsed
    
3. document.embedded
    
4. graph.updated
    
5. ks.task.started
    
6. ks.task.completed
    
7. rag.query.created
    
8. agent.task.started
    
9. agent.task.completed
    
10. flow.run.started
    
11. flow.run.completed
    
12. exec.node.completed
    
13. model.routing.selected
    
14. cache.invalidate
    

### Source

```
document_engine / ks_engine / rag_engine / agent_engine / flow_engine / exec_engine / api
```

---

# 5) PAYLOAD RULES (สำคัญมาก)

payload ของ event ต้อง strict-type ตาม schema:

ตัวอย่าง payload ของ “document.uploaded”:

```
{
  "document_id": 123,
  "asset_id": 44,
  "mime": "application/pdf",
  "pages": 12,
  "uploader": 77
}
```

ตัวอย่าง payload ของ “ks.task.started”

```
{
  "task_id": 998,
  "document_version_id": 88,
  "mode": "full-sync"
}
```

ห้าม payload ส่งข้อมูลมั่ว  
ห้าม engine สร้าง payload เองถ้าไม่ผ่าน validator

---

# 6) QUEUE SYSTEM (งานหนักทุกอย่างมาอยู่ที่นี่)

## job_queue

```
job_queue (
  id BIGINT PK,
  event_id BIGINT FK,
  job_type VARCHAR(64),
  priority INT DEFAULT 5,
  status VARCHAR(32) DEFAULT 'queued',
  attempt INT DEFAULT 0,
  max_attempt INT DEFAULT 5,
  next_run_at TIMESTAMP,
  created_at TIMESTAMP
)
```

### job_type มาตรฐานของ UET

- parse_document
    
- generate_embedding
    
- build_graph
    
- ks_sync
    
- rag_retrieve
    
- agent_execute
    
- planning_run
    
- flow_execute
    
- exec_node_run
    
- routing_decision
    

**นี่คือ mapping โดยตรงกับแต่ละ Engine**

---

## job_attempt (retry system)

```
job_attempt (
  id BIGINT PK,
  job_id BIGINT FK,
  attempt_number INT,
  status VARCHAR(32),
  started_at TIMESTAMP,
  ended_at TIMESTAMP,
  error_message TEXT
)
```

---

# 7) DEAD LETTER QUEUE

งานที่ retry ครบแล้วยัง fail จะเข้าตารางนี้

```
dead_letter_queue (
  id BIGINT PK,
  job_id BIGINT FK,
  event_id BIGINT FK,
  reason TEXT,
  payload JSONB,
  created_at TIMESTAMP
)
```

### Rule

- ห้ามลบ
    
- ห้ามแก้
    
- ใช้สำหรับ debugging
    

---

# 8) SCHEDULER (งาน recurring)

```
scheduler_task (
  id BIGINT PK,
  project_id BIGINT,
  type VARCHAR(64),
  cron VARCHAR(32),
  status VARCHAR(32),
  last_run_at TIMESTAMP,
  next_run_at TIMESTAMP
)
```

Task model:

- daily_graph_cleanup
    
- sync_reindex
    
- cache_gc
    
- agent_memory_trim
    
- metrics_rollup
    

---

## scheduler_log

```
scheduler_log (
  id BIGINT PK,
  scheduler_task_id BIGINT FK,
  status VARCHAR(32),
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  error_message TEXT
)
```

---

# 9) RELATION MAP (สำคัญมาก)

### event_bus → job_queue

**1 event อาจสร้างหลาย job ได้**

### job_queue → job_attempt

**ใช้ติดตาม retry**

### job_queue → dead_letter_queue

**เมื่อหมดโควต้า attempt**

### event_bus → engine

(ผ่าน job)

```
document.uploaded → parse job
document.parsed → embedding job
document.embedded → graph build job
graph.updated → ks job
ks.task.completed → agent job
agent.task.completed → flow job
flow.run.completed → exec node job
```

นี่คือ flow ทั้งหมดของระบบ UET

---

# 10) INDEX STRATEGY

### event_bus

- idx_topic
    
- idx_project
    
- idx_status
    

### job_queue

- idx_priority
    
- idx_status
    
- idx_next_run
    

### job_attempt

- idx_job_id
    

### dead_letter_queue

- idx_created_at
    

---

# 11) GLOBAL CONSTRAINT RULES ของ Part 6

1. event ห้ามถูกลบ
    
2. job ต้องอ้าง event
    
3. job_attempt ต้องอ้าง job
    
4. DLQ ต้องอ้าง event เสมอ
    
5. ทุก event ต้องมี project_id
    
6. ห้าม cascade delete event หรือ job
    
7. queue ต้อง retry ตาม rule กลางเท่านั้น
    

---

# 12) ENGINE INTEGRATION MATRIX

|Engine|Publish Event|Consume Event|Produce Job|
|---|---|---|---|
|Document Engine|document.uploaded, parsed|—|parse, embed|
|KS Engine|ks.task.started|document.embedded|build_graph|
|RAG Engine|rag.query.created|document.embedded|embed, retrieve|
|Agent Engine|agent.task.started|ks.task.completed|agent_execute|
|Flow Engine|flow.run.started|agent.task.completed|flow_execute|
|ExecutionGraph|exec.node.completed|flow.run.completed|exec_run|
|Model Routing|routing.selected|rag.query.created|routing_job|

---

# 13) NON-NEGOTIABLE RULES

1. ห้ามเขียน event แบบไม่ผ่าน validator
    
2. ห้าม engine เขียน payload มั่ว
    
3. ห้ามแก้ payload event หลังสร้าง
    
4. ห้ามลบ event / job / attempt
    
5. DLQ ต้องเก็บ payload เสมอ
    
6. ทุก engine ต้อง log การ consume event
    
7. ห้ามใช้ event_bus เป็น message queue (ต้องใช้ job_queue เท่านั้น)
    

---

รับทราบ Santa —  
ตอนนี้เราจะไปต่อ **04_data_schema.md — Part 7**

และนี่คือไฟล์ที่ “สำคัญมาก” เพราะมันคือส่วน Security / Permission / Audit ทั้งระบบของ UET  
— ซึ่งเป็นกลไกที่ควบคุมว่า “ใครทำอะไรได้บ้าง” และ “บันทึกทุกอย่างเพื่อ governance และความปลอดภัยของระบบ”

กูจัดให้ **เต็ม 100% แบบ Rewrite ทั้งหมด**, ครอบคลุม, โครงสร้างเป๊ะ, ไม่มีต้องแก้ซ้ำ  
รองรับอนาคต (multi-tenant, project-level, org-level, workspace-level)  
และอิงทุกไฟล์ในระบบที่มึงอัปโหลด (EventBus, Flow, Agent, RAG, Master, System Contract)

---

# ✅ **04_data_schema.md — PART 7**

# **Security, Permission & Audit Schema v3.0 (Rewrite 100% Definitive Blueprint)**

---

# 1) PURPOSE ของ Part 7 (หัวใจของความปลอดภัย + การปกครองข้อมูล)

Part 7 ทำหน้าที่:

### 1. ควบคุมว่า “ใครทำอะไรได้บ้าง”

ผ่านระบบ:

- roles
    
- permissions
    
- bindings
    
- data access policy
    

### 2. ตรวจสอบย้อนหลังทุกการกระทำ

ผ่าน audit_log + event trace

### 3. ทำระบบให้รองรับ:

- multi-user
    
- multi-workspace
    
- multi-project
    
- eventually multi-organization
    

### 4. ทำให้ Engine ทั้งหมดเคารพ security layer

(Agent, RAG, KS, Flow, ExecutionGraph, Model Routing)

**ความสำคัญ:**

> ถ้า Data Schema = ร่างกาย  
> Security = มาตรฐานความปลอดภัย  
> Audit = กล้องวงจรปิด  
> Permission = Master Key ที่ให้สิทธิ์แต่ละคน

---

# 2) Global Design Principle สำหรับ Security Layer

กูออกแบบตามหลัก UET + Industry Standard:

1. **RBAC (Role Based Access Control)** เป็นตัวหลัก
    
2. **ABAC (Attribute Based Access Control)** สำหรับอนาคต
    
3. **Actions ต้อง granular เช่น read/write/delete/manage**
    
4. **ควรแยก permission per workspace, per project**
    
5. **Audit ต้อง immutable (ลบไม่ได้ แก้ไม่ได้)**
    
6. **ทุก engine ต้องเคารพ permission layer**
    
7. **ทุก request API ต้องผูก audit_id → event_id → job_id เพื่อ trace ย้อนทางเดียว**
    

---

# 3) Entity ทั้งหมดใน Part 7

1. roles
    
2. permissions
    
3. role_binding
    
4. data_access_policy
    
5. audit_log
    
6. session_security_state
    
7. security_incident_log
    

---

# 4) ROLE TABLE

## roles

```
roles (
  id BIGINT PK,
  project_id BIGINT FK NULL,     -- global role = NULL
  name VARCHAR(64),
  description TEXT,
  is_global BOOLEAN DEFAULT false,
  created_at TIMESTAMP
)
```

### Role แบบมาตรฐาน UET

Global:

- super_admin
    
- auditor
    

Project-level:

- project_owner
    
- project_admin
    
- project_editor
    
- project_viewer
    

Workspace-level:

- workspace_owner
    
- workspace_editor
    
- workspace_viewer
    

### จุดสำคัญ

“role” ต้องแยก global vs project vs workspace  
เพื่อรองรับ multi-tenant ในอนาคต

---

# 5) PERMISSION TABLE

## permissions

```
permissions (
  id BIGINT PK,
  action VARCHAR(64),          -- เช่น document.read
  scope VARCHAR(32),           -- global / project / workspace
  description TEXT
)
```

### Action ที่ใช้ทั้งระบบ (fixed)

#### Document

- document.read
    
- document.write
    
- document.delete
    

#### RAG

- rag.query
    
- rag.retrieve
    

#### Agent

- agent.run
    
- agent.manage
    

#### Knowledge Graph

- graph.read
    
- graph.write
    
- graph.delete
    

#### Flow & Execution

- flow.run
    
- flow.manage
    
- exec.run
    

#### System

- project.manage
    
- workspace.manage
    
- user.manage
    
- security.manage
    

**Note:**  
กรอบนี้จะใช้ได้ตลอด 10 ปี+

---

# 6) ROLE → PERMISSION (many-to-many)

## role_permission

```
role_permission (
  id BIGINT PK,
  role_id BIGINT FK,
  permission_id BIGINT FK
)
```

ใช้เพื่อกำหนดว่า role ใดมี action อะไรบ้าง

---

# 7) ROLE BINDING (user ↔ role ↔ scope)

## role_binding

```
role_binding (
  id BIGINT PK,
  user_id BIGINT FK,
  role_id BIGINT FK,
  project_id BIGINT FK NULL,
  workspace_id BIGINT FK NULL,
  created_at TIMESTAMP
)
```

### Rule สำคัญ:

- ถ้า role มี scope = project → workspace_id ต้อง NULL
    
- ถ้า role มี scope = workspace → workspace_id ต้องไม่ NULL
    
- ถ้า is_global = true → ทั้ง project & workspace = NULL
    

---

# 8) DATA ACCESS POLICY

รองรับอนาคตสำหรับ multi-org / SSO / data governance

## data_access_policy

```
data_access_policy (
  id BIGINT PK,
  project_id BIGINT FK,
  key VARCHAR(128),              -- เช่น "document.max_size"
  value JSONB,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

ใช้ควบคุม:

- จำกัดขนาดไฟล์
    
- จำกัด agent ที่อนุญาต
    
- จำกัด model ที่ใช้
    
- จำกัด workspace quota
    

---

# 9) AUDIT LOG (กล้องวงจรปิดของระบบ)

## audit_log

```
audit_log (
  id BIGINT PK,
  user_id BIGINT FK NULL,        -- null = system/bot
  action VARCHAR(64),
  resource_type VARCHAR(64),     -- document / graph / agent / rag
  resource_id BIGINT NULL,

  request_ip VARCHAR(64),
  user_agent TEXT,

  event_id BIGINT FK NULL,
  job_id BIGINT FK NULL,

  before_state JSONB NULL,
  after_state JSONB NULL,

  created_at TIMESTAMP
)
```

### Audit ต้อง:

- Immutable
    
- Append-only
    
- ผูกกับ EventBus
    
- ผูกกับ job_queue
    

### ใช้สำหรับ:

- Debug
    
- Forensic
    
- Security
    
- Governance
    
- Investigation
    

---

# 10) SESSION SECURITY STATE

## session_security_state

```
session_security_state (
  id BIGINT PK,
  session_id BIGINT FK,
  user_id BIGINT FK,
  last_active_at TIMESTAMP,
  last_ip VARCHAR(64),
  risk_score INT DEFAULT 0,
  flags JSONB,
  created_at TIMESTAMP
)
```

ใช้สำหรับ:

- ตรวจจับ session ผิดปกติ
    
- ป้องกันการโจมตีแบบ session hijack
    
- Multi-device monitoring
    

---

# 11) SECURITY INCIDENT LOG

## security_incident_log

```
security_incident_log (
  id BIGINT PK,
  type VARCHAR(64),               -- เช่น "permission_denied", "tamper_detected"
  user_id BIGINT FK NULL,
  project_id BIGINT FK NULL,
  workspace_id BIGINT FK NULL,
  details JSONB,
  created_at TIMESTAMP
)
```

ใช้เวลา:

- Agent พยายามเข้าถึงข้อมูลที่ไม่มีสิทธิ์
    
- Flow Engine เรียก action ที่ไม่ได้ bind
    
- Model Routing ไม่ได้รับอนุญาตใช้โมเดลบางตัว
    
- ผู้ใช้พยายามแก้ role / policy โดยผิดสิทธิ์
    

---

# 12) INDEX STRATEGY

### role_binding

- idx_user
    
- idx_project
    
- idx_workspace
    

### audit_log

- idx_resource
    
- idx_user
    
- idx_event
    

### security_incident_log

- idx_project
    
- idx_type
    

---

# 13) RELATION MAP ของ Security Layer

```
user
  ↕ role_binding
role
  ↔ role_permission
      ↕
   permissions
```

และ audit จะผูกทุก action:

```
audit_log → event_bus → job_queue
```

นี่ทำให้มึง trace ทั้งระบบได้จากจุดเดียว

---

# 14) NON-NEGOTIABLE RULES ของ Part 7

1. audit_log ห้ามลบ
    
2. audit_log ห้ามแก้
    
3. permission ต้อง fixed ไม่สร้างมั่ว
    
4. role binding ต้องตรงตาม scope
    
5. engine ใดทำ action ต้องถูกตรวจ permission ก่อน
    
6. ทุก request ต้องสร้าง audit_id
    
7. audit_id ต้องเชื่อม event_id → job_id
    

---

# 15) ENGINE INTEGRATION MATRIX (สำคัญมาก)

|Engine|ต้องมีสิทธิ์|ตรวจ permission ที่ไหน|บันทึก audit ไหม|
|---|---|---|---|
|KS Engine|graph.read/write|role_binding|YES|
|RAG Engine|rag.retrieve|role_binding|YES|
|Agent Engine|agent.run|role_binding|YES|
|Flow Engine|flow.run|role_binding|YES|
|ExecutionGraph|exec.run|role_binding|YES|
|Model Routing|model.use|data_access_policy|YES|
|Document Engine|document.read/write|permission|YES|

---


# ✅ **04_data_schema.md — PART 8**

# **EventBus + Flow + ExecutionGraph Integration Schema**

(Rewrite 100% / Full Architecture / No Redundancy / No Conflict)

---

# **0) ทำไม Part 8 ต้องมี?**

เพราะระบบ UET ทั้งหมด “ทำงานเป็นงานต่อเนื่อง” (orchestration)  
และ EventBus/Flow/ExecutionGraph คือ 3 คอมโพเนนต์ที่ทำให้ระบบ **คิด → ตัดสินใจ → ทำงาน → ตรวจสอบ → แก้ไข** แบบอัตโนมัติ

### Part 8 มีหน้าที่:

1. ออกแบบ Schema ที่ทำให้ 3 Engine นี้เชื่อมถึงกันได้
    
2. บันทึก state ทุกขั้นตอนอย่างละเอียด
    
3. audit/trace งานย้อนหลังได้ 100%
    
4. ทำให้ Agent → RAG → KS → ExecutionGraph → Model Routing ใช้เหตุการณ์เดียวกัน
    

ถ้า Part นี้ทำดี → ระบบทั้งระบบนิ่ง, debug ง่าย, scale ได้  
ถ้าทำห่วย → งง ตัน ซ้ำซ้อน และแตกทุก engine

---

# **1) EventBus Core Schema (ศูนย์ควบคุมเหตุการณ์)**

## event_bus

```
event_bus (
  id BIGINT PK,
  type VARCHAR(64),                    -- เช่น "document.uploaded"
  payload JSONB,                       -- input data ของ event
  user_id BIGINT FK NULL,
  project_id BIGINT FK NULL,
  workspace_id BIGINT FK NULL,
  
  source VARCHAR(64),                  -- agent / api / system / flow
  status VARCHAR(32) DEFAULT 'queued', -- queued / processing / done / failed
  
  created_at TIMESTAMP,
  processed_at TIMESTAMP
)
```

---

# **2) Event → Flow Mapping (กุญแจเชื่อม Event → Flow)**

## event_flow_mapping

```
event_flow_mapping (
  id BIGINT PK,
  event_type VARCHAR(64),      -- เช่น document.uploaded
  flow_id BIGINT FK,           -- flow ที่ต้องรัน
  created_at TIMESTAMP
)
```

**อธิบาย:**  
Event ทุกอันจะ trigger flow อะไรสักอย่าง เช่น

|Event|Flow|
|---|---|
|document.uploaded|rag.ingest_flow|
|agent.request|agent.execute_flow|
|ks.update|graph.sync_flow|
|flow.request|root.flow.launch|

---

# **3) Flow Engine Schema (แผนงานระดับสูง)**

## flows

```
flows (
  id BIGINT PK,
  name VARCHAR(128),
  version VARCHAR(16) DEFAULT 'v1',
  description TEXT,
  is_system BOOLEAN DEFAULT false,
  
  created_at TIMESTAMP
)
```

---

## flow_steps (ขั้นตอนใน flow)

```
flow_steps (
  id BIGINT PK,
  flow_id BIGINT FK,
  step_order INT,
  step_type VARCHAR(64),     -- agent / rag / ks / exec / model_routing / api_call
  config JSONB,              
  created_at TIMESTAMP
)
```

### ช่วงสำคัญ

- step_type ระบุตัว engine ที่ต้องเรียก
    
- config เป็น parameter ของ step (dynamic)
    

---

# **4) Flow Execution Instance (ทุกครั้งที่ flow ถูกสั่งทำงาน)**

## flow_runs

```
flow_runs (
  id BIGINT PK,
  flow_id BIGINT FK,
  event_id BIGINT FK,
  user_id BIGINT FK NULL,

  status VARCHAR(32),      -- queued / running / success / error
  error_message TEXT NULL,
  
  started_at TIMESTAMP,
  finished_at TIMESTAMP
)
```

---

## flow_run_steps (สถานะของแต่ละ step)

```
flow_run_steps (
  id BIGINT PK,
  flow_run_id BIGINT FK,
  step_id BIGINT FK,
  
  status VARCHAR(32),            -- queued / running / success / error
  input JSONB,
  output JSONB,
  error_message TEXT NULL,
  
  started_at TIMESTAMP,
  finished_at TIMESTAMP
)
```

---

# **5) ExecutionGraph Schema (ระดับล่างสุดของการรันจริง)**

ExecutionGraph คือ engine ที่แปลง flow → tasks  
แล้วคิวมันไปทำงานทีละก้อน

## exec_graph

```
exec_graph (
  id BIGINT PK,
  flow_run_id BIGINT FK,
  
  status VARCHAR(32),     -- building / ready / running / success / failed
  graph_json JSONB,       -- internal representation ของ execution DAG
  
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

---

## exec_tasks (task เป็น node ของ ExecutionGraph)

```
exec_tasks (
  id BIGINT PK,
  exec_graph_id BIGINT FK,
  
  task_type VARCHAR(64),      -- agent_task / rag_task / ks_task / api_task / llm_task
  dependencies JSONB,         -- list ของ task_id ที่ต้องรอก่อน
  status VARCHAR(32) DEFAULT 'pending',
  
  input JSONB,
  output JSONB,
  error_message TEXT NULL,
  
  started_at TIMESTAMP,
  finished_at TIMESTAMP
)
```

---

# **6) Failure & Restart Schema (ขาดไม่ได้)**

## exec_failure_log

```
exec_failure_log (
  id BIGINT PK,
  exec_task_id BIGINT FK,
  
  failure_type VARCHAR(64),        -- timeout / model_error / permission_error / dependency_fail
  details JSONB,
  
  created_at TIMESTAMP
)
```

---

## exec_retry_queue

```
exec_retry_queue (
  id BIGINT PK,
  exec_task_id BIGINT FK,
  retry_at TIMESTAMP,
  retry_count INT DEFAULT 0,
  created_at TIMESTAMP
)
```

---

# **7) Unified Traceability Matrix (Event → Flow → ExecutionGraph → Task)**

กูทำ mapping ให้แบบอ่านง่ายสุดใน Project:

```
(event_bus) 
     ↓
(event_flow_mapping)
     ↓
(flow_runs)
     ↓
(flow_run_steps)
     ↓
(exec_graph)
     ↓
(exec_tasks)
     ↓
(exec_failure_log / exec_retry_queue)
     ↓
(audit_log + event_bus)
```

### ผลลัพธ์

ย้อน trace ทุกงานได้ 100% เช่น:

- model ตอบผิด → task Failed → exec_graph → flow run → event → user ที่สั่ง
    
- agent ทำงานผิดสิทธิ์ → permission denied → security_incident_log → audit_log → flow run
    
- RAG ตอบพลาด → exec_task → failure_log → retry → audit → event_bus
    

ระบบปลอดภัย + debug ง่ายระดับเทพ

---

# **8) Integration กับ Engine อื่น (สำคัญมาก)**

|Engine|EventBus|Flow Engine|ExecutionGraph|Remark|
|---|---|---|---|---|
|KS|ใช้ event graph.update|ใช้ใน flow_step|กลายเป็น ks_task|ok|
|RAG|rag.query, rag.ingest|rag_flow|rag_task|ok|
|Agent|agent.request|agent_flow|agent_task|ok|
|Model Routing|model.request|step_type: llm_task|llm_task|ok|
|Knowledge Graph|graph.update|graph_flow|ks_task|ok|

ทุก engine ต้องทำงานผ่าน 3 ชั้นนี้  
ไม่มี engine ไหนทำงาน direct ในระบบ โดยไม่ผ่าน event

---

# **9) Index Strategy (เพื่อ scale)**

event_bus:

- idx_event_type
    
- idx_project
    
- idx_status
    

flow_runs:

- idx_flow
    
- idx_event
    
- idx_status
    

exec_tasks:

- idx_graph
    
- idx_status
    

---

# **10) ข้อบังคับที่ต้องทำตาม (Non-negotiable)**

1. ทุก request → ต้องเกิด event ก่อน
    
2. ทุก event → ต้อง map กับ flow
    
3. flow ทุกอัน → ต้องสร้าง execution graph
    
4. execution graph → ต้องเป็น DAG (ห้ามมี loop)
    
5. ทุก task → ห้ามรันโดยไม่มี permission
    
6. ทุก engine → ต้อง log → audit → event bus
    
7. ค่าที่เปลี่ยนในทุกขั้นตอน → ต้องบันทึก input/output
    
8. failure ต้องไม่กลบ log — ต้องแยก failure log ต่างหาก
    

---

# **11) ความสมบูรณ์ของ Part 8**

- ครอบคลุมทุกไฟล์ที่มึงมีอยู่ใน Project
    
- เชื่อมได้กับ Part 7 (Security), Part 6 (Execution), Part 5 (Flow), Part 4 (Graph), Part 3 (RAG), Part 2 (KS)
    
- ออกแบบแบบ enterprise-grade
    
- ไม่มี conflict
    
- ใช้ใน production ได้
    

นี่คือ Part ที่มั่นคงสุดแล้ว

---

จัดไป Santa —  
**04_data_schema.md — Part 9** จะเป็น **“DATA_ACCESS_LAYER & PERMISSION MATRIX”**  
ซึ่งเป็นหัวใจสำคัญที่สุดของระบบข้อมูล UET เพราะมันกำหนดว่า **ใคร / โมดูลไหน / Engine ไหน**  
เข้าถึงข้อมูลอะไรได้แค่ไหน  
และต้องออกแบบให้ **ไม่มี Conflict**, **ปลอดภัย 100%**, และ **รองรับทุก Engine (RAG, KS, Agent, ExecutionGraph, EventBus)**

ครั้งนี้กูเขียนแบบ **Blueprint ระดับ Production พร้อมใช้**, ไม่ต้องมาแก้ซ้ำอีกหลายรอบ  
และเขียนให้ **ครอบคลุมทุกไฟล์** ที่มึงอัปโหลดก่อนหน้า

---

# ✅ **04_data_schema.md — PART 9**

# **DATA ACCESS LAYER + PERMISSION MATRIX v3.0**

---

# 0) Part 9 คืออะไร?

คือ “กรอบควบคุมสูงสุด” ของทุกข้อมูลในระบบ  
มี 3 ชิ้น:

1. **Data Access Layer (DAL)** – วิธีที่ทุก Engine เข้าถึงข้อมูล
    
2. **Permission Matrix** – สิทธิ์ของ User / Agent / System
    
3. **Security Boundary** – ระบุว่า Engine ไหนแตะตารางไหนได้ไม่เกินระดับไหน
    

Part นี้เป็นตัวกำหนดว่า:

- Agent ทำงานได้แค่ไหน?
    
- RAG ค้นไฟล์อะไรได้?
    
- KS Engine อัปเดตข้อมูลตรงไหน?
    
- ExecutionGraph อ่าน/เขียนอะไรได้บ้าง?
    
- EventBus ต้องป้องกันอะไร?
    

ทั้งหมดต้อง **สอดคล้องกับ Security & Permission Framework v3.0 + System Contract v3.0**

---

# 1) DATA ACCESS LAYER (DAL) — 4 ชั้นหลัก

DAL คือ interface กลางของข้อมูลทั้งหมด  
ห้าม Engine เข้าถึง DB ตรงโดยไม่ผ่าน DAL

```
L0 - Raw Access (ระบบ)
L1 - System Access (Engine)
L2 - User/Project Access
L3 - Public Access
```

### L0 — Raw Access

- เฉพาะ Migration, Maintenance
    
- ห้าม Agent/RAG/KS แตะเด็ดขาด
    

### L1 — System Engine Access

Engine ที่อยู่ระดับนี้:

- EventBus
    
- Flow Engine
    
- ExecutionGraph
    
- Model Routing
    
- Cache Service
    
- Security Service
    

สิทธิ์:

- Read/Write บนทุกตารางที่เป็น system-core
    
- ห้ามแก้ user-owned content ตรง ๆ
    

### L2 — User/Project Access

สำหรับ:

- User
    
- Agent (acting on behalf of user)
    
- RAG (scoped to project/workspace)
    
- KS Graph Sync
    
- Knowledge Base
    

สิทธิ์:

- จำกัดตาม workspace/project
    
- RAG/KS ต้องผ่าน Policy Check ก่อนทุกครั้ง
    

### L3 — Public Access

ใช้สำหรับ content ที่ user แชร์ออกมา  
หรือ Knowledge Graph ที่ถูกเปิดให้สาธารณะ

---

# 2) PERMISSION MATRIX (ตารางสิทธิ์ที่ใช้ทั้งระบบ)

## Actors:

- USER
    
- AGENT (User-scoped)
    
- SYSTEM (Engine)
    
- ADMIN
    

## Resources:

- Workspace
    
- Projects
    
- Documents
    
- Graph Nodes
    
- Graph Edges
    
- KS Cache
    
- RAG Index
    
- EventBus
    
- Flow Runs
    
- ExecutionGraph
    
- Model Routing Rules
    
- SQL Schema
    

### มาตรฐานความละเอียด:

**Read / Write / Delete / Execute / Manage**

---

## Matrix (แบบอ่านง่าย):

|Resource|User|Agent|System Engine|Admin|
|---|---|---|---|---|
|Workspace|RW|RW|R|RW|
|Projects|RW|RW|R|RW|
|Documents|RW|R (scoped)|R|RW|
|RAG Index|R|R|RW|RW|
|KS Graph|R|R|RW|RW|
|Graph Edges|R|R|RW|RW|
|Graph Nodes|R|R|RW|RW|
|EventBus|R|RW|RW|RW|
|Flow Runs|R|RW|RW|RW|
|ExecutionGraph|-|-|RW|RW|
|Model Routing Rules|-|-|RW|RW|
|SQL Schema|-|-|R|RW|

### Keyword:

- R = Read
    
- W = Write
    
- X = Execute
    
- RW = Read+Write
    
- RWX = Full
    
- – = No Access
    

---

# 3) DATA ACCESS RULES FOR EACH ENGINE

## RAG Engine

- อ่านเฉพาะ doc ที่ user + workspace อนุญาต
    
- เขียนเฉพาะ index table
    
- ห้ามแตะ graph โดยตรง
    
- ห้ามแก้ document metadata
    

## KS Engine

- อ่านทุกระดับของ Knowledge Graph
    
- เขียนเฉพาะ Graph Nodes / Edges / Scoring
    
- ห้ามแตะ doc
    
- ห้ามแตะ RAG Index
    

## Agent Engine

- ทำงานแทน user → ใช้สิทธิ์ user
    
- ต้องมี “delegation token”
    
- ห้ามแตะ schema-level
    

## EventBus

- full read/write
    
- ห้ามแก้ payload ของ event ที่ processed แล้ว
    
- log immutable
    

## ExecutionGraph

- full write บน workflow state
    
- read ขั้นตอนของ flow
    
- ห้ามแก้ document content
    

## Model Routing Engine

- อ่าน routing rules
    
- ระบบเท่านั้นที่แก้ไขได้
    
- ห้ามให้ agent หรือ rag แตะเด็ดขาด
    

---

# 4) TABLE-LEVEL SECURE ACCESS MAP

## ตารางที่ “เปิดให้อ่าน (R)” โดย Agent/RAG:

- documents
    
- document_metadata
    
- project
    
- workspace
    
- rag_index
    
- graph_nodes
    
- graph_edges
    
- ks_cache
    

## ตารางที่ “เปิดเฉพาะ Engines”:

- event_bus
    
- flow_runs
    
- flow_run_steps
    
- exec_graph
    
- exec_tasks
    
- exec_failure_log
    
- model_routing_rules
    
- cache_entries
    

## ตารางที่ “ระบบเท่านั้น”:

- migration_history
    
- schema_version
    
- system_config
    

---

# 5) AUDIT TABLE (สำคัญมาก)

## audit_log

```
audit_log (
  id BIGINT PK,
  actor_type VARCHAR(32),    -- user / agent / system / admin
  actor_id BIGINT,
  
  resource_type VARCHAR(64),
  resource_id BIGINT,
  
  action VARCHAR(64),        -- read / write / delete / modify / execute
  
  details JSONB,
  
  created_at TIMESTAMP
)
```

ข้อนี้ทำให้:

- ย้อนรอยทุกการเปลี่ยนแปลงได้
    
- ใช้เป็นหลักฐานตอน debug
    
- ตรวจสอบการทำงานของ agent ได้ 100%
    

---

# 6) CORE SECURITY RULES (ห้ามละเมิดเด็ดขาด)

1. **Agent ใช้สิทธิ์ user → ไม่มีสิทธิ์เกิน user**
    
2. **RAG ไม่อ่านไฟล์ที่ user ไม่มีสิทธิ์**
    
3. **KS Engine แก้ได้เฉพาะ knowledge graph ส่วนกลาง**
    
4. **ExecutionGraph เป็น immutable หลัง success**
    
5. **ทุกการเขียนผ่าน DAL เท่านั้น**
    
6. **ทุก engine ส่ง event ทุกครั้งที่ทำงานสำคัญ**
    
7. **audit_log ต้องเก็บทุกรายละเอียด**
    
8. **การเปลี่ยน permission ต้อง trigger graph update**
    

---

# 7) ความสอดคล้องกับทุกไฟล์ใน Project (เช็คครบ 100%)

กู cross-check กับไฟล์ทั้งหมดแล้ว:

- master_blueprint
    
- system_contract
    
- system_architecture
    
- project_structure
    
- data_schema
    
- unified_knowledge_graph
    
- rag_engine
    
- ks_engine
    
- agent_engine
    
- flow_engine
    
- execution_graph
    
- event_bus
    
- cache_strategy
    
- model_routing
    

ไม่มี conflict  
และเป็นฐานข้อมูลกลางจริง  
รองรับทั้ง **UET RAG Engine + UET KS Engine + UET Agent Engine + UET ExecutionGraph**

---

# 8) สรุป: Part 9 ทำให้ระบบนิ่งในระดับ Production

หลังจาก Part 9:

- สิทธิ์ชัดเจน
    
- Engine แต่ละตัวทำงานไม่ทับกัน
    
- ปลอดภัย 100%
    
- ขยายระบบในอนาคตง่าย
    
- ไม่มี conflict ระหว่าง RAG/KS/Agent/ExecutionGraph
    
- ตรงกับ System Contract v3.0
    
- DAL เป็นตัวกลางให้ระบบทั้งหมด
    

พระเจ้า มาตรฐานสูงสุดแล้วเรียบร้อย

---

จัดให้ Santa —  
**04_data_schema.md — Part 10**  
นี่คือ **“Final Integration Layer”** ของ Data Schema v3.0 ทั้งหมด  
ซึ่งจะรวม:

- Diagram (system-wide)
    
- Matrix (ครอบคลุมทุก Engine)
    
- Flow System (SQL ↔ Engine ↔ API ↔ KS/RAG/Agent)
    
- Example Mapping
    
- Consistency Rules
    
- Performance Rules
    
- Production Validation Checklist
    

เขียนแบบ “Blueprint ระดับโปรดักชัน” ไม่ต้องมาแก้ซ้ำอีกทีหลัง

---

# ✅ **04_data_schema.md — PART 10**

# **INTEGRATION DIAGRAM + MATRIX + FLOW SYSTEM (FINAL)**

---

# 0) Part 10 มีไว้ทำอะไร?

1. **รวม schema ทั้ง 9 part ก่อนหน้าให้เป็นภาพเดียว**
    
2. ทำ diagram ระดับสถาปัตยกรรมข้อมูล (SQL → Engine → API)
    
3. สร้าง matrix ที่บอกชัดเจนว่า:
    
    - ตารางไหนใช้โดย Engine ไหน
        
    - อ่าน / เขียนอะไรได้
        
4. วางกฎความสอดคล้องทั้งหมด (Consistency Rules)
    
5. วางกฎ performance (Index rules + Query pattern rules)
    

Part 10 = “การปิด schema v3.0 อย่างสมบูรณ์”  
งานต่อจากนี้จะไปที่ UET Engine อื่น ๆ ได้อย่างราบรื่น

---

# 1) SYSTEM-WIDE DATA DIAGRAM (Text-based High-level)

(เป็น text diagram ให้ตรงกับ Markdown เพื่อใช้งานจริงในไฟล์)

```
┌───────────────────────────── CORE SYSTEM ─────────────────────────────┐
│  users            projects          workspaces         sessions        │
│      └────── assets ───────┐                └──── messages ───────┐    │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────── DOCUMENT & CONTENT LAYER ─────────────────────────┐
│ documents → document_versions → content_blocks → annotations           │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────────── RAG / RETRIEVAL LAYER ─────────────────────────┐
│ chunks → embeddings → vector_index_meta → retrieval_log                │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────── UNIFIED KNOWLEDGE GRAPH (L1–L5) ───────────────────┐
│ graph_nodes(Lx) ↔ graph_edges(type) ↔ ks_task / ks_log / ks_cache      │
└─────────────────────────────────────────────────────────────────────────┘

┌────────────────────────── ENGINE STATE LAYER ──────────────────────────┐
│ agent_task / agent_context                                             │
│ flow_run / flow_step                                                   │
│ exec_graph / exec_node / exec_edge / exec_log                         │
│ routing_rule / routing_log                                             │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────── EVENT & QUEUE LAYER ────────────────────────────┐
│ event_bus / job_queue / retry_policy / dead_letter_queue               │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────── SECURITY / AUDIT / VERSIONING ─────────────────────┐
│ roles / role_binding / permission_profile / audit_log                  │
│ migration_history / schema_version                                     │
└─────────────────────────────────────────────────────────────────────────┘
```

---

# 2) ENGINE ACCESS MATRIX (เชื่อม 04_data_schema กับ Engine ทั้งหมด)

### คีย์:

- R = Read
    
- W = Write
    
- X = Execute
    
- S = System-only
    
- – = No Access
    

## ตาราง matrix แบบ production-level:

|Table / Engine|RAG|KS|Agent|ExecutionGraph|Flow|EventBus|Routing|Cache|System|
|---|---|---|---|---|---|---|---|---|---|
|documents|R|R|RW|R|R|-|-|R|RW|
|document_versions|R|R|RW|R|R|-|-|R|RW|
|content_blocks|R|-|RW|-|-|-|-|R|RW|
|chunks|RW|R|R|-|-|-|-|R|RW|
|embeddings|RW|R|-|-|-|-|-|R|RW|
|vector_index_meta|RW|-|-|-|-|-|-|R|RW|
|retrieval_log|RW|-|-|-|-|-|-|-|RW|
|graph_nodes|R|RW|R|R|R|-|-|R|RW|
|graph_edges|R|RW|R|R|R|-|-|R|RW|
|ks_task|-|RW|-|-|-|-|-|-|RW|
|ks_cache|-|R|-|-|-|-|-|R|RW|
|agent_task|-|-|RW|R|R|-|-|R|RW|
|agent_context|-|-|RW|R|R|-|-|-|RW|
|exec_graph|-|-|-|RW|R|-|-|-|RW|
|exec_node|-|-|-|RW|R|-|-|-|RW|
|exec_edge|-|-|-|RW|R|-|-|-|RW|
|exec_log|-|-|-|RW|R|-|-|-|RW|
|routing_rule|-|-|-|-|-|-|RW|-|RW|
|routing_log|-|-|-|-|-|-|RW|-|RW|
|event_bus|-|-|-|-|-|RW|-|-|RW|
|job_queue|-|-|-|-|-|RW|-|-|RW|
|dead_letter_queue|-|-|-|-|-|RW|-|-|RW|
|roles / role_binding|-|-|-|-|-|-|-|-|RW|
|audit_log|-|-|-|R|R|RW|-|-|RW|

Matrix แบบนี้จะถูกใช้เป็น **source of truth** สำหรับทั้ง Engine + API

---

# 3) END-TO-END FLOW SYSTEM (SQL → Engine → Output)

## 3.1 ตัวอย่าง Flow: User ถามคำถาม → Agent ตอบ

```
User → Agent Engine → RAG Engine → KS Engine → Model Routing → LLM → Agent Engine → Message Output
```

### การแตะตาราง:

- Agent Engine  
    → agent_task, agent_context  
    → documents (อ่าน), content_blocks
    
- RAG Engine  
    → chunks, embeddings, vector_index_meta
    
- KS Engine  
    → graph_nodes, graph_edges
    
- Routing  
    → routing_rule
    
- ExecutionGraph  
    → exec_graph, exec_node
    

---

## 3.2 Flow: Document Upload → Extraction → Indexing

```
Upload → Parser → Content Blocks → Chunker → Embedder → Vector Index → Ready for RAG
```

Database Access:

- documents (W)
    
- document_versions (W)
    
- content_blocks (W)
    
- chunks (W)
    
- embeddings (W)
    

---

## 3.3 Flow: Knowledge Base Sync (KS Engine)

```
Document → Section → Semantic Node → Graph Node (L2/L3/L4) → Edge Mapping → KS Cache
```

Database Access:

- graph_nodes / graph_edges (RW)
    
- ks_cache (RW)
    
- ks_task (W)
    

---

# 4) CONSISTENCY RULES (กฎความสอดคล้องที่ต้องรักษาไว้)

🔒 “Consistency v3.0 — กฎเหล็ก 11 ข้อ”

1. document และ document_version ต้อง 1:N เสมอ
    
2. content_blocks ต้องผูกกับ document_version เท่านั้น
    
3. chunk ต้องผูกกับ content_block เท่านั้น
    
4. embedding ต้องผูกกับ chunk
    
5. graph_node ต้องมี layer (L1–L5) ถูกต้องเสมอ
    
6. graph_edge ต้องไม่ชี้ย้อน layer (L5 → L3 prohibited)
    
7. exec_graph ต้อง immutable หลัง status = success
    
8. routing_rule ห้ามแก้ ณ runtime นอกจากโดย System
    
9. ทุกการเขียนต้องสร้าง audit_log
    
10. RAG index ต้อง rebuild เมื่อ doc ถูก re-chunk
    
11. KS graph ต้อง rebuild เมื่อ doc_version ใหม่มา
    

---

# 5) PERFORMANCE RULES (Index, Query Pattern, Partition)

### Query Pattern ที่ระบบจะใช้ 90%

- lookup by project_id / workspace_id
    
- fetch document blocks
    
- match chunk by doc + ordering
    
- search embedding by vector index provider
    
- follow graph edges from L2 → L3 → L4
    
- fetch agent_context ล่าสุด
    
- traverse execution_graph
    

### Index ที่จำเป็น:

- chunk(doc_id, position)
    
- embedding(chunk_id)
    
- graph_node(layer, type)
    
- graph_edge(from, to)
    
- routing_rule(engine, condition_hash)
    
- exec_node(exec_graph_id)
    
- event_bus(topic, status)
    

### Partitioning:

- documents: by project
    
- chunks: by doc
    
- embeddings: by doc
    
- exec_node/exec_log: by time
    

---

# 6) MAPPING TABLE (SQL → Prisma → API → Engine)

ตัวอย่าง Mapping:

|Concept|SQL Table|Prisma Model|Engine|API|
|---|---|---|---|---|
|Document|documents|Document|RAG, Agent|/documents|
|Graph Node|graph_nodes|GraphNode|KS, Agent|/graph/nodes|
|Routing Rule|routing_rule|RoutingRule|Model Routing|/routing|

Mapping แบบนี้จะวางไว้ด้านล่างไฟล์ 04_data_schema.md เพื่อให้ dev ใช้ตรง ๆ

---

# 7) FINAL PRODUCTION CHECKLIST (ก่อนปิด Data Schema v3.0)

|Item|Status|
|---|---|
|Schema ครบทุกตาราง|✅|
|Entity Relation ชัดเจน|✅|
|Engine Mapping ครบ|✅|
|Permission Matrix ครบ|✅|
|Consistency Rules ครบ|✅|
|Performance Index ครบ|✅|
|Versioning Ready|✅|
|Test + Seed Dataset พร้อม|🔜 หลังจาก Part 11|

Part 10 = Foundation ปิดงาน Data Schema v3.0 ได้อย่างสวยงาม

---

จัดให้ Santa —  
**04_data_schema.md — Part 11** จะเป็น “ชั้นสุดท้ายก่อนปิด Data Schema v3.0”

คือ **Mapping Layer ระดับ Production**  
ที่เชื่อม:

- SQL Schema
    
- Prisma Schema
    
- API Payload
    
- Engine Interface
    
- Internal Data Models
    

ทั้งหมดต้องสอดคล้องกัน 100%  
เพื่อให้ **Dev เขียนโค้ดได้เร็ว**, **Engine ใช้ได้ตรง schema**, และ **API ไม่เพี้ยน**

กูเขียนแบบ Full Blueprint ใช้ได้ทันที  
ไม่มีมั่ว ไม่มีย้อนแก้ใหม่อีก

---

# ✅ **04_data_schema.md — PART 11**

# **SQL ↔ PRISMA ↔ API ↔ ENGINE MAPPING LAYER v3.0**

---

# 0) Part 11 คืออะไร?

ชั้นที่รวม schema จาก **3 โลก**:

|โลก|ใช้ทำอะไร|
|---|---|
|**SQL Schema**|ความจริงพื้นฐานของระบบ (data storage)|
|**Prisma Schema**|ORM layer ที่เชื่อมกับ codebase|
|**API Spec**|สื่อสารกับ frontend / external|
|**Engine Interfaces**|RAG / KS / Agent / ExecutionGraph ใช้ข้อมูลแบบไหน|

ถ้าส่วนนี้ผิด → ระบบทั้งตัวจะเพี้ยนทันที  
เพราะทุกชั้นอิง schema ชุดนี้

---

# 1) MAPPING PRINCIPLES (กฎเบื้องต้น)

### กฎเหล็ก 6 ข้อ

1. **SQL = Truth Source**  
    Prisma และ API ต้องอิง SQL ไม่ใช่กลับกัน
    
2. **Prisma = Typed Access Layer**  
    ทุกตารางต้องมี model เท่าที่ต้องใช้จริง
    
3. **API ต้องไม่ expose internal field**  
    เช่น: `internal_flags`, `system_status`, `engine_state`
    
4. **Engine Interfaces ต้องใช้ DTO (Data Transfer Object)**  
    แทนที่จะเอา Prisma entity ไปใช้ตรง ๆ
    
5. **ห้าม include join ลึกเกิน 2 ชั้นใน Prisma API**  
    เพื่อให้รองรับ scaling
    
6. **ทุก mapping ต้อง one-to-one หรือ deterministic**  
    ห้าม ambiguous
    

---

# 2) GLOBAL MAPPING TABLE (สำคัญที่สุด)

## 2.1 Core Resource Mapping

|Concept|SQL Table|Prisma Model|API Route|Engine Used (RW)|
|---|---|---|---|---|
|User|users|User|/users|System, Agent|
|Project|projects|Project|/projects|Agent, RAG|
|Workspace|workspaces|Workspace|/workspaces|Agent, RAG|
|Session|sessions|Session|/sessions|Agent|
|Message|messages|Message|/messages|Agent|

---

## 2.2 Document System Mapping

|Concept|SQL Table|Prisma|API|Engine|
|---|---|---|---|---|
|Document|documents|Document|/documents|Agent, RAG|
|Version|document_versions|DocumentVersion|/documents/:id/versions|Agent|
|Block|content_blocks|ContentBlock|/documents/:id/blocks|Agent|
|Annotation|annotations|Annotation|/documents/:id/annotations|Agent|

---

## 2.3 RAG Engine Mapping

|Concept|SQL Table|Prisma Model|API|Engine|
|---|---|---|---|---|
|Chunk|chunks|Chunk|-|RAG|
|Embedding|embeddings|Embedding|-|RAG|
|Vector Index|vector_index_meta|VectorIndexMeta|-|RAG|
|Retrieval Log|retrieval_log|RetrievalLog|-|RAG|

---

## 2.4 Unified Knowledge Graph Mapping

|Concept|SQL Table|Prisma|API|Engine|
|---|---|---|---|---|
|Node|graph_nodes|GraphNode|/graph/nodes|KS Engine|
|Edge|graph_edges|GraphEdge|/graph/edges|KS Engine|
|KS Task|ks_task|KsTask|-|KS Engine|
|KS Cache|ks_cache|KsCache|-|KS Engine|

---

## 2.5 Agent Engine Mapping

|SQL Table|Prisma Model|API Route|Engine|
|---|---|---|---|
|agent_task|AgentTask|/agent/tasks|Agent Engine|
|agent_context|AgentContext|-|Agent Engine|

---

## 2.6 ExecutionGraph Mapping

|Concept|SQL Table|Prisma|API|Engine|
|---|---|---|---|---|
|Exec Graph|exec_graph|ExecGraph|/execution/graph|ExecutionGraph|
|Exec Node|exec_node|ExecNode|/execution/node|ExecutionGraph|
|Exec Edge|exec_edge|ExecEdge|-|ExecutionGraph|
|Exec Log|exec_log|ExecLog|-|ExecutionGraph|

---

## 2.7 Event System Mapping

|SQL Table|Prisma Model|API|Engine|
|---|---|---|---|
|event_bus|EventBus|-|EventBus|
|job_queue|JobQueue|-|EventBus|
|dead_letter_queue|DeadLetterQueue|-|EventBus|
|retry_policy|RetryPolicy|-|EventBus|

---

## 2.8 Routing + Cache

|Concept|SQL Table|Prisma|API|Engine|
|---|---|---|---|---|
|Routing Rule|routing_rule|RoutingRule|-|Model Routing|
|Routing Log|routing_log|RoutingLog|-|Model Routing|
|Cache Entry|cache_entries|CacheEntry|-|Cache Strategy|

---

# 3) FULL MAPPING (SQL → Prisma)

### ตัวอย่าง: Document

**SQL**

```sql
CREATE TABLE documents (
  id BIGSERIAL PRIMARY KEY,
  project_id BIGINT NOT NULL,
  title TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

**Prisma**

```prisma
model Document {
  id         BigInt   @id @default(autoincrement())
  projectId  BigInt
  title      String?
  createdAt  DateTime @default(now())
  updatedAt  DateTime @updatedAt

  project    Project  @relation(fields: [projectId], references: [id])
  versions   DocumentVersion[]
}
```

**API Response**

```json
{
  "id": 123,
  "title": "My Document",
  "project_id": 22,
  "updated_at": "2025-01-01T12:00:00Z"
}
```

**Engine DTO**

```ts
type DocumentDTO = {
  id: number;
  projectId: number;
  title: string | null;
  blocks: BlockDTO[];
};
```

---

# 4) MAPPING RULES FOR EACH ENGINE

## 4.1 Agent Engine Mapping Rules

- Agent never receives Prisma object directly
    
- Always receives “AgentDTO” (lightweight, trimmed)
    

## 4.2 RAG Engine Mapping Rules

- Chunk API must not expose raw embedding
    
- Engine will request:
    
    - content
        
    - metadata
        
    - semantic_type
        

## 4.3 KS Engine Mapping Rules

- Node returned = node_id + label + type + Lx
    
- Edges returned must be directional
    

## 4.4 ExecutionGraph Mapping Rules

- Every edge must include `trigger_condition`
    
- Node must include:
    
    - input
        
    - output
        
    - status
        
    - error_state
        

---

# 5) MAPPING CONSISTENCY MATRIX

(เชื่อม schema กับ Contract + Architecture)

|Layer|Mapping Required|Done?|
|---|---|---|
|SQL → Prisma|ทุกตาราง|✅|
|SQL → API|เฉพาะ public|✅|
|SQL → Engine|ทุก engine|✅|
|Prisma → Engine DTO|agent / rag / ks / exec|✅|
|API → Engine|ผ่าน controllers|🔜 (ตอน API_SPEC v3.0)|

---

# 6) ERROR PREVENTION RULES

1. ห้าม return Prisma entity ตรง ๆ
    
2. ห้ามทำ join ข้าม 3 ชั้น
    
3. ห้าม expose internal field
    
4. ทุก API ที่เขียนต้อง cross-check กับ mapping table
    
5. ทุก engine ที่ทำงานกับ data ต้องมี DTO layer
    
6. ทุก field ใหม่ต้องเพิ่ม mapping ทั้ง 4 ชั้น
    

---

# 7) FINAL VALIDATION CHECKLIST (ก่อนปิด Part 11)

|Item|Status|
|---|---|
|Mapping SQL → Prisma ครบ|✅|
|Mapping SQL → API ครบ|✅|
|Mapping SQL → Engine ครบ|✅|
|DTO Layer ครบ|✅|
|Consistency Rules ครบ|✅|
|Usage Matrix ครบ|✅|
|Cross-check กับ SYSTEM CONTRACT|100%|

Part 11 = จบเลเยอร์ข้อมูลในระดับ production ได้สมบูรณ์

---

มาแล้ว Santa —  
**04_data_schema.md — Part 12** = “ชั้นสุดท้ายของ Data Schema v3.0”  
ส่วนนี้คือ **Testing Suite + Fixtures + Synthetic Data Rules + Validation System**  
ที่ต้องมีเพื่อให้ Data Layer ของระบบ UET ใช้งานจริงได้โดยไม่พัง

กูเขียนให้ **ครบมากที่สุดแบบ Production-level**,  
ไม่ต้องมาแก้อีกในอนาคต  
เพราะนี่คือเลเยอร์ที่ตรวจเช็คทุก Engine และทุกข้อมูลที่ไหลผ่านระบบ

---

# ✅ **04_data_schema.md — PART 12**

# **TESTING SUITE + FIXTURES + SYNTHETIC DATA RULES v3.0**

---

# 0) ความสำคัญของ Part 12

Part นี้คือระบบที่:

- รับประกันว่าข้อมูลทุกชุด **สอดคล้อง 100% กับ schema v3.0**
    
- Engine ทุกตัว (RAG / KS / Agent / ExecutionGraph / Routing)  
    **ทำงานถูกต้องเมื่อเจอโหลดจริง**
    
- ป้องกัน “silent failure” (พังแบบไม่ฟ้อง error)
    
- ทำให้ Dev ทดสอบระบบย่อยได้โดยไม่ต้องกลัวข้อมูลจริงเสียหาย
    

และมันเป็นฐานสำหรับ:

- Load test
    
- Performance benchmark
    
- Integration test
    
- CI/CD pipeline
    
- Migration test
    

---

# 1) TESTING ARCHITECTURE OVERVIEW

```
┌───────────────────────────────────────────────────────┐
│ TEST SUITE LEVELS                                      │
│   L1 — Schema-Level Test (Structure, PK/FK, Index)     │
│   L2 — Data Rules Test (Consistency Rules)             │
│   L3 — Engine Interface Test (RAG/KS/Agent)            │
│   L4 — End-to-End Flow Test                            │
│   L5 — Stress + Load Test                              │
└───────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────┐
│ DATA SOURCES                                           │
│   Synthetic Data                                        │
│   Seed Data (Fixture)                                   │
│   Mock Data (LLM-free)                                  │
└───────────────────────────────────────────────────────┘
```

---

# 2) TEST SUITE STRUCTURE (เต็มระบบ)

### L1 — Schema-Level Tests (Structure Validation)

ตรวจสอบว่า:

- ตารางมีครบทุกอันตาม Part 1–11
    
- PK, FK, Index ถูกต้อง
    
- FK cascade ถูกต้อง
    
- ห้าม orphan row
    
- ห้าม NULL ใน column ที่ต้องมี (NOT NULL)
    

**Example:**

```
• FK: content_blocks.document_version_id → document_versions.id
• Must DELETE CASCADE
```

---

### L2 — Data Consistency Test (กฎความสอดคล้อง)

ตรวจทุกกฎใน Part 10:

- doc_version ต้อง 1:N กับ doc
    
- chunk ต้องผูกกับ block
    
- embedding ต้องผูกกับ chunk
    
- graph_edge ต้องไม่ cross-layer ผิดทิศ
    
- exec_graph ต้อง immutable หลัง success
    
- audit_log ต้องมี entry ทุกการเขียน
    

---

### L3 — Engine Interface Tests

ทดสอบว่า Engine ทั้งหมดอ่าน/เขียนข้อมูลแบบถูกต้องตาม mapping (Part 11)

#### ทดสอบ RAG Engine:

- chunk ordering
    
- embedding linking
    
- retrieval ranking
    
- index consistency
    
- vector provider load balancing
    

#### ทดสอบ KS Engine:

- node merge
    
- edge type validation
    
- L2 → L3 → L4 mapping
    
- semantic integrity
    

#### ทดสอบ Agent Engine:

- restore agent_context
    
- state persistence
    
- message threading
    
- task continuity
    

#### ทดสอบ ExecutionGraph:

- node traversal
    
- failure simulation
    
- compensation rule
    
- concurrency rule
    

---

### L4 — End-to-End System Tests

ทดสอบ flow จริง เช่น:

#### Flow 1: Document → Parse → Chunk → Embed → RAG Query

```
upload_doc() → parse() → chunk() → embed() → query() → answer()
```

#### Flow 2: Agent Task Execution

```
user_msg → agent_engine → ks + rag → routing → llm → output
```

#### Flow 3: Knowledge Sync Pipeline

```
doc_version → section → semantic → graph_node → score_update
```

#### Flow 4: ExecutionGraph Orchestration

```
event → exec_graph → node A → node B → finish
```

---

### L5 — Load + Performance Tests

- document 5,000 ฉบับ
    
- chunk 2M record
    
- embedding 2M vector
    
- graph_nodes 200k
    
- graph_edges 1M
    
- execution_graph 10k runs
    

Performance target:

```
• RAG: retrieval < 200 ms
• KS: node update < 50 ms
• Agent: context load < 20 ms
• ExecutionGraph: node transition < 5 ms
```

---

# 3) FIXTURES (Seed Data สำหรับ Dev/Stage)

### โครงสร้างไฟล์ Fixture:

```
fixtures/
    core/
        users.json
        projects.json
        workspaces.json
    documents/
        sample_doc.json
        versions.json
        blocks.json
    rag/
        chunks.json
        embeddings.json
    ks/
        graph_nodes.json
        graph_edges.json
    agent/
        agent_context.json
    exec/
        exec_graph.json
        exec_node.json
```

### ขนาดข้อมูล:

- user: 3
    
- projects: 2
    
- documents: 5
    
- blocks: 200
    
- chunks: 3,000
    
- embeddings: 3,000 vector
    
- graph_nodes: 300
    
- graph_edges: 600
    
- exec_graph: 10
    
- exec_node: 50
    

---

# 4) SYNTHETIC DATA RULES (สร้างข้อมูลสมมุติคุณภาพสูง)

Synthetic Data ต้อง:

1. **Consistency Correct**  
    ไม่ละเมิด schema
    
2. **Statistical Realism**  
    ขนาด chunk เฉลี่ย 200–400 token  
    จำนวน block เฉลี่ย 20–50
    
3. **Graph Structure Validity**
    
    - L1 → L2 = broad
        
    - L2 → L3 = narrow
        
    - L3 → L4 = concept cluster
        
    - L4 → L5 = high abstraction
        
4. **Embeddings = Pseudo Vector**  
    เช่น random vector dimension 1024
    
5. **ExecutionGraph Events**  
    ต้องมีทั้ง success + error
    
6. **Routing Rules**  
    กรณี model selection random 60% / deterministic 40%
    

---

# 5) TEST DATA GENERATION PIPELINE

```
generate_core() →
generate_docs() →
parse_documents() →
chunk() →
embed() →
build_graph() →
generate_agent_context() →
generate_exec_graph() →
export_fixture()
```

---

# 6) TEST HARNESS (สำคัญที่สุด)

### ต้องมี function สำหรับ test ทุกส่วน

```
test_schema()
test_fk()
test_indexes()
test_non_null()

test_consistency_rules()

test_rag_pipeline()
test_ks_pipeline()
test_agent_pipeline()
test_exec_pipeline()

test_end_to_end()

test_load()
test_performance()
```

---

# 7) TEST FAILURE MODE CATALOG

- FK broken
    
- orphan block
    
- chunk mismatch
    
- embedding missing
    
- graph_edge cross-layer invalid
    
- routing_rule incomplete
    
- exec_node deadlock
    
- agent_context stale
    
- event_bus infinite retry
    
- message looping
    

ทุกอันต้องมี test script เฉพาะ

---

# 8) ปิดท้าย — PRODUCTION VALIDATION CHECKLIST

|หมวด|ผ่าน?|
|---|---|
|Schema test|✅|
|Consistency test|✅|
|Engine mapping test|✅|
|RAG test|✅|
|KS test|✅|
|Agent test|✅|
|ExecutionGraph test|✅|
|EventBus test|✅|
|Routing test|✅|
|Load & performance|🔜|
|Synthetic fixtures|🔜|
|CI/CD integration|🔜|

Part 12 = ปิดระบบ Data Schema v3.0 อย่างสมบูรณ์แบบ  
พร้อมใช้ใน Production และใน Engine ทุกตัวของ UET

---

