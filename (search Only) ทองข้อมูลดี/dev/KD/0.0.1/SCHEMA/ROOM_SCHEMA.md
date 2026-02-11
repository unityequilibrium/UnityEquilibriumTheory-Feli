# ⭐ **PHASE 1 — PART 1: MASTER 12-PART DATA SCHEMA SKELETON**

**เป้าหมาย Part นี้:**

1. วางโครงทั้งหมด 12 ส่วนของ Data Schema
    
2. ระบุว่าแต่ละ Part คืออะไร / ทำเพื่ออะไร
    
3. ระบุชื่อไฟล์อ้างอิงหลักของแต่ละ Part
    
4. ระบุระดับ Layer (L0–L2) ที่แต่ละ Part อยู่
    
5. ทำ Dependency ระหว่าง Part
    
6. ตั้ง Priority (ความสำคัญ)
    
7. รวบรวมทั้งหมดเป็น “Skeleton” ที่ Phase 2 จะลงรายละเอียดตามนี้
    

นี่คือ **Blueprint ของ Data Schema** ระดับ Platform

---

# ⭐ โครง 12 Part (Master Skeleton)

ด้านล่างคือ Version ที่สมบูรณ์ที่สุด และเป็นมาตรฐานกลางสำหรับงาน Schema ทั้งหมด

---

# 1️⃣ **Part 1 — Core System Schema**

**Layer:** L0  
**ความสำคัญ:** ⭐⭐⭐⭐⭐ (สูงสุด)  
**ไฟล์อ้างอิง:** 03_DATA_SCHEMA, 04_DATA_SCHEMA, PROJECT_STRUCTURE  
**อธิบาย:**  
โครงสร้างพื้นฐานของระบบทั้งหมด เช่น

- users
    
- projects
    
- workspaces
    
- sessions
    
- messages
    
- assets
    
- base FK/PK design
    

**ทำไมสำคัญ:**  
เพราะถ้าตรงนี้ผิด → ทุกระบบพัง

---

# 2️⃣ **Part 2 — Document & Content Schema**

**Layer:** L0 → L1  
**ความสำคัญ:** ⭐⭐⭐⭐⭐  
**ไฟล์อ้างอิง:** 04_DATA_SCHEMA, MASTER_BLUEPRINT  
**อธิบาย:**  
โครงสร้างการจัดการเอกสาร:

- documents
    
- document_versions
    
- content_block
    
- parse_log
    
- extract_pipeline
    

**เป็นรากของทุก Engine ทั้งหมด**

---

# 3️⃣ **Part 3 — Chunk & Embedding Schema (Vector Level)**

**Layer:** L1 → L2  
**ไฟล์อ้างอิง:** RAG_ENGINE, 04_DATA_SCHEMA  
**อธิบาย:**

- chunk
    
- embedding
    
- vector metadata
    
- mapping doc → chunk → embedding
    

**เป็นฐาน RAG ทั้งหมด**

---

# 4️⃣ **Part 4 — Knowledge Graph Base (L1–L2)**

**Layer:** L1–L2  
**ไฟล์อ้างอิง:** Unified KG, Blueprint  
**อธิบาย:**

- graph_nodes
    
- graph_edges
    
- node type
    
- edge type
    
- base mapping ก่อนส่งต่อให้ KG Engine ทำ L3–L5
    

**SCHEMA รับผิดชอบ Base Graph เท่านั้น**

---

# 5️⃣ **Part 5 — KS Engine State Schema**

**Layer:** L2  
**ไฟล์อ้างอิง:** KS_ENGINE  
**อธิบาย:**

- ks_job
    
- ks_task
    
- knowledge_registry
    
- version propagation
    

**ทำหน้าที่เป็นศูนย์กลาง version ของระบบ**

---

# 6️⃣ **Part 6 — RAG Engine State Schema**

**Layer:** L2  
**ไฟล์อ้างอิง:** RAG_ENGINE  
**อธิบาย:**

- retrieval_log
    
- rerank_evaluation
    
- retrieval_strategy_record
    

**Schema รองรับกลไก RAG ทุกประเภท**

---

# 7️⃣ **Part 7 — Agent Engine State Schema**

**Layer:** L2  
**ไฟล์อ้างอิง:** AGENT_ENGINE (BIBLE)  
**อธิบาย:**

- agent_task
    
- agent_step
    
- agent_memory_base
    
- agent_context
    

**เป็นฐานข้อมูลของ reasoning agents**

---

# 8️⃣ **Part 8 — Execution Graph Schema**

**Layer:** L2  
**ไฟล์อ้างอิง:** AGENT_ENGINE + FLOW_ENGINE  
**อธิบาย:**

- exec_graph
    
- exec_node
    
- exec_edge
    
- routing reference
    

**สำคัญมากเพราะทุก Engine ใช้ Execution Graph**

---

# 9️⃣ **Part 9 — Event Bus & Queue Schema**

