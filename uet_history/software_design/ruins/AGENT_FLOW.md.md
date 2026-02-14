โอเค Santa —  
นี่คือ **AGENT_FLOW.md v2.0 (ยกเครื่องใหม่ระดับสูงสุด)**  
ฉันรวบรวมข้อมูลจากทุกไฟล์ที่นายมี:

- SYSTEM_CONTRACT v2.0
    
- FLOW_CONTROL v2.0
    
- MODEL_ROUTING
    
- DATA_SCHEMA
    
- KB_SYNC
    
- RAG ENGINE
    
- CACHE STRATEGY
    
- EVENT BUS
    
- ERROR HANDLING
    
- UI Panels
    
- DEPLOYMENT GUIDE
    

แล้วสร้างเป็น **Agent Flow รุ่นใหม่แบบ deterministic 100%**  
ที่ “คุม AI ได้เหมือนคุมระบบจริง” ไม่มั่ว ไม่หลุด ไม่ผิด state

นี่คือ **หัวใจของระบบใหม่ UET Platform**  
(โคตรชัด, กระชับ, สมบูรณ์ที่สุด)

---

# 📘 **AGENT_FLOW.md (v2.0)**

**UET Platform — Unified Agent Execution Flow (v2.0)**

---

# ⭐ 0. เป้าหมายของ Agent Flow v2.0

- ทำให้ Agent ทำงาน “เป็นระบบ” ไม่สุ่ม, ไม่เดา
    
- ผูกกับ Model Routing, KB, RAG, Flow Control, State Machine
    
- ควบคุมการทำงานแบบ deterministic
    
- ป้องกันปัญหา hallucination / cross-project leak
    
- ให้ Agent ทำงานได้ถูกต้อง เสถียร และตรวจสอบได้ 100%
    

> **Agent v2.0 = Operating System ของงาน AI บน UET**

---

# ⭐ 1. โครงสร้าง Agent Engine

```
AGENT ENGINE consists of:
1. Context Loader
2. Task Analyzer
3. Model Router
4. Executor
5. Validator
6. Safety Filter
7. State Controller
8. Event Dispatcher
9. Logger
```

เป็นโมดูลที่ทำงานแบบ pipeline ต่อกันโดยห้ามข้ามขั้นตอน

---

# ⭐ 2. Agent Main Flow (Flow หลักที่สุด)

```
AGENT_RUN
→ LOAD_CONTEXT
→ TASK_ANALYZE
→ ROUTING_DECISION
→ EXECUTE_MODEL
→ VALIDATE_OUTPUT
→ SAFETY_FILTER
→ POST_PROCESS
→ LOG
→ EMIT_EVENTS
→ RESPOND
```

นี่คือแกนกลางของ agent v2.0 ทุกประเภท

---

# ⭐ 3. State Machine (Agent FSM)

Agent ต้องเดินตาม state ต่อไปนี้เท่านั้น:

```
IDLE
→ CONTEXT_LOAD
→ ANALYZE
→ ROUTING
→ EXECUTION
→ VALIDATION
→ SAFETY
→ FINALIZE
→ EMIT_EVENTS
→ RETURN_RESULT
→ RESET
```

**ห้ามข้าม state ใด ๆ**  
**ห้ามย้อนกลับ state**  
**ห้ามข้าม routing**

---

# ⭐ 4. Step-by-step (รายละเอียดแต่ละขั้น)**

---

## **STEP 1 — LOAD_CONTEXT**

โหลดบริบททั้งหมดที่ agent ต้องใช้:

- ไฟล์ในโปรเจกต์
    
- instruction จากระบบ
    
- panel mode (chat/studio/system)
    
- user role
    
- history context
    
- KB context (ถ้าจำเป็น)
    

```
INPUT:
  user input
  project_id
  mode
OUTPUT:
  agent.context
```

---

## **STEP 2 — TASK_ANALYZE**

Agent ตรวจสอบประเภทงาน:

- generate
    
- rewrite
    
- reasoning
    
- explain
    
- code
    
- math
    
- rag_needed?
    
- file-edit?
    
- studio-mode?
    

```
agent.task = {
   type: "generate",
   need_rag: boolean,
   complexity: low|medium|high
}
```

---

## **STEP 3 — ROUTING_DECISION**

ใช้ Model Routing Engine v2.0

เอาปัจจัย:

- task type
    
- prefix intent
    
- user role
    
- token size
    
- rag requirement
    
- cost
    
- performance
    
- override rules
    
- fallback rules
    

```
agent.model = routing_engine.select(agent.task)
```

Event:  
`MODEL_ROUTED`

---

## **STEP 4 — EXECUTE_MODEL**

เรียก LLM ที่ถูก routing มา

การทำงาน:

- สร้าง prompt ที่ผ่าน contract
    
- ผนวกรวม context
    
- integrate RAG (ถ้า need_rag)
    
- send to model provider
    
- handle timeout / retry / fallback model
    

```
agent.output = llm.generate(agent.prompt)
```

Event:  
`AGENT_STEP_EXECUTED`

---

## **STEP 5 — VALIDATE_OUTPUT**

