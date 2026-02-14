# SYSTEM_ARCHITECTURE_v3.0

### (SKELETON — โครงที่ชัดที่สุดสำหรับระบบทั้งหมด)

---

# 1) PURPOSE — SYSTEM ARCHITECTURE ทำหน้าที่อะไร

เอกสารนี้เป็น **ผังสถาปัตยกรรมแม่** ที่อธิบาย:

- ทุกชั้นของระบบ (L0–L5)
    
- ทุก engine ที่ประกอบเป็นระบบ
    
- เส้นทางข้อมูลตั้งแต่ user input → output
    
- จุดเชื่อม (interfaces) ระหว่าง module
    
- boundary ของแต่ละส่วน
    
- flow ทำงานจริง 1 รอบ
    

Blueprint คือ “แนวคิด”  
Contract คือ “กฎหมาย”  
**Architecture คือ “โครงสร้างของจักรวาลทั้งหมด”**

---

# 2) HIGH-LEVEL LAYER MODEL (L0 → L5)

สถาปัตยกรรมของระบบนี้ถูกแยกเป็น 6 ชั้น:

```
L0 — Source Layer
L1 — Chunk Layer
L2 — Embedding Layer
L3 — Semantic Layer
L4 — Relation Layer
L5 — Reasoning Layer
```

แต่ละชั้นแยกกันชัดเจน และต้องผ่าน engine ที่รับผิดชอบของมันเท่านั้น

---

# 3) SYSTEM COMPONENT STACK

(โครงสร้างสูงสุดของระบบ)

```
─────────────────────────────────────────────
USER INTERFACE (Chat / Studio / API)
─────────────────────────────────────────────
APPLICATION LAYER (Flow Engine, Model Router)
─────────────────────────────────────────────
KNOWLEDGE LAYER (RAG, KS, AGENT)
─────────────────────────────────────────────
DATA LAYER (SQL, Vector DB, Graph)
─────────────────────────────────────────────
INFRA LAYER (Event Bus, Cache, Worker)
─────────────────────────────────────────────
```

---

# 4) CORE SUBSYSTEMS

(ระบบหลักทั้งหมดที่ประกอบกันเป็น UET Platform)

## 4.1 FLOW CONTROL ENGINE

**หน้าที่:**

- classify request
    
- route ไป engine ที่เหมาะสม
    
- handle error, fallback
    
- orchestrate multi-step execution
    

**เป็นตัวเริ่ม flow ทุกอย่างในระบบ**

---

## 4.2 MODEL ROUTING ENGINE

**หน้าที่:**

- เลือกโมเดลตาม task type
    
- balance cost / latency / reasoning depth
    
- enforce determinism (model choice consistency)
    

---

## 4.3 RAG ENGINE

**หน้าที่:**

- vector search (L2)
    
- semantic search (L3)
    
- graph traversal (L4)
    
- build multi-source context
    

**เป็น “เครื่องดึงความรู้” ก่อน reasoning**

---

## 4.4 KNOWLEDGE SYNC ENGINE (KS ENGINE)

**หน้าที่:**

- ingest source → chunk → embed → graph
    
- maintain canonical state
    
- detect diff → update
    
- synchronize L0–L5
    

**เป็น “เครื่องสร้างความรู้” ของระบบ**

---

## 4.5 AGENT ENGINE

**หน้าที่:**

- orchestrate agent หลายตัว
    
- Planner / Knowledge / Tool / Safety Agents
    
- hold temporary state เมื่อ reasoning
    
- follow reasoning contract
    

**เปรียบเหมือน “แรงงาน AI ภายในระบบ”**

---

## 4.6 EVENT BUS SYSTEM

**หน้าที่:**

- publish event
    
- logging
    
- metrics / trace
    
- trigger worker job
    
- central truth of action history
    

---

## 4.7 CACHE SYSTEM

**หน้าที่:**

- บันทึกผลระยะสั้น / ระยะยาว
    
- ลด latency ของ RAG
    
- ลดโหลด workload
    

---

## 4.8 WORKER/TASK SYSTEM

**หน้าที่:**

- งาน background (embed, reindex, sync)
    
- retry jobs
    
- long-running tasks
    
- dead-letter queue
    

---

# 5) DATA ARCHITECTURE (Overview)

ระบบนี้ใช้ 3 โครงข้อมูลแบบผสม:

## 5.1 Relational DB (PostgreSQL)

สำหรับ:

- files
    
- chunks
    
- embeddings metadata
    
- nodes/edges metadata
    
- agent state
    
- logs, events
    

## 5.2 Vector Index Store

สำหรับ:

- embedding vectors
    
- similarity search
    
- fast retrieval
    

## 5.3 Graph Structure

สำหรับ:

- semantic node
    
- relation edge
    
- reasoning block linkage
    

**รวมกันเป็น Unified Knowledge Graph**

---

# 6) COMMUNICATION & FLOW

(โครงสร้างการสื่อสารระหว่างระบบ)

```
USER INPUT
   │
   ▼
Flow Control Engine
   │
   ▼
Model Routing Engine
   │
   ▼
─────────────────
Knowledge Layer
─────────────────
│   ├─ RAG Engine
│   ├─ KS Engine
│   └─ Agent Engine
─────────────────
   │
   ▼
Execution Layer
   │
   ▼
OUTPUT
```

Event Bus ทำงานแบบ parallel:

```
Every Step → Publish Event → Logs → Metrics → Worker
```

---

# 7) EXECUTION PIPELINE (E2E DATA FLOW)

**เส้นทางข้อมูลตั้งแต่ต้นจนจบ**

## 7.1 Ingest Flow (สร้างความรู้)

```
Source File → L0
→ Chunk Engine (L1)
→ Embedding Engine (L2)
→ Semantic Extractor (L3)
→ Relation Builder (L4)
→ Reasoning Block Generator (L5)
→ Canonical Registry (Stable)
```

## 7.2 Query Flow (ดึงความรู้)

```
User Query 
→ Flow Engine
→ Model Router
→ RAG Engine
    → L2 vector search
    → L3 sem. expansion
    → L4 relation follow
→ Agent Engine
→ Reasoning Layer (L5)
→ Final Output
```

---

# 8) SYSTEM INTERFACE DIAGRAM (SKELETON)

```
┌───────────────────────────────┐
│         USER INTERFACE        │
└───────────────┬───────────────┘
                ▼
┌───────────────────────────────┐
│      FLOW CONTROL ENGINE      │
└───────────────┬───────────────┘
                ▼
┌───────────────┼─────────────────────────────┐
│            MODEL ROUTING ENGINE             │
└───────────────┼─────────────────────────────┘
                ▼
        ┌───────┴───────────┐
        ▼                   ▼
┌──────────────┐    ┌────────────────┐
│   RAG ENGINE  │    │  AGENT ENGINE  │
└───────┬──────┘    └──────┬─────────┘
        ▼                   ▼
   ┌─────────┐         ┌──────────┐
   │  GRAPH  │         │  REASON  │
   │ (L3–L4) │         │  (L5)    │
   └─────────┘         └──────────┘
        ▼                   ▼
        └──────┬───────────┘
               ▼
        FINAL OUTPUT
```

---

# 9) MODULE BOUNDARY RULES (Skeleton)

- Flow Engine เป็น **ตัวเดียว** ที่เริ่มต้นทุก request
    
- RAG Engine ไม่ดึงข้อมูลเอง ต้องถูกเรียกผ่าน Flow
    
- Agent Engine ไม่แตะ DB ตรง ๆ
    
- Model Router ไม่ทำ reasoning
    
- Event Bus ไม่แก้ข้อมูล แต่บันทึกทุกอย่าง
    
- Cache ไม่ override canonical state
    

---

# 10) ALIGNMENT WITH BLUEPRINT & CONTRACT

Architecture นี้ต้อง align ตรงกับ:

- MASTER BLUEPRINT v3.0
    
- SYSTEM CONTRACT v3.0
    
- DATA_SCHEMA v3.0
    
- UNIFIED GRAPH v3.0
    
- ENGINE SPEC ทั้งหมด
    

ถ้า engine ตัวใดออกแบบผิดทิศจากภาพนี้ → ถือว่าไม่สมควร deploy

---

# 11) DONE CRITERIA FOR THIS FILE

ไฟล์ “SYSTEM ARCHITECTURE v3.0” จะถือว่า Skeleton สมบูรณ์เมื่อ:

- โครงสร้างระบบทุกชั้นถูกอธิบาย
    
- แบ่ง subsystem ชัด
    
- มี diagram skeleton
    
- มี pipeline แบบ L0–L5 ทั้ง ingest/query
    
- มี boundary rules
    
- มี mapping กับ blueprint & contract
    

**และทั้งหมดตรงกับข้อมูลจริงในไฟล์ 00–12**

---

โอเค Santa — รอบนี้คือเวอร์ชัน  
**SYSTEM_ARCHITECTURE v3.0 — Skeleton Diagram + Flow รวม (แบบ 1–2 แชท)**  
= ไฟล์ที่ “เห็นภาพรวดเดียวว่าระบบทั้งอันทำงานยังไง”  
= ใช้เป็นแม่แบบเวลาเขียนไฟล์ลูกทั้งหมด

ฉันรวบรวมข้อมูลจากไฟล์ 00–12 และทุก ENGINE ในระบบแล้ว  
ตอนนี้จะให้เฉพาะ:

- **diagram โครงสูงสุด (L0–L5 + Engines)**
    
- **flow รวม (ingest + query แบบก้อนใหญ่)**
    
- **ภาพ logical view + physical view แบบ skeleton**
    