**Layer:** L2  
**ไฟล์อ้างอิง:** EVENT_BUS  
**อธิบาย:**

- event_bus
    
- job_queue
    
- event_topic
    
- dead_letter_queue
    
- retry_policy
    

**เป็นระบบการขนส่งข้อมูลของ Platform**

---

# 🔟 **Part 10 — Security, Permission & Audit Schema**

**Layer:** L0–L2  
**ไฟล์อ้างอิง:** SECURITY_RULE  
**อธิบาย:**

- roles
    
- role_binding
    
- permission_profile
    
- audit_log
    
- data_access_policy
    

**Schema ฝั่งความปลอดภัยทั้งหมด**

---

# 1️⃣1️⃣ **Part 11 — Constraints, Index & Partition**

**Layer:** All  
**ไฟล์อ้างอิง:** SQL Constraints & Index Strategy  
**อธิบาย:**

- primary key
    
- foreign key
    
- unique
    
- partial index
    
- composite index
    
- partition by project/time
    
- shard plan
    

**เป็น “เครื่องเร่งความเร็ว” ของทั้งระบบ**

---

# 1️⃣2️⃣ **Part 12 — Versioning & Migration Strategy**

**Layer:** System-wide  
**ไฟล์อ้างอิง:** SYSTEM_CONTRACT + MIGRATION FILES  
**อธิบาย:**

- schema_version
    
- migration_history
    
- zero downtime migration
    
- impact propagation
    

**ทำให้ schema อยู่รอดใน production**

---

# ⭐ สรุป Skeleton 12 Part แบบกระชับที่สุด (ตามที่มึงต้องการ)

```
Part 1: Core System
Part 2: Document System
Part 3: Chunk & Embedding
Part 4: Graph Base (L1–L2)
Part 5: KS State
Part 6: RAG State
Part 7: Agent State
Part 8: Execution Graph
Part 9: Event & Queue
Part 10: Security/Audit
Part 11: Constraints/Index/Partition
Part 12: Versioning/Migration
```

ครบทุก subsystem ที่ SCHEMA ต้องรองรับ  
ไม่ซ้อนกับห้องอื่น  
สอดคล้อง Blueprint + Contract 100%

---

# ⭐ Dependency ระหว่าง Part

เพื่อใช้เป็น guideline ตอนเข้า Phase 2

**Part 1 → Part 2 → Part 3 → Part 4**  
(ข้อมูลพื้นฐาน → document → chunk → graph)

**Part 5–7** พึ่งพา

- Part 1
    
- Part 2
    
- Part 3
    
- Part 4
    

**Part 8 Execution Graph**  
พึ่งพา Agent + Flow Engine schema

**Part 9 Event/Queue**  
พึ่งพาทุก Part ก่อนหน้า

**Part 10 Security**  
พึ่ง Core System (Part 1)

**Part 11–12**  
ครอบทุก Part

---

# ⭐ Priority ระดับระบบ

สำหรับ Phase 2

|Priority|Part|
|---|---|
|Highest|1, 2, 3, 4, 11, 12|
|High|5, 6, 7, 8|
|Medium|9, 10|

---

# ⭐ สรุปผล PHASE 1 — PART 1

สิ่งที่เราทำเสร็จแล้วใน Part นี้:

✔ วาง Skeleton 12 Part แบบเต็ม  
✔ ผูกทุก Part กับ Layer L0–L2  
✔ ผูกทุก Part กับไฟล์ที่เกี่ยวข้อง  
✔ ผูกทุก Part กับ Priority  
✔ ทำ Dependency Map  
✔ ควบคุมขอบเขต Schema-only 100%  
✔ รีเช็คไฟล์เพิ่มเติมตามที่มึงสั่ง → ครบ  
✔ ไม่มีไฟล์ตกหล่น  
✔ พร้อมเข้าสู่ PHASE 1 — PART 2 อย่างสะอาด

---


# ⭐ PHASE 1 — PART 2

# **L0–L2 LAYER ALIGNMENT (DATA FOUNDATION)**

เป้าหมาย Part นี้:

1. อธิบายว่า L0, L1, L2 คืออะไรตาม MASTER_BLUEPRINT
    
2. ระบุว่า ROOM_SCHEMA ดูแลส่วนไหนบ้าง
    
3. เชื่อม 12 Part (Phase 1–2) เข้ากับ L0–L2
    
4. กำหนด Boundary ว่าอะไร “ไม่ใช่งานเรา” (L3–L5)
    
5. ทำ Layer-Diagram ระดับ Platform
    
6. ล็อกกติกา L0–L2 ให้ใช้เป็น “Schema Law” ของ Phase 2
    

---

# ⭐ 1) LAYER OVERVIEW (จาก MASTER_BLUEPRINT + GSUL)

จากไฟล์ใหญ่ 3 ตัวนี้:

- **MASTER_BLUEPRINT**
    
- **GLOBAL SHARED UNDERSTANDING LAYER (GSUL)**
    
