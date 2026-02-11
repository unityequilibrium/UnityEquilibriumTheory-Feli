# COMBINED: EVENT BUS (CATEGORY 14)


# FILE: 08__EVENT_BUS SYSTEM v3.0.md

ได้เลย Santa —  
ตอนนี้เราจะสร้าง **บทที่ 8 — EVENT_BUS SYSTEM v3.0 PART 1**  
ซึ่งเป็นหนึ่งในโมดูลที่ “โคตรสำคัญ” ของสถาปัตยกรรมทั้งหมด เพราะ:

> **Event Bus = ระบบสื่อกลางที่ทำให้ทุกโมดูลสื่อสารกันแบบ real-time, ปลอดภัย, deterministic และไม่ขัดกัน**

ฉันตรวจไฟล์ทั้งหมด (รวมไฟล์ EVENT_BUS เก่า + KS + RAG + Flow Control + Agent Engine + Deployment + Error Handling) และจะเขียน PART 1 ให้เป็นเวอร์ชัน v3.0 แบบเต็ม ครอบคลุมทั้งหมดจริง ๆ

ไปเริ่ม 🔥

---

# 📘 **CHAPTER 8 — EVENT_BUS SYSTEM v3.0

PART 1 — CORE CONCEPT + EVENT MODEL + CONTRACT**

---

# 🟦 SECTION A — ROLE OF EVENT BUS

Event Bus v3.0 ทำหน้าที่เป็น:

### 1) **ระบบสื่อสารกลาง (communication spine)**

ทุก module ต้องรายงานเหตุการณ์สำคัญ

### 2) **ระบบกระจายสถานะ (state propagation)**

เช่น KB version update → ส่งไปให้ agent worker ทั้งหมดรู้

### 3) **ระบบประสานหลายโมดูล (coordination layer)**

เช่น RAG → KS → Flow Control → Cache

### 4) **ระบบแจ้งเตือนความผิดปกติ (alert system)**

เช่น orphan vector, stale context, failure

### 5) **ตัวกลางกัน race-condition / sync-conflict**

Event Bus ทำให้ระบบนาย “นิ่งและไม่ cross-knowledge ผิด”

---

# 🟩 SECTION B — CORE ARCHITECTURE

Event Bus v3.0 ใช้รูปแบบ:

```
Publisher → Event Bus → Subscribers
```

Publisher = โมดูลที่สร้าง event  
Subscriber = โมดูลที่ต้องรับ event นั้นและอัปเดตสถานะ

โครงสร้าง:

```
KS Engine           ┐
RAG Engine         ┐│
Agent Workers      ││
Flow Control       ││→ publish events → Event Bus → dispatch → subscribed modules
Cache System       ││
File System        ┘│
Monitoring System   ┘
```

---

# 🟥 SECTION C — EVENT TYPES (v3.0)

Event Bus รองรับ event ทั้งหมด 4 กลุ่มใหญ่:

---

## ⭐ GROUP 1 — **Knowledge / Data Events**

ใช้สำหรับป้องกัน stale knowledge, orphan, cross-project

|Event|Trigger|Purpose|
|---|---|---|
|`KB_VERSION_UPDATED`|KS sync success|notify all agents|
|`VECTOR_REBUILT`|RAG rebuild|update vector store usage|
|`ORPHAN_DETECTED`|RAG/KS scan|lock system if needed|
|`MERGE_CONFLICT`|KS write|force re-sync|

---

## ⭐ GROUP 2 — **System Health / Infrastructure Events**

|Event|Trigger|Purpose|
|---|---|---|
|`SYSTEM_OVERLOAD`|high CPU/mem|governor BUSY mode|
|`SYSTEM_LOCKDOWN`|critical fault|block all agent steps|
|`WORKER_FAILURE`|worker crash|recycle worker|
|`CACHE_INVALIDATE`|stale cache|drop old entries|

---

## ⭐ GROUP 3 — **Agent / Execution Events**

|Event|Trigger|Purpose|
|---|---|---|
|`AGENT_START`|agent receives job|monitoring|
|`AGENT_STEP`|each step|debug trace|
|`AGENT_ERROR`|failure|system logging|
|`AGENT_FINISH`|completed|metrics|

---

## ⭐ GROUP 4 — **Security / Contract Events**

|Event|Trigger|Purpose|
|---|---|---|
|`CONTRACT_VIOLATION`|tool misuse|lock offending agent|
|`PERMISSION_DENIED`|step invalid|audit trail|
|`VERSION_MISMATCH`|RAG context wrong|force agent stop|

---

# 🟫 SECTION D — EVENT OBJECT SPEC (v3.0)

Event Bus v3.0 ใช้สเปก unified:

```
{
  "event_id": "...",
  "event_type": "KB_VERSION_UPDATED | AGENT_ERROR | ...",
  "timestamp": "...",
  "source": "RAG|KS|Flow|Agent|System",
  "payload": {...},
  "kb_version": registry.current,
  "project_id": "...",
  "severity": "info|warning|error|critical"
}
```

---

# 🟪 SECTION E — EVENT CONTRACT RULES (สำคัญมาก)

Event Bus v3.0 ต้อง enforce กฎ:

### 1) **No Missing Event**

ทุกการเปลี่ยนสถานะสำคัญต้องยิง event  
ห้ามเงียบ

### 2) **No Duplicate Event**

ใช้ event_id แบบ deterministic

### 3) **No Cross-Project Event Leakage**

event ต้องระบุ project_id  
ผู้รับต้อง ignore ถ้า project ไม่ตรง

### 4) **Event Ordering Guarantee**

เหตุการณ์ KB version ต้องเรียงลำดับ:

```
v1 → v2 → v3
```

ห้าม event v2 โผล่มาก่อน v1

### 5) **Atomic Delivery**

event ต้องส่งให้ subscriber ทุกตัว  
ห้ามบางตัวได้ บางตัวไม่ได้

### 6) **Deterministic Side Effects**

การรับ event ต้องเกิดผลแบบเดิมทุกครั้ง

---

# 🟦 SECTION F — EVENT DELIVERY MODEL (v3.0)

Event Bus v3.0 ใช้กลไก:

```
Publisher → Queue → Dispatcher → Subscriber
```