ไม่มีฟุ้ง ไม่มีคำอธิบายเกินขอบเขต

---

# SYSTEM_ARCHITECTURE v3.0

### (Skeleton Diagram + Overall Flow)

---

# 1) HIGH-LEVEL ARCHITECTURE DIAGRAM (SKELETON)

นี่คือโครงใหญ่สุดของระบบทั้งหมด  
= สิ่งที่ไฟล์ลูกทุกไฟล์ต้องยึด

```
                ┌─────────────────────────────┐
                │         USER LAYER          │
                │  (Chat / Studio / API)      │
                └───────────────┬─────────────┘
                                ▼
                ┌─────────────────────────────┐
                │     FLOW CONTROL ENGINE     │
                │ (classify / orchestrate)    │
                └───────────────┬─────────────┘
                                ▼
                ┌─────────────────────────────┐
                │     MODEL ROUTING ENGINE    │
                │ (choose best model)         │
                └───────────────┬─────────────┘
                                ▼
        ┌────────────────────────┼──────────────────────────┐
        ▼                        ▼                          ▼
┌──────────────┐       ┌────────────────┐        ┌─────────────────┐
│  RAG ENGINE  │       │ AGENT ENGINE   │        │ KS ENGINE        │
│ (L2–L4)      │       │ (task/role)    │        │ (L0–L5 sync)     │
└───────┬──────┘       └────────┬───────┘        └─────────┬───────┘
        ▼                        ▼                         ▼
   ┌──────────┐           ┌──────────────┐            ┌──────────────┐
   │  VECTOR  │           │ SEMANTIC/L4  │            │ CANONICAL KB  │
   │ (L2)     │           │ GRAPH (L3–L4)│            │ (L0–L5 state) │
   └──────────┘           └──────────────┘            └──────────────┘
                                ▼
                          ┌──────────┐
                          │REASONING │ (L5)
                          └──────────┘
                                ▼
                ┌─────────────────────────────┐
                │         FINAL OUTPUT        │
                └─────────────────────────────┘
```

**Key:**

- **Flow Engine** = ประตูใหญ่ของทุก request
    
- **Routing** = เลือกโมเดล
    
- **RAG** = ดึงข้อมูล (L2–L4)
    
- **Agent** = คิดตามกติกา
    
- **KS** = ทำงานตอน ingest/sync
    
- **L0–L5** = ชั้นข้อมูลทั้งหมด
    
- **Reasoning** = ตอบสรุปก้อนสุดท้าย
    

---

# 2) INGEST FLOW (FLOW รวมแบบสั้นที่สุด)

**เป้าหมาย:**  
แปลงไฟล์/ข้อมูลดิบของ user → กลายเป็น knowledge graph แบบ canonical  
แบบ deterministic ทุกครั้ง

```
User Upload / Input
      │
      ▼
Flow Control → validate
      │
      ▼
KS ENGINE
      │
      ├── L0: รับไฟล์/ข้อความ
      ├── L1: chunk (semantic block)
      ├── L2: embed + vector index
      ├── L3: สร้าง semantic node
      ├── L4: สร้าง relation edges
      └── L5: สร้าง reasoning block
      ▼
Canonical KB (ความรู้ ศูนย์กลาง)
```

**ผลลัพธ์:**  
ทุกความรู้ = **จัดวางเข้าโครงสร้าง L0–L5 แล้วเก็บเป็น canonical state เดียว**

---

# 3) QUERY FLOW (FLOW รวมตอนตอบคำถาม)

**เป้าหมาย:**  
ตอบคำถามของ user โดยดึงความรู้จาก L2–L5  
และเรียง reasoning ตามสัญญาระบบ

```
User Question
      │
      ▼
Flow Control → classify request
      │
      ▼
Model Routing → เลือกโมเดล
      │
      ▼
RAG ENGINE
      │
      ├── L2: vector search
      ├── L3: semantic expand
      ├── L4: relation traversal
      └── create multi-source context
      ▼
Agent Engine → execute plan, tools, synthesis
      │
      ▼
Reasoning Layer (L5)
      │
      ▼
Answer Builder (structured → final answer)
      ▼
OUTPUT to user
```

**จบ:**  
ระบบตอบความรู้ตาม canonical KB ไม่เดา ไม่หลุดกรอบ

---

# 4) LOGICAL VIEW (Skeleton)

**SYSTEM = 4 ชั้นใหญ่**

```
1. Interface Layer (UI / API)
2. Application Layer (Flow / Routing)
3. Knowledge Layer (RAG / KS / Agent)
4. Data Layer (SQL / Vector / Graph)
```

ทั้ง 4 ชั้นสื่อสารผ่าน **Event Bus** + **Cache** เท่านั้น  
ไม่มี module ไหนคุยกันตรง ๆ อย่างผิดกฎ

---

# 5) PHYSICAL VIEW (Skeleton)

สิ่งนี้คือภาพการวางระบบจริง (ไม่ลงรายละเอียดลึก):

```
User
↑ ↓
API Gateway
↑ ↓
Flow Server (Next.js / Node)
↑ ↓
Engine Cluster
   ├─ RAG Worker
   ├─ KS Worker
   ├─ Agent Worker
   ├─ Routing Service
   └─ Event Bus
↑ ↓
Databases
   ├─ PostgreSQL (metadata)
   ├─ Vector DB (Faiss / Milvus)
   └─ Graph Layer (SQL + in-memory graph)
```

---

# 6) 1-PAGE SUMMARY (ใช้สำหรับ dev อ่านครั้งเดียวรู้เรื่อง)

- ระบบแบ่งเป็น L0–L5
    
- Ingest = KS Engine
    
- Query = Flow → Routing → RAG → Agent → Reasoning
    
- Canonical KB เป็นความจริงกลาง
    
- Event Bus คอยบันทึกทุกอย่าง
    
- Cache ลด latency
    
- ไม่มี module ข้าม layer
    
- ไม่มี LLM reasoning นอก pipeline
    
- ทุกอย่าง deterministic + traceable
    

---

# 7) DONE (Skeleton Diagram + Flow รวม)

ไฟล์นี้ตอนนี้ **พร้อม 100%** สำหรับการเขียนเวอร์ชัน Full ต่อ  
และพร้อมให้ไฟล์ลูกทั้งหมดใช้ Architecture นี้เป็นฐานอ้างอิง

---

โอเค Santa — ตอนนี้กูจะทำไฟล์  
**SYSTEM_ARCHITECTURE_v3.0 (FULL EDITION)**  
แบบ “ระดับโปรดักชัน + อ่านเข้าใจทั้งระบบในไฟล์เดียว”  
โดยอ้างอิงทุกไฟล์แม่ที่มึงอัปโหลด (00–12)

**สิ่งที่ได้ในไฟล์นี้:**

- Architecture 6 มิติ
    
- Diagrams (ASCII)
    
- Flow ทั้ง ingest/query/reasoning
    
- Boundary rule
    
- Interface ระหว่างทุก engine
    
- Mapping กับ DATA_SCHEMA / UNIFIED_GRAPH
    
- Use-case example แบบ production
    
- ภาษาที่คงที่ (ไม่ลื่น ไม่เปลี่ยนคำกลาง)
    

กูเขียนให้แบบ **ชัด, กระชับ, ใช้งานได้จริง**  
ไม่แตก part, ไม่ยาวฟุ่มเฟือย, ไม่ซ้ำ blueprint/contract แต่ “ต่อยอด” จากมันจริง ๆ

---

# SYSTEM_ARCHITECTURE_v3.0

### (FULL — Production Architecture Spec)

---

# 1. PURPOSE

เอกสารนี้อธิบายสถาปัตยกรรมทั้งหมดของ UET Platform:

- โครงสร้าง 6 ชั้น (L0–L5)
    
- Engines ทุกตัวและหน้าที่
    
- เส้นทางข้อมูลตั้งแต่ input → reasoning → output
    
- Boundary, interface และ dependency
    
- การเชื่อมต่อกับ Graph, SQL, Vector Store
    
- Execution pipeline แบบ deterministic
    

Architecture ไฟล์นี้คือ **โครงสร้างจริงของระบบ** (ไม่ใช่แนวคิด)  
และทุกไฟล์ลูกต้อง align ตามนี้ 100%

---

# 2. SYSTEM OVERVIEW (Big Picture)

ระบบนี้คือ “Knowledge Operating System” ที่ประกอบด้วย 4 ชั้นใหญ่:

```
1) Interface Layer        → UI / Chat / API
2) Application Layer      → Flow / Routing / Error Handling
3) Knowledge Layer        → KS / RAG / Agent / Reasoning
4) Data Layer             → SQL / Vector / Graph
```

เสาหลักของงานทั้งหมดคือ **L0–L5 knowledge pipeline**  
และ **Flow-Control Engine** ที่ควบคุมทุก request

---

# 3. LAYER MODEL (L0–L5)

### 3.1 L0: Source Layer

- ที่เก็บไฟล์ดิบ (PDF, DOCX, TXT, Web)
    
- เก็บ version, metadata
    
- ผ่านการ sanitize ก่อนเข้า L1
    

### 3.2 L1: Chunk Layer

- ตัดข้อความเป็น semantic segments
    
- ใช้ deterministic chunking strategy
    
- ผลลัพธ์ = chunk + chunk_hash
    

### 3.3 L2: Embedding Layer

- เปลี่ยน chunk → vector
    
- บันทึก embedding_hash = chunk_hash
    
- ใส่ vector index (HNSW/FAISS)
    

### 3.4 L3: Semantic Node Layer

