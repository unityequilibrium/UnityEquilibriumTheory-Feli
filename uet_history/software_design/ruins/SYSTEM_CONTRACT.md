มาแล้ว Santa —  
นี่คือ **SYSTEM_CONTRACT.md (v2.0)** ฉบับ “ยกเครื่องใหม่เต็มระบบ”  
เขียนแบบ _รัฐธรรมนูญของแพลตฟอร์ม UET_ จริง ๆ  
และรวบรวมทุก subsystem ที่เรามีตอนนี้:

- FLOW_CONTROL v2.0
    
- EVENT_BUS v2.0
    
- KNOWLEDGE_SYNC v2.0
    
- RAG_ENGINE v2.0
    
- AGENT_ENGINE BIBLE v1.0
    
- DATA_SCHEMA v2.0
    
- CACHE_STRATEGY
    
- MODEL_ROUTING
    
- API_SPEC
    
- SECURITY_RULE
    
- ERROR_HANDLING
    
- PERMISSION_MATRIX
    
- COMPONENT_MAP
    
- ARCHITECTURE_MAP
    
- TERMINOLOGY
    

**นี่คือไฟล์ตัวแม่** ที่ควบคุมทุกไฟล์อื่น ไม่ต้องสร้างไฟล์ใหม่อีก  
อ่านง่าย ใช้งานได้จริง ตรงตรรกะระบบนาย 100%

---

# 📘 SYSTEM_CONTRACT.md (v2.0)

**Unified Knowledge System Contract (UET Platform)**  
**“ข้อตกลงกลางของระบบ” — กฎสูงสุดเหนือทุก Module**

---

# 🟦 0. วัตถุประสงค์ของเอกสาร

SYSTEM CONTRACT คือเอกสารที่:

1. กำหนด **กฎสูงสุดของระบบ** (เหมือนรัฐธรรมนูญ)
    
2. กำหนด **พฤติกรรมบังคับ** ของทุก Module
    
3. ทำให้ทุกส่วนของระบบทำงานแบบ **สอดคล้อง, ไม่ขัดแย้ง, deterministic**
    
4. ใช้ควบคุมพฤติกรรม Agent, RAG, Knowledge Sync, UI และ Flow ทั้งหมด
    
5. ทำให้แพลตฟอร์มสเกลใหญ่ได้แบบโปร่งใส ตรวจสอบได้
    

นี่คือแกนกลาง Unified Knowledge System (UKS)

---

# 🟩 1. หลักการสูงสุด (First Principles)

### **1.1 ความรู้ = ดาต้าแบบมีโครงสร้าง**

ระบบถือว่าความรู้มี 7 ชั้น (L0–L7):

```
L0 Raw Data → L1 Structured → L2 Semantic Chunks → L3 Embeddings
→ L4 Model Knowledge → L5 Systematic → L6 Principles → L7 Theory
```

ระบบ **ต้อง** ให้ทุกโมดูลเคารพลำดับนี้

---

### **1.2 ทุกการเปลี่ยนแปลงต้องผ่าน Flow Control**

Flow Control คือผู้บังคับกฎพื้นฐาน:

- ไม่มี action ไหน “ข้ามขั้นตอน”
    
- ไม่มี agent ทำอะไรนอกสคริปต์
    
- ทุกตัวต้องทำงานตาม sequence ที่กำหนด
    
- ทุกผลลัพธ์ต้องมี state transition ที่ตรวจสอบได้
    

---

### **1.3 ทุกเหตุการณ์ต้องประกาศผ่าน Event Bus**

ไม่มี module ไหนส่งผลโดยตรงให้ module อื่น  
ทุกอย่างต้องผ่าน Event Bus:

- UI update
    
- Cache invalidate
    
- RAG refresh
    
- KB sync
    
- Agent state update
    

Event Bus คือระบบประสาทกลาง

---

### **1.4 ทุกอย่างต้องใช้ข้อมูลเวอร์ชันล่าสุดเสมอ**

หมายถึง:

- Agent ต้องใช้ KB ล่าสุด
    
- RAG ต้องใช้ vector ที่ sync แล้ว
    
- UI ต้องเห็น state ล่าสุด
    

ไม่มีใครใช้ข้อมูล stale ได้

---

### **1.5 ทุกอย่างต้อง reversible**