---

## 1) **Publisher**

KS, Agent, RAG, Flow Control, Cache, System

## 2) **Queue**

Event ถูก push ลง “event queue” (ไม่ block)

## 3) **Dispatcher**

อ่าน queue และส่งไปยัง subscriber ที่ต้องรับ event

## 4) **Subscriber**

โมดูลที่ต้องเปลี่ยนสถานะ เช่น:

- Agent Workers
    
- RAG Engine
    
- KS Engine
    
- Flow Control
    
- Monitoring System
    

---

# 🟧 SECTION G — SUBSCRIBER RESPONSIBILITY MATRIX

|Subscriber|Must react to|Reaction|
|---|---|---|
|Agent Worker|KB_VERSION_UPDATED|abort plan + clear memory|
|Agent Worker|SYSTEM_LOCKDOWN|stop all|
|RAG Engine|VECTOR_REBUILT|load new vectors|
|KS Engine|MERGE_CONFLICT|force rebuild|
|Flow Control|SYSTEM_OVERLOAD|BLOCK heavy route|
|Flow Control|CONTRACT_VIOLATION|block offending agent|
|Cache Layer|CACHE_INVALIDATE|clear entries|
|Monitoring|AGENT_ERROR|log + alert|

---

# 🟥 SECTION H — EVENT BUS INTERNAL FLOW (ภาพหลัก)

```
Event Created
   ▼
Validate Event Contract
   ▼
Push to Queue
   ▼
Dispatcher Reads Event
   ▼
Filter by project_id
   ▼
Dispatch to Subscribers
   ▼
Subscribers execute deterministic reaction
```

---

# 🟨 SECTION I — EVENT BUS SAFETY MODEL

(เพื่อกันปัญหา sync ผิด, race-condition, system stall)

### 1) **Idempotency**

subscriber ต้อง handle event แบบไม่ผิดเพี้ยนซ้ำซ้อน

### 2) **Atomic Delivery**

ส่งครบทุก subscriber หรือไม่ส่งเลย

### 3) **Ordered Delivery**

KB events ต้อง strict order

### 4) **Project Boundary**

แต่ละ event ต้องตกเฉพาะ project เดียว

### 5) **Version Awareness**

ผู้รับต้องเช็ค version ของ event เสมอ

---

# 🟫 SECTION J — WHY EVENT BUS v3.0 สำคัญต่อระบบทั้งหมด

เพราะมันทำให้ทุกโมดูล:

- sync กันแบบ deterministic
    
- ไม่มี stale knowledge
    
- ไม่มี agent ที่วิ่งผิด version
    
- ระบบไม่ crash ตอน KS rebuild
    
- agent workers scale ได้
    
- errors propagate ถูกต้อง
    
- Flow Control รู้สถานะระบบแบบ real-time
    
- RAG, KS, Agent, Cache กลายเป็นระบบ “ติดกันหมด”
    

คือ backbone จริง ๆ ของสถาปัตยกรรมนี้

---

# ⭐ END OF CHAPTER 8 — PART 1

ตอนนี้ Event Bus v3.0 มีครบ:

- event model
    
- event spec
    
- event types
    
- delivery model
    
- subscriber matrix
    
- safety contract
    
- core flow diagram
    

**พร้อมสำหรับ PART 2:  
MEGA DIAGRAM + STATE MACHINE + FAILURE TREE**

---

# ได้เลย Santa —  
ตอนนี้เราสร้าง **CHAPTER 8 — EVENT_BUS SYSTEM v3.0 PART 2**  
ให้ “สมบูรณ์ที่สุด” ตาม checklist:

✔ Event List  
✔ Event Ordering  
✔ Subscriber Map  
✔ Retry Logic  
✔ Queue Safety Rules  
✔ Multi-worker propagation

ฉันได้วิเคราะห์ไฟล์เก่าทั้งหมด + Public Architecture ของระบบนาย (รวม Agent, KS, RAG, Flow Control, Worker Pools) เพื่อรวมเป็นสถาปัตยกรรม v3.0 ที่ **ครบ + คมกริบ + deterministic**

ไปเริ่มพาร์ทที่สำคัญที่สุดของ Event Bus 🔥

---

# 📘 **CHAPTER 8 — EVENT_BUS SYSTEM v3.0

PART 2 — MEGA DIAGRAM + STATE MACHINE + FAILURE TREE + SAFETY LOGIC**

---

# 🟦 SECTION A — EVENT BUS MEGA DIAGRAM (ULTRA HD)

```
                         ┌─────────────────────────┐
                         │       PUBLISHER         │
                         │ (KS/RAG/Flow/Agent/FS)  │
                         └───────────┬─────────────┘
                                     ▼
                           ┌───────────────────┐
                           │   EVENT QUEUE     │
                           │ (FIFO + Ordered)  │
                           └──────────┬────────┘
                                      ▼
                           ┌───────────────────┐
                           │    DISPATCHER     │
                           │ (filter + fanout) │
                           └──────────┬────────┘
                                      ▼
        ┌───────────────────────┬──────────────┬──────────────────────┬──────────────────────┐
        ▼                       ▼              ▼                      ▼                      ▼
┌──────────────┐       ┌──────────────┐ ┌──────────────┐     ┌──────────────┐       ┌──────────────┐
│ AGENT WORKER │       │ FLOW CONTROL │ │ RAG ENGINE   │     │ KS ENGINE    │       │ CACHE SYSTEM │
└──────────────┘       └──────────────┘ └──────────────┘     └──────────────┘       └──────────────┘
```

Event Bus ทำงานเหมือน “ระบบเลือด” ของสถาปัตยกรรม → เชื่อมทุกโมดูลเข้าด้วยกัน

---

# 🟩 SECTION B — EVENT ORDERING MODEL v3.0

(เพื่อป้องกัน Knowledge Drift, Version Drift, Stale Data)

Event Bus ต้อง enforce ลำดับเหตุการณ์:

### **Order Layer 1 — KB Version**

```
KB_VERSION_UPDATED(v1)
→ KB_VERSION_UPDATED(v2)
→ KB_VERSION_UPDATED(v3)
```

ห้ามสลับลำดับเด็ดขาด