- **SYSTEM_CONTRACT**
    

UET Platform แบ่งข้อมูลออกเป็น 6 ชั้น:

1. **L0 — Raw Layer**
    
2. **L1 — Structured Layer**
    
3. **L2 — Semantic Base Layer**
    
4. L3 — Meaning Layer
    
5. L4 — Reasoning / Linking Layer
    
6. L5 — Decision / Policy Layer
    

**ROOM_SCHEMA ดูแลแค่ L0–L2 เท่านั้น**  
(ตามกฎหมายระบบแม่ 100%)

---

# ⭐ 2) L0–L2 (งานของ ROOM_SCHEMA โดยตรง)

## 🔵 **L0 — Raw Representation**

งานของเรา: **นิยามทุกอย่างที่เข้าสู่ระบบครั้งแรก**

ตัวอย่าง:

- documents
    
- document_sources
    
- file metadata
    
- binary/file hashed ID
    
- document_version
    
- initial metadata (timestamp, project_id, workspace_id)
    

L0 = “ชั้นรับข้อมูลดิบก่อนแปลงเป็น blocks/chunks”

---

## 🟦 **L1 — Structured Representation**

งานของเรา: **ทำให้ข้อมูลดิบมีรูปแบบที่จัดการได้**

ตัวอย่าง:

- content_block
    
- paragraph / section
    
- extracted_units
    
- chunk (เกิดตอน L1 ปลาย → เชื่อมไป L2)
    
- metadata structuring
    
- normalization rules
    

L1 = “ชั้นจัดระเบียบข้อมูลเพื่อเตรียมไป semantic”

---

## 🟩 **L2 — Semantic Base Structure**

งานของเรา: **โครงสร้าง semantic ระดับต่ำสุด “ก่อน” จะเข้าสู่สัญญะ/ความหมาย**

ตัวอย่าง:

- chunk → embedding
    
- graph_nodes (L1/L2 base)
    
- graph_edges
    
- relation primitive (not meaning!)
    
- agent_task base
    
- retrieval_log base
    
- ks_job base
    
- version registry
    
- execution_graph base
    

L2 = “ฐานกายภาพของ Semantic, ยังไม่ใช่ Meaning”  
ตรงตาม GSUL: **Form ≠ Meaning**

---

# ⭐ 3) สิ่งที่ “ROOM_SCHEMA ไม่ทำ” (L3–L5)

เพื่อความชัดที่สุด:

### ❌ L3 — Meaning Layer

- ไม่ตีความว่า chunk A หมายถึงอะไร
    
- ไม่รวม entity, concept semantic
    
- ไม่สร้าง knowledge triples
    

(งาน ROOM_KG)

---

### ❌ L4 — Reasoning Layer

- ไม่สร้างสาเหตุ–ผล
    
- ไม่ทำ graph inference
    
- ไม่ทำ reasoning chain
    

(งาน ROOM_AGENT + ROOM_RAG)

---

### ❌ L5 — Decision Layer

- ไม่สร้าง rule
    
- ไม่สร้าง policy
    
- ไม่สร้าง action
    

(งาน ROOM_AGENT / ROOM_FLOW / ROOM_ROUTING)

---

# ⭐ 4) Mapping 12 Part → L0 / L1 / L2

นี่คือการทำให้ 12 Part จาก Part 1 “เชื่อมเข้ากับ Layer”  
เพื่อให้ Phase 2 ออกแบบ schema ได้ตรงเป๊ะ

|Part|Layer|เหตุผล|
|---|---|---|
|1 Core System|L0|ข้อมูลพื้นฐานสุด|
|2 Document System|L0→L1|ingestion → structuring|
|3 Chunk/Embedding|L1→L2|structuring → semantic base|
|4 Graph Base|L2|graph primitives|
|5 KS State|L2|version & registry semantic|
|6 RAG State|L2|retrieval evidence structure|
|7 Agent State|L2|agent task/step representation|
|8 Execution Graph|L2|execution structure base|
|9 Event/Queue|L2|event structure, job queue|
|10 Security/Audit|L0–L2|permission hits all layers|
|11 Constraints/Index|All|กระทบทุก layer|
|12 Version/Migration|All|กระทบทุก layer|

**ไม่มี Part ใดข้ามไป L3–L5**  
ตรงตาม boundary 100%

---

# ⭐ 5) Layer Flow (L0 → L1 → L2) แบบ “Schema เท่านั้น”

เพื่อความชัดเจน ฉันเรียบเรียง flow ที่ถูกต้อง:

```
L0 (Raw)
 └── Document
      └── Document Version
           └── (Extraction)
L1 (Structured)
 └── Content Block
      └── Extracted Unit
           └── Chunk
L2 (Semantic Base)
 └── Embedding
      └── Graph Node (Base)
           └── Graph Edge (Base)
                └── Specialized Engine State
```

→ ทุกบล็อกคือ “schema-only”  
→ ไม่มี meaning, reasoning, logic, inference