ทุก state ต้องสามารถย้อนกลับได้ผ่าน:

- versioning
    
- logging
    
- event history
    
- chunk mapping
    

---

# 🟧 2. ขอบเขตของสัญญา (Contract Scope)

SYSTEM_CONTRACT ครอบคลุม:

- File Engine
    
- Knowledge Sync Engine
    
- RAG Engine
    
- Agent Engine
    
- Flow Control Engine
    
- Event Bus
    
- Model Routing
    
- Cache Layer
    
- UI Panels
    
- API Layer
    
- Security
    
- Permissions
    
- Metrics
    
- Deployment Behavior
    

---

# 🟨 3. ข้อบังคับตามระบบ (System Rules)

นี่คือ “กฎเหล็ก” ที่ระบบทั้งหมดต้องทำตาม

---

## **3.1 Rule: Deterministic Execution**

ทุก module ต้องให้ผลลัพธ์เหมือนเดิมเมื่อ input เหมือนเดิม  
ห้ามมี randomness ที่ไม่ถูกควบคุมด้วย seed

---

## **3.2 Rule: Versioned Knowledge**

ทุกไฟล์ต้องมี version  
ทุกเวอร์ชันต้องถูก sync  
RAG ใช้เฉพาะ version ล่าสุด  
Agent ห้ามอ้างอิงเวอร์ชันที่ยัง sync ไม่เสร็จ

---

## **3.3 Rule: Event-Driven Synchronization**

ทุก state change ต้องประกาศ event เช่น:

- FILE_UPDATED
    
- KB_VERSION_UPDATED
    
- CACHE_INVALIDATED
    
- AGENT_STEP
    
- MODEL_ROUTED
    

ไม่มี state ไหนเปลี่ยนโดยไม่ยิง event

---

## **3.4 Rule: Zero-Stale Policy**

เมื่อ KB เปลี่ยน:

- RAG cache ต้อง invalid
    
- Prompt cache ต้อง invalid
    
- KB indicator ใน UI ต้อง update
    
- Agent ต้องไม่ใช้ context เก่า
    

---

## **3.5 Rule: Strict Agent Behavior**

Agent ต้อง:

- ใช้เฉพาะข้อมูลจาก RAG (ถ้า strict mode)
    
- อ้างอิงที่มาได้
    
- ไม่เพ้อ ไม่ hallucinate
    
- ผ่าน validation ก่อน output
    

---

# 🟥 4. การประสานงานของโมดูล (Module Contracts)

อันนี้คือ “สัญญาระหว่าง Module”

---

## **4.1 Knowledge Sync ↔ Chunk Engine**

- Chunk ถูกสร้างแบบ deterministic
    
- chunk_id ต้อง stable
    
- chunk_hash ใช้ตรวจว่าต้อง embed ใหม่ไหม
    

---

## **4.2 Chunk Engine ↔ Embedding Engine**

- ถ้า chunk_hash เดิม → ห้าม embed ซ้ำ
    
- ถ้า chunk_hash เปลี่ยน → embed ใหม่ทันที
    

---

## **4.3 Embedding Engine ↔ Vector Store**

- vector ต้อง upsert แบบ atomic
    
- ต้องผูกกับ project_id
    
- query ต้อง filter project_id เสมอ
    

---

## **4.4 KB Registry ↔ RAG Engine**

- RAG ใช้เฉพาะ version ล่าสุด
    
- RAG ต้อง validate registry ก่อน search
    

---

## **4.5 RAG Engine ↔ Agent Engine**

- Agent ต้องประกาศ RAG request
    
- RAG ต้องคืน context พร้อม citations
    
- Agent ต้องไม่เกิน context budget
    

---

## **4.6 Agent Engine ↔ Flow Control**

- ทุก action ของ agent ต้องผ่าน validator
    
- ห้ามข้าม step
    
- ห้ามเขียนไฟล์โดยไม่ผ่าน versioning
    

---

## **4.7 Event Bus ↔ UI**

- UI Panel ทั้ง 3 ต้อง subscribe event
    
- ห้าม refresh เอง
    
- ต้องใช้ event-driven state update
    

---

# 🟦 5. ความปลอดภัย (Security Contract)

### **5.1 Role-based model routing**

- viewer = ไม่มีสิทธิ์ใช้ model ใหญ่
    