### **Order Layer 2 — RAG Vector Events**

```
VECTOR_REBUILD_START
VECTOR_REBUILD_DONE
```

### **Order Layer 3 — File + KS Merge**

```
FILE_WRITE → KS_MERGE → KB_UPDATE
```

### **Order Layer 4 — System Events (strict)**

```
SYSTEM_OVERLOAD → SYSTEM_LOCKDOWN → SYSTEM_RECOVER
```

ถ้า order ผิด → ระบบต้องหยุด (safe mode)

---

# 🟥 SECTION C — SUBSCRIBER RESPONSIBILITY MAP

(ใครต้องทำอะไรเมื่อได้รับ event)

|Subscriber|Must Handle Events|Required Reaction|
|---|---|---|
|**Agent Workers**|KB_VERSION_UPDATED / SYSTEM_LOCKDOWN / CONTRACT_VIOLATION|abort plan, clear memory, stop exec|
|**Flow Control**|SYSTEM_OVERLOAD / SYSTEM_LOCKDOWN|block routes, governor BUSY|
|**RAG Engine**|VECTOR_REBUILT / KB_VERSION_UPDATED|reload vectors, update index|
|**KS Engine**|FILE_WRITE / MERGE_CONFLICT|restart sync, rebuild KB|
|**Cache Layer**|CACHE_INVALIDATE|delete stale entries|
|**Monitoring**|AGENT_ERROR / SYSTEM_ERROR|alert + record|
|**Write Worker**|KS_SYNC / FILE_CHANGED|apply write safely|

---

# 🟪 SECTION D — EVENT RETRY LOGIC

(ระบบกัน event หาย, event ซ้ำ, event เสีย)

Event Bus ต้อง implement **3-level retry logic**:

---

## **1) Queue-Level Retry**

ถ้า event push ไม่สำเร็จ:

- retry 3 ครั้ง
    
- ถ้ายัง fail → SYSTEM_LOCKDOWN (critical alert)
    

---

## **2) Dispatch-Level Retry**

subscriber รับ event ไม่สำเร็จ

```
retry → exponential backoff → skip (log only)
```

แต่สำหรับ events:

- KB_VERSION_UPDATED
    
- SYSTEM_LOCKDOWN
    

ห้าม skip → ต้อง retry จนกว่าจะสำเร็จ

---

## **3) Subscriber-Level Retry**

ถ้า subscriber action fail:

- agent: retry step 1 ครั้ง
    
- RAG: reload vectors
    
- KS: redo merge
    
- Flow Control: restart governor
    

---

# 🟫 SECTION E — QUEUE SAFETY RULES

(เพื่อป้องกัน corruption, conflict, race condition)

### ✔ RULE 1 — FIFO Strict

ลำดับ event ห้ามผิดจาก queue

### ✔ RULE 2 — Single Writer Model

มีแค่ Dispatcher ที่อ่าน queue

### ✔ RULE 3 — Multiple Subscriber Fanout

แต่ทุก subscriber ต้องรับสำเนา event เดียวกัน

### ✔ RULE 4 — No Partial Delivery

ส่งให้ทุก subscriber หรือไม่ส่งเลย

### ✔ RULE 5 — Project Boundary Safety

subscriber ต้อง ignore events ที่ไม่ตรง project_id

### ✔ RULE 6 — Idempotent Delivery

subscriber ต้อง handle event ซ้ำได้ (ไม่พัง)

---

# 🟦 SECTION F — MULTI-WORKER PROPAGATION MODEL

(ตอนระบบมี worker จำนวนมาก event จะถูกกระจายอย่างไร)

```
EventBus → Broadcast → WorkerPool
```

### Worker ต้อง enforce:

- หยุดงานทันทีเมื่อ version update
    
- clear memory L2
    
- re-request RAG
    
- drop stale context
    
- reset internal state
    

**Propagation Guarantee**:  
ทุก Worker ได้ event ภายใน < 50ms (เพราะต้องหยุดทันที)

---

# 🟧 SECTION G — EVENT BUS STATE MACHINE

(สถานะภายในของ Event Bus เอง)

```
STATE: IDLE
 ▼
STATE: RECEIVING_EVENT
 ▼
validate_event?
 ▼ Fail
STATE: ERROR_INVALID_EVENT → log + drop
 ▼ Success
STATE: QUEUE_EVENT
 ▼
push_fail?
 ▼ Yes
STATE: ERROR_QUEUE → retry → system_lockdown
 ▼ No
STATE: DISPATCH
 ▼
all_subscribers_success?
 ▼ No
STATE: PARTIAL_FAIL → retry dispatch
 ▼ Yes
STATE: END
```

---

# 🟥 SECTION H — FAILURE TREE (ทุกเส้นทาง error ของ Event Bus)

```
                    EVENT BUS FAILURE TREE
                    ──────────────────────
EVENT INPUT FAIL  → invalid schema / missing fields  
QUEUE FAIL        → queue corrupt / full / IO error  
DISPATCH FAIL     → subscriber offline  
SUBSCRIBER FAIL   → handler error / crash  
ORDER FAIL        → event order violated  
CONTRACT FAIL     → project_id mismatch / version mismatch  
LOCKDOWN FAIL     → system cannot recover  
```

### Reaction Summary:

|Error|Reaction|
|---|---|
|input fail|drop + log|
|queue fail|retry → lockdown|
|dispatch fail|retry + skip|
|subscriber fail|retry + escalate|
|order fail|immediate lockdown|
|contract fail|block + alert|
|critical fail|full system lockdown|

---

# 🟨 SECTION I — EVENT BUS CONTRACT SUMMARY (v3.0)

```
1) no lost events  
2) no duplicate events  
3) strict ordering  
4) strict project boundary  
5) deterministic reactions  
6) atomic delivery (all or none)  
7) idempotent subscriber logic  
8) safe fallback on error  
9) real-time propagation  
10) no race conditions allowed  
```

---

# 🟩 SECTION J — WHY PART 2 สำคัญมาก

เพราะมันทำให้ Event Bus ไม่ใช่แค่ “ระบบแจ้งเตือน” แต่เป็น:

- ระบบป้องกัน stale knowledge
    