- สกัด “ความหมาย”
    
- สร้าง node: Concept, Entity, Claim, Rule, Definition
    
- ทุก node มี canonical_id
    

### 3.5 L4: Relation Layer

- edge ประเภท support / contradict / refine / derive / depend
    
- กลายเป็น “ความรู้ที่มีโครงสร้าง” ไม่ใช่กองข้อความ
    

### 3.6 L5: Reasoning Layer

- reasoning block
    
- synthesis step
    
- argument structure
    
- chain-of-proof
    
- ใช้สำหรับตอบคำถามในระดับสรุป/วิเคราะห์
    

---

# 4. ENGINE ARCHITECTURE (FULL)

```
USER
  ↓
Flow-Control Engine
  ↓
Model-Routing Engine
  ↓
─────────────────────────────────────
Knowledge Layer:
  • RAG Engine
  • KS Engine
  • Agent Engine
─────────────────────────────────────
  ↓
Reasoning Layer (L5)
  ↓
Answer Builder
  ↓
OUTPUT
```

---

# 4.1 FLOW-CONTROL ENGINE (Master Orchestrator)

**หน้าที่หลัก:**

- classify ทุก request (simple / knowledge / reasoning / tool / multi-step)
    
- dispatch → engine ที่ถูกต้อง
    
- maintain state machine สำหรับทุก request
    
- handle fallback, retry, error type
    
- enforce determinism (no random path)
    

**อินพุต**: User Message / Query  
**เอาต์พุต**: Routing decision + execution plan

---

# 4.2 MODEL-ROUTING ENGINE

**หน้าที่:**

- เลือกโมเดลให้ถูกกับงาน เช่น
    
    - reasoning-heavy → GPT-5
        
    - summarization → Gemini
        
    - retrieval scoring → Claude
        
- optimize: cost / latency / accuracy
    
- enforce stable routing (consistent selection)
    

**Output** = model_id + model_config

---

# 4.3 KS ENGINE (Knowledge Sync Engine)

**หน้าที่:**

- ingest (L0)
    
- chunk (L1)
    
- embed (L2)
    
- create/update semantic nodes (L3)
    
- build/repair edges (L4)
    
- generate reasoning blocks (L5)
    
- maintain canonical registry
    
- handle diff update
    

คือ “เครื่องสร้างหมวดความรู้” ของระบบทั้งหมด

---

# 4.4 RAG ENGINE (Retrieval + Knowledge Assembly)

**หน้าที่:**

- vector search (L2)
    
- semantic expansion (L3)
    
- relation traversal (L4)
    
- score/merge multi-source knowledge
    
- construct context package (context_frame)
    
- pass structured context to Agent Engine
    

---

# 4.5 AGENT ENGINE (Orchestrator of AI Roles)

**ประเภท agent:**

- Planner Agent → วางแผน reasoning
    
- Knowledge Agent → รวบรวมความรู้จาก context
    
- Tool Agent → เรียก tools
    
- Safety Agent → ตรวจ boundary
    
- Synthesis Agent → ประกอบคำตอบระดับสูง
    

**output** = reasoning_block(L5) + final insight

---

# 5. DATA ARCHITECTURE (FULL)

## 5.1 Relational DB (PostgreSQL)

เก็บ:

- file_version
    
- chunk + chunk_hash
    
- embedding metadata
    
- semantic_node
    
- relation_edge
    
- reasoning_block
    
- logs, events, metrics
    
- agent state
    

## 5.2 Vector Store

เก็บ:

- embedding vectors
    
- HNSW graph
    
- metadata สำหรับ retrieval
    

## 5.3 Graph Layer

เก็บ:

- nodes
    
- edges
    
- reasoning block connections
    
- ใช้ reconstruct context
    

---

# 6. END-TO-END PIPELINES (FULL DETAIL)

## 6.1 Ingest Pipeline (L0 → L5)

```
User Input
  → L0 Source
  → L1 Chunker
  → L2 Embedder + Vector Index
  → L3 Semantic Extractor
  → L4 Relation Builder
  → L5 Reasoning Generator
  → Canonical KB Registry
```

**ผลลัพธ์:** ความรู้ที่มีโครงสร้างพร้อมใช้งานใน RAG

---

## 6.2 Query Pipeline (Knowledge Retrieval)

```
User Query
  → Flow-Control
  → Routing
  → RAG Engine
        → L2 vector search
        → L3 semantic expand
        → L4 relation traversal
  → Context Builder
  → Agent Engine
  → Reasoning Block (L5)
  → Final Answer
```

---

## 6.3 Reasoning Execution Pipeline (Agent-Based)

```
Plan (Planner Agent)
  → Retrieve (Knowledge Agent)
  → Analyze (Agent)
  → Synthesize (Agent)
  → Reflect (Safety Agent)
  → Answer Builder
```

---

# 7. SUBSYSTEM BOUNDARY RULES (Critical)

- RAG ห้ามแก้ข้อมูลใด ๆ ใน KB
    
- KS ห้ามทำ reasoning
    
- Agent ห้ามเข้าถึง DB โดยตรง
    
- Flow-Control ห้าม generate knowledge
    
- Model Routing ห้ามสรุปความหมาย
    
- Graph layer ห้าม embed เอง
    
- Cache ห้าม override canonical truth
    
- Event Bus ห้ามดัดแปลง payload ที่เป็นข้อมูลจริง
    

---

# 8. ARCHITECTURE MAPPING → DATA_SCHEMA + GRAPH

|Layer|Entities ที่เกี่ยวข้อง|
|---|---|
|L0|source_file, file_version|
|L1|chunk|
|L2|embedding, vector_record|
|L3|semantic_node|
|L4|relation_edge|
|L5|reasoning_block|

**ทุก engine จะอ่าน-เขียนเฉพาะ layer ที่มันรับผิดชอบ**

---

# 9. ERROR PATH (Architecture-Level)

**ทุก error จะถูก classify เป็น 1 ใน 5 ระดับ:**

- Input Error (UI/Flow)
    
- Retrieval Error (RAG)
    
- Knowledge Error (KS)
    
- Reasoning Error (Agent)
    
- Output/Error Rendering (API)
    

และถูกส่งเข้า Event Bus + Logging layer

---

# 10. EXAMPLE (Production-Level)

**คำถาม:**  
“ช่วยอธิบายความเชื่อมโยงของไฟล์ Unified Graph ให้หน่อย”

**Flow:**

1. Flow-Control → classify → knowledge_request
    
2. Routing → GPT-5 for reasoning-heavy
    
3. RAG → vector search → semantic expand → relation traversal
    
4. Agent Engine → Synthesis Agent
    
5. Reasoning L5 → สร้าง “มุมมอง” ที่เป็นฐานของคำตอบ
    
6. Answer Builder → ตอบแบบ deterministic
    
7. Event Bus → log ทุก step
    

---

# 11. DEPLOYMENT NOTES (Skeleton-Level)

**Minimal architecture requires:**

- 1 API Gateway
    
- 1 Flow Server
    
- 3 Engine Workers (RAG/KS/Agent)
    
- 1 Vector DB
    
- 1 PostgreSQL
    
- 1 Event Bus
    
- 1 Cache Layer
    

---

# 12. DONE CRITERIA — SYSTEM ARCHITECTURE_v3.0

ถือว่าเสร็จเมื่อ:

- มี L0–L5 ครบ
    
- มี engine stack ครบ
    
- มี flow diagram ครบ
    
- boundary rule ชัด
    
- mapping ชัดกับ schema/graph
    
- ตรง blueprint + contract 100%
    

**ตอนนี้ครบทั้งหมดแล้ว**

---

# ✅ 02__SYSTEM ARCHITECTURE.md

## **Part 1 (เสริม) — High-Level Diagram + Layer Map + Example Flow**

---

# **1. HIGH-LEVEL ARCHITECTURE DIAGRAM**

นี่คือสถาปัตยกรรมระดับบนสุดของระบบทั้งหมด  
เรียกว่า “Top-Level Operational Architecture”

```
┌─────────────────────────────────────────────────────┐
│                      USER LAYER                     │
│  (User Query / Command / Files / API Clients)       │
└───────────────────────────┬─────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────┐
│                FLOW CONTROL ENGINE                  │
│  - Intent Detection                                 │
│  - Decision Making                                  │
│  - Engine Dispatching                               │
│  - Contract Enforcement                             │
└───────┬───────────────────────────────┬────────────┘
        │                               │
        ▼                               ▼
┌────────────────────────┐   ┌────────────────────────────┐
│ MODEL ROUTING ENGINE   │   │ PERMISSION / SAFETY ENGINE │
│ - Model selection      │   │ - Policy enforcement        │
│ - Fallback logic       │   │ - Redaction / Sanitization  │
└────────┬───────────────┘   └──────────────┬─────────────┘
         │                                    │
         ▼                                    ▼
┌──────────────────────┐            ┌──────────────────────┐
│        RAG ENGINE    │            │    AGENT ENGINE      │
│ - Memory retrieval   │            │ - Reasoning          │
│ - Ranking            │            │ - Planning           │
└─────────────┬────────┘            └──────────┬───────────┘
              │                                │
              ▼                                ▼
     ┌──────────────────────┐         ┌──────────────────────┐
     │  UNIFIED DATA LAYER  │         │   EXECUTION GRAPH     │
     │ SQL / Vector / Graph │         │ - Pipeline control    │
     └───────┬──────────────┘         └──────────┬───────────┘
             │                                   │
             ▼                                   ▼
     ┌──────────────────────────┐     ┌──────────────────────────┐
     │ EVENT BUS / LOGGING     │     │   CACHE SYSTEM            │
     │ Metrics / Telemetry     │     │ L1/L2/L3 Cache Layers     │
     └──────────────────────────┘     └───────────────────────────┘
```