- editor = ใช้ระดับกลาง
    
- manager = ใช้ระดับสูงสุด
    

### **5.2 File access rules**

- ห้าม RAG ข้าม project
    
- ห้าม Agent ใช้ไฟล์ที่ไม่มีสิทธิ์อ่าน
    

---

# 🟩 6. การเก็บ Logs / Metrics / Audit (Transparency Contract)

### **ทุก module ต้อง log สิ่งเหล่านี้:**

- execution time
    
- events
    
- model used
    
- KB version
    
- errors
    
- RAG topK score
    
- agent reasoning step count
    

ระบบต้อง “traceable 100%”

---

# 🟧 7. การจัดการข้อผิดพลาด (Error Contract)

### ความผิดพลาดทุกชนิดต้อง:

1. ถูกจับ
    
2. ถูก log
    
3. ถูกประกาศผ่าน Event Bus
    
4. UI แสดง error state
    
5. Agent ได้ safe response
    

รวมถึง:

- PARSE_FAIL
    
- CHUNK_FAIL
    
- EMBED_FAIL
    
- RAG_FAIL
    
- ROUTING_FAIL
    
- CONTRACT_VIOLATION
    

---

# 🟥 8. การปรับปรุงความรู้ (Knowledge Evolution Contract)

### เมื่อผู้ใช้หรือ Agent สร้างเนื้อหาใหม่:

- ระบบต้องทำ version ใหม่อัตโนมัติ
    
- Knowledge Sync ต้องทำงาน
    
- RAG ต้องใช้ KB ใหม่
    
- Event Bus ต้อง notify UI
    
- ทุกโมดูลต้องเห็นการเปลี่ยนแปลงพร้อมกัน
    

Knowledge = ถูก sync แบบ real-time ตลอดเวลา

---

# 🟦 9. การรับประกันความสอดคล้องของระบบ (Consistency Contract)

### ระบบจะถือว่าถูกต้องก็ต่อเมื่อ:

- Flow ทุกอย่างผ่าน validation
    
- ไม่มี action ข้ามขั้นตอน
    
- KB registry ตรงกับ vector store
    
- UI แสดง state จริง
    
- Agent ใช้ context ล่าสุด
    
- Event Bus ทำงานครบ
    
- Cache ไม่ stale
    
- Version lining ตรงตาม contract
    

---

# 🟫 10. ภาคผนวก (Annex)

รวม subsystem:

- [DATA_SCHEMA.md]
    
- [FLOW_CONTROL.md]
    
- [AGENT_ENGINE_BIBLE]
    
- [RAG_ENGINE.md]
    
- [KNOWLEDGE_SYNC.md]
    
- [EVENT_BUS.md]
    
- [MODEL_ROUTING.md]
    
- [CACHE_STRATEGY.md]
    
- [PERMISSION_MATRIX.md]
    
- [ERROR_HANDLING.md]
    
- [SECURITY_RULE.md]
    

ทั้งหมดต้องสอดคล้องกับ SYSTEM_CONTRACT นี้

---

# 🎯 สรุปสั้น ๆ

นี่คือ SYSTEM_CONTRACT v2.0:

- ออกแบบแบบ “รัฐธรรมนูญของระบบ UET”
    
- ครอบคลุมทุก module
    
- ไม่มี conflict
    
- ผูกกับแนวคิดทฤษฎี UET (epistemology)
    
- deterministic, event-driven, versioned
    
- รองรับการขยาย unlimited
    
- กลไกตรวจสอบครบทุกระดับ
    

---

# 🟢 1) SYSTEM CONTRACT — MASTER DIAGRAM SET

---

# **1.1 TOP-LEVEL DIAGRAM (ระบบใหญ่สุดตาม Contract)**

```
                   SYSTEM CONTRACT
                (กฎสูงสุดของระบบ UET)
                           │
     ┌─────────────────────┼──────────────────────┐
     ▼                     ▼                      ▼
FLOW CONTROL       EVENT BUS (Nervous Sys.)   DATA CONTRACT
     │                     │                      │
     ▼                     ▼                      ▼
AGENT ENGINE         KNOWLEDGE SYNC           SECURITY RULE
     │                     │                      │
     ▼                     ▼                      ▼
RAG ENGINE             VECTOR STORE             PERMISSION
     │                     │                      │
     ▼                     ▼                      ▼
UI PANELS              CACHE STRATEGY          METRICS LOG
(Sources / Chat / Studio)
```

