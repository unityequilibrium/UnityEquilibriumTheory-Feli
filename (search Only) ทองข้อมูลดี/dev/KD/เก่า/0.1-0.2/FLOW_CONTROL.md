โอเค Santa —  
ฉันจะทำ **FLOW_CONTROL.md v2.0 (ยกเครื่องใหม่ทั้งฉบับ)**  
โดยรวบรวมทุกข้อมูลจาก:

- SYSTEM_CONTRACT v2.0
    
- AGENT_FLOW เก่า
    
- DATA_LIFECYCLE
    
- MODEL_ROUTING
    
- KB_SYNC
    
- EVENT_BUS
    
- API_SPEC
    
- CACHE_STRATEGY
    
- ERROR_HANDLING
    
- PROJECT_STRUCTURE
    
- ARCHITECTURE_MAP
    

และออกแบบให้เป็น **Flow กลางของทั้งระบบ**  
ที่ “ทุก feature, ทุก module, ทุก panel” ต้องเดินตาม  
แบบ deterministic (ไม่สุ่ม) และ predictable (คาดเดาได้)

**นี่จะเป็นหัวใจของทั้ง Platform — ตัวควบคุมหลักของระบบ**

ชัด, กระชับ, แต่ครบทุกกรณี

---

# 📘 **FLOW_CONTROL.md (v2.0)**

**UET Platform — Unified Flow Control System (v2.0)**

---

# ⭐ 0. จุดประสงค์ของ FLOW_CONTROL v2.0

- กำหนดลำดับการทำงานของระบบ (Execution Order)
    
- ควบคุม state machine ของทุกโมดูล
    
- ป้องกันการข้ามขั้นตอน, ลูปซ้ำ, หรือ flow ผิดตามสัญญาระบบ
    
- เชื่อม UI → API → Engine → Storage → Event → Response
    
- ทำให้ระบบทำงาน “เสถียร, เดาได้, แก้ปัญหาได้ง่าย”
    

FLOW_CONTROL = **กฎหมายคุมลำดับการทำงานของแพลตฟอร์ม**

---

# ⭐ 1. ภาพรวมโครงสร้าง Flow

นี่คือ “Flow ใหญ่ที่สุด” ของแพลตฟอร์มทั้งหมด:

```
USER ACTION
    ↓
UI PANEL
    ↓
API REQUEST
    ↓
FLOW CONTROL ENGINE
    ↓
PERMISSION CHECK
    ↓
ROUTING ENGINE / KB / FILE / AGENT / RAG
    ↓
EXECUTION
    ↓
VALIDATION
    ↓
STATE COMMIT
    ↓
EVENT EMIT
    ↓
CACHE INVALIDATE (ถ้าจำเป็น)
    ↓
RESPONSE
```

ทุก action ของระบบ **ต้องผ่านเส้นทางนี้เสมอ**

---

# ⭐ 2. Unified State Machine (FSM)

state หลักที่ระบบต้องใช้เหมือนกันทุกโมดูล

```
IDLE
→ CONTEXT_LOAD
→ PERMISSION_CHECK
→ ROUTING
→ EXECUTION
→ VALIDATE
→ COMMIT
→ EMIT_EVENTS
→ RESPOND
→ RESET
```

แต่ละโมดูลจะใช้ FSM เหมือนกัน เช่น Agent, KB Sync, File Upload, RAG

---

# ⭐ 3. Flow กลางสำหรับ “ทุก Request”

### **3.1 FLOW ขั้นพื้นฐาน**

```
1. RECEIVE_REQUEST
2. ASSIGN_REQUEST_CONTEXT
3. VALIDATE_SCHEMA
4. PERMISSION_CHECK
5. SELECT_HANDLER (File / Agent / RAG / KB / Routing)
6. EXECUTE_HANDLER
7. VALIDATE_OUTPUT
8. COMMIT_STATE
9. EMIT_EVENTS
10. FORMAT_RESPONSE
```

**ห้ามข้ามขั้นตอนใด ๆ**

---

# ⭐ 4. UI → API → ENGINE Flow

แยกตาม Panel

## **4.1 Sources Panel Flow**

สำหรับ File, Version, KB