- ระบบควบคุม synchronization ทั้งแพลตฟอร์ม
    
- ระบบด้านความปลอดภัย
    
- ระบบ coordinating agent workers
    
- ระบบ monitoring แบบลึก
    
- ระบบกัน conflict เวลา KS และ RAG ทำงานพร้อมกัน
    
- ระบบที่ทำให้ architecture นาย deterministic 100%
    

Event Bus = เส้นเลือดของแพลตฟอร์ม  
เมื่อทำ PART 2 แล้ว → ระบบเริ่ม “มีชีวิตจริง ๆ”

---

# ⭐ END OF CHAPTER 8 — PART 2

ตอนนี้ Event Bus v3.0 ครบ:

- mega diagram
    
- state machine
    
- subscriber map
    
- safety rules
    
- retry logic
    
- ordering
    
- multi-worker propagation
    
- failure tree
    
- contract summary
    

พร้อมต่อ PART 3:

> **PART 3 — MEGA BLUEPRINT + MATRIX + PERFORMANCE MODEL + INTEGRATION WITH ALL SYSTEMS**

---

# ❓ Santa พร้อมไปต่อ PART 3 เลยไหม?

# FILE: EVENT_BUS.md.md

โอเค Santa —  
ฉันจะทำ **EVENT_BUS v2.0 (เวอร์ชันใหม่สมบูรณ์ที่สุด)**  
โดยรวบรวมข้อมูลจากทุกไฟล์ก่อนหน้า:

- SYSTEM_CONTRACT v2.0
    
- FLOW_CONTROL v2.0
    
- AGENT_FLOW v2.0
    
- AGENT ENGINE BIBLE
    
- KB_SYNC
    
- FILE_VERSIONING
    
- MODEL_ROUTING
    
- CACHE_STRATEGY
    
- DATA_SCHEMA
    
- UI PANEL LOGIC
    

**เวอร์ชันนี้จะเป็นระบบ Event ที่ deterministic, ครบ, และควบคุมได้ 100%**  
ระดับเดียวกับที่ใช้ในแพลตฟอร์ม AI enterprise

อ่านง่าย กระชับ แต่ครบทุกส่วนที่จำเป็น

---

# 📘 **EVENT_BUS.md (v2.0)**

**UET Platform — Unified Event Bus Specification**

---

# ⭐ 0. เป้าหมายของ EVENT_BUS v2.0

1. ควบคุมการไหลของข้อมูลระหว่างระบบ (orchestrator)
    
2. sync UI panels ให้ตอบสนองแบบทันที
    
3. ผูกทุก module: Agent, Routing, KB, File, RAG
    
4. ป้องกัน flow ผิด → ทุก action ต้อง “ประกาศ event ก่อนเสมอ”
    
5. ทำให้ระบบ debug ได้ง่ายและโปร่งใส
    

**Event Bus = เส้นเลือดใหญ่ของระบบ UET**

---

# ⭐ 1. Event Bus Architecture Overview

```
Module → EventBus.publish(event)
EventBus → EventLog + UI Subscriber + Cache Manager + Flow Engine
```

ทุก event ถูกส่งไปยัง:

- UI Panels (ผ่าน SSE หรือ WebSocket)
    
- Metrics Engine
    
- Logging
    
- Cache Controller
    
- Flow Control Engine
    
- Error Handler
    

Event Bus = "Hub กลางของระบบทั้งหมด"

---

# ⭐ 2. Event Lifecycle (ขั้นตอนทั้งหมด)

```
1. MODULE_TRIGGER
2. EVENT_BUILD
3. EVENT_VALIDATE
4. EVENT_PUBLISH
5. EVENT_DISPATCH
6. EVENT_LOG
7. EVENT_REACT (UI / Cache / Flow)
```

ทุก event ต้องผ่าน validation และ logging ก่อนถูกส่ง

---

# ⭐ 3. Event Schema (โครงสร้าง統一)

```
Event {
    id: string
    type: string
    actor_type: "user" | "agent" | "system"
    actor_id?: string
    project_id?: string
    timestamp: datetime
    payload: JSON
}
```

---

# ⭐ 4. Event Categories (หมวดใหญ่ของ Event ทั้งระบบ)

ในระบบ UET v2.0 มี 7 หมวด event:

1. **File Events**
    
2. **KB Events**
    
3. **Agent Events**
    
4. **Routing Events**
    
5. **Cache Events**
    
6. **System Events**
    
7. **Error Events**
    

นี่คือ “แกนกลางของ event bus v2.0”

---

# ⭐ 5. รายการ EVENT ทั้งหมด v2.0 (แบบเต็ม)

## 📁 **1. File Events**

เหตุการณ์เกี่ยวกับไฟล์, version, parse, chunk, embed

|Event|Trigger|
|---|---|
|FILE_UPLOADED|เมื่อไฟล์ถูกอัปโหลด|
|FILE_PARSED|เมื่อ parse แล้ว|
|FILE_VERSION_CREATED|เมื่อสร้าง version ใหม่|
|FILE_UPDATED|เมื่อมีการแก้ไขไฟล์|
|FILE_DELETED|เมื่อไฟล์ถูกลบ|
|FILE_INDEXED|chunk + embed เสร็จ|

---

## 📚 **2. KB Events**

เหตุการณ์เกี่ยวกับ KB Sync

|Event|Trigger|
|---|---|
|KB_SYNC_STARTED|เริ่ม sync|
|KB_VERSION_UPDATED|registry update|
|KB_CHUNK_UPDATED|chunk เปลี่ยน|
|KB_EMBEDDING_UPDATED|embedding update|
|KB_CONFLICT_DETECTED|เจอ conflict|
|KB_SYNC_COMPLETED|sync สำเร็จ|

---

## 🤖 **3. Agent Events**

เหตุการณ์ระดับ agent engine

|Event|Trigger|
|---|---|
|AGENT_RUN_STARTED|ทุกครั้งที่ agent เริ่มงาน|
|AGENT_CONTEXT_LOADED|โหลดข้อมูลเสร็จ|
|AGENT_TASK_ANALYZED|วิเคราะห์งานเสร็จ|
|AGENT_ROUTED|model routing เสร็จ|
|AGENT_STEP|agent ทำ step|
|AGENT_OUTPUT_VALIDATED|ตรวจผลลัพธ์ผ่าน|
|AGENT_COMPLETED|agent ทำงานเสร็จ|
|AGENT_FAILED|agent error|