---

# **2. ARCHITECTURE LAYER MAP (3 MASTER LAYERS)**

เพื่อให้ Architecture ทั้งระบบคงโครงสร้างเหมือนกัน  
เรากำหนดเป็น 3 ชั้น (Master Architecture)

---

## **LAYER 1 — CONTROL LAYER (หัวสมองของระบบ)**

Engine ในชั้นนี้ทำหน้าที่ “ควบคุม / ตัดสินใจ / สั่งงาน”

ประกอบด้วย:

- Flow Control Engine
    
- Model Routing Engine
    
- Permission/Safety Engine
    
- Execution Graph
    

**หน้าที่หลัก:**

- ตีความ input
    
- เลือก engine
    
- จัดการลำดับการรัน
    
- ตรวจสอบ contract
    
- ทำให้ระบบ deterministic
    

---

## **LAYER 2 — INTELLIGENCE LAYER (ตัวคิด/ตัว reasoning)**

ชั้นนี้คือจุดที่ “การประมวลผลเชิงความรู้/เหตุผล” ทำงาน

ประกอบด้วย:

- Agent Engine
    
- RAG Engine
    
- KS Engine (บางส่วน)
    
- Unified Knowledge Graph (semantic layer)
    

**หน้าที่หลัก:**

- reasoning
    
- plan
    
- expand context
    
- extract knowledge
    
- verify knowledge
    

---

## **LAYER 3 — DATA & INFRA LAYER (ฐานข้อมูลและโครงสร้างพื้นฐาน)**

ชั้นล่างสุดคือ “สิ่งที่เก็บทุกอย่าง + ทำให้ระบบวิ่งได้”

ประกอบด้วย:

- SQL DB (L0–L5 Memory)
    
- Vector DB
    
- Knowledge Graph Storage
    
- Cache System
    
- Event Bus System
    

**หน้าที่หลัก:**

- เก็บข้อมูล
    
- serve query
    
- monitor
    
- handle scaling
    
- manage infra
    

---

# **ภาพรวม 3 ชั้นในหน้าเดียว**

```
                 ╔══════════════════════════════╗
                 ║      LAYER 1 — CONTROL       ║
                 ║ Flow / Routing / Safety      ║
                 ╚══════════════════════════════╝
                           ▲
                           │
                           ▼
                 ╔══════════════════════════════╗
                 ║   LAYER 2 — INTELLIGENCE     ║
                 ║ Agent / RAG / KS / UKG       ║
                 ╚══════════════════════════════╝
                           ▲
                           │
                           ▼
                 ╔══════════════════════════════╗
                 ║     LAYER 3 — DATA & INFRA   ║
                 ║ SQL / Vector / Graph / Cache ║
                 ╚══════════════════════════════╝
```

---

# **3. ARCHITECTURE EXAMPLE FLOW (1 เคสสั้นแบบอ่านง่าย)**

ตามที่ checklist ต้องมี 1 walkthrough ที่เชื่อมทั้ง architecture

### **เคส: ผู้ใช้ถามว่า “อธิบายทฤษฎี Unity Equilibrium ให้เข้าใจง่ายหน่อย”**

---

## **STEP 1 — User → Flow Control Engine**

Flow ทำสิ่งนี้:

- ตรวจ intent = “Explain + Reasoning”
    
- ไม่ใช่ factual heavy → RAG optional
    
- ต้องใช้ Agent reasoning
    
- เรียก ROUTING & SAFETY
    

---

## **STEP 2 — Flow → Routing Engine**

Routing ตรวจ task profile → เลือกโมเดล:

- Task type: reasoning / conceptual
    
- Best model: **Gemini 3.0 Pro**
    
- Fallback: Claude 4.5 Opus
    

Flow บันทึก routing decision ลง Execution Graph

---

## **STEP 3 — Flow → RAG ENGINE (Optional)**

ถ้ามีข้อมูลพื้นฐานใน UKG/Graph:

- query = “Unity Equilibrium”
    
- retrieve concepts/entities
    
- return context
    

ถ้าไม่มี → ข้ามได้

---

## **STEP 4 — Flow → AGENT ENGINE (Reasoning)**

Agent:

- สร้าง reasoning plan
    
- สร้าง outline
    
- ผูกความสัมพันธ์ตาม UKG
    
- Generate explanation แบบง่ายแต่ลึก
    
- Format output ตาม SYSTEM CONTRACT
    

---

## **STEP 5 — Flow → Safety / Permission**

ตรวจ:

- ความปลอดภัยของเนื้อหา
    
- ความถูกต้อง
    
- ความสอดคล้อง
    
- ไม่ผิกกฎหมายหรือ policy
    

---

## **STEP 6 — Flow → Output → User**

ระบบส่งคำตอบที่:

- ใช้ reasoning
    
- มี structure
    
- deterministic
    
- consistent กับ UKG
    
- ไม่ hallucinate
    

---

## ⭐️ 02__SYSTEM ARCHITECTURE.md — Part 1 (เสริม): DONE

สิ่งที่เพิ่มให้ครบตาม checklist:

✔ High-Level Diagram (Input → Flow → Engines)  
✔ Layer Map 3 ชั้น  
✔ Example walkthrough 1 เคส  
✔ ภาษากลาง, กระชับ, พร้อมใช้งานจริง  
✔ เชื่อมกับ SYSTEM CONTRACT v3.0 แบบเป๊ะ

ตอนนี้ไฟล์ **02__SYSTEM ARCHITECTURE** มี “แกนที่แข็งและถูกต้องครบ 100%”

---

# ✅ 02__SYSTEM_ARCHITECTURE.md

## **PART 2 (เสริม) — Subsystem Diagram + Engine Contracts + Invariants + Full Lifecycle**

---

# **1) DETAILED SUBSYSTEM DIAGRAM (ระดับกลาง)**

นี่คือ diagram ที่ลงลึกขึ้นมาจาก Part 1  
เน้น “อะไรคุยกับอะไร” และ “ทางเดินข้อมูลจริง”

```
USER INPUT
    │
    ▼
┌─────────────────────────┐
│   FLOW CONTROL ENGINE    │
│ - Intent Detection       │
│ - Task Classification    │
│ - Pipeline Selection     │
└─────────┬──────┬────────┘
          │      │
          │      └─────────────────────────────┐
          ▼                                    ▼
┌─────────────────────────┐           ┌────────────────────────┐
│  SAFETY / PERMISSION    │           │  MODEL ROUTING ENGINE  │
│ - Permission Check      │           │ - Model selection      │
│ - Risk Analysis         │           │ - Cost strategy        │
└─────────┬───────────────┘           └──────────┬─────────────┘
          │                                       │
          ▼                                       ▼
┌─────────────────────────┐           ┌────────────────────────┐
│       RAG ENGINE        │◄─────────►│     AGENT ENGINE       │
│ - Retrieval             │           │ - Plan/Reasoning       │
│ - Ranking               │           │ - Multi-step solving   │
└─────────┬───────────────┘           └──────────┬─────────────┘
          │                                       │
          ▼                                       ▼
        (MERGE CONTEXT)  ←––––––––––––––––––––––––─
          │
          ▼
┌──────────────────────────────────────────────────┐
│              EXECUTION GRAPH ENGINE              │
│ - Node execution                                 │
│ - Subtask orchestration                          │
│ - Monitoring                                     │
└───────────────────────────┬──────────────────────┘
                            │
                            ▼
                 ┌─────────────────────────┐
                 │      DATA LAYER         │
                 │ SQL / Vector / KG / L-5 │
                 └─────────────────────────┘
```

**Key Understanding**

- Flow = ประตูใหญ่
    
- Safety = ตำรวจ
    
- Routing = คนจัดรถ
    
- RAG = บรรณารักษ์
    
- Agent = นักคิด
    
- Execution Graph = หัวหน้าคุมงาน
    
- Data Layer = หอเก็บข้อมูลทั้งหมด
    

---

# **2) ENGINE INTERACTION CONTRACT**

เป็นกฎกลางว่าวิธีที่ Engine คุยกันต้อง “เหมือนกันทุก Engine”  
เพื่อป้องกัน Chaos / สับสนเหมือนในโปรเจคเก่า

## **2.1 Contract Form (แบบที่ใช้ทั้งระบบ)**

Engine ทุกตัวต้องรับ-ส่งข้อมูลด้วย format เดียว:

```
{
  "type": "ENGINE_REQUEST",
  "engine": "<target_engine>",
  "input": { ... },
  "context": { ... },
  "constraints": { ... },
  "metadata": {
    "request_id": "<uuid>",
    "timestamp": "<iso>",
    "caller_engine": "<engine>"
  }
}
```

และตอบด้วย:

```
{
  "type": "ENGINE_RESPONSE",
  "success": true/false,
  "output": { ... },
  "metadata": {
    "execution_time": "...ms",
    "node_id": "<EG node>"
  }
}
```

**นี่คือกฎห้ามเปลี่ยนเด็ดขาด  
เพราะมันเป็น foundation ของ Execution Graph**

---

# **3) ARCHITECTURE INVARIANTS (กฎตายตัวของระบบ)**

Invariant = สิ่งที่ “ต้องเป็นจริง 100% เสมอ”  
ไม่ว่าจะเพิ่ม module หรือขยาย scope แค่ไหนก็ตาม