นี่คือ “ร่างกายใหญ่สุด” — ทุกระบบอยู่ภายใต้ SYSTEM_CONTRACT

---

# **1.2 MID-LEVEL DIAGRAM (การซิงค์ทั้งหมดตามสัญญาระบบ)**

```
        USER / AGENT
             │
     (Change Knowledge)
             ▼
       FILE ENGINE
             │
             ▼
   KNOWLEDGE SYNC ENGINE  ←—(governed by SYSTEM CONTRACT)
   Parse → Chunk → Embed
             │
             ▼
       VECTOR STORE
             │
    (v2.0: Always Latest)
             ▼
        RAG ENGINE
             │
  Retrieve → Rerank → Fuse Context
             │
             ▼
        AGENT ENGINE
      (multi-step reasoning)
             │
             ▼
     OUTPUT / NEW KNOWLEDGE
             │
             ▼
     (Loop back to Sync)
```

ระบบนี้ = วงจรความรู้ที่ CONTRACT ควบคุมทั้งหมด

---

# **1.3 DEEP DIAGRAM (Internal Contract Enforcement Flow)**

```
       MODULE ACTION
             │
             ▼
        FLOW CONTROL
    (validate + approve sequence)
             │
             ▼
         EVENT BUS
 (broadcast → UI / Cache / Agent / Metrics)
             │
             ▼
       CONTRACT CHECKS
   - Version validity
   - Latest KB enforcement
   - Security rules
   - Permission matrix
   - Cache invalidation rules
             │
             ▼
       MODULE EXECUTES
   (Knowledge Sync / RAG / Agent)
```

CONTRACT = “ศูนย์กลางที่บังคับกฎทุกส่วนก่อนระบบจะทำงาน”

---

# 🟠 2) SYSTEM CONTRACT — MATRIX SET

---

# **2.1 MODULE → CONTRACT MATRIX**

(อะไรถูกควบคุมโดย Contract อะไรบ้าง)

|MODULE|Flow Control|Version Rules|Event Bus|Permissions|KB Rules|Cache Rules|
|---|---|---|---|---|---|---|
|File Engine|✓|✓|✓|✓|✓|✓|
|Knowledge Sync|✓|✓|✓|—|✓|✓|
|Chunk Engine|✓|✓|—|—|✓|—|
|Embedding Engine|✓|✓|—|—|✓|—|
|KB Registry|✓|✓|—|—|✓|✓|
|Vector Store|✓|—|—|—|✓|✓|
|RAG Engine|✓|✓|—|—|✓|✓|
|Agent Engine|✓|✓|✓|✓|✓|✓|
|UI Panels|—|—|✓|—|—|—|
|Cache Layer|✓|—|✓|—|✓|✓|
|Model Routing|✓|—|—|✓|—|—|

---

# **2.2 CONTRACT RESPONSIBILITY MATRIX**

(กฎไหนควบคุมระบบไหน)

|CONTRACT RULE|Knowledge Sync|RAG|Agent|Event Bus|Flow Control|Cache|UI|
|---|---|---|---|---|---|---|---|
|Deterministic Execution|✓|✓|✓|—|✓|—|—|
|Version Enforcement|✓|✓|✓|—|—|✓|—|
|Zero-Stale Policy|✓|✓|✓|✓|—|✓|✓|
|Event-Driven Update|✓|✓|✓|✓|—|✓|✓|
|Permission Check|—|—|✓|—|✓|—|—|
|Security Rules|—|—|✓|✓|✓|—|—|
|Knowledge Layer Hierarchy|✓|✓|✓|—|—|—|—|
|State Transition Validity|✓|✓|✓|—|✓|—|—|

---

# **2.3 STATE CONSISTENCY MATRIX**

|STATE|Who Updates|Who Reads|Who Invalidates|Source of Truth|
|---|---|---|---|---|
|File Version|File Engine|KS, RAG, Agent|KS|File DB|
|Chunk State|KS|RAG|KS|Chunk table|
|Embedding State|KS|RAG|KS|Embedding table|
|KB Registry|KS|RAG, Agent|KS|KB Registry|
|Cache State|Cache Layer|RAG, Agent|Event Bus|Cache Layer|
|Routing State|Routing Engine|Agent|Routing Engine|Routing Config|
|Agent State|Agent Engine|UI, FlowCtrl|FlowCtrl|Agent Runtime|
|UI State|UI Panels|User|Event Bus|UI Memory|