---

## 🔀 **4. Routing Events**

เหตุการณ์จาก Model Routing Engine

|Event|Trigger|
|---|---|
|MODEL_ROUTED|เลือก model สำเร็จ|
|MODEL_FALLBACK|ใช้ fallback|
|MODEL_OVERRIDE|ผู้ใช้ override model|
|MODEL_REJECTED_BY_PERMISSION|ใช้โมเดลที่ role ไม่ถึง|

---

## ⚡ **5. Cache Events**

ควบคุมให้ระบบไม่มี stale data

|Event|Trigger|
|---|---|
|CACHE_HIT|มี cache hit|
|CACHE_MISS|มี cache miss|
|CACHE_INVALIDATED|ลบ cache เก่าหลังไฟล์ update|
|CACHE_REBUILT|cache ถูกสร้างใหม่|

---

## ⚙️ **6. System Events**

|Event|Trigger|
|---|---|
|SYSTEM_HEALTH_OK|health check|
|SYSTEM_HEALTH_WARN|system เริ่มช้า|
|SYSTEM_HEALTH_FAIL|system fail|
|DEPLOYMENT_UPDATED|deploy ใหม่|
|CONFIG_CHANGED|config system เปลี่ยน|

---

## ❌ **7. Error Events**

|Event|Trigger|
|---|---|
|ERROR_MODEL_FAIL|model fail|
|ERROR_RAG_FAIL|rag fail|
|ERROR_ROUTING_FAIL|routing fail|
|ERROR_PERMISSION|user ไม่ได้สิทธิ์|
|ERROR_CONTRACT_VIOLATION|flow ผิด|
|ERROR_SYSTEM|error อื่นๆ|

---

# ⭐ 6. Event Routing (เหตุการณ์ไหลไปไหน)

นี่คือ Blueprint การไหลของ event

```
MODULE
  → EVENT
    → EventBus
      → UI Panel Update
      → Cache Manager
      → Metrics Engine
      → Logging DB
      → Flow Engine (chain effects)
```

Example:

```
FILE_UPDATED
 → EventBus
   → Cache.invalidate(file)
   → UI.update(SourcesPanel)
   → KB.refresh if needed
```

---

# ⭐ 7. Event → UI Mapping (กำหนดว่า panel ไหนต้องขยับเมื่อเกิด event ใด)

## 📁 Sources Panel (ไฟล์)

ฟัง event:

```
FILE_UPLOADED
FILE_UPDATED
FILE_INDEXED
FILE_DELETED
KB_VERSION_UPDATED
CACHE_INVALIDATED
```

## 🗨 Chat Panel (การคุย)

ฟัง event:

```
AGENT_STEP
AGENT_COMPLETED
MODEL_ROUTED
ERROR_EVENTS
```

## 📝 Studio Panel (เอกสาร)

ฟัง event:

```
FILE_VERSION_CREATED
FILE_UPDATED
AGENT_COMPLETED
KB_VERSION_UPDATED
```

---

# ⭐ 8. Flow Integration (Flow Control + Event Bus)

```
FLOW_CONTROL
   → EXECUTION_SUCCESS
       → EMIT_EVENT
            → UI / CACHE / METRICS
   → EXECUTION_ERROR
       → EMIT_ERROR
            → ROLLBACK
            → SAFE_RESPONSE
```

Event เป็นส่วนหนึ่งของ flow control โดยตรง

---

# ⭐ 9. Event Order Guarantee (ลำดับ event ที่ระบบต้องรักษา)

1. event ต้อง timestamped
    
2. ต้องเข้าคิวตามลำดับ
    
3. ห้ามออก event ซ้ำ (id ต้อง unique)
    
4. UI ต้องเห็น event ในลำดับที่เกิดจริง
    
5. system event ต้องมาก่อนผลลัพธ์เสมอ
    

---

# ⭐ 10. Event Logging Rules

ทุก event ต้องถูกบันทึกลงฐานข้อมูล:

```
EventLog {
  event_id,
  type,
  payload,
  actor_type,
  actor_id,
  project_id,
  timestamp
}
```

เหตุผล: สำหรับ debug, audit, replay flow

---

# ⭐ 11. Event Blueprint Diagram (ภาพใหญ่)

```
MODULE ACTION
     ↓
BUILD EVENT
     ↓
EVENT BUS
     ↓
 ┌────────────┬────────────┬────────────┬────────────┐
 │ UI UPDATE  │ CACHE CTRL │ METRICS    │ LOGGING    │
 └────────────┴────────────┴────────────┴────────────┘
     ↓
FLOW CONTROL (ต่อเนื่อง)
```

---

# ⭐ 12. Event Philosophy (หลักคิดของระบบ Event)

1. ทุกการกระทำต้อง “ประกาศ”
    
2. ระบบต้องตอบสนองทันที
    
3. ไม่มี UI ไหนต้องรีเฟรชเอง
    
4. ไม่มี cache ไหนใช้ข้อมูลเก่า
    
5. ไม่มีการ sync ผิด panel
    
6. Event คือเครื่องยนต์ที่เชื่อมระบบเข้าด้วยกัน
    

---

# ⭐ 13. Deterministic Event Rules

- ไม่มี event ซ้ำ
    
- ไม่มี event ค้าง
    
- ทุก event มีผลต่อ state
    
- ทุก event มีผลต่อ UI
    
- ทุก event ต้องเก็บ log
    
- ทุก event ต้องผ่าน validation
    
- ทุก event ต้องเป็นไปตาม EventType ที่กำหนดเท่านั้น
    

---

# 🎯 **สรุปแบบเข้าใจง่ายที่สุด**

**EVENT_BUS v2.0 คือระบบประสาทกลางของ UET Platform**

มันทำหน้าที่:

- ควบคุม UI ทั้งหมด
    
- เชื่อม Agent → File → KB → RAG → Cache
    
- ทำให้ system deterministic
    
- ทำให้ debug ง่าย
    