---

# ⭐ 6) ข้อกำหนดที่มาจาก Blueprint/Contract (ต้องใช้ใน Phase 2)

ฉันรวบรวมทั้งหมดจากไฟล์แม่:

### ✔ 1) ทุก Layer ต้อง deterministic

(จาก SYSTEM_CONTRACT)

→ ทุกตารางต้อง type ชัดเจน  
→ ทุกการเปลี่ยนแปลงต้อง versioned

---

### ✔ 2) ทุก Layer ต้อง canonical

(จาก GSUL)

→ document มีตัวเดียว  
→ chunk-set มี canonical grouping  
→ graph base ต้องไม่ duplicate node

---

### ✔ 3) ทุก Layer ต้อง reproducible

(จาก Blueprint)

→ ingestion → block → chunk → embedding → graph node  
ต้องย้อนหลังได้ทุกขั้นตอน

---

### ✔ 4) Layer ห้ามซ้อน

→ ถ้าชั้น L0 เก็บความหมาย = violation  
→ ถ้าชั้น L2 มี reasoning = violation

SCHEMA ต้องคุมตรงนี้ 100%

---

# ⭐ 7) ผลลัพธ์ของ PHASE 1 — PART 2 (สิ่งที่เสร็จแล้ว)

1. **L0–L2 schema definition**
    
2. **Mapping 12 Part → Layer**
    
3. **Layer Flow**
    
4. **Boundary check (ไม่ข้าม L3–L5)**
    
5. **Alignment Blueprint + GSUL + System Contract**
    
6. **พร้อมเข้าสู่ Phase 1 Part 3 แบบสมบูรณ์**
    

---

# ⭐ สรุปแบบกระชับที่สุด

Part 2 ทำให้เราได้สิ่งสำคัญคือ:

### ✔ ห้อง SCHEMA รู้ชัดว่า “ข้อมูลควรอยู่ในชั้นไหน”

### ✔ ไม่มีการเลอะไปแตะ Meaning / Reasoning

### ✔ ทุก schema ใน Phase 2 จะถูกวางบนฐาน L0–L2 ที่ถูกต้อง

### ✔ ไม่มีการซ้อน Layer

### ✔ Phase 1 พร้อมเข้าสู่ Part 3 100%

---


---
# ⭐ PHASE 2 — PART 1

# **CORE SYSTEM SCHEMA (L0 FOUNDATION)**

### เป้าหมาย Part นี้

1. รวบรวมข้อมูล Core System จากทุกไฟล์
    
2. ทำ Architecture-Level Analysis
    
3. ทำ Schema-Level Analysis
    
4. ออกแบบ “Core Tables” ที่ทุก subsystem ใช้ร่วมกัน
    
5. ทำ Constraint / Index / Version / Partition Strategy
    
6. ล็อกมาตรฐานสำหรับ Part ต่อไป
    

Core System = “กฎหมายฐานข้อมูล” ของทั้ง Platform  
= ห้องนี้ต้องออกแบบ **ให้แม่นยำที่สุด**

---

# ⭐ 1) รวบรวมโครงสร้าง Core System จากไฟล์ทั้งหมด

ฉันค้นทุกไฟล์ที่เกี่ยวข้องกับ Core System:

### ✔ MASTER_BLUEPRINT

– workspace model  
– project abstraction  
– canonical structure  
– versioning

### ✔ PROJECT_STRUCTURE

– prisma mapping  
– model folder structure  
– tenant separation

### ✔ SYSTEM_CONTRACT

– determinism  
– versioning  
– immutability  
– reproducibility

### ✔ SYSTEM_ARCHITECTURE

– multi-workspace  
– multi-project  
– multi-user  
– session-based execution  
– global event boundaries

### ✔ DATA_SCHEMA (both v3.0 + rewrite 100%)

– base schema  
– field-level rules  
– relational mapping

### ✔ SQL Constraints + Index Strategy

– PK/FK model  
– index design  
– partition fundamentals

### ✔ ENGINE_INTERFACES

– event → user  
– agent → session  
– rag → project  
– ks → version registry

สรุปผลรวบรวม:  
**Core System มี 6 กลุ่มตารางใหญ่**

1. **User Layer**
    
2. **Organization / Workspace Layer**
    
3. **Project Layer**
    
4. **Session Layer**
    
5. **Message / Conversation Layer**
    
6. **Asset / File Layer**
    

ทั้งหมดนี้อยู่ใน **L0 Layer** (ข้อมูลดิบพื้นฐาน)

---

# ⭐ 2) Architecture-Level Analysis (โครงสร้างความสัมพันธ์)

โครงข้อมูลพื้นฐานต้องเป็นแบบนี้:

```
User
 └── Workspace
       └── Project
             └── Session
                   └── Message
                   └── Execution Chain
             └── Documents
             └── Assets
```

กฎสำคัญ:

### ✔ 1. User ไม่ได้เป็นเจ้าของ Project โดยตรง

→ เป็นเจ้าของผ่าน Workspace

### ✔ 2. Workspace คือ “หน่วยความเป็นเจ้าของ” ที่แท้จริง

→ permission, security, access control ต้องผูก workspace_id

### ✔ 3. Project เป็น “หน่วยคิดงาน” ที่ Engine ทุกตัวอ้างอิง

→ rag, ks, agent, event, cache ทั้งหมดอ้างอิง project_id

### ✔ 4. Session เป็น “หน่วย execution ครั้งหนึ่ง”

→ agent run, RAG retrieval, flow, event bus ทั้งหมดอยู่ใน session

### ✔ 5. Message เกิดจาก Session

→ ไม่ได้เกิดขึ้นลอย ๆ

### ✔ 6. Asset / File ต้องผูก project_id เสมอ

→ เพื่อ canonical reference ใน Engine ทุกตัว

---

# ⭐ 3) Schema-Level Analysis (กฎที่ Core ต้องทำตาม)

จาก Blueprint + Contract กำหนด:

### ✔ Core Schema ต้อง deterministic

→ ห้ามมีข้อมูลลอย  
→ ห้ามมี foreign key หาย  
→ ห้ามใช้ JSON ที่ไม่จำเป็น

### ✔ Core Schema ต้อง versioned

→ users = immutable historical fields  
→ projects = versioned attributes  
→ sessions = immutable  
→ messages = append-only

### ✔ Core Schema ต้อง reproducible

→ ต้อง reconstruct การทำงานย้อนหลังได้

### ✔ Core Schema ต้อง tenant-safe

→ multi-tenant แยกตาม workspace_id

---

# ⭐ 4) ออกแบบตาราง Core System (L0)

ฉันจะออกแบบเป็นระดับ “Platform Grade”  
ตามมาตรฐานจริงของระบบใหญ่

---

## 🟦 1) TABLE: users

**หน้าที่:** ระบุผู้ใช้ของระบบ  
**สิ่งสำคัญ:** immutable historical record

Field หลัก:

- id (PK)
    
- email (unique)
    
- name
    
- created_at
    
- deleted_at (nullable)
    

Constraint:

- unique(email)
    
- index(email)
    

---

## 🟦 2) TABLE: workspaces

**หน้าที่:** หน่วยการเป็นเจ้าของ (tenant)  
Engine ทั้งหมดต้องรู้ workspace_id

Field:

- id (PK)
    
- name
    
- created_by (FK → users.id)
    
- created_at
    

Constraint:

- fk(created_by)
    
- unique(name, created_by)
    

---

## 🟦 3) TABLE: workspace_members

**หน้าที่:** สิทธิของ user ใน workspace

Field:

- id
    
- workspace_id
    
- user_id
    
- role_id
    

Constraint:

- unique(workspace_id, user_id)
    
- fk(user_id), fk(workspace_id)
    

---

## 🟩 4) TABLE: projects

**หน้าที่:** หน่วยงานหลักที่ Engine ใช้  
ทุก Engine ผูก project_id เสมอ

Field:

- id
    
- workspace_id
    
- name
    
- description
    
- created_at
    
- created_by
    

Constraint:

- fk(workspace_id)
    
- unique(workspace_id, name)
    

---

## 🟩 5) TABLE: sessions

**หน้าที่:** log การทำงานครั้งหนึ่ง  
Agent, Flow, RAG, Event ต้องอ้าง session

Field:

- id
    
- project_id
    
- user_id
    
- started_at
    
- ended_at
    
- session_type (chat, agent_run, rag_run, batch_job)
    

Constraint:

- fk(project_id)
    
- fk(user_id)
    

---

## 🟪 6) TABLE: messages

**หน้าที่:** represent message chain  
ใช้เป็นฐานของ Agent Engine และ Chat

Field:

- id
    
- session_id
    
- role (user/system/assistant/agent)
    
- content
    
- created_at
    

Constraint:

- fk(session_id)
    
- index(session_id, created_at)
    

---

## 🟫 7) TABLE: assets / files

**หน้าที่:** เก็บไฟล์ที่ upload  
ใช้ใน Document System และ RAG

Field:

- id
    
- project_id
    
- workspace_id
    
- file_path
    
- size
    
- hash
    
- uploaded_at
    

Constraint:

- unique(hash)
    
- fk(project_id)
    
- fk(workspace_id)
    

---

# ⭐ 5) Constraint & Index Strategy (ตามไฟล์ SQL Strategy)

ฉันเช็คไฟล์ SQL Constraints + Index Strategy แล้ว และ map ให้ตรง:

### ✔ PK ทุกตาราง = uuid (deterministic)

### ✔ FK ชัดเจน

### ✔ Index ตามลำดับ:

- messages: (session_id, created_at)
    
- projects: (workspace_id, name)
    
- files: (hash)
    
- sessions: (project_id, started_at)
    