```
UPLOAD
→ PARSE
→ VERSION_CREATE
→ CHUNK
→ EMBED
→ INDEX
→ KB_SYNC
→ EMIT(KB_VERSION_UPDATED)
→ CACHE_INVALIDATE
→ RESPOND
```

## **4.2 Chat Panel Flow**

สำหรับ Chat + Agent

```
PROMPT_INPUT
→ CONTEXT_LOAD
→ ROUTING_DECISION
→ AGENT_EXECUTION
→ VALIDATE
→ LOG
→ EMIT(AGENT_STEP / MODEL_ROUTED)
→ RESPOND
```

## **4.3 Studio Panel Flow**

สำหรับ canvas / editing / generation

```
EDIT_REQUEST
→ LOAD_FILE_VERSION
→ ROUTING_DECISION
→ AGENT_GENERATE
→ VALIDATE
→ UPDATE_FILE_VERSION
→ CHUNK + EMBED + INDEX
→ KB_SYNC
→ EMIT(FILE_UPDATED)
→ RESPOND
```

---

# ⭐ 5. Module-specific Flow

---

# **5.1 File Upload Flow**

```
FILE_UPLOAD
→ MIME_CHECK
→ NORMALIZE
→ VERSION_CREATE
→ PARSE (PDF/DOCX/etc.)
→ EXTRACT_TEXT
→ CHUNK
→ EMBED
→ VECTOR_UPSERT
→ REGISTRY_UPDATE
→ CACHE_INVALIDATE
→ EMIT(FILE_UPDATED)
→ RESPOND
```

---

# **5.2 KB Sync Flow**

```
KB_SYNC_REQUEST
→ VALIDATE_VERSION
→ CREATE_REGISTRY_ENTRY
→ UPDATE_CHUNKS
→ UPDATE_EMBEDDINGS
→ INDEX_UPDATE
→ EMIT(KB_VERSION_UPDATED)
→ RESPOND
```

---

# **5.3 RAG Query Flow**

```
RAG_QUERY
→ CONTEXT_CHECK
→ TOP_K_SEARCH
→ RERANK
→ BUILD_RESPONSE
→ VALIDATE
→ RESPOND
```

---

# **5.4 Model Routing Flow**

```
ROUTING_REQUEST
→ TASK_ANALYSIS
→ PERMISSION_FILTER
→ COST_FILTER
→ CONTEXT_FILTER
→ SELECT_MODEL
→ EMIT(MODEL_ROUTED)
→ RESPOND
```

---

# **5.5 Agent Flow (เวอร์ชันใหม่)**

```
AGENT_RUN
→ LOAD_CONTEXT
→ ROUTING_DECISION
→ EXECUTE_MODEL
→ VALIDATE_OUTPUT
→ SAFETY_FILTER
→ CHAIN_STEP (if multi-step)
→ LOG
→ EMIT(AGENT_STEP)
→ RESPOND
```

---

# ⭐ 6. Flow Control Rules (กฎสำคัญที่สุด)

### **Rule 1 — Flow ต้องเป็นเส้นตรง (Linearized)**

ห้ามข้ามลำดับขั้นตอน

### **Rule 2 — Error = หยุด flow ทันที**

flow จะพุ่งไปที่ ERROR_HANDLER → EVENT → RESPONSE

### **Rule 3 — ทุก commit ต้องผ่าน Validation**

ห้ามบันทึกไฟล์/KB ที่ไม่ผ่านหน่วยตรวจสอบ

### **Rule 4 — ทุก “write action” ต้องสร้าง Version ใหม่**

การเปลี่ยนแปลง = version, ไม่มีการเขียนทับ

### **Rule 5 — ทุก action ต้องยิง Event**

Event = สัญญาณควบคุม panel อื่น ๆ

### **Rule 6 — Cache ต้องถูก invalidate ทันทีเมื่อมี file update**

ห้ามใช้ข้อมูลเก่า

---

# ⭐ 7. Event Flow Integration

(Flow Control เชื่อมเข้ากับ Event Bus)

```
FLOW → EMIT_EVENT → UI_UPDATE
          │
          └──CACHE_INVALIDATE (if file changed)
```

Event ตัวสำคัญ:

- FILE_UPDATED
    