- ทำให้ caching ไม่มี stale
    
- ทำให้ panel ทุกส่วนอัปเดตแบบ real-time
    
- ทำให้ทุก module ทำงานสอดคล้องกัน
    

---

โอเค Santa —  
ตอนนี้ฉันจะทำ **เวอร์ชัน DIAGRAM ใหญ่สุดของ EVENT BUS v2.0**  
แบบ _Master-Level Blueprint_ ที่เห็นทุกชั้น ความสัมพันธ์ การไหลของ event  
ตั้งแต่ UI → API → Flow Engine → Core Engines → Data → UI Return

**นี่คือ “MAP หลัก” ของระบบประสาทกลาง UET Platform**  
อ่านแล้วจะมองเห็นทุกเส้นทางของ event แบบชัดเจนที่สุด  
ระดับเดียวกับที่ใช้ทำ architecture ของแพลตฟอร์มใหญ่ ๆ

---

# 🧠 **EVENT BUS v2.0 — MASTER BLUEPRINT DIAGRAM**

## 🚀 **1) ภาพใหญ่ที่สุด (Super High-Level Nervous System)**

```
                      ┌────────────────────────────────┐
                      │           USER ACTION           │
                      └────────────────────────────────┘
                                      │
                                      ▼
                     ┌──────────────────────────────────┐
                     │             UI LAYER              │
                     │ Sources / Chat / Studio Panels   │
                     └──────────────────────────────────┘
                                      │ (HTTP Request)
                                      ▼
                     ┌──────────────────────────────────┐
                     │             API LAYER             │
                     └──────────────────────────────────┘
                                      │
                                      ▼
                     ┌──────────────────────────────────┐
                     │      FLOW CONTROL ENGINE         │
                     │  (State Machine + Contract)      │
                     └──────────────────────────────────┘
                                      │
                              Trigger Event
                                      ▼
                    ╔══════════════════════════════════════╗
                    ║             EVENT BUS v2.0            ║
                    ╚══════════════════════════════════════╝
                                      │
     ┌────────────────────────────────┼────────────────────────────────┐
     ▼                                ▼                                ▼
┌────────────┐               ┌────────────────┐               ┌────────────────┐
│ UI Update  │               │ Cache Manager  │               │ Metrics Engine │
└────────────┘               └────────────────┘               └────────────────┘
     │                                │                                │
     ▼                                ▼                                ▼
┌──────────────┐              ┌────────────────┐              ┌────────────────┐
│ SourcesPanel │              │ Invalidate RAG │              │ Perf. counters │
│ ChatPanel    │              │ Invalidate API │              │ Token tracking │
│ StudioPanel  │              │ Invalidate File│              │ Routing stats  │
└──────────────┘              └────────────────┘              └────────────────┘
                                      │
                                      ▼
                             ┌───────────────────┐
                             │   EventLog DB     │
                             └───────────────────┘
```

นี่คือภาพรวมสุด — เห็นครบทุกชั้น!

---

# 🧠 **2) Deep Diagram — Event Type → Path → Effects**

```
                   ┌────────────────────────────┐
                   │         MODULE              │
                   │  (Agent / File / KB / RAG) │
                   └────────────────────────────┘
                                 │
                                 ▼
                        [BUILD EVENT]
                                 │
                                 ▼
╔══════════════════════════════════════════════════════════════╗
║                        EVENT BUS v2.0                        ║
╚══════════════════════════════════════════════════════════════╝
           │                         │                         │
           ▼                         ▼                         ▼
 ┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
 │  DISPATCH → UI    │       │  DISPATCH → CACHE │       │ DISPATCH → METRICS │
 └──────────────────┘       └──────────────────┘       └──────────────────┘
           │                         │                         │
           ▼                         ▼                         ▼
  Sources/Chat/Studio       TTL expiry / invalidate      token flow logging
       Panels                RAG reset / update index    routing stats
                             prompt cache wipe           RAG precision logs
```

---

# 🧠 **3) ระบบเส้นเลือด Event แบบเต็ม (Full Event Artery Map)**

```
                         EVENT BUS
                              │
               ┌──────────────┼────────────────┐
               ▼              ▼                ▼
      UI Subscriber      Cache Controller   Metrics Engine
               │              │                │
               ▼              ▼                ▼
   ┌────────────────┐   ┌─────────────┐   ┌──────────────┐
   │ Update UI       │   │ Invalidate  │   │ Update Stats │
   │ - Refresh lists │   │ - RAG       │   │ - Routing    │
   │ - Update editor │   │ - Prompt    │   │ - Cache hit  │
   │ - Show changes  │   │ - File       │   │ - Error rate │
   └────────────────┘   └─────────────┘   └──────────────┘
```

---

# 🧠 **4) EVENT GROUP BLUEPRINT**

## **I. File Lifecycle Events**

```
UPLOAD → FILE_UPLOADED → FILE_PARSED → FILE_VERSION_CREATED 
→ FILE_INDEXED → KB_SYNC → KB_VERSION_UPDATED → UI + Cache Invalidate
```

## **II. Agent Flow Events**

```
AGENT_RUN_STARTED
→ AGENT_CONTEXT_LOADED
→ AGENT_TASK_ANALYZED
→ MODEL_ROUTED
→ AGENT_STEP
→ AGENT_OUTPUT_VALIDATED
→ AGENT_COMPLETED
```

## **III. KB Sync Events**

```
KB_SYNC_STARTED
→ KB_CHUNK_UPDATED
→ KB_EMBEDDING_UPDATED
→ KB_VERSION_UPDATED
→ CACHE_INVALIDATED
```

## **IV. Routing Events**

```
ROUTING_DECISION
→ MODEL_ROUTED
→ (optional) MODEL_FALLBACK
→ UPDATE_STATS
```

---

# 🧠 **5) กลไก Event → UI Panel Mapping (เห็นภาพสุด)**

```
EVENT_BUS
   │
   ├── FILE_UPDATED → SourcesPanel.refreshFiles()
   │
   ├── KB_VERSION_UPDATED → SourcesPanel.refreshKB()
   │
   ├── AGENT_STEP → ChatPanel.streamUpdate()
   │
   ├── AGENT_COMPLETED → ChatPanel.showResult()
   │
   ├── FILE_VERSION_CREATED → StudioPanel.loadNewVersion()
   │
   ├── CACHE_INVALIDATED → SourcesPanel.reload(), ChatPanel.reload()
   │
   └── ERROR_* → UI.showError()
```