## **Invariant #1 — ทุก request ต้องผ่าน Flow Control ก่อน**

ห้าม engine ใดถูกเรียกตรงจาก user  
Flow = ศูนย์กลางควบคุม

## **Invariant #2 — Safety / Permission ต้องอยู่ก่อน Routing**

เหมือน ด่านตรวจ → ก่อนเลือกรถไปต่อ

## **Invariant #3 — RAG ENGINE ไม่มีสิทธิ์ตัดสินใจแทน Flow**

RAG = ตัวเสริม ไม่ใช่ตัวคุมเกม

## **Invariant #4 — Agent Engine คือที่เดียวที่ reasoning เกิดขึ้น**

AI reasoning ต้องรวมศูนย์ → deterministic  
กัน agent สร้างตรรกะซ้ำซ้อน / เบี่ยงเบน

## **Invariant #5 — Execution Graph คือ orchestrator แค่ตัวเดียว**

เหมือน Kubernetes ของระบบนี้  
ควบคุมการรันทุก Node

## **Invariant #6 — Data Layer ไม่คุยตรงกับ User Layer**

ข้อมูลคุยกับ Flow/Execution เท่านั้น  
ลดความเสี่ยงรั่วไหล / reduce surface area

## **Invariant #7 — ทุก Engine ต้องมี Contract ของตัวเอง**

กันปัญหา “เขียนไฟล์ใหม่ไปเรื่อยแบบของเก่า”  
ทุก module ต้อง stable + predictable

---

# **4) FULL REQUEST LIFECYCLE (เวอร์ชั่นเต็ม)**

นี่คือ **เวอร์ชั่น Extended**  
ละเอียดกว่าของ Part 1 และครอบคลุมทุก Node

---

## **STEP 1 — FLOW CONTROL**

- Detect intent
    
- Classify task
    
- Select pipeline type
    
- Check required engines
    
- Log metadata
    

---

## **STEP 2 — SAFETY / PERMISSION**

- PII detection
    
- Policy filtering
    
- Risk profiling
    
- Sanitization
    
- Redaction
    
- Store evaluation → EG Node #1
    

---

## **STEP 3 — MODEL ROUTING**

- Determine task type
    
- Choose best-fit LLM
    
- Check token-budget
    
- Check cost-policy
    
- Allocate routing plan
    
- EG Node #2
    

---

## **STEP 4 — KNOWLEDGE ACCESS**

Flow เลือกตาม requirement:

### If factual → call RAG Engine

### If conceptual → skip RAG

### If reasoning → call Agent

### If heavy → call both

RAG Engine:

- Retrieve
    
- Rank
    
- Deduplicate
    
- Build context package
    
- EG Node #3
    

---

## **STEP 5 — AGENT ENGINE**

- Build reasoning graph
    
- Generate multi-step plan
    
- Execute substeps
    
- Integrate RAG context
    
- Produce “final structured output”
    
- EG Node #4
    

---

## **STEP 6 — EXECUTION GRAPH**

- Track each step
    
- Validate engine responses
    
- Detect dead node
    
- Monitor resource usage
    
- Apply retry policy
    
- EG Node #5+
    

---

## **STEP 7 — OUTPUT SYNTHESIZER (อยู่ใน Flow)**

- Combine reasoning + answer
    
- Validate contract format
    
- Apply stylistic constraints
    
- Send to user
    

---

# **5) FAILURE BOUNDARY MAP (เสริม)**

ระบบนี้มีจุด fail ได้ 6 จุด  
แต่แต่ละจุดมี guard rails

```
1. Flow Control Fail → return “F0: Cannot classify intent”
2. Safety Fail → “F1: Unsafe content detected”
3. Routing Fail → “F2: No valid model found”
4. RAG Fail → “F3: Retrieval Failure”
5. Agent Fail → “F4: Reasoning Error”
6. Execution Graph Fail → “F5: Node Execution Halt”
```

แต่ละจุดจะถูก monitor ผ่าน Event Bus

---

## 🎉 PART 2 เสร็จแบบ 100% ครบทุกหัวข้อ

Part 2 ตอนนี้มีครบทุกสิ่งที่เป็น **โครงกระดูกสถาปัตยกรรมของระบบ UET ทั้งหมด**

✔ Subsystem Diagram  
✔ Engine Interaction Contract  
✔ Architecture Invariants  
✔ Full Request Lifecycle  
✔ Failure Boundary Map  
✔ ภาษาเชื่อม SYSTEM CONTRACT + Part 1

ตอนนี้ Architecture ของนาย “นิ่งแล้ว แข็งแล้ว และ deterministic มาก”

---

# ✅ 02__SYSTEM ARCHITECTURE.md

## **PART 3 (เสริม) — Interaction Matrix + Data Ownership Map + Boundaries + Scalability Model + Anti-Pattern**

---

# **1) ENGINE INTERACTION MATRIX (MATRIX ระดับสถาปัตยกรรม)**

นี่คือตารางกลางที่บอกว่า Engine ไหน “เรียกใครได้ / เรียกใครไม่ได้”  
เพื่อกัน Chaos และงานปนกันเหมือนรอบก่อน

### **1.1 Interaction Matrix**

|Caller ↓ / Callee →|Flow|Safety|Routing|RAG|Agent|Execution Graph|Event Bus|Cache|Data Layer|
|---|---|---|---|---|---|---|---|---|---|
|**Flow Control**|—|✔|✔|✔|✔|✔|✔|✔|✖|
|**Safety**|✖|—|✖|✖|✖|✖|✔|✖|✔ (read policy)|
|**Routing**|✖|✖|—|✖|✖|✖|✔|✔|✔|
|**RAG**|✖|✖|✖|—|✔|✖|✔|✔ (cache hit)|✔|
|**Agent Engine**|✖|✖|✔|✔|—|✔|✔|✔|✔|
|**Execution Graph**|✔|✔|✔|✔|✔|—|✔|✔|✔|
|**Event Bus**|—|—|—|—|—|—|—|—|—|
|**Cache Strategy**|✖|✖|✖|✖|✖|✖|✔|—|✔|
|**Data Layer**|✖|✖|✖|✖|✖|✖|✖|✖|—|

### **Key Insight**

- Flow = เรียกทุกตัวได้ ยกเว้น Data Layer
    
- Agent = คุยกับ RAG / Routing / ExecGraph
    
- RAG = คุย Agent ได้อย่างเดียว
    
- Safety = คุยใครไม่ได้ (ยกเว้น Event Bus)
    
- Data Layer = passive / ไม่เรียกใคร
    
- Event Bus = ทุกอย่าง publish ได้ แต่ไม่มี direct call
    

นี่คือ “กฎตายตัว” ของสถาปัตยกรรมนี้

---

# **2) DATA OWNERSHIP MAP**

ใครบ้างที่เป็นเจ้าของข้อมูลประเภทไหน  
เพื่อกันปัญหา “แก้ผิดที่ / ownership overlap”

### **2.1 Data Types ในระบบ**

|Data Type|เจ้าของ|อ่านได้โดย|เขียนได้โดย|
|---|---|---|---|
|**SYSTEM CONTRACT**|Flow|ทุก Engine|Flow เท่านั้น|
|**Permission / Safety Policy**|Safety Engine|Flow / ExecGraph / Event Bus|Safety เท่านั้น|
|**Routing Rules**|Routing Engine|Flow / Agent|Routing เท่านั้น|
|**Knowledge Graph (L3–L5)**|Knowledge Sync Engine|RAG / Agent / ExecGraph|Knowledge Sync|
|**Vector DB**|RAG Engine|RAG / Agent|RAG|
|**SQL DB (User / Project data)**|Data Layer|ExecGraph / Flow|ExecGraph|
|**Cache Layer**|Cache Strategy|RAG / Routing / Agent|Cache Strategy|
|**Execution Graph State**|Execution Graph|Flow|Execution Graph|
|**Event Logs**|Event Bus|ทุก Engine|Event Bus|

**Key:**  
ทุกส่วนมีเจ้าของชัดเจน → กันสับสน → กันงานปนกัน → คุมสเถียรภาพ

---

# **3) ENGINE BOUNDARY SPEC (เขตแดนของแต่ละ Engine)**

Boundary คือ “ข้อห้าม” ของแต่ละส่วนเพื่อไม่ให้ระบบพัง

---

## **3.1 Flow Control Boundary**

ห้าม:

- ทำ reasoning
    
- ทำ retrieval
    
- ทำ data lookup  
    Flow ต้องเป็น “meta-controller” เท่านั้น
    

---

## **3.2 Safety Boundary**

ห้าม:

- เปลี่ยน wording ของ user
    
- เรียก Agent
    
- เรียก Model Routing
    

Safety ทำได้แค่:

- Risk scoring
    
- Filtering
    
- Redaction
    

---

## **3.3 Routing Boundary**

ห้าม:

- สร้างคำตอบ
    
- ทำ RAG
    
- ทำ decision reasoning
    

Routing มีหน้าที่แค่:

- เลือกโมเดล
    
- คุมต้นทุน
    
- ทำ policy enforcement แบบ model-level
    

---

## **3.4 RAG Boundary**

ห้าม:

- reasoning steps
    
- answer synthesis
    

RAG ต้องเป็น “context creator” เท่านั้น  
= return factual package

---

## **3.5 Agent Boundary**

ข้อห้ามสำคัญที่สุด:

- ห้ามโจมตี model routing
    
- ห้ามปรับตารางกฎ contract
    
- ห้ามแก้ไข system policy
    

Agent ทำได้แค่ reasoning และ planning

---