- KB_VERSION_UPDATED
    
- MODEL_ROUTED
    
- AGENT_STEP
    
- CONTRACT_VIOLATION
    
- CACHE_INVALIDATED
    

---

# ⭐ 8. Failure Flow (เมื่อมี error เกิดขึ้น)

```
EXECUTION_FAIL
→ ERROR_HANDLER
→ UNIFIED_ERROR_SCHEMA
→ EMIT(ERROR_EVENT)
→ NO_STATE_COMMIT
→ SAFE_RESPONSE
```

ระบบจะไม่มีทาง “พังคา flow”  
แต่จะตอบแบบ Safe Always

---

# ⭐ 9. Flow Comparison (OLD vs NEW)

|หมวด|เวอร์เก่า|เวอร์ใหม่ v2.0|
|---|---|---|
|การควบคุมลำดับ|กระจาย|รวมศูนย์|
|Agent|ขั้นตอนไม่ครบ|100% deterministic|
|KB|ยังไม่มี merge-flow|เวอร์ชันสมบูรณ์|
|Routing|ไม่มี|มี routing-engine เต็ม|
|Versioning|ไม่บังคับ|บังคับทุกการเขียน|
|Cache|ไม่มี flow|รวมใน flow-control|
|Event|แตกไฟล์|รวมเป็นระบบเดียว|

---

# ⭐ 10. Master Flow Diagram (ภาพรวมสุดท้าย)

นี่คือ “Flow ใหญ่ที่สุด” ของระบบ v2.0

```
USER_ACTION
   ↓
UI_PANEL
   ↓
API_LAYER
   ↓
FLOW_CONTROL_ENGINE
   ↓
PERMISSION_CHECK
   ↓
ROUTING_ENGINE
   ↓
EXECUTION_MODULE
   ↓
VALIDATION
   ↓
STATE_COMMIT
   ↓
EVENT_EMIT
   ↓
CACHE_INVALIDATE
   ↓
FORMAT_RESPONSE
   ↓
USER
```

นี่คือรากแกนของระบบทั้งหมด พร้อมนำไปใช้จริง

---

# 🧭 **SYSTEM BLUEPRINT v2.0 — HIGH LEVEL**

```
USER
  ↓
UI (3 Panels)
  ↓
API LAYER
  ↓
FLOW CONTROL ENGINE
  ↓
CORE ENGINES (Agent / RAG / KB / File / Routing)
  ↓
DATA LAYER (Files / Versions / Chunks / Embeddings / KB)
  ↓
EVENT BUS
  ↓
CACHE + LOGS + METRICS
  ↓
RESPONSE → UI
```

นี่คือ “แม่โครงสร้าง” ของระบบทั้งหมด  
อ่านจบแล้วเข้าใจว่าระบบ UET ทำงานยังไงในระดับภาพรวม

---

# 🧭 **SYSTEM BLUEPRINT v2.0 — MID LEVEL (Subsystem Based)**

```
                                USER
                                  ↓
                           ┌──────────────┐
                           │  UI LAYER    │
                           │ Sources / Chat / Studio
                           └──────────────┘
                                  ↓
                            (HTTP Request)
                                  ↓
                         ┌─────────────────┐
                         │    API LAYER    │
                         └─────────────────┘
                                  ↓
                         ┌─────────────────┐
                         │ FLOW CONTROL     │
                         │  (State Machine) │
                         └─────────────────┘
                                  ↓
    ┌────────────────────────────────────────────────────────────────────────────┐
    │                            CORE ENGINE LAYER                               │
    │                                                                            │
    │  ┌──────────────┐   ┌───────────────┐   ┌─────────┐   ┌──────────────┐     │
    │  │ File Engine  │   │ KB Sync Engine│   │ RAG     │   │ Agent Engine │     │
    │  │ (parse/chunk)│   │ (versioning)  │   │ Search  │   │ Routing Exec │     │
    │  └──────────────┘   └───────────────┘   └─────────┘   └──────────────┘     │
    │                                                                            │
    └────────────────────────────────────────────────────────────────────────────┘
                                  ↓
                         ┌─────────────────┐
                         │  DATA LAYER     │
                         │ Files / DB / Vectors
                         └─────────────────┘
                                  ↓
                         ┌─────────────────┐
                         │   EVENT BUS     │
                         └─────────────────┘
                                  ↓
                ┌────────────────────┬────────────────────────┐
                │                    │                        │
        ┌─────────────┐     ┌──────────────────┐    ┌────────────────┐
        │   CACHE      │     │    METRICS       │    │     LOGS       │
        └─────────────┘     └──────────────────┘    └────────────────┘
                                  ↓
                              RESPONSE
                                  ↓
                              UI UPDATE
```