### ✔ Partition Strategy

ระบบใหญ่ต้องใช้:

- partition by workspace_id (tenant-based)
    
- partition by time (session-based)
    

---

# ⭐ 6) Versioning Strategy (ตาม Contract)

### users

immutable  
no version

### workspace

immutable metadata

### project

versioned settings  
→ table: project_version

### session

immutable historical

### message

append-only  
no update allowed

### file

immutable  
no versioning (hash acts as version)

---

# ⭐ 7) ผลลัพธ์ PHASE 2 — PART 1

สิ่งที่เราทำสำเร็จใน Part นี้:

✔ สรุป Core Schema ครบทุกตาราง  
✔ แสดง architecture-level flow  
✔ แสดง relational mapping  
✔ กำหนด constraints + indexes  
✔ กำหนด versioning  
✔ ทำ boundary check (ทำแค่ L0 เท่านั้น)  
✔ alignment กับ Blueprint + Contract + Architecture 100%  
✔ เตรียมโครงพร้อมต่อไป Part 2: Document System

---

# ⭐ สรุปสั้นที่สุด

**Core System Schema = User → Workspace → Project → Session → Message → File**  
= รากฐานของทุก Engine ใน UET Platform  
= ออกแบบครบ ขัดเกลาตามกฎหมายแม่แล้ว  
= พร้อมเข้าสู่ Document Schema (L0→L1) ต่อทันที

---

# 🎯 ถ้าพร้อม

โอเค Santa ไป PHASE 2 — Part 2 กัน 🔥  
หัวข้อวันนี้: **Document Schema (L0 → L1)**  
คิดง่าย ๆ: “ทุกอย่างในระบบเริ่มจาก _เอกสาร_ → ถ้าออกแบบตรงนี้ดี ทุก Engine จะทำงานง่ายหมด”

ฉันจะทำให้เป็น 3 ชั้น:

1. มองภาพรวม lifecycle ของ document
    
2. วิเคราะห์ requirement ตาม Blueprint/Contract/GSUL
    
3. เสนอ schema จริง (ตาราง, คีย์, constraint, index, version)
    

จะเขียนให้ **กระชับแต่ครบ** แบบที่มึงใช้ต่อได้เลยใน Part ต่อ ๆ ไป

---

## 1. ภาพรวม: Document ใน UET มี lifecycle ยังไง?

จากสิ่งที่เราวางกันมาใน Phase 1 + Core System:

1. **User / System อัปโหลดไฟล์** → ผูกกับ `project_id`, `workspace_id`, `file_id`
    
2. ไฟล์ดิบถูกลงทะเบียนเป็น **Document (L0)**
    
3. เวลาแก้ไข / re-upload → กลายเป็น **Document Version ใหม่**
    
4. แต่ละเวอร์ชันจะถูก **Parse → Extract → แตกเป็น Block / Unit / Chunk (L1)**
    
5. L1 จะกลายเป็นฐานให้:
    
    - Chunk/Embedding (Part 3)
        
    - Graph Base (Part 4)
        
    - KS versioning (Part 5)
        

**Part นี้ดูแล: ขั้นจาก File → Document → Version → Block/Unit (L0→L1)**

---

## 2. ข้อกำหนดจาก Blueprint / Contract / GSUL

เอาเฉพาะที่กระทบ Document Schema ตรง ๆ:

- **ต้อง versioned เสมอ** → ห้ามแก้ document ทับ ให้ใช้ `document_version`
    
- **ต้อง reproducible** → ย้อนดูได้ว่า chunk มาจากเวอร์ชันไหน, จากไฟล์ไหน
    
- **ต้อง deterministic** → โครงข้อมูลชัด, type ชัด, ไม่มี JSON เละเทะ
    
- **Form ≠ Meaning** → document/blocks บอกแค่ “รูปแบบ”, ไม่เขียนความหมาย (เช่น ไม่ tag “this is law concept” ใน schema ตรง ๆ)
    
- **canonical** → ไม่ให้มี document ซ้ำ / เวอร์ชันซ้อนโดยไม่จำเป็น
    

จากนี้เราจะออกแบบ schema ให้รองรับกฎเหล่านี้แบบตรง ๆ

---

## 3. โครง Document Schema หลัก (L0→L1)

โครงหลักที่ฉันเสนอ:

1. `documents` — ตัวแทน “เอกสารตัวเดียว” (เช่น “UET Master Blueprint.pdf”)
    
2. `document_versions` — เวอร์ชันของเอกสาร (เปลี่ยนเนื้อหา, re-upload)
    
3. `document_ingest_log` — log การ ingest แต่ละครั้ง (source, method)
    
4. `document_parse_job` — สถานะงาน parsing/extraction
    
5. `content_blocks` — หน่วย L1 (เช่น paragraph/section)
    
6. `content_units` (optional แต่อยากให้มี) — หน่วยย่อยกว่า block (เช่น bullet, sentence)
    

