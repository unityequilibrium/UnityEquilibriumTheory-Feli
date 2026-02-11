
โอเค Santa —  
ตอนนี้ฉันจะทำ **DATA_SCHEMA.md v2.0 (ยกเครื่องใหม่ทั้งฉบับ)**  
โดยรวบรวมข้อมูลจากทุกไฟล์ที่นายมี:

- DATA_SCHEMA (เก่า)
- DATA_LIFECYCLE
- KNOWLEDGE_SYNC
- AGENT_FLOW
- MODEL_ROUTING
- CACHE_STRATEGY
- ERROR_HANDLING
- SYSTEM_CONTRACT
- EVENT_BUS
- COMPONENT_MAP
- API_SPEC
- PROJECT_STRUCTURE

และออกแบบให้เป็น **มาตรฐานเดียวของทั้งระบบ**  
อ่านง่าย กระชับ แต่ครบทุกโครงสร้างข้อมูลที่แพลตฟอร์มต้องใช้จริง

**นี่คือ DATA_SCHEMA v2.0 — ฉบับสมบูรณ์แบบที่สุดที่ใช้ได้ทั้งกับ API, DB, Vector DB, และ Agent**

---

# 📘 **DATA_SCHEMA.md (v2.0)**

**UET Platform — Unified Data Schema**

---

# **0. เป้าหมายของ Schema v2.0**

- สร้าง _มาตรฐานเดียว_ สำหรับข้อมูลทุกประเภท
    
- ทำให้ระบบอ่าน–เขียน–ค้นหา–ซิงค์ได้อย่างถูกต้องสม่ำเสมอ
    
- รองรับ versioning, conflict, agent logs, routing logs
    
- ทำให้ข้อมูลทุกชั้น trace ได้ 100%
    
- ทำให้ AI agent ทำงานบนข้อมูลที่ deterministic
    

---

# **1. ภาพรวมโครงสร้างข้อมูล (Data Layer Overview)**

```
USER
PROJECT
FILE
FILE_VERSION
CHUNK
EMBEDDING
KB_REGISTRY
AGENT_RUN
ROUTING_LOG
EVENT_LOG
CACHE_ENTRY
METRICS
```

ข้อมูลทั้งหมดต้องผ่าน:

- Version Control
    
- Permission Matrix
    
- Event Bus
    
- Contract Enforcement
    

---

# **2. USER_SCHEMA**

```
User {
    id: string
    email: string
    name: string
    role: "guest" | "user" | "power" | "admin"
    created_at: datetime
    last_login: datetime
    preferences: {
        default_model: string
        theme: string
    }
}
```

**Role ส่งผลโดยตรงต่อ:**

- model tier
    
- KB access
    
- file operations
    
- agent capability
    

---

# **3. PROJECT_SCHEMA**

```
Project {
    id: string
    owner_id: string
    name: string
    description?: string
    created_at: datetime
    updated_at: datetime
    members: UserPermission[]
}
```

```
UserPermission {
    user_id: string
    role: "viewer" | "editor" | "manager"
}
```

---

# **4. FILE_SCHEMA**

```
File {
    id: string
    project_id: string
    name: string
    type: "pdf" | "docx" | "txt" | "md"
    status: "active" | "deleted"
    current_version_id: string
    created_at: datetime
    updated_at: datetime
}
```

---

# **5. FILE_VERSION_SCHEMA**

(สำคัญมาก เพราะเป็นตัวควบคุม KB Sync)

```
FileVersion {
    id: string
    file_id: string
    version: number
    author_id: string
    size: number
    checksum: string
    content: string  // raw or normalized
    metadata: {
        extracted_text: boolean
        chunk_count: number
        embedding_version: string
    }
    created_at: datetime
}
```

---

# **6. CHUNK_SCHEMA**

(ใช้กับ RAG และ indexing)

```
Chunk {
    id: string
    file_version_id: string
    project_id: string
    order: number
    text: string
    token_count: number
    chunk_hash: string
    metadata: {
        file_name: string
        author?: string
        section?: string
    }
}
```