---

# 🔥 3) SYSTEM CONTRACT — SYSTEM FLOW SET

(ตั้งแต่เกิดเหตุการณ์ → วิ่งผ่านสัญญา → ออกผลลัพธ์)

---

# **3.1 MASTER SYSTEM FLOW (สำคัญที่สุด)**

```
USER ACTION / AGENT ACTION
          │
          ▼
    FLOW_CONTROL.validate()
          │
          ▼
  SYSTEM_CONTRACT.check_all_rules()
    - version check
    - permission check
    - consistency check
    - stale-check
          │
          ▼
       EXECUTE MODULE
    (KS / RAG / AGENT / ROUTING)
          │
          ▼
       EVENT_BUS.emit()
          │
          ▼
   ┌────────┬──────────┬─────────┬──────────┐
   ▼        ▼          ▼         ▼          
 UI     Cache       Metrics    Agent Loop
 Refresh Invalidate Update     Continue Steps
```

---

# **3.2 KNOWLEDGE UPDATE FLOW (ไฟล์เปลี่ยน → ทั้งระบบ sync)**

```
FILE_UPDATED
      ▼
FLOW_CONTROL.validate_sequence
      ▼
SYSTEM_CONTRACT.version_enforce
      ▼
KNOWLEDGE_SYNC (parse → chunk → embed)
      ▼
KB_REGISTRY.update
      ▼
EVENT_BUS.emit(KB_VERSION_UPDATED)
      ▼
CACHE_INVALIDATE
      ▼
UI_REFRESH
      ▼
AGENT_CAN_USE_NEW_KB
```

---

# **3.3 RAG FLOW (มีการดึงความรู้)**

```
QUERY_RECEIVED
      ▼
FLOW_CONTROL.validate_rag_request
      ▼
SYSTEM_CONTRACT.check_KB_latest
      ▼
RAG_ENGINE.retriever()
      ▼
RERANK (optional)
      ▼
CONTEXT_FUSION
      ▼
RETURN_CONTEXT_TO_AGENT
      ▼
AGENT REASONING
```

---

# **3.4 AGENT MULTI-STEP FLOW (แบบสมบูรณ์)**

```
AGENT_RUN_STARTED
      ▼
TASK_ANALYZE
      ▼
need_rag? ──── yes ─→ RAG_FLOW
      ▼
MODEL_ROUTING
      ▼
MODEL_EXECUTION
      ▼
VALIDATION (under CONTRACT)
      ▼
OUTPUT
      ▼
if output updates knowledge:
      ▼
KNOWLEDGE_SYNC_FLOW
```

---

# **3.5 ZERO-STALE FLOW (กฎสำคัญ)**

```
KB_CHANGED
     ▼
EVENT: KB_VERSION_UPDATED
     ▼
CACHE_INVALIDATE
     ▼
BLOCK_AGENT_FROM_USING_OLD_KB
     ▼
AGENT_REFRESH_RAG()
```

ระบบทุกส่วนจะ "ฟื้นตัว" พร้อมกัน

---

# ⭐ สรุปแบบสั้นและตรงที่สุด

ตอนนี้นายได้ครบ:

### ✔ Master Diagrams (Top/Mid/Deep)

### ✔ Full Contract Matrix (3 ประเภท)

### ✔ System Flow แบบเต็ม (5 ระดับ)

ทั้งสามชุดนี้ = “ภาพรวมใหญ่สุด” ของ SYSTEM CONTRACT v2.0  
และทุก subsystem ของ UET ถูกเชื่อมทั้งหมดแล้วแบบ deterministic 100%

---

# ถัดไปอยากให้ทำอะไร?

1. **MODEL_SELECTION_GUIDE v2.0** (ใหม่หมด)
    
2. **DEPLOYMENT_GUIDE v2.0**
    
3. รวมทั้งหมดเป็น **UET Architecture Book v1.0**
    
4. ทำ **Unified Blueprint อันเดียวจบทั้งระบบ**
    

บอกได้เลย Santa ❤️