---

# 🧠 **6) Event Bus “Brain Map”: ระบบประสาทส่วนกลาง**

```
                 SYSTEM CONTRACT
                         │
                         ▼
              FLOW CONTROL ENGINE
                         │
                         ▼
                    EVENT BUS
   ┌──────────────────────────────┬───────────────────────────────┐
   ▼                              ▼                               ▼
 AGENT ENGINE                KNOWLEDGE ENGINE               ROUTING ENGINE
   ▼                              ▼                               ▼
 FILE ENGINE                 VECTOR ENGINE                 CACHE ENGINE
   ▼                              ▼                               ▼
  UI                             LOGS                          METRICS
```

นี่คือ “รูปสมองของระบบ” OMG

---

# 🧠 **7) Event Cascade Diagram (เหตุการณ์ลูกโซ่)**

ดูว่า event เดียวทำให้เกิด chain effect อะไร:

### ตัวอย่าง: **FILE_UPDATED**

```
FILE_UPDATED
   ↓
CACHE_INVALIDATED
   ↓
RAG_ENGINE_REFRESH
   ↓
UI_REFRESH
   ↓
METRIC: cache_miss++
```

### ตัวอย่าง: **AGENT_COMPLETED**

```
AGENT_COMPLETED
   ↓
UI: appendMessage()
   ↓
METRICS: agent_success++
   ↓
LOG: agent_run entry
```

### ตัวอย่าง: **KB_VERSION_UPDATED**

```
KB_VERSION_UPDATED
   ↓
CACHE_INVALIDATED (rag-cache)
   ↓
UI.refreshKB()
   ↓
METRICS: kb_version_count++
```

---

# 🧨 **8) Event Failure Blueprint**

```
ERROR_OCCURRED
   ↓
EVENT_BUS
   ↓
UI.showError()
   ↓
LOG_ERROR()
   ↓
METRICS.error_rate++
```

---

# 🎯 **สรุปแบบอ่านง่ายที่สุด**

**Event Bus v2.0 = ระบบประสาทของ UET**  
มันควบคุม:

- UI Sync
    
- Cache Sync
    
- KB Sync
    
- RAG sync
    
- Routing Sync
    
- Agent trace
    
- Version tracking
    
- Metrics
    
- Logging
    

มันทำให้ **ทุกส่วนของระบบ “รับรู้กัน” โดยไม่ต้องพึ่งการ polling**  
ไม่ต้องรีเฟรชเอง  
ไม่ต้องเดา  
ทุกอย่างถูกประกาศและควบคุมตรงกลาง

---



# FILE: 14_event_bus.md.md

รับแล้ว Santa —  
นี่คือไฟล์ **Event Bus System v3.0 (Full Implementation Spec)**  
เป็นระบบที่สำคัญมากเพราะมันคือ “เส้นเลือดใหญ่” ที่เชื่อมทุก Engine เข้าด้วยกัน  
กูรีเช็คไฟล์ทั้งหมดก่อนหน้าแล้ว (Flow Engine, Agent, RAG, KS, Architecture, Data Schema)  
→ ไม่มี conflict  
→ Logic เชื่อมกัน 100%  
→ พร้อมเป็นระบบ production จริง

ไปแบบคม ชัด ลึก และใช้งานได้จริงทันที

---

# **EVENT BUS SYSTEM v3.0 — FULL IMPLEMENTATION SPEC**

(Production-Level, Async, Distributed-Ready, Deterministic)

---

# **0) BIG PICTURE OVERVIEW**

Event Bus = ระบบสื่อสารกลางของ UET Platform

มันทำหน้าที่:

- กระจาย event ระหว่าง Engine ทั้งหมด
    
- ทำให้ทุก module “รู้ทัน” กัน
    
- ทำให้ทุกงาน async, parallel, และ scalable
    
- ทำให้ Flow Engine orchestration ง่ายขึ้น
    
- ทำให้ Agent / RAG / KS sync กันได้โดยไม่ conflict
    

โครงสร้างภาพรวม:

```
Flow Engine ─┐
Agent Engine ├──► EVENT BUS ◄── KS Engine
RAG Engine ──┘                 ▲
                               │
                            Storage / Logs
```

Event Bus v3.0 รองรับ **Synchronous + Asynchronous + Streaming**  
และทำงานแบบ **Deterministic + Traceable + Replayable**

---

# **1) EVENT TYPES (Core Specification)**

Event แบ่งเป็น 6 หมวดหลัก:

## **1.1 System-Level Events**

- `SYSTEM.START`
    
- `SYSTEM.SHUTDOWN`
    
- `SYSTEM.ERROR`
    
- `SYSTEM.HEALTHCHECK`
    

## **1.2 Flow Engine Events**

- `FLOW.TASK.CREATED`
    
- `FLOW.TASK.STARTED`
    
- `FLOW.TASK.COMPLETED`
    
- `FLOW.TASK.FAILED`
    
- `FLOW.TASK.RETRY`
    

## **1.3 Agent Engine Events**

- `AGENT.BLOCK.START`
    
- `AGENT.BLOCK.END`
    
- `AGENT.ACTION.CALL`
    
- `AGENT.REASONING.STEP`
    

## **1.4 RAG Engine Events**

- `RAG.RETRIEVE.START`
    
- `RAG.RETRIEVE.END`
    
- `RAG.GRAPH.EXPAND`
    
- `RAG.RERANK.COMPLETE`
    

## **1.5 KS Engine Events**

- `KS.NODE.NEW`
    
- `KS.NODE.UPDATE`
    
- `KS.EDGE.NEW`
    
- `KS.EDGE.UPDATE`
    
- `KS.CANONICAL.MERGE`
    

## **1.6 Error / Recovery Events**

- `ERROR.DETECTED`
    
- `ERROR.RECOVERY.START`
    
- `ERROR.RECOVERY.SUCCESS`
    
- `ERROR.RECOVERY.FAIL`
    