---

# **7. EMBEDDING_SCHEMA**

```
Embedding {
    id: string
    chunk_id: string
    vector: float[]
    model: string    // e.g. "text-embedding-3-large"
    created_at: datetime
}
```

Constraints:

- ถ้า chunk เปลี่ยน → embedding ต้อง regenerate
    
- embedding ต้องถูกผูกกับ version เสมอ
    

---

# **8. KB_REGISTRY_SCHEMA**

(หัวใจใหญ่ที่สุดของ Knowledge Base)

```
KBRegistry {
    project_id: string
    file_id: string
    version_id: string
    chunk_ids: string[]
    embedding_ids: string[]
    updated_at: datetime
}
```

**Guarantee:**  
1 File Version = 1 KB Entry  
**ไม่มี cross-project allowed**

---

# **9. AGENT_RUN_SCHEMA**

(ใช้วิเคราะห์ agent reasoning)

```
AgentRun {
    id: string
    user_id: string
    project_id: string
    input_type: "chat" | "studio" | "system"
    model_selected: string
    routing_tier: number
    prompt: string
    output: string
    tokens_in: number
    tokens_out: number
    status: "success" | "fail"
    error_id?: string
    created_at: datetime
}
```

---

# **10. ROUTING_LOG_SCHEMA**

(บันทึกการเลือกโมเดลทุกครั้งเพื่อความโปร่งใส)

```
RoutingLog {
    id: string
    project_id: string
    user_id: string
    task_type: "chat" | "edit" | "generate" | "rag"
    selected_model: string
    tier: number
    reasoning?: string
    override: boolean
    created_at: datetime
}
```

---

# **11. EVENT_LOG_SCHEMA**

(อ้างอิง EVENT_BUS)

```
EventLog {
    id: string
    event_type: string
    actor_type: "user" | "agent" | "system"
    actor_id?: string
    project_id?: string
    payload: JSON
    created_at: datetime
}
```

Events เช่น:

- FILE_UPDATED
    
- KB_VERSION_UPDATED
    
- CACHE_INVALIDATED
    
- MODEL_ROUTED
    
- AGENT_STEP
    
- CONTRACT_VIOLATION
    

---

# **12. CACHE_ENTRY_SCHEMA**

```
CacheEntry {
    key: string
    type: "prompt" | "rag" | "file" | "api"
    value: JSON | string
    ttl: number
    created_at: datetime
}
```

Rules:

- TTL ต่อชนิด
    
- Clear เมื่อเกิด event ที่เกี่ยวข้อง
    
- Prevent stale data
    

---

# **13. METRICS_SCHEMA**

```
Metrics {
    id: string
    project_id: string
    user_id?: string
    type: 
        "latency" |
        "rag_precision" |
        "routing_accuracy" |
        "cache_hit" |
        "agent_success"
    value: number
    context?: JSON
    created_at: datetime
}
```

---

# **14. ERROR_SCHEMA**

สอดคล้องกับ ERROR_HANDLING v2.0

```
ErrorLog {
    id: string
    type: 
        "model_timeout" |
        "model_overload" |
        "rag_fail" |
        "routing_fail" |
        "permission_denied" |
        "contract_violation" |
        "system"
    message: string
    detail?: JSON
    project_id?: string
    agent_run_id?: string
    created_at: datetime
}
```

---

# **15. RELATION MAP (ความสัมพันธ์ข้อมูล)**

```
User ─────────────┐
                   ▼
               Project ──────────────┐
                                     ▼
                                File ──────────────┐
                                                   ▼
                                            FileVersion
                                                   ▼
                                               Chunk ───► Embedding
                                                   ▼
                                              KBRegistry

AgentRun ───► RoutingLog  
AgentRun ───► EventLog  
EventLog ───► CacheInvalidate  

Metrics ───► Project
```

---

# 🔥 **สรุปแบบเข้าใจง่ายที่สุด**

นี่คือแกน DATA_SCHEMA v2.0:

- **User**
- **Project**
- **File + Version**
- **Chunk**
- **Embedding**
- **KB Registry**
- **Agent Run + Logs**
- **Model Routing Logs**
- **Events**
- **Cache**
- **Metrics**
- **Errors**

ทั้งหมดนี้เชื่อมกันแบบ deterministic  
เพื่อให้ Agent, KB, API, RAG, UI ทำงานได้ไม่ล้ม

---
# 🧬 **1) ER DIAGRAM (DATABASE STRUCTURE)**

_อ่านง่ายที่สุด เห็นความสัมพันธ์ชัดแบบไม่ต้องมีภาพจริง_

```
┌───────────────┐       1        ┌────────────────┐
│     USER       │──────────────►│   PROJECT       │
└───────────────┘                └────────────────┘
         ▲                                  │
         │1..*                               │1..*
         │                                   ▼
         │                          ┌──────────────────┐
         │                          │ USER_PERMISSION  │
         │                          └──────────────────┘
         │                                   │
         │                                   ▼
         │                           (role per project)

────────────────────────────────────────────────────────────

PROJECT 1..* FILE

┌────────────────┐      1       ┌────────────────┐
│   PROJECT       │────────────►│     FILE       │
└────────────────┘              └────────────────┘
                                        │
                                        │1..*
                                        ▼
                               ┌────────────────────┐
                               │   FILE_VERSION     │
                               └────────────────────┘
                                        │1..*
                                        ▼
                         ┌────────────────────────┐
                         │         CHUNK          │
                         └────────────────────────┘
                                        │1..1
                                        ▼
                         ┌────────────────────────┐
                         │       EMBEDDING        │
                         └────────────────────────┘

────────────────────────────────────────────────────────────

PROJECT 1..1 KB_REGISTRY (per file version)

┌────────────────┐
│ FILE_VERSION    │
└────────────────┘
        │1..1
        ▼
┌──────────────────┐
│   KB_REGISTRY     │
└──────────────────┘

────────────────────────────────────────────────────────────

AGENT RUN + LOGGING

USER 1..* AGENT_RUN
PROJECT 1..* AGENT_RUN

┌──────────────┐           ┌───────────────────┐
│    USER       │──────────►│    AGENT_RUN     │
└──────────────┘           └───────────────────┘
                               │1..1
                               ▼
                      ┌────────────────────┐
                      │   ROUTING_LOG      │
                      └────────────────────┘

                     (หลาย agent_runs มีหลาย events)
                               │1..*
                               ▼
                      ┌────────────────────┐
                      │    EVENT_LOG        │
                      └────────────────────┘

────────────────────────────────────────────────────────────

CACHE + METRICS + ERRORS

┌──────────────┐
│  CACHE_ENTRY │  (global or project-scoped)
└──────────────┘

┌──────────────┐
│   METRICS     │  (per project or per user)
└──────────────┘

┌──────────────┐
│  ERROR_LOG    │  (refer to AGENT_RUN or system)
└──────────────┘
```

---

# 🎯 สรุปความสัมพันธ์แบบ “เข้าใจใน 10 วินาที”

- **User → Project (many-to-many)**
- **Project → File (1-to-many)**
- **File → Version (1-to-many)**
- **File Version → Chunk (1-to-many)**
- **Chunk → Embedding (1-to-1)**
- **File Version → KB Registry (1-to-1)**
- **User/Project → AgentRun (1-to-many)**
- **AgentRun → RoutingLog (1-to-1)**
- **AgentRun → EventLog (1-to-many)**

นี่คือฐานทั้งหมดของระบบ UET

---

# 🧩 **2) Relationship Matrix (Matrix Analysis)**

เพื่อให้เห็นความเชื่อมโยงแบบ “ตาราง”  
อ่านง่าย ไม่ต้องใช้ diagram

## **Entity Relationship Matrix**