ระดับนี้คือ “ระบบย่อย” ทั้งหมด  
แสดงการไหลระหว่าง UI → API → Engine → Storage → Event

---

# 🧭 **SYSTEM BLUEPRINT v2.0 — DEEP LEVEL (Full Flow Map)**

นี่คือ “ภาพแม่สมบูรณ์ที่สุด”  
รวมทุกระบบ ทุก flow ทุกโมดูล

```
USER ACTION
    ↓
──────────────────────────── UI LAYER ──────────────────────────────
 Sources Panel         Chat Panel                Studio Panel
 (File/KB)             (LLM + Agent)             (Canvas/Generate)
    ↓                      ↓                          ↓
──────────────────────────── API LAYER ─────────────────────────────
  /auth     /files     /kb       /rag     /agent      /routing
    ↓
──────────────────────── FLOW CONTROL ENGINE ─────────────────────────
   RECEIVE_REQUEST
   → SCHEMA_VALIDATE
   → PERMISSION_CHECK
   → SELECT_HANDLER
   → EXECUTE_HANDLER
   → VALIDATE_OUTPUT
   → COMMIT_STATE
   → EMIT_EVENTS
   → FORMAT_RESPONSE
    ↓
────────────────────────── CORE ENGINE LAYER ─────────────────────────
     ┌──────────────────────────┬─────────────────────────────┬──────────────────────────┐
     │                          │                             │                          │
 File Engine              KB Sync Engine                 RAG Engine                  Agent Engine
 parse → normalize        versioning → merge             search → rerank             routing → exec
 chunk → embed           registry update                citation build              validate → chain
 index update            conflict detect                result scoring              safety + logs
     └──────────────────────────┴─────────────────────────────┴──────────────────────────┘
    ↓
────────────────────────── DATA LAYER ──────────────────────────────
 Files → Versions → Chunks → Embeddings → KB Registry → Vector DB → Postgres
    ↓
────────────────────────── EVENT BUS ───────────────────────────────
 FILE_UPDATED
 KB_VERSION_UPDATED
 MODEL_ROUTED
 AGENT_STEP
 CACHE_INVALIDATED
 CONTRACT_VIOLATION
 ERROR_OCCURRED
    ↓
─────────────────── INFRA LAYER (Cache/Logs/Metrics) ─────────────────
 Cache Engine     Metrics Collector      Logging Engine     Health Monitor
 TTL / Invalidate    rag_precision         all actions      cluster checks
    ↓
─────────────── RESPONSE (Unified Response Schema) ───────────────────
    ↓
─────────────── UI UPDATE (Panels react to events) ───────────────────
```

นี่คือ **แผนที่แม่ครบทั้งระบบ**  
แบบ “รู้ทั้ง flow, engine, event, storage, state, permission”

---

# 🧠 **สรุปแบบเข้าใจง่ายที่สุด**

**SYSTEM BLUEPRINT v2.0 = โครงสร้างการทำงานทั้งหมดของ UET ตั้งแต่ผู้ใช้สั่งงาน → ผลลัพธ์กลับมาที่ UI**

จุดเด่น:

- flow เดินเป็นเส้นตรง ควบคุมด้วย state machine
    
- ไม่มี action ไหนข้ามขั้น
    
- ทุก action ยิง event
    
- ทุกการเขียนไฟล์ต้องสร้าง version
    
- Agent / Routing / KB / RAG / Cache รวมเป็นระบบเดียว
    
- ทั้งหมด deterministic (คาดเดาได้)
    
- debug ง่ายเพราะมี event + logs ทุกชั้น
    
- UI ไม่ต้องเดา ใช้ event-driven 100%
    

---