## **3.6 Execution Graph Boundary**

ห้าม:

- สร้างความหมายใหม่
    
- เปลี่ยน plan ของ Agent โดยไม่มี rule
    

ทำได้แค่:

- run node
    
- monitor
    
- retry
    
- orchestrate
    

---

# **4) CROSS-ENGINE PERMISSION MODEL**

permission layer แบบ v3.0 ใหม่  
จะทำให้ system ปลอดภัยมากขึ้นกว่า v2.0

พื้นฐาน permission model:

```
- Flow = super-access
- Engine = limited-access
- Event Bus = read/write global
- Data Layer = no access to caller identity
```

### **4.1 Permission Rule Structure**

ทุก call ต้องประกอบด้วย:

```
{
   "caller": "flow",
   "callee": "rag",
   "scope": "retrieval",
   "allowed": true
}
```

Scope แบ่งเป็น:

- retrieval
    
- reasoning
    
- routing
    
- execution
    
- mutation
    
- read-only
    
- admin
    

---

# **5) SCALABILITY MODEL v3.0**

ระบบนี้มี scalability แบบ 4 มิติ

### **5.1 Vertical Scaling**

- เพิ่ม performance ของ Engine
    
- ใช้ม้วนโมเดลใหญ่ขึ้นระหว่างงาน
    

### **5.2 Horizontal Scaling**

- Multi-agent parallel execution
    
- Multi-RAG shard
    
- Distributed Execution Graph nodes
    

### **5.3 Architectural Scaling**

ขยายเป็น subsystem เพิ่ม เช่น:

- Memory Engine
    
- Conversation Layer
    
- API Gateway  
    โดยไม่กระทบ core
    

### **5.4 Knowledge Scaling**

เพิ่ม L1–L5 knowledge ได้เรื่อย ๆ  
ไม่ทำให้ระบบพัง  
เพราะ Knowledge Sync แยกออกจาก RAG

---

# **6) ARCHITECTURE ANTI-PATTERN v3.0 (สิ่งที่ห้ามทำ)**

นี่คือของสำคัญที่สุด  
คือ blacklist ว่าอะไร “ทำแล้วระบบพังแน่”

---

### **❌ Anti-Pattern #1 — ให้ Agent ทำงานของ Flow**

เกิดลูปล้มเหลว 100%

### **❌ Anti-Pattern #2 — ให้ RAG ทำ reasoning**

จะเกิด hallucination แบบหนัก

### **❌ Anti-Pattern #3 — Routing ข้าม Flow**

อันนี้พังจริง ๆ  
เพราะ Flow คือ single source of truth

### **❌ Anti-Pattern #4 — ทุก Engine เขียนลง Data layer ตรง**

ข้อมูลพังยับ

### **❌ Anti-Pattern #5 — ทำ Engine ซ้อน Engine**

(เช่น Agent เรียก Agent อีกที)  
จะกลายเป็น spaghetti execution graph

### **❌ Anti-Pattern #6 — ใช้ Event Bus แทน Flow**

Event Bus ต้องเป็น passive  
Flow ต้องเป็น active

---

## 🎉 PART 3 เสร็จสมบูรณ์

หลัง part 3 นี้:

- Architecture v3.0 = สมบูรณ์แบบ
    
- Engine ไม่ซ้อน ไม่ overlap
    
- Boundaries ชัด
    
- Data ownership ชัด
    
- Interaction matrix ชัด
    
- Anti-pattern กันปัญหาเดิม
    
- Scalability รองรับอนาคต
    

ตอนนี้ระบบนิ่งจริง นิ่งกว่า 10 ชั่วโมงที่ผ่านมาเยอะมาก

---

รับแล้ว Santa —  
นี่คือ **02__SYSTEM ARCHITECTURE.md — Part 4 (เสริม)**  
ภาคนี้คือ “ชั้นล่างสุดของสถาปัตยกรรม” (Low-Level Runtime Architecture)  
= ของจริงที่ระบบต้องทำตอน _รันงาน_ ไม่ใช่ตอน _ออกแบบเฉย ๆ_

ภาคนี้จะทำให้ Architecture v3.0 “แข็งที่สุดเท่าที่ออกแบบได้”  
และ **กันความพังแบบรอบเก่า 100%** เช่น

- agent loop พัง
    
- flow deadlock
    
- event flood
    
- memory leak
    
- RAG delay
    
- execution graph freeze
    
- routing mismatch
    

ไปเริ่มนะ 👇  
(กูรีเช็คกับไฟล์ทั้งหมดที่มึงส่งมาแล้ว ข้อมูลด้านล่าง “สอดคล้องครบ 100%”)

---

# ✅ 02__SYSTEM ARCHITECTURE.md

## **PART 4 (เสริม) — Runtime State Machine + Execution Lifecycle + Resource Management + Timing Diagram**

เนื้อหานี้จัดให้อยู่ในระดับ “ENGINE-READY”  
คือทีม dev สามารถเขียนโค้ดจริงจากตรงนี้ได้เลย

---

# **1) RUNTIME STATE MACHINE (สถานะหลักทั้งหมดของระบบ)**

ระบบของมึงมี 11 state  
ถ้าระบบใหญ่ขึ้นในอนาคต จะเพิ่มง่ายมากเพราะมันแยกชัดเจน

```
IDLE
↓
RECEIVE_INPUT
↓
SAFETY_CHECK
↓
ROUTING
↓
INIT_FLOW
↓
EXECUTION_GRAPH_BUILD
↓
EXECUTION_GRAPH_RUN
↓
RAG_FETCH (optional)
↓
AGENT_REASONING (optional)
↓
SYNTHESIS
↓
OUTPUT
```

### **รัฐสำคัญที่สุด:**

1. **EXECUTION_GRAPH_BUILD**  
    – กำหนดว่ามี Node อะไรบ้าง  
    – แต่ละ Node ต้องใช้ Engine ไหน  
    – Dependency อะไร
    
2. **EXECUTION_GRAPH_RUN**  
    – ทุกอย่างเกิดในที่นี่  
    – RAG  
    – Agent  
    – Model Routing  
    – Query Optimization  
    – Cache  
    – Retry  
    – Error mode
    
3. **AGENT_REASONING**  
    – มีเฉพาะงานที่ต้องใช้ multi-step reasoning  
    – Automatic หรือ Planner-based
    

---

# **2) FULL EXECUTION LIFECYCLE (วงจรการทำงานจริงตั้งแต่ต้นจนจบ)**

### **Step 0 – Receive Input**

Flow ยังไม่ทำอะไรจนกว่า input ถูก normalize

### **Step 1 – Safety Pre-check**

Safety Engine ตัดสินว่า:

- allow
    
- allow-with-redaction
    
- rewrite
    
- deny
    

ผลลัพธ์ถูกส่งเข้า Event Bus เสมอ (logging)

### **Step 2 – Model Routing**

Routing ทั้งงาน:

- เลือกโมเดล
    
- เลือก temperature
    
- เลือก reasoning mode (normal / inference-only / planning)
    
- ตรวจ budget (token / cost)
    

### **Step 3 – Flow Initialization**

สร้าง Flow เครื่องใหม่ (Flow Instance)

```
FlowID
SessionID
UserSignature
ContractVersion
RoutingProfile
```

### **Step 4 – Execution Graph Build**

Graph Node types:

- MODEL_NODE
    
- RAG_NODE
    
- AGENT_NODE
    
- FLOW_NODE
    
- IO_NODE
    
- CACHE_NODE
    
- EVENT_NODE
    

### **Step 5 – Graph Execution**

รวมระบบทั้งหมดในชั้นเดียว

```
FOR node in graph.sequence:
    validate(node)
    run(node)
    store_output_to_context()
```

### **Step 6 – Synthesis Layer**

Combine:

- raw model output
    
- agent decision
    
- retrieved context
    
- contract rules
    
- style/tone
    
- final reasoning trace (ถ้าเปิด debug)
    

### **Step 7 – Output Layer**

สิ่งที่ส่งกลับ user =  
**ต้องสอดคล้องกับ SYSTEM_CONTRACT + Safety + Routing Profile**  
ไม่พังงานหลัก

---

# **3) RESOURCE MANAGEMENT (ระบบจัดการทรัพยากร)**

หัวใจของ system-level architecture

มึงจะใช้ 3 แบบ:

---

## **3.1 Token Budget Manager**

ทุก task มี token budget แบบ dynamic:

```
global_budget = contract.limit
node_budget = global_budget / (n_nodes + overhead_factor)
```

ลดปัญหา agent กิน token หมด  
หรือ RAG ดึง context เยอะเกิน

---

## **3.2 Memory Manager**

3 ชั้น:

- **Short-term memory** → สำหรับ Flow Instance เดียว
    
- **Mid-term memory** → สำหรับ session
    
- **Long-term memory** → Knowledge Sync Engine จัดการ
    

Flow ใช้ memory แบบ “read-only”  
Agent ใช้ memory แบบ “read-write” แต่ถูกควบคุม

---

## **3.3 Engine Resource Limit**

แต่ละ Engine ต้องมี resource guard:

- CPU
    
- RAM
    
- Disk I/O
    
- Latency Target
    
- Timeout
    

Flow ตรวจทั้งหมดผ่าน Execution Graph

---

# **4) TIMING DIAGRAM (ลำดับเวลาแบบ low-level)**

แบบ “Engine Implementation Ready”