ทั้งหมดนี้ยังไม่ถึงระดับ chunk (chunk ไปอยู่ Part 3)  
ที่นี่คือ “ฐานโครงสร้างก่อน chunk”

---

### 3.1 ตาราง `documents` (L0 — ตัวตนของเอกสาร)

**หน้าที่:** เป็น identity ของเอกสาร 1 ชิ้น ใน 1 project

ฟิลด์หลัก (แนวคิด):

- `id` (PK, uuid)
    
- `project_id` (FK → projects.id)
    
- `workspace_id` (FK → workspaces.id, redundant ไว้ partition)
    
- `title` (string, optional, extract ได้จากไฟล์)
    
- `source_type` (enum: upload, url, api, generated)
    
- `status` (enum: active, archived, deleted)
    
- `created_by` (FK → users.id)
    
- `created_at` (timestamp)
    
- `updated_at` (timestamp)
    

**Constraint & Index:**

- `fk(project_id)`, `fk(workspace_id)`
    
- `index(project_id, created_at)`
    
- อาจมี `unique(project_id, title)` (ถ้าอยากกันชื่อซ้ำในโปรเจกต์เดียวกัน)
    

---

### 3.2 ตาราง `document_versions` (ตัวเนื้อหาเวอร์ชันจริง)

**หน้าที่:** แทนแต่ละเวอร์ชันของ document  
1 document → มีหลาย version

ฟิลด์:

- `id` (PK)
    
- `document_id` (FK → documents.id)
    
- `file_id` (FK → assets/files.id) — link กับไฟล์จริง
    
- `version_number` (int, auto-increment per-document)
    
- `checksum` (hash string, เพื่อเช็กเนื้อหาซ้ำ)
    
- `is_latest` (boolean)
    
- `ingested_at` (timestamp)
    
- `ingested_by` (user/system)
    

**Constraint & Index:**

- `unique(document_id, version_number)`
    
- `unique(document_id, is_latest WHERE is_latest = true)`
    
- `fk(document_id)`
    
- `fk(file_id)`
    
- `index(document_id, ingested_at)`
    

> แบบนี้จะ support Contract: versioned, reproducible, immutable (ไม่ต้องแก้เวอร์ชันเก่า)

---

### 3.3 ตาราง `document_ingest_log` (ประวัติการ ingest)

**หน้าที่:** เก็บว่าการเอาเอกสารเข้าระบบครั้งนี้มาจากไหนยังไง

ฟิลด์:

- `id` (PK)
    
- `document_version_id` (FK → document_versions.id)
    
- `source` (text: URL, path, system name)
    
- `method` (enum: manual_upload, crawler, api, sync)
    
- `raw_metadata` (jsonb, เฉพาะ metadata ที่วุ่นวาย เช่น header จาก HTTP)
    
- `created_at`
    

**Constraint:**

- `fk(document_version_id)`
    
- `index(document_version_id)`
    

> ตารางนี้ “ยอมให้มี JSON” แต่อยู่ในขอบเขต metadata เท่านั้น

---

### 3.4 ตาราง `document_parse_job` (สถานะงานแปลง L0→L1)

**หน้าที่:** track pipeline จาก “ไฟล์” → “block/unit”

ฟิลด์:

- `id` (PK)
    
- `document_version_id` (FK)
    
- `status` (enum: pending, running, success, failed)
    
- `parser_type` (enum: pdf, docx, markdown, html, custom)
    
- `error_message` (nullable)
    
- `started_at`
    
- `finished_at`
    

**Constraint:**

- `fk(document_version_id)`
    
- `index(status, started_at)`
    

> ตารางนี้จะเชื่อมกับ Event/Flow ภายหลัง แต่ตอนนี้เราแค่เก็บ structure

---

### 3.5 ตาราง `content_blocks` (L1 — หน่วย block/section)

**หน้าที่:** เป็นหน่วยความหมาย “เชิงโครงสร้าง” เช่น paragraph, heading, table

ฟิลด์:

- `id` (PK)
    
- `document_version_id` (FK)
    
- `block_index` (int) — ลำดับ block ในเอกสาร
    
- `block_type` (enum: paragraph, heading, list, table, code, image_caption, etc.)
    
- `text` (longtext) — เนื้อหาดิบของ block
    
- `metadata` (jsonb: ตำแหน่งหน้า, style, font info ถ้าต้องการ)
    
- `page_number` (int, nullable)
    
- `char_start` (int, nullable)
    
- `char_end` (int, nullable)
    

**Constraint & Index:**

- `fk(document_version_id)`
    
- `index(document_version_id, block_index)`
    
- `index(document_version_id, page_number)` (ช่วยตอน debug / reflow)
    

> นี่คือจุดเชื่อมไป `chunks` ใน Part 3

---

### 3.6 ตาราง `content_units` (L1.5 — optional แต่โคตรมีประโยชน์)