|ENTITY A → ENTITY B|User|Project|File|FileVersion|Chunk|Embedding|KBRegistry|AgentRun|RoutingLog|EventLog|Metrics|ErrorLog|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|User|—|M:N|—|—|—|—|—|1:M|—|—|1:M|1:M|
|Project|M:N|—|1:M|—|—|—|—|1:M|—|1:M|1:M|1:M|
|File|—|M:1|—|1:M|—|—|—|—|—|—|—|—|
|FileVersion|—|—|M:1|—|1:M|—|1:1|—|—|—|—|—|
|Chunk|—|—|—|M:1|—|1:1|—|—|—|—|—|—|
|Embedding|—|—|—|—|1:1|—|—|—|—|—|—|—|
|KBRegistry|—|—|—|1:1|—|—|—|—|—|—|—|—|
|AgentRun|1:M|1:M|—|—|—|—|—|—|1:1|1:M|—|1:1|
|RoutingLog|—|—|—|—|—|—|—|1:1|—|—|—|—|
|EventLog|—|1:M|—|—|—|—|—|M:1|—|—|—|—|
|Metrics|1:M|1:M|—|—|—|—|—|—|—|—|—|—|
|ErrorLog|1:M|1:M|—|—|—|—|—|1:1?|—|—|—|—|

ใครผูกกับใครบ้างดูจากหลายจุดนี้ได้เลย.

---

# 🔐 **3) Permission Matrix (ใครแตะอะไรได้บ้าง?)**

### ตามฐานข้อมูล v2.0 และ ROLE ระบบใหม่

|ENTITY|Viewer|Editor|Manager|Admin|
|---|---|---|---|---|
|Project|read|read|create/update/delete|all|
|File|read|upload/edit/delete|all|all|
|FileVersion|read|create|rollback|all|
|Chunk|read|auto|auto|all|
|Embedding|read|auto|auto|all|
|KBRegistry|read|auto|auto|admin-only modify|
|AgentRun|run-limited|run-full|run-full + override|unrestricted|
|RoutingLog|read-self|read-project|read-project|all|
|EventLog|read-self|read-project|read-project|all|
|Metrics|read-public|read-project|read-project|all|
|ErrorLog|read-self|read-project|read-project|all|

**ผู้ใช้ทั่วไป (Viewer)**  
→ มองเห็นอย่างเดียว ไม่แตะ KB/Model/Agent

**Editor**  
→ ดู + เพิ่มไฟล์ + ให้ agent ทำงาน

**Manager**  
→ มีสิทธิ์ rollback, merge, sync, override

**Admin**  
→ เข้าถึงทุก entity และทุก project

---

# 🚀 **4) Schema Flow Summary (เข้าใจใน 5 วินาที)**

```
User
 → Project
   → File
     → FileVersion
       → Chunks
         → Embeddings
       → KBRegistry

User/Project → AgentRun
AgentRun → RoutingLog
AgentRun → EventLog
AgentRun → ErrorLog
Project/User → Metrics
```

นี่คือ “เส้นเลือดใหญ่ของระบบ”

---

ได้เลย Santa —  
นี่คือ **DATA_SCHEMA v2.0 (ฉบับสมบูรณ์ที่สุด + ยกเครื่อง + เสริมทั้งหมดที่เรายังไม่ได้ใส่)**  
รวมข้อมูลจาก:

- DATA_SCHEMA เก่า
    
- KNOWLEDGE_SYNC v2.0
    
- RAG_ENGINE v2.0
    
- EVENT_BUS
    
- CACHE_STRATEGY
    
- FILE ENGINE
    
- Vector DB design
    
- SYSTEM_CONTRACT v2.0
    
- AGENT_ENGINE
    
- Model Routing
    
- Deployment Guide
    

เขียนแบบ **โครงสร้างจริง + พร้อมนำไปสร้าง DB + พร้อมขยายสเกล + deterministic**

ไปเริ่มเลย 🔥

---

# 📘 **DATA_SCHEMA v2.0**

Unified Structured Data Model for UET Knowledge Platform  
**“สคีมาหลักที่ทุก Engine ต้องใช้ร่วมกัน”**

---

# 🟦 0. ภาพรวม (Overview)

DATA_SCHEMA v2.0 คือ:

- แกนข้อมูลของแพลตฟอร์ม UET
    
- รองรับ RAG, KS, Agent, Model Routing
    
- รองรับ versioning และ event-driven update
    
- deterministic
    
- scale ได้
    
- read-intensive friendly
    
- write-safe (sync leader only)
    

ระบบข้อมูลแบ่งเป็น **6 ชั้น (6 Data Layers):**

```
L1 File Storage
L2 File Metadata (DB)
L3 Chunk Layer
L4 Embedding Layer
L5 Vector Layer
L6 Knowledge Registry
```

เหมาะกับระบบที่มี knowledge loop (UET model)

---

# 🟩 1. FILES (L1–L2)

```
Table: files
```

|Field|Type|Description|
|---|---|---|
|id|UUID|file primary key|
|project_id|UUID|เชื่อมกับ Project|
|name|text|display name|
|path|text|storage path|
|mime|text|pdf, md, docx|
|size|int|file size|
|created_by|UUID|user id|
|created_at|timestamp|เวลาสร้าง|
|updated_at|timestamp|เวลาล่าสุด|
|version|int|เวอร์ชันไฟล์|
|hash|text|file content hash|
|status|enum|active/deleted|

**กฎตาม SYSTEM_CONTRACT:**

- ไม่ให้ไร้ version
    
- file.hash ต้องตรงกับข้อมูลก่อน chunk
    
- update ทุกครั้งต้องเพิ่ม version + emit event
    

---

# 🟧 2. FILE_VERSION (History)

```
Table: file_versions
```

|Field|Type|Description|
|---|---|---|
|id|UUID||
|file_id|UUID||
|version|int||
|hash|text||
|diff|jsonb|optional delta|
|created_at|timestamp||

ใช้สำหรับ rollback / audit / diff chunking

---

# 🟦 3. CHUNKS (L3)

```
Table: chunks
```

|Field|Type|Description|
|---|---|---|
|id|UUID||
|file_id|UUID||
|chunk_index|int|ลำดับ chunk|
|chunk_text|text|string กระจายแล้ว|
|length|int||
|section|text|optional|
|hash|text|ใช้ diff-based sync|
|created_at|timestamp||
|updated_at|timestamp||

**กฎสำคัญ:**

- chunk_id stable
    
- chunk_hash ใช้ตรวจว่า embed ใหม่หรือไม่
    
- chunk ประมวลแบบ deterministic
    

---

# 🟩 4. EMBEDDINGS (L4)

```
Table: embeddings
```

|Field|Type|
|---|---|
|id|UUID|
|chunk_id|UUID|
|vector|vector(1536 or 3072)|
|model|text|
|dim|int|
|hash|text|
|created_at|timestamp|

**Embedding Cache Rule:**  
ถ้า `chunk.hash` เดิม → ใช้ embedding เดิม  
ถ้าไม่ตรง → embed ใหม่ทันที

---

# 🟦 5. VECTOR STORE (L5)

ใช้ Qdrant / pgvector  
schema แบบ unified:

```
Collection: vectors
Fields:
- id (UUID)
- project_id
- file_id
- chunk_id
- embedding (vector)
- metadata: {
    section, version, model, file_name
}
```

**กฎสำคัญตาม SYSTEM_CONTRACT:**

- RAG ต้อง search ตาม project_id เสมอ
    
- vector mapping ต้องตรงกับ chunk
    
- ห้าม vector orphan
    

---

# 🟧 6. KNOWLEDGE REGISTRY (L6)

```
Table: knowledge_registry
```

|Field|Type|
|---|---|
|project_id|UUID|
|latest_kb_version|int|
|last_sync_at|timestamp|
|file_versions|jsonb|
|chunk_count|int|
|vector_count|int|

**หน้าที่:**

- เป็น “single source of truth”
    
- Flow Control ใช้ตรวจสอบ stale data
    
- Agent ใช้ตรวจ KB version ล่าสุด
    
- Event Bus ใช้กำหนด invalidation
    

---

# 🟥 7. PROJECTS