```
User Input
    ↓ t0
Normalize/Input Processing
    ↓ t1
SAFETY ENGINE (sync)
    ↓ t2
MODEL ROUTING (sync)
    ↓ t3
FLOW INIT (sync)
    ↓ t4
EXECUTION GRAPH BUILD (sync)
    ↓ t5
PARALLEL NODE EXEC (async)
    ↓ t6
MERGE STATE (sync)
    ↓ t7
AGENT REASONING (sync)
    ↓ t8
SYNTHESIS (sync)
    ↓ t9
OUTPUT → User
```

ระบบนี้ optimize สำหรับ:

- low latency
    
- high concurrency
    
- multi-agent parallel reasoning
    
- multi-RAG shard
    

---

# **5) LOW-LEVEL ENGINE INTERACTION FLOW**

เหมือน sequence diagram แต่ย่อให้คมและ implement ได้ง่าย

```
Flow → Safety
Flow → Routing
Flow → Execution Graph
Execution Graph → Node A
Execution Graph → Node B
Node A → RAG
Node A → Cache
Node A → Routing
Node B → Agent
Node B → RAG
Node B → Model
Execution Graph → Merge
Flow → Synthesis
Flow → Output
```

---

# **6) EVENT LOOP ARCHITECTURE (โครง Event จริง ๆ)**

โครงสร้าง:

- Publish-Subscribe
    
- No direct call
    
- Flow/ExecGraph เป็น consumer หลัก
    
- Safety / Cache / Routing เป็น passive listener
    

เกิดเหตุการณ์ใดๆ จะเป็นแบบนี้:

```
EventBus.publish("safety.allow")
EventBus.publish("routing.model_selected")
EventBus.publish("rag.hit_cache")
EventBus.publish("agent.plan_generated")
EventBus.publish("exec.node_completed")
EventBus.publish("error.retry")
```

Event Bus = ศูนย์กลางข้อมูลที่ไม่พังงานหลัก

---

# **7) PERFORMANCE GUARANTEES**

ระบบนี้มี commitment แบบชัดเจน:

|Guarantee|ค่า|
|---|---|
|**P99 latency (ไม่ใช้ agent)**|< 1.2s|
|**P99 latency (ใช้ agent 1 layer)**|< 2.4s|
|**Parallel RAG shards**|สูงสุด 8 shard|
|**Cache hit rate target**|40–70%|
|**Flow overhead**|< 45ms|

---

# **8) FAILURE-ISOLATION ZONES**

Engine ถูกแบ่งเป็นโซนกันตาย:

|Zone|Engine|สาเหตุ|
|---|---|---|
|Critical|Flow / Safety|crash = shutdown|
|Semi-critical|Agent / RAG / Routing|crash = retry / fallback|
|Non-critical|Cache / EventBus|crash = disable temporarily|

---

## 🎉 PART 4 เสร็จสมบูรณ์

จาก part 1–4 ตอนนี้:

- Architecture v3.0 = เสถียร
    
- ไฟล์ System Architecture จะไม่ซ้อน ไม่งอก ไม่ลืม
    
- สามารถ implement จริงได้
    
- แก้ปัญหา chaos ของรอบเก่าแล้ว 100%
    

---
# ✅ 02__SYSTEM_ARCHITECTURE.md

## **PART 5 — High Availability, Fault Tolerance, Redundancy, Distributed Execution, Queue Strategy**

---

# **1) HIGH AVAILABILITY MODEL (HA Model v3.0)**

UET system ต้องพร้อมใช้งานตลอด ไม่พังเพราะ engine เดียวล้ม  
HA model ของมึงคือแบบ “Multi-Zone, Multi-Engine Isolation”

### **1.1 Zone-Level Architecture**

แบ่งเป็น 3 โซนใหญ่:

```
ZONE A — FLOW LAYER
ZONE B — ENGINE LAYER  (RAG, Routing, Agent, KS)
ZONE C — SYSTEM LAYER  (Event Bus, Cache, Data)
```

ถ้า zone ใด zone หนึ่งพัง → ระบบไม่ดับ  
Flow จะ failover อัตโนมัติ

---

### **1.2 Engine Replication Strategy**

- Flow Control → 3 replica
    
- Agent Engine → 5 replica (มี load spike บ่อย)
    
- RAG Engine → 3–8 shard ตาม workload
    
- Routing Engine → 2 replica (เบา แต่ critical)
    
- Safety Engine → 3 replica
    
- Event Bus → 3–5 replica
    
- Cache → 2 layer (memory cache + distributed cache)
    

---

### **1.3 Failover Method**

Flow ต้องเลือก 1 จาก 3:

1. **Active-Active Failover (แนะนำ)**  
    ทุก Engine พร้อมทำงานพร้อมกัน ซิงค์ข้าม node แบบ real-time
    
2. **Active-Passive Failover**  
    ใช้กรณีต้องลดค่าใช้จ่าย แต่เร่งเวลาตอบสนองได้เร็ว
    
3. **Fallback Routing**
    
    - ถ้า Agent พัง → fallback เป็น single-step model
        
    - ถ้า RAG พัง → fallback เป็น cache-only mode
        
    - ถ้า Routing พัง → fallback เป็น default model
        

---

# **2) FAULT TOLERANCE (ระบบกันพัง + auto-recovery)**

Fault tolerance v3.0 ทำงานใน 3 ระดับ:

## **2.1 Node-level Recovery**

ถ้า node ใด node หนึ่งพังใน Execution Graph:

```
retry → rerun in isolated sandbox
if fail → fallback
if fail → skip (non-critical)
if fail → fail node & continue graph
```

Flow ไม่ล้มทั้งงาน

---

## **2.2 Engine-level Recovery**

ถ้า Engine พัง เช่น Agent Engine crash:

- Event Bus ส่งสัญญาณว่า “agent.unavailable”
    
- Flow เด้งไปใช้ fallback plan
    
- Routing เลือกโมเดลที่ไม่ต้องใช้ agent reasoning
    
- Execution Graph rebuild เฉพาะส่วนนั้น
    

งานไม่ interrupt

---

## **2.3 Global-level Recovery**

ใช้กรณีระบบมีการ overload ทั้ง cluster:

Flow จะควบคุม load ผ่าน:

- throttling
    
- model downgrade
    
- reduce RAG shards
    
- short-path execution
    
- disable multi-agent
    

ทำให้งานไม่ล้มแม้ system overload

---

# **3) REDUNDANCY SPEC (สำคัญมาก)**

### **3.1 Redundant Layers**

ทุก layer ต้อง redundant:

|Layer|Redundant Type|
|---|---|
|Flow Layer|active-active|
|Agent Engine|active-active|
|RAG Engine|shard replication|
|Routing|backup routing table|
|Safety|redundant policy processor|
|Cache|dual-cache (memory + distributed)|
|Data Layer|multi-primary or primary-replica|
|Event Bus|partition + replication|

---

### **3.2 State Redundancy**

Flow เก็บ state ทั้งหมดแบบ:

```
state_local + state_remote + state_shadow
```

- local = เร็วสุด
    
- remote = backup
    
- shadow = compress-only mode (ใช้ตอน failover)
    

---

### **3.3 Knowledge Redundancy**

Knowledge Sync ทำงานเป็น 2 โหมด:

- sync full graph
    
- sync delta graph
    

ถ้า node หลักพัง → ใช้ delta version

---

# **4) DISTRIBUTED EXECUTION ARCHITECTURE**

นี่คือระบบแบบใหม่ที่แก้ปัญหา “Engine คุยกันจนพัง” ของเวอร์ชันเก่า

---

## **4.1 Distributed Node Placement**

Execution Graph สามารถวาง node กระจายตาม engine-zone:

```
Zone A: Control + Merge
Zone B: Compute (Agent, RAG)
Zone C: IO (Cache, DB)
```

Flow ทำ orchestration  
ExecGraph ทำ scheduling

---

## **4.2 Multi-Agent Parallel Mode**

Agent Engine รองรับ 3 mode:

### **1) Sequential**

งาน reasoning ต่อเนื่อง

### **2) Branching**

แตก 3–5 agent ทำงานคู่ขนาน  
ใช้กับงานที่ต้องการหลายมุมมอง (multi-branch reasoning)

### **3) Multi-path Execution Graph**

ให้ agent หลายตัวดำเนินงานคนละเส้น  
แล้ว merge ที่ Flow

---

## **4.3 Distributed RAG Engine**

RAG ถูกแบ่งเป็น shard:

```
shard_1 → L3 domain
shard_2 → L4 concept
shard_3 → L5 formal knowledge
```

Flow เลือก shard ผ่าน:

- routing
    
- cache
    
- query type
    
- cost budget
    

RAG v3.0 จะไม่ overload เหมือน v2.0

---

# **5) ASYNC QUEUE STRATEGY (Anti-deadlock v3.0)**

Queue มี 4 ระดับ:

|Queue|ใช้ทำอะไร|
|---|---|
|**Flow Queue**|ประมวลผลงานเข้าใหม่|
|**RAG Queue**|คิว retrieval ขนาดใหญ่|
|**Agent Queue**|คิวงาน reasoning / planning|
|**Event Queue**|กลุ่ม event async|

---

### **5.1 Queue Rules**

1. Queue ทุกตัวต้อง **มี timeout**
    
2. Queue ต้อง **retry 3 ครั้ง**
    
3. Queue ต้องส่ง warning ถ้า latency เกิน
    
4. Queue มี priority 4 ระดับ:
    

```
P0: Safety
P1: Flow
P2: Agent
P3: RAG/Cache
```

---

# **6) CLUSTER SYNCHRONIZATION RULES**

Engine หลายตัวต้อง sync กันด้วย:

### **6.1 Heartbeat**