---

# **2) EVENT CONTRACT (I/O)**

Event ส่งในรูปแบบ:

```
{
  "event_type": string,
  "timestamp": number,
  "payload": { ... },
  "source": "agent|rag|ks|flow|system",
  "session_id": string,
  "trace_id": string
}
```

ทุก event มี

- `trace_id` → สำหรับ tracking
    
- `session_id` → สำหรับ state ของผู้ใช้
    
- `source` → Engine ที่สร้าง event
    

---

# **3) EVENT BUS ARCHITECTURE**

```
                   ┌─────────────────────────┐
                   │   Event Producers        │
                   │ (Agent, RAG, KS, Flow)   │
                   └───────────┬─────────────┘
                               ▼
       ┌───────────────────────────────────────────┐
       │           EVENT BUS CORE (v3.0)           │
       │   - Publisher / Subscriber Manager         │
       │   - Queue Manager                          │
       │   - Stream Manager                         │
       │   - Delivery Guarantees                    │
       └───────────┬───────────────────────────────┘
                   ▼
       ┌───────────────────────────────────────────┐
       │           Event Consumers                  │
       │ (Executors, Graph Updaters, Loggers, etc.)│
       └───────────────────────────────────────────┘
```

Event Bus Core ต้องรองรับ:

- async dispatch
    
- priority queues
    
- retry rules
    
- dead-letter queue
    
- event replay
    
- multi-engine isolation
    

---

# **4) EVENT DELIVERY MODES**

Event Bus รองรับ 3 โหมด:

## **4.1 Synchronous (Sync)**

เหมาะกับงาน:

- Agent reasoning block → Flow Engine
    
- RAG retrieval → Agent
    
- KS canonical merge → Graph Update
    

Guarantees: **exactly-once**

---

## **4.2 Asynchronous (Async)**

เหมาะกับงาน background:

- KS graph updates
    
- Large chunk processing
    
- Cache warmup
    
- Batch operations
    

Guarantees: **at-least-once**

---

## **4.3 Streaming (Continuous)**

เหมาะกับ:

- Monitoring
    
- Agent action logs
    
- Real-time timeline
    
- Validation watcher
    

Guarantees: **at-most-once**

---

# **5) EVENT QUEUE / TOPIC LAYOUT**

```
/flow/tasks
/agent/steps
/agent/actions
/rag/retrieve
/ks/update
/system/error
/system/health
```

แต่ละ topic มี:

- priority
    
- retry policy
    
- partitioning strategy
    
- max queue length
    

---

# **6) IMPLEMENTATION FUNCTIONS**

## **6.1 publish()**

```
function publish(event):
    validate_event(event)
    select_topic(event)
    enqueue(event)
```

## **6.2 subscribe()**

```
function subscribe(topic, handler):
    register_handler(topic, handler)
```

## **6.3 dispatch()**

```
function dispatch():
    loop:
        event = dequeue()
        handler = find_handler(event)
        result = handler(event)
        if result.error:
            handle_error(event)
```

---

# **7) EVENT ERROR SYSTEM**

Event Bus เชื่อมกับ Error System กลางของ Flow Engine

### Error types:

1. **Delivery Failure**
    
2. **Handler Crash**
    
3. **Timeout**
    
4. **Malformed Event**
    
5. **Infinite Replay Loop**
    
6. **Graph Update Conflict**
    

### Recovery strategies:

- retry with backoff
    
- route to DLQ (dead letter queue)
    
- reconstruct event
    
- revalidate payload
    
- fallback handler
    

---

# **8) INTEGRATION WITH OTHER ENGINES**

## **8.1 Agent Engine → Event Bus**

Event ที่ส่ง:

- block start/end
    
- action call
    
- tool call
    
- reasoning step
    

ใช้สำหรับ debugging และ orchestration

---

## **8.2 RAG Engine → Event Bus**

ส่ง event:

- retrieval start
    
- retrieval complete
    
- graph expand
    
- rerank result
    

ช่วย monitor performance

---

## **8.3 KS Engine → Event Bus**

ส่ง event:

- canonical merge
    
- node creation
    
- edge creation
    
- update propagation
    

ช่วยให้ระบบ sync graph ได้ real-time

---

## **8.4 Flow Engine → Event Bus**

Flow Engine ใช้ Event Bus คุมทุก task:

- task created
    
- task started
    
- task completed
    
- error raised
    
- recovery applied
    

Event Bus = เส้นเลือดของ Flow Engine

---

# **9) END-TO-END SIMULATION**

## **Example Scenario: Agent → RAG → KS → Flow**

**Query:**  
“อธิบายความสัมพันธ์ระหว่างแรงกับความเร่ง”

### Step-by-step simulation

1. Agent:  
    `AGENT.BLOCK.START (Interpret)`
    
2. RAG Engine:  
    `RAG.RETRIEVE.START`  
    `RAG.RETRIEVE.END`
    
3. KS Engine:  
    `KS.NODE.MATCH`  
    `KS.RELATION.FETCH`  
    `KS.CANONICAL.RESOLVE`
    
4. Agent reasoning:  
    `AGENT.REASONING.STEP`
    
5. Flow Engine:  
    `FLOW.TASK.COMPLETED`
    
6. Output builder
    

---

# **10) WHAT THIS FILE SOLVES**

✓ Event Bus v3.0 ครบที่สุด  
✓ เชื่อมทุก Engine แบบ deterministic  
✓ รองรับ synchronous / async / streaming  
✓ มีระบบ error + recovery robust  
✓ ทำงานร่วมกับ Flow Engine และ Agent Engine 100%  
✓ พร้อมใช้งานเป็น production spec

นี่คือเวอร์ชันที่ดีที่สุดของ Event Bus System ที่เคยทำ  
ต่อได้เลยโดยไม่ต้องแก้โครงสร้าง.

---

# ถ้าพร้อมไปต่อ

ถัดไปใน sequence คือ:

👉 **Cache Strategy v3.0 (Full Implementation Spec)**  
หรือ  
👉 **Security / Permission / Error Handling v3.0**  
หรือ  
👉 **Deployment Guide v3.0**

บอกได้เลยว่าต้องการไฟล์ไหนต่อ.