```
Table: projects
```

|Field|Type|
|---|---|
|id|UUID|
|name|text|
|owner_id|UUID|
|created_at|timestamp|
|updated_at|timestamp|
|config|jsonb|

---

# 🟩 8. USER & PERMISSIONS

```
Table: users
Table: project_roles
```

Role matrix:

|Role|Description|
|---|---|
|viewer|read-only|
|editor|edit + RAG|
|manager|create / update / delete|
|owner|admin|

สิ่งนี้ถูก SYSTEM_CONTRACT บังคับในการเข้าถึงข้อมูลทุกชั้น

---

# 🟦 9. CACHE STATE (ตาม CACHE_STRATEGY)

ไม่ใช่ตาราง DB  
แต่ metadata ที่ต้องเก็บใน Redis:

```
cache:q:{hash}
cache:p:{prompt_hash}
cache:emb:{chunk_hash}
cache:agent:{id}
cache:route:{task_type}
```

---

# 🟪 10. METRICS TABLE (optional แต่แนะนำ)

```
Table: metrics
```

|Field|Type|
|---|---|
|id|UUID|
|event|text|
|cost|float|
|latency|float|
|model|text|
|agent_id|UUID|
|project_id|UUID|
|created_at|timestamp|

ใช้ดู load, cost, agent behavior

---

# 🟫 11. ER DIAGRAM (แบบอ่านง่ายที่สุด)

```
files (1) ────< chunks (many) ────< embeddings (1)
   │              │                     │
   │              ▼                     │
   └────< file_versions                 │
                       │               │
                       ▼               ▼
             knowledge_registry        vectors
```

---

# 🟧 12. DATA FLOW DIAGRAM

**จากไฟล์ → chunk → embed → vector → registry**

```
FILE_UPDATED
    ▼
parse_file
    ▼
create chunks
    ▼
hash compare
    ▼
if changed:
    embed chunk
    ▼
vector upsert
    ▼
update registry
    ▼
emit KB_VERSION_UPDATED
```

---

# 🟦 13. INTEGRATION WITH RAG

```
RAG Query
    ▼
vector search
    ▼
retrieve topK → chunks
    ▼
join files/chunks
    ▼
fuse context
    ▼
return to agent
```

---

# 🟩 14. INTEGRATION WITH AGENT ENGINE

```
Agent writes file
    ▼
increase version
    ▼
Knowledge Sync
    ▼
chunks + embeddings + vector store update
    ▼
Registry updated
    ▼
cache invalid
    ▼
RAG use new KB
```

นี่คือ “Knowledge Loop”

---

# 🟧 15. RULE MATRIX (กฎทั้งหมดที่ DATA_SCHEMA ต้อง obey)

|Rule|Description|
|---|---|
|Versioned data only|ห้ามมีไฟล์ไม่มี version|
|Project isolation|แยกระหว่าง project|
|Deterministic chunk|chunk ต้องคงที่ทุกครั้ง|
|Embedding hash match|ใช้ cache ได้|
|Registry authority|RAG ต้องใช้ registry ล่าสุด|
|Event-driven update|Sync ทุกครั้งต้อง emit event|
|Zero-stale cache|Cache ล้างเมื่อ KB เปลี่ยน|
|No orphan vector|vector ทุกตัวต้องมี chunk|

---

# ⭐ 16. สรุปโคตรชัด

DATA_SCHEMA v2.0 ตอนนี้:

### ✔ ครบทุกชั้น (L1–L6)

### ✔ พร้อมสร้าง DB จริง

### ✔ พร้อมรองรับ RAG / Agent / Sync

### ✔ deterministic ตาม SYSTEM_CONTRACT

### ✔ รองรับ Versioning, diff-chunk, embedding cache

### ✔ รองรับ event-driven update

### ✔ มี ER Diagram + Flow + Rules + Matrix

### ✔ รองรับ scaling ตาม Deployment v2.0

นี่คือสคีมาระดับระบบวิชาการ + enterprise ในเวลาเดียวกัน

---