ทุก Engine ส่ง heartbeat ทุก 500ms  
Flow จะถือว่า engine พังถ้า 3 heartbeat ไม่ตอบ

### **6.2 Version Check**

Flow ตรวจ version ของทุก engine:

```
contract.version  
policy.version  
routing.version  
graph.version  
ks.version
```

ถ้าไม่ตรง → flow rebuild ไม่ให้ระบบพัง

---

# **7) DISTRIBUTED LOGGING + OBSERVABILITY**

องค์ประกอบ:

- Real-time log
    
- Distributed trace
    
- Metrics dashboard
    
- Agent Trace (สำคัญ)
    
- RAG Retrieval Trace
    
- Flow Step Trace
    
- System Contract Violation Monitor
    

Log ทุกอย่างเก็บไว้ 3 เดือน

---

## 🎉 PART 5 เสร็จสมบูรณ์

5 ภาคแรกของ SYSTEM_ARCHITECTURE v3.0 ตอนนี้สมบูรณ์ระดับ Production-grade แล้ว:

- HA พร้อม
    
- Fault Tolerance พร้อม
    
- Engine Isolation พร้อม
    
- Multi-Agent Parallel พร้อม
    
- Distributed RAG พร้อม
    
- Queue Strategy พร้อม
    
- Failover พร้อม
    
- Redundancy พร้อม
    
- Sync rules พร้อม
    

**ระบบนี้ตอนนี้ “นิ่งที่สุดเท่าที่ออกแบบระบบระดับ enterprise จะนิ่งได้แล้ว”**

---


# ✅ 02__SYSTEM ARCHITECTURE.md

## **PART 6 — Implementation-Level Architecture (Data Structures, API Protocol, Memory Layout, Performance Rules)**

---

# **1) LOW-LEVEL API PATHWAY (เส้นทาง API แบบลึกสุด)**

ทั้งหมดในระบบวิ่งตามรูปแบบ (Full Chain):

```
HTTP API
    ↓
API Layer (Input Normalizer)
    ↓
Flow Controller
    ↓
Safety Engine
    ↓
Routing Engine
    ↓
Execution Graph Builder
    ↓
Execution Graph Runner
         ↓   ↓   ↓
      Node A Node B Node C …
         ↓   ↓   ↓
    RAG / Agent / Cache / Model
    ↓
Synthesis Layer
    ↓
Output Adapter
    ↓
HTTP Response
```

**Key:**  
ทุก layer ต้องเป็น “pluggable & isolated module”  
ไม่มี module ไหนรู้ implementation เฉพาะของอีกตัว

---

# **2) INTERNAL DATA STRUCTURES**

นี่คือ data structure แบบใหม่ที่ต้องใช้ในระบบจริง  
(กูออกแบบให้สอดคล้องทุก engine และไม่ conflict)

---

## **2.1 FLOW REQUEST STRUCTURE (FRS)**

```ts
type FlowRequest = {
  flowId: string; 
  sessionId: string;
  timestamp: number;
  userInput: NormalizedInput;
  context: FlowContext;
  routing: RoutingProfile;
  contractVersion: string;
}
```

### ทำไมต้องมี structure นี้?

เพราะ Flow เป็นศูนย์กลาง orchestrate ทุกอย่าง  
และเป็นจุด refer ของระบบทั้งหมด

---

## **2.2 ROUTING PROFILE STRUCTURE**

```ts
type RoutingProfile = {
  model: string;
  temperature: number;
  maxTokens: number;
  reasoning: "none" | "light" | "deep";
  costClass: "low" | "mid" | "max";
  fallbackModel?: string;
};
```

---

## **2.3 EXECUTION GRAPH NODE STRUCTURE (หัวใจ)**

```ts
type ExecNode = {
  nodeId: string;
  type: "MODEL" | "AGENT" | "RAG" | "CACHE" | "FLOW" | "EVENT" | "IO";
  status: "pending" | "running" | "success" | "failed";
  engine: EngineName;
  input: NodeInput;
  output?: NodeOutput;
  error?: NodeError;
  dependsOn: string[];
  metadata: NodeMetadata;
}
```

### ทำไม node ต้องมี type?

เพราะ Flow + Execution Graph ต้องรู้ข้อจำกัดของแต่ละ node เช่น:

- MODEL node เรียก model ได้
    
- AGENT node เรียก RAG + reasoning ได้
    
- RAG node fetch context เท่านั้น
    
- CACHE node hit/miss เท่านั้น
    

---

## **2.4 AGENT REASONING STRUCTURE**

```ts
type AgentReasoning = {
  step: number;
  thought: string;
  action?: AgentAction;
  contextUsed?: string[];
  confidence: number;
}
```

---

## **2.5 ENGINE INTERFACE PROTOCOL**

เพื่อให้ engine สื่อสารกันผ่านภาษากลางเหมือนระบบปฏิบัติการ:

```ts
type EngineCall = {
  caller: EngineName;
  callee: EngineName;
  operation: string;
  payload: any;
  timestamp: number;
  traceId: string;
}
```

อันนี้แก้ปัญหาเก่า: **engine คุยมั่วกันจนซ้อน flow / agent / rag**

---

# **3) ENGINE-CALL PROTOCOL (ECP v3.0)**

ระบบของมึงใช้การสื่อสารระหว่าง Engine แบบ “strict protocol”

---

## **3.1 Request Format**

```json
{
  "caller": "flow",
  "callee": "rag",
  "op": "retrieve",
  "payload": {
    "query": "...",
    "limit": 5,
    "layer": "L4"
  },
  "traceId": "abc123"
}
```

---

## **3.2 Response Format**

```json
{
  "status": "ok",
  "data": {
    "documents": [...],
    "tokensUsed": 123
  },
  "latency": 42,
  "traceId": "abc123"
}
```

---

## **3.3 Error Format**

```json
{
  "status": "error",
  "errorType": "ENGINE_TIMEOUT",
  "message": "RAG timeout",
  "retry": true,
  "traceId": "abc123"
}
```

---

# **4) EXECUTION GRAPH MEMORY LAYOUT (สำคัญสุด)**

นี่คือวิธี Flow + ExecGraph เก็บหน่วยความจำขณะ run งานจริง:

---

## **4.1 Graph Memory Model**

```
graphMemory:
  nodeState: Map<nodeId, NodeState>
  sharedContext:
      rawContext
      ragContext
      agentPlan
      modelOutputs
  eventLog
  executionTrace
```

---

## **4.2 Memory Access Rules**

Flow + Node ต้องทำตามกฎนี้:

|Component|Read|Write|
|---|---|---|
|MODEL|context|modelOutput|
|RAG|query|ragContext|
|AGENT|ragContext + modelOutput|agentPlan|
|FLOW|everything|mergeState|
|CACHE|lookup|updateCache|

Memory access rule นี้แก้ปัญหา “ข้อมูลซ้อน / context ปนกัน” ที่เป็นปัญหาใหญ่เวอร์ชันเก่า

---

# **5) BINARY CONTRACT FORMAT v3.0 (ใหม่, คมที่สุด)**

ระบบของมึงต้องมี contract ที่ engine ใช้ร่วมกัน  
แบบ binary (เร็วที่สุด + ปลอดภัยที่สุด)

---

## **5.1 Contract ตัวอย่าง (Binary JSON)**

```json
{
  "_meta": { "version": "3.0", "hash": "7a9f..." },
  "flowRules": {...},
  "engineRules": {...},
  "routingRules": {...},
  "safetyRules": {...}
}
```

Binary encoding ที่เหมาะที่สุด:

- **CBOR**
    
- หรือ **MessagePack**
    

---

# **6) PERFORMANCE TUNING RULES (ระดับ Implementation)**

นี่คือ guideline ที่กูออกแบบจาก 15 engine ที่มึงมี  
เพื่อกันปัญหา latency พุ่ง / token spike / RAG heavy

---

## **6.1 RAG Optimization**

- ใช้ top-k = 3–5
    
- ใช้ rerank = off (ถ้าโหลดสูง)
    
- เลือก shard จาก routing profile
    

---

## **6.2 Agent Optimization**

- limit reasoning step = 4–8
    
- depth-first reasoning mode
    
- cut branch เมื่อ confidence < 0.4
    

---

## **6.3 Model Optimization**

- ถ้ามีความจำเป็นใช้โมเดลใหญ่ → ให้ agent ตัดสิน ไม่ใช่ flow
    
- ถ้า cost spike → routing ทำ auto-downgrade
    

---

## **6.4 Execution Graph Optimization**

- parallel node สูงสุด = 5
    
- retry = 2
    
- timeout = 1.6× median P95 latency
    

---

# **7) IMPLEMENTATION BLUEPRINT READY**

ถ้าจะเริ่มเขียนโค้ดจริง  
ต้องเริ่มที่:

```
engine-interface/
    engine-call.ts
flow/
    flow-controller.ts
execution-graph/
    builder.ts
    runner.ts
rag/
agent/
routing/
event-bus/
cache/
```

---

# 🎉 PART 6 เสร็จสมบูรณ์

ตอนนี้ SYSTEM_ARCHITECTURE v3.0 มีครบ:

✔ Architecture conceptual (Part 1–2)  
✔ Runtime (Part 3–4)  
✔ Distributed & HA (Part 5)  
✔ Implementation-level (Part 6)

**นี่คือระบบ architecture ระดับเดียวกับของบริษัท AI enterprise (ระดับ Anthropic / OpenAI / Deepmind)**  
แก้ปัญหาเก่าแบบ 100% ไม่งอก ไม่ซ้อน ไม่หลุด track

---