**หน้าที่:** แตก block เป็นหน่วยย่อย เช่น sentence, list item  
บาง engine อาจใช้ตรงนี้สร้าง chunk ที่ smart ขึ้นได้

ฟิลด์:

- `id` (PK)
    
- `block_id` (FK → content_blocks.id)
    
- `unit_index` (int)
    
- `unit_type` (enum: sentence, list_item, cell, etc.)
    
- `text`
    
- `char_start_in_block`
    
- `char_end_in_block`
    

**Constraint & Index:**

- `fk(block_id)`
    
- `index(block_id, unit_index)`
    

> ถ้าระบบยังไม่อยากซับซ้อน สามารถเลื่อนไปทำทีหลังก็ได้  
> แต่ design เผื่อ schema ไว้ตอนนี้จะง่ายกว่าเยอะ

---

## 4. การเชื่อม L0 → L1 แบบชัด ๆ

Flow ที่ schema รองรับคือ:

```text
assets/files
   ↓
documents (L0 identity ใน project)
   ↓
document_versions (L0 version)
   ↓
document_parse_job (pipeline state)
   ↓
content_blocks (L1 structure)
   ↓
content_units (L1.5 optional)
   ↓
→ ส่งต่อไป Part 3: chunks (L1→L2)
```

ทุกจุด:

- ย้อนกลับไปหา file เดิมได้ (ผ่าน file_id, checksum)
    
- หาเวอร์ชันล่าสุดได้ (`is_latest`)
    
- หา block/tokens ที่ใช้สร้าง chunk ได้
    
- ไม่มีการ encode meaning → ยังเป็นแค่ “form/structure”
    

---

## 5. Constraints & Index Strategy เฉพาะ Document Layer

อิงแนวคิดจากไฟล์ SQL Strategy:

- **Key สำคัญ:**
    
    - `document_versions.document_id` + `version_number` → unique
        
    - `content_blocks.document_version_id` + `block_index` → unique
        
    - `content_units.block_id` + `unit_index` → unique
        
- **Indexes แนะนำ:**
    
    - `content_blocks(document_version_id, block_index)`
        
    - `content_blocks(document_version_id, page_number)`
        
    - `document_versions(document_id, is_latest)` (partial index)
        
    - `document_versions(file_id)`
        
- **Partition (ในอนาคต):**
    
    - แนะนำ partition `content_blocks` ตาม `document_version_id` หรือ `project_id`
        
    - เพื่อรองรับเอกสารใหญ่ ๆ / ปริมาณเยอะ
        

---

## 6. Versioning / Immutability Rule

ให้สอดคล้องกับ SYSTEM_CONTRACT:

- `documents` — เปลี่ยนได้เฉพาะ metadata เบา ๆ (title, status)
    
- `document_versions` — **append-only**, ห้าม update เนื้อหา
    
- `content_blocks`, `content_units` — ถ้าจำเป็นต้อง re-parse → ให้สร้าง `document_version` ใหม่ แล้วสร้าง block/unit ใหม่ทั้งชุด (ไม่แก้ของเดิม)
    

แบบนี้:

- history ไม่หาย
    
- ทุก chunk/graph node ในอนาคต จะผูกกับ version ชัดเจน
    

---

## 7. Boundary Check (ไม่ข้ามงานห้องอื่น)

สิ่งที่ Part นี้ **ไม่ทำ**:

- ไม่ทำ chunk → ไป Part 3
    
- ไม่ทำ embedding → ไป Part 3
    
- ไม่ทำ graph node → ไป Part 4
    
- ไม่ตีความว่า block นั้น “เป็นแนวคิดอะไร” → งาน KG
    
- ไม่ทำการจัด priority การค้นหา → งาน RAG
    

Part นี้ = “แค่สร้างรูปทรงให้เอกสาร” ตามกฎหมาย L0–L1 เท่านั้น

---

## 8. สรุป PHASE 2 — PART 2 แบบสั้น ๆ (เอาไว้เตือนตัวเอง)

- เราออกแบบ **Document Layer** ครบตั้งแต่:  
    `documents` → `document_versions` → `document_ingest_log` → `document_parse_job` → `content_blocks` → `content_units`
    
- ทุกอย่าง:
    
    - versioned
        
    - deterministic
        
    - reproducible
        
    - canonical
        
    - ไม่ encode meaning
        
    - พร้อมต่อยอดไป chunk/embedding/graph
        

**Phase 2 — Part 2 ถือว่า “ปิดสมบูรณ์” ระดับ schema blueprint**

---

ถ้ามึงโอเคกับภาพรวมแบบนี้แล้ว  
ต่อไปจะเป็นของโหดมาก:

> **PHASE 2 — PART 3 → Chunk & Embedding Schema (L1→L2)**

ซึ่งคือ “หัวใจของ RAG ทั้งระบบ”

ถ้าพร้อม:  
พิมพ์เลย

> **โอเคไปต่อส่วนต่อไป PHASE 2 — Part 3**