ตรวจสอบความถูกต้องตามระบบ:

- JSON schema (ถ้าจำเป็น)
    
- safety
    
- hallucination guard
    
- file-format guard
    
- no forbidden content
    
- no cross-project content
    
- no OS-level commands
    

```
if !valid → ERROR_HANDLER
```

---

## **STEP 6 — SAFETY_FILTER**

ตรวจสอบ:

- toxic content
    
- harmful instructions
    
- non-deterministic output
    
- leakage
    

ถ้าผ่าน → ต่อ  
ถ้าไม่ผ่าน → แก้ & regenerate (ตาม policy)

---

## **STEP 7 — POST_PROCESS**

หลังจาก validate แล้ว:

- รวม context (studio)
    
- แพ็คผลให้ UI
    
- สร้าง citation (ถ้ามี RAG)
    
- สร้าง diff (ถ้าเป็น file-edit mode)
    

---

## **STEP 8 — LOG**

บันทึกทุกอย่างลง:

- AGENT_RUN
    
- ROUTING_LOG
    
- EVENT_LOG
    
- ERROR_LOG (ถ้ามี)
    

---

## **STEP 9 — EMIT_EVENTS**

ส่ง event:

- AGENT_STEP
    
- MODEL_ROUTED
    
- FILE_UPDATED (ถ้ามี)
    
- KB_VERSION_UPDATED (ถ้ามี)
    
- CACHE_INVALIDATED (ถ้ามี)
    

---

## **STEP 10 — RESPOND**

คืนผลลัพธ์แบบ unified schema:

```
{
  success: true,
  output: ...,
  model: ...,
  tokens: { in, out },
  runId: ...
}
```

---

# ⭐ 5. Multi-step Agent Flow (Chain-mode)

สำหรับงานยาว เช่นทำสรุป, rewrite หลายไฟล์, แก้ code

```
STEP_1: EXECUTION
↓
STEP_2: VALIDATION
↓
STEP_3: DECISION
    if continue → loop
    if finished → finalize
↓
FINALIZE
```

Agent จะทำหลายรอบได้ในตัวเอง  
แต่ **ต้องผ่าน Validation ทุกครั้ง**

---

# ⭐ 6. RAG-Integrated Agent Flow

ถ้า task ต้องใช้ข้อมูลจากการค้นหา:

```
LOAD_CONTEXT
↓
RAG_QUERY
↓
RELEVANCE_CHECK
↓
PROMPT_FUSION (รวมผล RAG เข้ากับ prompt)
↓
EXECUTE_MODEL
```

แบบนี้ agent จะ “รู้จริง” ไม่เพ้อ

---

# ⭐ 7. Studio Agent Flow (ใช้กับ Canvas)

```
EDIT_REQUEST
→ LOAD_FILE_VERSION
→ ROUTING
→ EXECUTE_MODEL
→ VALIDATE_OUTPUT
→ UPDATE_FILE_VERSION
→ KB_SYNC
→ CACHE_INVALIDATE
→ EMIT(FILE_UPDATED)
→ RESPOND
```

นี่คือโหมดแก้ไฟล์อย่างปลอดภัยแบบ deterministic

---

# ⭐ 8. Error Flow (สำคัญที่สุด)

```
EXECUTION_FAIL
→ ERROR_HANDLER
→ UNIFIED_ERROR_SCHEMA
→ EMIT(ERROR_EVENT)
→ ROLLBACK
→ SAFE_RESPONSE
```

Agent ไม่ทำให้ระบบพัง  
ผิด = ส่ง event + error กลับ UI แบบปลอดภัย

---

# ⭐ 9. Agent Restrictions (ข้อจำกัด)

- อ่านเฉพาะไฟล์ในโปรเจกต์
    
- เขียนเฉพาะใน Studio Panel
    
- ห้าม override Routing ถ้า role ไม่ถึง
    
- ห้าม generate file binary
    
- ห้ามใช้คำสั่ง OS
    
- ห้ามเข้าถึง Global KB
    
- ห้ามข้าม Validation
    

---

# ⭐ 10. Diagram — Agent Flow Blueprint (ภาพใหญ่)

```
USER_INPUT
   ↓
UI_PANEL
   ↓
API /agent/run
   ↓
FLOW_CONTROL
   ↓
LOAD_CONTEXT
   ↓
TASK_ANALYZE
   ↓
ROUTING_ENGINE
   ↓
EXECUTE_MODEL
   ↓
VALIDATE_OUTPUT
   ↓
SAFETY_FILTER
   ↓
POST_PROCESS
   ↓
LOG
   ↓
EMIT_EVENTS
   ↓
RESPOND
```

นี่คือหัวใจใหม่ของ Agent v2.0

---

# 🎯 สรุปแบบเข้าใจง่ายที่สุด

**Agent v2.0 = ระบบ AI ที่มีการควบคุมระดับ OS**

- deterministic
    
- predictable
    
- controllable
    
- safe
    
- traceable
    
- event-driven
    
- routing-aware
    
- versioned
    
- tied to KB
    
- tied to permission
    

เป็นการอัปเกรดครั้งใหญ่ที่สุดของระบบ UET

---

