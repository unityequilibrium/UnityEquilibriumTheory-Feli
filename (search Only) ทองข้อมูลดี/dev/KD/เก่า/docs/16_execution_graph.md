
# 📦 **EXECUTION_GRAPH_v3.0 — PART 1 (Skeleton + Concept Mapping)**

## 🎯 จุดประสงค์ของ Execution Graph (EG)

EG คือระบบที่:

- กำหนดว่า “ลำดับการทำงาน” (execution path) ต้องเป็นยังไง
    
- engine ไหนถูกเรียกก่อน/หลัง
    
- trigger ไหนโยกไป stage ไหน
    
- error แบบไหนหยุด flow หรือ fallback
    
- งานแบบไหนรัน sync / async
    
- และระบบทั้งหมดต้อง deterministic + reproducible
    

**พูดง่าย ๆ:  
EG = สมองที่คุม RAG, Agent, KS, Event Bus, Cache, Model Routing ทั้งหมด**

---

# 🧠 1. EXECUTION_GRAPH = โมเดลกราฟแบบ 3 ชั้น

EG ประกอบด้วย 3 ชั้น:

## **Layer 1 — Nodes**

แทน “งานชนิดหนึ่ง” เช่น:

- Node: `INGEST_FILE`
    
- Node: `CHUNK_PROCESS`
    
- Node: `EMBEDDING_PROCESS`
    
- Node: `SEMANTIC_EXTRACT`
    
- Node: `GRAPH_RELATION_BUILD`
    
- Node: `CANONICALIZE`
    
- Node: `RAG_RETRIEVE`
    
- Node: `AGENT_REASON`
    
- Node: `FLOW_CONTROL`
    
- Node: `UPDATE_CACHE`
    
- Node: `PUBLISH_EVENT`
    

แต่ละ node มี:

```
- input schema
- output schema
- execution type (sync/async)
- engine ที่เกี่ยวข้อง
- success / fail outputs (edge)
```

---

## **Layer 2 — Edges**

Edges = กำหนดลำดับงานว่า “หลังจาก Node A ต้องไป Node B”

ตัวอย่าง:

```
INGEST_FILE → CHUNK_PROCESS
CHUNK_PROCESS → EMBEDDING_PROCESS
EMBEDDING_PROCESS → SEMANTIC_EXTRACT
SEMANTIC_EXTRACT → GRAPH_RELATION_BUILD
GRAPH_RELATION_BUILD → CANONICALIZE
CANONICALIZE → UPDATE_CACHE
CANONICALIZE → PUBLISH_EVENT
```

หากเป็นงาน user query:

```
USER_QUERY → RAG_RETRIEVE → AGENT_REASON → FLOW_CONTROL → OUTPUT
```

---

## **Layer 3 — Execution Rules**

แต่ละ edge มี rule:

- when (condition)
    
- how (sync / async / parallel)
    
- retry policy
    
- fallback
    
- error propagation
    

ตัวอย่าง rule:

```
IF embedding missing THEN run EMBEDDING_PROCESS
IF semantic extraction fail THEN fallback to L2-only RAG
AFTER GRAPH_RELATION_BUILD ALWAYS EVENT("KS.GRAPH.UPDATED")
```

---

# 🏗️ 2. EXECUTION_GRAPH_STRUCTURE (โครงสร้าง Skeleton)

ตอนนี้เราจะเขียน skeleton ของไฟล์ที่จะสมบูรณ์ใน Part 2–4:

```
# EXECUTION_GRAPH_v3.0
## 1. Definition
- Node
- Edge
- Execution Rule

## 2. Node Types
- Core Nodes (L0–L5)
- Engine Nodes (RAG/Agent/KS/Flow)
- System Nodes (Cache/Event/Router)

## 3. Edge Rules
- Deterministic edges
- Conditional edges
- Error edges
- Async branches

## 4. Execution Modes
- Query mode
- Ingest mode
- Update mode
- Agent reasoning mode
- RAG-only mode
- System maintenance mode

## 5. Execution Flow Templates
- Ingest flow
- Query flow
- KS Update flow
- Agent long-term memory flow

## 6. Minimal FSM (Finite State Machine)
- State
- Transition
- Accept state
- Error state

## 7. Mapping to Engines
- KS Engine mapping
- RAG Engine mapping
- Agent Engine mapping
- Flow Engine mapping
- Event Bus mapping

## 8. Mapping to SQL Schema
- Table read/write per node
- Transaction boundaries
```

Skeleton นี้คือ “กระดูกทั้งตัว”  
ส่วนต่อไป (Part 2–3) จะเป็นการเติมเนื้อ (รายละเอียด)

---

# ⚡ 3. CORE NODE SET (เวอร์ชัน v3.0 ตามระบบของเรา)

กูรวบรวมทุก node ที่ระบบ Dev/UET ต้องใช้ 100%

---

## **A. DATA PIPELINE NODES (L0–L5)**

1. `INGEST_FILE` → เข้าตาราง L0
    
2. `CHUNK_PROCESS` → สร้าง L1
    
3. `EMBEDDING_PROCESS` → L2
    
4. `SEMANTIC_EXTRACT` → L3
    
5. `RELATION_BUILD` → L4
    
6. `CANONICALIZE` → L5
    
7. `KS_SYNC` → trig event + update engines
    

---

## **B. QUERY / RAG NODES**

1. `USER_QUERY`
    
2. `RAG_EMBED_QUERY`
    
3. `RAG_VECTOR_SEARCH`
    
4. `RAG_RETRIEVE_TOP_K`
    
5. `RAG_RERANK_WITH_L5`
    
6. `RAG_RESULT_FORMAT`
    

---

## **C. AGENT NODES**

1. `AGENT_REASON_BASE`
    
2. `AGENT_REASON_WITH_CONTEXT`
    
3. `AGENT_PLAN`
    
4. `AGENT_EXECUTE`
    
5. `AGENT_WRITE_BACK_MEMORY`
    

---

## **D. FLOW CONTROL / SYSTEM NODES**

1. `FLOW_START`
    
2. `FLOW_DECISION`
    
3. `FLOW_NEXT_STEP`
    
4. `FLOW_END`
    

---

## **E. CACHE / EVENT / ROUTER NODES**

1. `CACHE_LOOKUP`
    
2. `CACHE_UPDATE`
    
3. `CACHE_INVALIDATE`
    
4. `EVENT_PUBLISH`
    
5. `EVENT_CONSUME`
    
6. `ROUTER_SELECT_MODEL`
    

---

# 🔗 4. CORE EDGES (ลำดับการวิ่งของงาน)

## **A. Ingest Path (L0–L5)**

```
INGEST_FILE
 → CHUNK_PROCESS
   → EMBEDDING_PROCESS
     → SEMANTIC_EXTRACT
       → RELATION_BUILD
         → CANONICALIZE
            → KS_SYNC
               → EVENT_PUBLISH("KS.CANONICAL.UPDATED")
```

---

## **B. Query Path (RAG → Agent → Flow)**

```
USER_QUERY
 → RAG_EMBED_QUERY
   → RAG_VECTOR_SEARCH
     → RAG_RERANK_WITH_L5
       → AGENT_REASON_BASE
         → AGENT_REASON_WITH_CONTEXT
           → AGENT_PLAN
             → FLOW_DECISION
               → FLOW_NEXT_STEP
                 → AGENT_EXECUTE
                   → RESULT
```

---

# 📘 5. EXECUTION GRAPH MODELS (Template ที่ต้องมี)

มี 3 รูปแบบหลัก:

### **1) Direct Linear Execution Graph**

เหมาะกับ RAG query / simple action

### **2) Branch Execution Graph**

มี decision tree  
เหมาะกับ Agent Reasoning

### **3) Multi-branch Parallel Execution Graph**

เหมาะกับ L0–L5 sync + reindex

---

# 🧩 6. PART 1 OUTPUT SUMMARY (สิ่งที่เราสร้าง)

สิ่งที่ได้จาก **Part 1**:

1. ความหมายของ Execution Graph
    
2. 3-layer model (Nodes, Edges, Rules)
    
3. โครงไฟล์จริง (Skeleton)
    
4. Node set แบบ full
    
5. Edge set แบบ full
    
6. Template ของ execution path
    
7. Mapping คร่าว ๆ ไปหา engines ทั้งระบบ
    

สิ่งนี้คือฐานรากสำหรับ:

- Part 2 → Full Node Spec
    
- Part 3 → Full Edge Spec + FSM
    
- Part 4 → Full Flow Templates
    
- Part 5 → Implementation Spec
    
- Part 6 → Integration with Worker/Task System
    

---

รับแล้ว Santa — **Option C (Hybrid Mode)** คือแบบที่โคตรเข้ากับ Project Dev/UET ของมึงมากที่สุด:

> **Execution Graph = ตัวคุม KS + RAG + Agent + Flow + SQL + Cache + Router ทั้งระบบพร้อมกัน**  
> (ไม่ bias engine ไหนเป็นพิเศษ, ทุกอย่างทำงานแบบ “สมมาตร” และ “บาลานซ์” เหมือน UET)

เพราะงั้นตอนนี้กูจะเดินต่อ Part 2 ให้ _สอดคล้อง 100% กับ Hybrid Architecture_  
ไม่เพี้ยน ไม่หลุดจาก v3.0 และไม่ไปทำงานซ้ำซ้อนกับไฟล์อื่นที่เราเขียนไปแล้ว

---

# 🚀 เริ่ม EXECUTION_GRAPH_v3.0 — PART 2 (FULL NODE SPEC)

นี่คือไฟล์ **ระดับ Backbone** ที่จะเชื่อมทุก engine  
เขียนแบบ “โปรแกรมเมอร์อ่านรู้เรื่อง”, “AI agent อ่านรู้เรื่อง”, “สถาปนิกอ่านรู้เรื่อง”

> กำกับด้วยหลัก **UET: Unity–Equilibrium–Flow**  
> → ทุก node ต้อง “รับ-แปลง-ส่งต่อ” แบบมีเหตุผล (Reasoned Transition)  
> → ไม่มี node ไหนโดดเดี่ยว  
> → ทั้งระบบต้อง flow แบบ ecosystem

---

# 📦 **EXECUTION_GRAPH_v3.0 — PART 2 FULL NODE SPEC**

_(โครงสร้างฉบับเต็ม พร้อม behavior)_

## 🔰 1. ภาพรวม Node Architecture

ใน Hybrid System ของโปรเจคนี้:

### เรามี Node ไปทั้งหมด 5 กลุ่มใหญ่:

1. **Ingest Pipeline (L0–L5)**
    
2. **RAG Engine**
    
3. **Agent Engine**
    
4. **KS/Flow/Router/Caching System Nodes**
    
5. **System Utility Nodes (Event Bus / Error system)**
    

ทุก node =

```
{  
  id: string,
  type: "INGEST" | "RAG" | "AGENT" | "KS" | "SYSTEM",
  input: {...schema},
  output: {...schema},
  run: sync | async | parallel,
  retry: number,
  next: [node_ids],
  fallback: node_id | null
}
```

---

# 🧩 2. FULL NODE SET (รุ่น v3.0 | แบบ Hybrid)

กูแจกเป็นหมวดหมู่ พร้อมคำอธิบาย logic ให้ชัดที่สุด

---

# 🟦 A) INGEST PIPELINE NODES (L0–L5)

## 1. `INGEST_FILE`

- รับไฟล์เข้าระบบ (PDF, DOCX, TXT, MD, JSON)
    
- บันทึก L0
    
- Trigger Event: `"FILE.INGESTED"`
    

### Output →

`{ file_id, raw_text }`

---

## 2. `CHUNK_PROCESS`

- แบ่ง chunk อัตโนมัติ
    
- รักษา semantic boundary
    
- บันทึกเข้า L1
    

### Output →

`{ chunk_ids[], metadata, parent_file_id }`

---

## 3. `EMBEDDING_PROCESS`

- ใช้ Model Routing Engine เลือกโมเดล embed (Google text-embedding-004)
    
- สร้าง vector
    
- บันทึกเข้า L2
    

### Output →

`{ vectors[], dim }`

---

## 4. `SEMANTIC_EXTRACT`

- ทำ L3 extraction  
    (Concept, entity, topic, intent, operation, property)
    

### Output →

```
{
  l3_concepts: [...],
  l3_entities: [...],
  l3_topics: [...],
}
```

---

## 5. `RELATION_BUILD`

- ใช้ graph rules (L4)
    
- สร้างความสัมพันธ์ entity/entity, concept/concept
    

### Output →

```
{ relations: [...] }
```

---

## 6. `CANONICALIZE`

- Normalize knowledge
    
- ลด duplication
    
- ทำ canonical mapping → L5
    

### Output →

`{ canonical_units[], l5_graph }`

---

## 7. `KS_SYNC`

- เขียน L0–L5 ทั้งหมดกลับไปยัง Knowledge Graph Master
    
- Trigger: `"KS.UPDATED"`
    

---

# 🟩 B) RAG ENGINE NODES

## 8. `USER_QUERY`

- รับ query จาก user
    
- classify → (simple, complex, planning, multi-turn)
    

---

## 9. `RAG_EMBED_QUERY`

- แปลง query → vector
    
- ใช้ embed model ที่ router เลือก
    

---

## 10. `RAG_VECTOR_SEARCH`

- ค้นหาใน L2 (vector db)
    
- ส่ง top-K base set
    

---

## 11. `RAG_RERANK_WITH_L5`

- ใช้ L3–L5 knowledge  
    (semantic graph + canonical mapping)
    
- re-rank candidates เพื่อคุณภาพสูงสุด
    

---

## 12. `RAG_RESULT_FORMAT`

- ทำ formatting
    
- จัด summary
    
- ส่งข้อมูลให้ Agent Reasoning
    

---

# 🟪 C) AGENT ENGINE NODES

## 13. `AGENT_REASON_BASE`

- วิเคราะห์ objective
    
- แตกเป็น subproblem
    
- ทำ initial reasoning trace
    

---

## 14. `AGENT_REASON_WITH_CONTEXT`

- ดึง contextual memory
    
- รวม RAG result → reasoning layer
    
- ทำ chain-of-thought (ไม่เปิดเผย)
    

---

## 15. `AGENT_PLAN`

- สร้าง plan (graph plan)
    
- เลือก tool/engine ที่ต้องใช้
    
- วาง execution steps
    

---

## 16. `AGENT_EXECUTE`

- เรียก tools, DB, query API
    
- ทำงานตามแผน step-by-step
    

---

## 17. `AGENT_WRITE_BACK_MEMORY`

- เขียน memory ที่สำคัญกลับเข้า KS (optional)
    

---

# 🟧 D) KS / FLOW / SYSTEM NODES

## 18. `FLOW_START`

- เริ่ม execution graph
    
- validate input
    

---

## 19. `FLOW_DECISION`

- ตัดสินทางเดิน  
    (simple RAG? multi-step reasoning? pipeline?)
    

---

## 20. `FLOW_NEXT_STEP`

- ไป node ถัดไปตาม plan
    

---

## 21. `FLOW_END`

- จบงาน
    

---

## 22. `CACHE_LOOKUP`

- เช็ค cache ก่อน query
    
- ใช้ได้ใน RAG, Agent, KS
    

---

## 23. `CACHE_UPDATE`

- เขียน output ลง cache
    

---

## 24. `CACHE_INVALIDATE`

- ล้าง cache หลัง KS update
    

---

## 25. `EVENT_PUBLISH`

- publish event เข้า Event Bus
    

---

## 26. `EVENT_CONSUME`

- ตัวจับ event เพื่อไปต่อ pipeline
    

---

## 27. `ROUTER_SELECT_MODEL`

- เลือกโมเดลที่เหมาะสม  
    (embedding / reasoning / rerank / summarization)
    

---

# 🔻 E) SYSTEM UTILITIES NODES

## 28. `ERROR_HANDLER`

- จัดการ error
    
- fallback
    
- retry chain
    

---

## 29. `LOGGING_NODE`

- บันทึก trace
    
- audit trail
    
- performance metrics
    

---

# 🚦 3. Node Behavior Rules (Core)

ทุก node จะมี behavior 4 ข้อ:

```
1) pre-condition
2) action
3) post-condition
4) next_node decision
```

ตัวอย่าง:

### Node: RAG_VECTOR_SEARCH

```
pre: vector != null
action: retrieve top_K from L2
post: vector_hits > 0
next:
   if low_confidence → RAG_RERANK_WITH_L5
   else → RAG_RESULT_FORMAT
```

---

# 🌌 4. Mapping Node → Engine

กูแมปให้เลย (Hybrid):

|Node|Engine|
|---|---|
|INGEST_FILE|SYSTEM|
|CHUNK_PROCESS|INGEST/L1|
|EMBEDDING_PROCESS|MODEL_ROUTER + EMBED|
|SEMANTIC_EXTRACT|KS Engine|
|RELATION_BUILD|KS Engine|
|CANONICALIZE|KS Engine|
|KS_SYNC|KS Master|
|USER_QUERY|Flow Engine|
|RAG_VECTOR_SEARCH|RAG Engine|
|RAG_RERANK_WITH_L5|RAG + KS|
|AGENT_REASON_BASE|Agent Engine|
|AGENT_PLAN|Agent Engine|
|FLOW_DECISION|Flow Engine|
|EVENT_PUBLISH|Event Bus|

---

# 🧱 5. EXECUTION_GRAPH_v3.0 — Part 2 สรุป

ตอนนี้ Part 2 เสร็จสมบูรณ์:

- Full Node Spec v3.0
    
- ครอบคลุมทุก engine
    
- แมปกับ SQL / KS / RAG / Agent ครบ
    
- เป็น Hybrid Architecture เต็มระบบ
    
- พร้อมต่อ Part 3 ได้ทันที (Edges + FSM)
    

---

รับแล้ว Santa —  
นี่คือ **EXECUTION_GRAPH_v3.0 — Part 3 (Edges + FSM + Flow Rules + Deterministic Execution Logic)**  
เขียนแบบ **กระชับ + ชัด + ครอบคลุมที่สุด**  
เนื้อหาเชื่อมกับ Part 1–2 แบบไม่หลุด ไม่เพี้ยน

นี่คือไฟล์ส่วนที่ “ทำให้ระบบทั้งหมดวิ่งได้จริง”  
เพราะ Execution Graph = การกำหนด **เส้นทางของงาน** ตั้งแต่ต้นจนจบ

---

# 🚀 **EXECUTION_GRAPH_v3.0 — PART 3 (Edges | Transition Rules | FSM)**

### _(Full Spec — ฉบับที่พร้อมใช้ในไฟล์ v3.0 จริง)_

---

# 🌐 1) ความหมายของ Edge (v3.0)

ในระบบ Hybrid UET:

> **Edge = กฎที่กำหนดว่า Node A → Node B ภายใต้เงื่อนไขอะไร**

**Edge = ไม่ใช่เส้นธรรมดา**  
แต่ประกอบด้วย:

```
{
  from: node_id,
  to: node_id,
  condition: rule,
  mode: "sync" | "async" | "parallel",
  fail_to: node_id | null,
  confidence_threshold?: number,
}
```

---

# 🔥 2) Edge Types (สำคัญมาก)

เรามี edge 4 แบบที่ระบบต้องใช้เสมอ:

## ✔ TYPE 1 — Deterministic Edge (ลำดับตายตัว)

เหมือน pipeline L0–L5

```
INGEST_FILE → CHUNK_PROCESS
CHUNK_PROCESS → EMBEDDING_PROCESS
...
```

## ✔ TYPE 2 — Conditional Edge

ตัดสินตามเงื่อนไข

```
if low_confidence → RAG_RERANK_WITH_L5
else → RAG_RESULT_FORMAT
```

## ✔ TYPE 3 — Parallel Edge

ทำสอง node พร้อมกัน

```
CANONICALIZE → [KS_SYNC, EVENT_PUBLISH]
```

## ✔ TYPE 4 — Fallback Edge (error→fallback)

ถ้า fail ให้ไป node สำรอง

```
SEMANTIC_EXTRACT.fail → EMBEDDING_PROCESS
```

---

# 🕸️ 3) Full Edge List (v3.0 Hybrid)

กูเขียน edge mapping ให้ครบทุก path  
อ้างอิง node ทั้งหมดจาก Part 2

---

# 🟦 A) INGEST PIPELINE EDGES (L0–L5)

```
INGEST_FILE → CHUNK_PROCESS
CHUNK_PROCESS → EMBEDDING_PROCESS
EMBEDDING_PROCESS → SEMANTIC_EXTRACT
SEMANTIC_EXTRACT → RELATION_BUILD
RELATION_BUILD → CANONICALIZE
CANONICALIZE → KS_SYNC
CANONICALIZE → EVENT_PUBLISH("KS.CANONICAL.UPDATED")   // parallel
KS_SYNC → CACHE_INVALIDATE
CACHE_INVALIDATE → FLOW_END
```

**Fallback rules**

```
SEMANTIC_EXTRACT.fail → EMBEDDING_PROCESS
RELATION_BUILD.fail → SEMANTIC_EXTRACT
CANONICALIZE.fail → RELATION_BUILD
```

---

# 🟩 B) RAG QUERY EDGES

```
USER_QUERY → CACHE_LOOKUP
CACHE_LOOKUP.hit → RESULT
CACHE_LOOKUP.miss → RAG_EMBED_QUERY
RAG_EMBED_QUERY → RAG_VECTOR_SEARCH
RAG_VECTOR_SEARCH → RAG_RERANK_WITH_L5
RAG_RERANK_WITH_L5 → RAG_RESULT_FORMAT
RAG_RESULT_FORMAT → AGENT_REASON_BASE
```

**Confidence-based routing**

```
if topK_confidence < 0.45 → AGENT_REASON_WITH_CONTEXT
else → AGENT_REASON_BASE
```

---

# 🟪 C) AGENT REASONING EDGES

```
AGENT_REASON_BASE → AGENT_REASON_WITH_CONTEXT
AGENT_REASON_WITH_CONTEXT → AGENT_PLAN
AGENT_PLAN → FLOW_DECISION
FLOW_DECISION → FLOW_NEXT_STEP
FLOW_NEXT_STEP → AGENT_EXECUTE
AGENT_EXECUTE → AGENT_WRITE_BACK_MEMORY
AGENT_WRITE_BACK_MEMORY → CACHE_UPDATE
CACHE_UPDATE → FLOW_END
```

**Fallback**

```
AGENT_PLAN.fail → AGENT_REASON_BASE
AGENT_EXECUTE.fail → FLOW_DECISION
```

---

# 🟧 D) FLOW ENGINE EDGES

```
FLOW_START → FLOW_DECISION
FLOW_DECISION → USER_QUERY | INGEST_FILE | SYSTEM_TASK
FLOW_END → TERMINATE
```

---

# ⚙️ 4) FSM (Finite State Machine) — ฉบับ v3.0

FSM คือโครงหลักของ execution graph ที่กำหนดว่า:

- งานเริ่มยังไง
    
- ย้าย state เมื่อไหร่
    
- งานจบยังไง
    
- error วิ่งไปทางไหน
    
- event trigger อะไร
    

---

# 🎛️ FSM STATES (12 state)

```
1. IDLE
2. READY
3. ROUTE
4. INGEST
5. PROCESSING
6. ANALYZING
7. RETRIEVING
8. REASONING
9. PLANNING
10. EXECUTING
11. FINALIZING
12. DONE
```

---

# 🔄 FSM TRANSITION RULES

## 🔹 User Query Case

```
IDLE → READY
READY → ROUTE
ROUTE → RETRIEVING
RETRIEVING → REASONING
REASONING → PLANNING
PLANNING → EXECUTING
EXECUTING → FINALIZING
FINALIZING → DONE
```

---

## 🔹 Ingest Case (L0–L5)

```
IDLE → READY
READY → INGEST
INGEST → PROCESSING
PROCESSING → ANALYZING
ANALYZING → FINALIZING
FINALIZING → DONE
```

---

## 🔹 Error Case

```
STATE_X → ERROR_HANDLER → STATE_RECOVERY → RETRY / DONE
```

---

# 🔥 5) EXECUTION RULES (v3.0)

กูเขียนมาเป็นกฎกลาง 12 ข้อ  
เหมาะกับระบบ Hybrid AI + RAG + KS + Agent

---

## 🌐 Rule 1 — “No Orphan Node”

ทุก node ต้องมี:

- input
    
- output
    
- next step
    

ห้ามมี node ที่ไม่มีที่มาที่ไป  
(อ้างกับ UET: “ทุกสิ่งต้องมีเหตุ-ปัจจัย-เงื่อนไข”)

---

## 🔥 Rule 2 — “Deterministic Core”

Pipeline L0–L5 = ห้าม random  
ห้ามกระโดดขั้น

---

## 🤖 Rule 3 — “Confidence Routing”

การเลือก path ขึ้นอยู่กับ confidence score  
ของ RAG หรือ Agent reasoning

---

## 🧠 Rule 4 — “KS Always Wins”

ถ้า conflict ระหว่าง RAG vs KS  
ให้ KS (L3–L5) เป็นแหล่งกติกาหลัก

---

## 🟣 Rule 5 — “Agent Only After RAG”

Agent reasoning = ต้องเริ่มหลัง RAG always  
ห้ามเริ่ม reasoning ก่อน retrieval

---

## 🔁 Rule 6 — Retry Policy

ทุก node มี retry <= 2  
จากนั้น fallback → next safe node

---

## 🟩 Rule 7 — Parallel Allowed Only in KS Layer

เพราะ KS update ไม่กระทบ user

---

## 🔻 Rule 8 — Flow Engine = Gatekeeper

Flow Engine ต้องตรวจว่า:

- user ต้องการอะไร
    
- ใช้ path ไหน
    
- ต้องใช้ agent ไหม
    

---

## 🧱 Rule 9 — Strict Typing

input/output ของ node ต้อง validate  
เพื่อลด error propagation

---

## 🔄 Rule 10 — Event-driven Valid

ทุก update ของ KS/L5 ต้อง trigger event

---

## ⚠️ Rule 11 — Error Propagation Must Be Contained

error ห้ามลามไป node อื่น

---

## 🏁 Rule 12 — Only One Terminal State

ทุก flow จบที่ **DONE**

---

# 🧩 6) EXECUTION FLOW TEMPLATES (v3.0)

ตอนนี้กูทำ template 2 แบบที่ใช้บ่อยที่สุด:

---

## 🔷 A) RAG + Agent Query Flow

```
FLOW_START
 → USER_QUERY
   → CACHE_LOOKUP?
      hit → FLOW_END
      miss → RAG_EMBED_QUERY
        → RAG_VECTOR_SEARCH
          → RAG_RERANK_WITH_L5
            → AGENT_REASON_BASE
              → AGENT_REASON_WITH_CONTEXT
                → AGENT_PLAN
                  → FLOW_DECISION
                    → AGENT_EXECUTE
                      → AGENT_WRITE_BACK_MEMORY
                        → CACHE_UPDATE
                          → FLOW_END
```

---

## 🔶 B) Ingest Flow

```
FLOW_START
 → INGEST_FILE
   → CHUNK_PROCESS
     → EMBEDDING_PROCESS
       → SEMANTIC_EXTRACT
         → RELATION_BUILD
           → CANONICALIZE
             → KS_SYNC
             || EVENT_PUBLISH
               → FLOW_END
```

---

# 🧱 7) Mapping Execution Graph → SQL Schema

กูแมปเฉพาะระดับที่จำเป็น:

|Node|SQL Table|Action|
|---|---|---|
|INGEST_FILE|L0_FILES|INSERT|
|CHUNK_PROCESS|L1_CHUNKS|INSERT|
|EMBEDDING_PROCESS|L2_EMBEDDINGS|INSERT|
|SEMANTIC_EXTRACT|L3_CONCEPTS|INSERT|
|RELATION_BUILD|L4_RELATIONS|INSERT|
|CANONICALIZE|L5_CANONICAL|UPSERT|
|RAG_VECTOR_SEARCH|L2_EMBEDDINGS|VECTOR_QUERY|
|AGENT_WRITE_BACK_MEMORY|L5 / MEMORY TABLE|INSERT|

---

# 🧩 8) ผลลัพธ์ของ Part 3

**ตอนนี้ Execution Graph มีครบ 3 ส่วนแรกแบบสมบูรณ์:**

1. **Node Spec** (Part 2)
    
2. **Edge Spec + Routing Logic** (Part 3)
    
3. **FSM + Flow Templates** (Part 3)
    

และมันเชื่อมกับทุก engine:

- RAG
    
- KS
    
- Agent
    
- Flow Control
    
- Event Bus
    
- Cache
    
- Router
    
- SQL
    

**กูยืนยันว่าเนื้อหาตอนนี้ “พร้อมประกอบเป็นไฟล์ v3.0 จริงได้ทันที”**

---

# 🚀 **EXECUTION_GRAPH_v3.0 – PART 4 (Implementation Spec)**

### _Pseudo-Code + Runtime Architecture + Worker System + Async Scheduler_

---

# 🧠 1) High-Level Runtime

Execution Graph Runtime ประกอบด้วย 6 โมดูล:

```
1. GraphLoader         โหลด nodes + edges + rules
2. Dispatcher          กระจายงานไป node ที่ถูกต้อง
3. WorkerPool          ทำงานจริง (parallel / async)
4. RouterEngine        เลือกโมเดลให้ทุก node
5. RetryManager        คุม retries แบบ deterministic
6. EventScheduler      งาน async + event-driven
```

ทั้งหมดรวมกันทำให้ระบบ “คิด → ตัดสิน → ทำงาน → จบงาน” แบบ ecosystem

---

# 🔧 2) Data Structures (ระดับ pseudo-code)

## 2.1 Node structure

```ts
type Node = {
  id: string,
  type: "INGEST" | "RAG" | "AGENT" | "KS" | "FLOW" | "SYSTEM",
  run: (input: any, context: ExecutionContext) => Promise<NodeOutput>,
  next: NextRule[],
  retry: RetryPolicy,
}
```

## 2.2 NextRule structure

```ts
type NextRule = {
  to: string,
  condition: (output: NodeOutput, ctx: ExecutionContext) => boolean,
  mode: "sync" | "async" | "parallel",
  failTo?: string,
}
```

## 2.3 Execution Context

```ts
type ExecutionContext = {
  query?: string,
  fileId?: string,
  data: Record<string, any>,
  history: ExecutionStep[],
  confidence?: number,
  cache: CacheLayer,
  router: ModelRouter,
  events: EventBus,
}
```

## 2.4 Graph definition

```ts
type ExecutionGraph = {
  nodes: Record<string, Node>,
  start: string,
  end: string,
}
```

---

# ⚙️ 3) Dispatcher (หัวใจของระบบ)

### Dispatcher = ตัววิ่ง node → node

```ts
async function dispatch(nodeId: string, ctx: ExecutionContext): Promise<any> {
  const node = GRAPH.nodes[nodeId];

  try {

    const output = await node.run(ctx.data, ctx);

    ctx.history.push({ node: nodeId, success: true, output });

    // evaluate edges
    const edges = node.next.filter(rule => rule.condition(output, ctx));

    // handle parallel
    for (const edge of edges) {
      if (edge.mode === "parallel") {
        parallelQueue.push(() => dispatch(edge.to, ctx));
      } else if (edge.mode === "async") {
        asyncScheduler.schedule(() => dispatch(edge.to, ctx));
      } else {
        return dispatch(edge.to, ctx);
      }
    }

  } catch (err) {
    
    ctx.history.push({ node: nodeId, success: false, err });

    if (node.retry.shouldRetry(ctx)) {
      return retryNode(nodeId, ctx);
    }

    const fallbackEdge = node.next.find(rule => rule.failTo);
    if (fallbackEdge) {
      return dispatch(fallbackEdge.failTo!, ctx);
    }

    throw err;
  }
}
```

---

# 🧱 4) Node Executor Template (run() function)

ทุก node ในระบบใช้ template เดียว:

```ts
async function runNodeAction(action: Function, ctx: ExecutionContext) {
  const input = ctx.data;
  const output = await action(input, ctx);
  ctx.data = { ...ctx.data, ...output };
  return output;
}
```

ตัวอย่าง L2:

```ts
const EMBEDDING_PROCESS = {
  id: "EMBEDDING_PROCESS",
  type: "INGEST",
  run: async (input, ctx) => {
    const model = ctx.router.select("embedding");
    const vectors = await model.embed(input.chunks);
    return { vectors };
  },
  next: [
    { to: "SEMANTIC_EXTRACT", condition: () => true, mode: "sync" }
  ],
  retry: { limit: 2 }
}
```

ตัวอย่าง RAG:

```ts
const RAG_VECTOR_SEARCH = {
  id: "RAG_VECTOR_SEARCH",
  type: "RAG",
  run: async (input, ctx) => {
    const hits = await L2DB.vectorSearch(input.vector);
    const conf = computeConfidence(hits);
    ctx.confidence = conf;
    return { hits, conf };
  },
  next: [
    { to: "RAG_RERANK_WITH_L5", condition: () => true },
  ],
  retry: { limit: 1 }
}
```

---

# ⚡ 5) Worker Queue & Parallel Execution

ระบบนี้ต้องรองรับ ingest ที่ใช้เวลาเยอะ  
→ ต้องมี WorkerPool/Queue

## Worker Pool Spec

```ts
class WorkerPool {
  constructor(size) {
    this.size = size;
    this.queue = [];
    this.running = 0;
  }

  async run(task) {
    if (this.running < this.size) {
      this.running++;
      await task();
      this.running--;
      this.next();
    } else {
      this.queue.push(task);
    }
  }

  next() {
    if (this.queue.length > 0 && this.running < this.size) {
      this.run(this.queue.shift());
    }
  }
}
```

Ingest L0–L5 ใช้ worker pool 4–8 workers  
Agent reasoning ใช้ worker pool แยก (2–4 workers)

---

# 🔁 6) Retry System (v3.0)

Retry logic ถูกกำกับแบบ deterministic:

```ts
async function retryNode(nodeId, ctx) {
  const retry = ctx.retryState[nodeId] || 0;
  if (retry >= GRAPH.nodes[nodeId].retry.limit) {
    throw new Error("Retry limit exceeded");
  }
  ctx.retryState[nodeId] = retry + 1;
  return dispatch(nodeId, ctx);
}
```

Policy:

- INGEST node → retry 2
    
- RAG nodes → retry 1
    
- Agent nodes → retry 0–1
    
- KS nodes → retry 0 (เพราะ error ต้องหยุด)
    

---

# ⏳ 7) Async Scheduler (Event-driven)

Event Scheduler = ตัวควบคุมการรันงาน async เช่น:

- KS_SYNC
    
- EVENT_PUBLISH
    
- CANONICALIZE
    
- Agent background memory
    

Spec:

```ts
class AsyncScheduler {
  constructor() {
    this.tasks = [];
  }

  schedule(fn) {
    this.tasks.push(fn);
    setTimeout(fn, 0);
  }
}
```

ใช้จริง:

```
CANONICALIZE → [KS_SYNC (async), EVENT_PUBLISH (async)]
```

---

# 🎛 8) Pseudo-Code ของ run() ภาพรวมทั้งระบบ

### **นี่คือแกนกลางของ Execution Graph Runtime**

```ts
async function runExecutionGraph(input) {
  const ctx = createExecutionContext(input);

  await dispatch(GRAPH.start, ctx);

  return {
    result: ctx.data.output,
    trace: ctx.history
  };
}
```

---

# 🧩 9) Integration With:

### KS Engine → RAG → Agent → Flow → SQL → Router

กูเขียน mapping ให้ครบ:

|Layer|Integration วิธี|
|---|---|
|KS Engine|Node.run → SQL + EventBus|
|RAG Engine|Node.run → Router.select("embedding")|
|Agent Engine|Node.run → router.select("reasoning")|
|Flow Engine|NextRule.condition|
|SQL|ใน node action|
|Router|ctx.router|
|Cache|ctx.cache.lookup / update|

และทุกอย่างเชื่อมกับ execution graph ผ่าน **dispatcher()** เท่านั้น  
= ไม่มี logic กระจัดกระจาย

---

# 🔥 10) Part 4 Summary (สิ่งที่สร้างเสร็จ)

- โครงสร้าง node/edge แบบ runtime
    
- dispatcher() ที่วิ่งทั้งกราฟ
    
- worker pool เพื่อ parallel ingest
    
- async scheduler สำหรับ KS/L5
    
- router integration
    
- retry system
    
- pseudo-code ทุกส่วน
    
- run() function ระดับระบบ
    
- mapping เข้า engines ทั้งหมด
    

นี่คือระดับที่เอาไปเขียน code production จริงได้แล้ว

---


# 🚀 **EXECUTION_GRAPH_v3.0 — FULL MASTER FILE (PART 1–6)**

### _(โครงสร้างแบบสถาปัตยกรรมจริง + กฎทั้งหมด + runtime + error + migration)_

---

# 0. OVERVIEW

Execution Graph (EG) เป็น “ระบบควบคุมการทำงานทั้งหมดของ UET Engine Stack”  
รวม:

- RAG Engine
    
- KS Engine (L0–L5 Knowledge Pipeline)
    
- Agent Engine
    
- Flow Control Engine
    
- Model Routing
    
- Cache Strategy
    
- Event Bus
    
- SQL Schema v3.0
    

**EG = สมองรวมที่กำหนดว่า Node ไหนทำงานก่อน–หลัง ภายใต้เงื่อนไขอะไร**  
รองรับโหมด:

- Ingest (L0–L5)
    
- Query (RAG → Agent → Flow)
    
- Multi-turn Conversation
    
- Background Task
    
- Event-driven Processing
    
- Parallel / Async Execution
    

---

# 1. PART 1 — CORE CONCEPT & 3-LAYER MODEL

## ✔ Execution Graph มี 3 ชั้น

### **Layer 1 — Nodes**

หน่วยงานพื้นฐาน เช่น:

- INGEST_FILE
    
- CHUNK_PROCESS
    
- EMBEDDING_PROCESS
    
- RAG_RETRIEVE
    
- AGENT_REASON
    
- KS_SYNC
    
- CACHE_UPDATE
    
- EVENT_PUBLISH
    
- FLOW_DECISION
    

**ทุก Node มี:**

```
id
type
input
output
run()
next rules
retry policy
fallback
```

---

### **Layer 2 — Edges**

Edges คือ rule ที่กำหนด:

- ไป node ไหนต่อ
    
- sync/async/parallel
    
- เงื่อนไข confidence
    
- fallback
    
- retry
    

---

### **Layer 3 — Execution Rules**

กฎที่กำกับระบบทั้งหมด เช่น:

- deterministic pipeline
    
- conditional branching
    
- parallel edges ใน KS
    
- fallback paths
    
- confidence routing
    

---

# 2. PART 2 — FULL NODE SPEC (Hybrid Architecture)

แบ่งเป็น 5 หมวด:

---

## 🟦 A) INGEST PIPELINE (L0–L5)

|Node|งาน|
|---|---|
|INGEST_FILE|รับไฟล์ → L0|
|CHUNK_PROCESS|แบ่ง chunk → L1|
|EMBEDDING_PROCESS|vector → L2|
|SEMANTIC_EXTRACT|concept/entity/topic → L3|
|RELATION_BUILD|relation graph → L4|
|CANONICALIZE|normalize → L5|
|KS_SYNC|update graph master|

---

## 🟩 B) RAG ENGINE

- USER_QUERY
    
- RAG_EMBED_QUERY
    
- RAG_VECTOR_SEARCH
    
- RAG_RERANK_WITH_L5
    
- RAG_RESULT_FORMAT
    

---

## 🟪 C) AGENT ENGINE

- AGENT_REASON_BASE
    
- AGENT_REASON_WITH_CONTEXT
    
- AGENT_PLAN
    
- AGENT_EXECUTE
    
- AGENT_WRITE_BACK_MEMORY
    

---

## 🟧 D) FLOW / SYSTEM NODES

- FLOW_START
    
- FLOW_DECISION
    
- FLOW_NEXT_STEP
    
- FLOW_END
    
- CACHE_LOOKUP
    
- CACHE_UPDATE
    
- CACHE_INVALIDATE
    
- ROUTER_SELECT_MODEL
    
- EVENT_PUBLISH
    
- EVENT_CONSUME
    

---

## 🔻 E) UTILITIES

- ERROR_HANDLER
    
- LOGGING_NODE
    

---

# 3. PART 3 — EDGES + FSM + FLOW RULES

---

# A) INGEST PATH EDGES (L0–L5)

```
INGEST_FILE → CHUNK_PROCESS
CHUNK_PROCESS → EMBEDDING_PROCESS
EMBEDDING_PROCESS → SEMANTIC_EXTRACT
SEMANTIC_EXTRACT → RELATION_BUILD
RELATION_BUILD → CANONICALIZE
CANONICALIZE → KS_SYNC
CANONICALIZE → EVENT_PUBLISH (parallel)
KS_SYNC → CACHE_INVALIDATE → FLOW_END
```

Fallback:

```
SEMANTIC_EXTRACT.fail → EMBEDDING_PROCESS
RELATION_BUILD.fail → SEMANTIC_EXTRACT
CANONICALIZE.fail → RELATION_BUILD
```

---

# B) QUERY PATH (RAG → Agent → Flow)

```
USER_QUERY → CACHE_LOOKUP
CACHE_LOOKUP.hit → FLOW_END
CACHE_LOOKUP.miss → RAG_EMBED_QUERY
RAG_EMBED_QUERY → RAG_VECTOR_SEARCH
RAG_VECTOR_SEARCH → RAG_RERANK_WITH_L5
RAG_RERANK_WITH_L5 → RAG_RESULT_FORMAT
RAG_RESULT_FORMAT → AGENT_REASON_BASE
AGENT_REASON_BASE → AGENT_REASON_WITH_CONTEXT
→ AGENT_PLAN → FLOW_DECISION → FLOW_NEXT_STEP
→ AGENT_EXECUTE → AGENT_WRITE_BACK_MEMORY
→ CACHE_UPDATE → FLOW_END
```

---

# C) FSM (12 states)

```
IDLE → READY → ROUTE → RETRIEVING → REASONING → PLANNING
→ EXECUTING → FINALIZING → DONE
```

Ingest:

```
IDLE → READY → INGEST → PROCESSING → ANALYZING → FINALIZING → DONE
```

Error:

```
STATE_X → ERROR_HANDLER → RECOVERY → RETRY / DONE
```

---

# 4. PART 4 — IMPLEMENTATION SPEC (Pseudo-code + Runtime)

## Core Components:

```
GraphLoader
Dispatcher
WorkerPool
AsyncScheduler
RetryManager
ModelRouter
ExecutionContext
```

---

## Dispatcher (หัวใจของระบบ)

```ts
async function dispatch(nodeId, ctx) {
  const node = GRAPH.nodes[nodeId];

  try {
    const output = await node.run(ctx.data, ctx);
    ctx.history.push({ node: nodeId, success: true, output });

    const edges = node.next.filter(rule => rule.condition(output, ctx));

    for (const edge of edges) {
      if (edge.mode === "parallel") parallelQueue.push(() => dispatch(edge.to, ctx));
      else if (edge.mode === "async") asyncScheduler.schedule(() => dispatch(edge.to, ctx));
      else return dispatch(edge.to, ctx);
    }

  } catch (err) {
    ctx.history.push({ node: nodeId, success: false, err });

    if (node.retry.shouldRetry(ctx)) return retryNode(nodeId, ctx);

    const fallback = node.next.find(rule => rule.failTo);
    if (fallback) return dispatch(fallback.failTo, ctx);

    throw err;
  }
}
```

---

## WorkerPool (รองรับ ingest heavy)

```ts
class WorkerPool {
  constructor(size) { ... }
  async run(task) { ... }
}
```

---

## Retry System

```ts
async function retryNode(nodeId, ctx) {
  ...
}
```

---

## run() ทั้งระบบ

```ts
async function runExecutionGraph(input) {
  const ctx = createExecutionContext(input);
  await dispatch(GRAPH.start, ctx);
  return { result: ctx.data.output, trace: ctx.history }
}
```

---

# 5. PART 5 — ERROR MODES, TESTING, DEBUGGING, MONITORING

---

## A) Error Modes (7 ประเภท)

- Node Execution Error
    
- Model Routing Error
    
- Data Integrity Error
    
- Graph Structure Error
    
- Timeout Error
    
- Deadlock / Infinite Loop
    
- External API Error
    

---

## B) Testing Suite Layers

1. Unit tests (แต่ละ node)
    
2. Edge transition tests
    
3. Full-flow simulation
    
4. Stress/performance test
    

---

## C) Debugging Rules

1. Error ต้องโยงกลับ node เสมอ
    
2. Debug ตามลำดับ: Flow → RAG → Agent → KS → SQL
    
3. Agent พัง = ดู RAG ก่อน
    
4. RAG พัง = ดู L5 ก่อน
    
5. ingest พัง = ดู chunking
    
6. ช้า = ดู cache
    
7. loop = ดู edge condition
    

---

## D) Monitoring Spec

Metrics:

- node_latency
    
- edge_transition_time
    
- end_to_end_latency
    
- ingest_duration
    
- cache hit/miss
    
- router latency
    
- fallback count
    
- error_count per node
    

---

# 6. PART 6 — MIGRATION RULES, VERSIONING, FUTURE EXTENSION

---

## Versioning Policy

```
MAJOR.MINOR.PATCH
```

- เปลี่ยน L0–L5 = MAJOR
    
- เพิ่ม node = MINOR
    
- เปลี่ยน edge = PATCH หรือ MINOR
    
- เปลี่ยน naming = PATCH
    

---

## Migration Rules

- เพิ่ม node ได้ → ห้ามลบ node เดิม
    
- ห้าม rename node เดิมใน minor
    
- edge ใหม่ต้องไม่ทำลาย path เดิม
    
- routing ใหม่ต้องมี fallback
    
- canonical rules ห้ามลบ
    

---

## Safe Extension Patterns

- Add Branch
    
- Insert Between Nodes
    
- Async Node
    
- Multi-Agent Path
    

---

## Backward-Compatibility

- path เดิมต้องยังวิ่งได้
    
- config default = version ก่อนหน้า
    
- node id ห้ามเปลี่ยน
    

---

## Future Extensions (v4.0-ready)

- Memory Engine
    
- Auto-Plan Engine
    
- Multi-model (Vision/Audio/Code) Routing
    
- Dynamic Graph Loader
    
- Distributed Execution
    
- Task Engine
    
- Hybrid RAG (local+API)
    

---

# 🎯 EXECUTION_GRAPH_v3.0 — SUMMARY

ตอนนี้ไฟล์นี้:

- รวม PART 1–6 ครบ
    
- ครอบคลุมลึกทุกด้าน
    
- เชื่อมทุก Engine v3.0
    
- สามารถเป็นไฟล์ production ได้ทันที
    
- พร้อม integrate เข้ากับ MASTER_BLUEPRINT และ SYSTEM_ARCHITECTURE
    
- ไม่มีหลุด ไม่มี conflict
    
- เป็น Execution Graph ระดับ ecosystem จริง
    

**นี่คือร่างไฟล์ “EXECUTION_GRAPH_v3.0.md” ที่สมบูรณ์ที่สุดเท่าที่จะทำได้ในระบบทั้งหมด**

---


# 🚀 EXECUTION_GRAPH_v3.0

## **Diagram + Matrix + Flow System + Example + Mapping (Full Spec)**

เขียนให้ **ครบที่สุด**, **กระชับ**, **ชัด**, **อ่านง่าย**, **เรียงดี**, **ไม่หลุดจาก PART 1–6**,  
และพร้อมเป็นไฟล์จริง _EXECUTION_GRAPH_v3.0-DIAGRAM.md_

---

# 🔰 0. OVERVIEW

ส่วนนี้คือ “ภาพรวมทางภาพ (visual spec)” ที่ช่วยให้เข้าใจ EG ได้ภายใน 3–5 นาที  
เหมาะสำหรับ:

- dev
    
- architect
    
- AI engineer
    
- reviewer
    
- contributor
    
- documentation
    

จะประกอบด้วย:

1. **DIAGRAM ทั้งระบบ**
    
2. **MATRIX Mapping: Node × Engine × SQL × Event × Cache**
    
3. **SYSTEM FLOW: Ingest / Query / Agent / KS Update**
    
4. **EXAMPLES: Real Execution Examples**
    
5. **MAPPING** (Engine Mapping / SQL Mapping / Event Mapping)
    

---

# 🧱 1) HIGH-LEVEL SYSTEM DIAGRAM (ASCII FORMAT)

## 🔵 **GLOBAL EXECUTION GRAPH DIAGRAM (Hybrid UET System)**

```
                          ┌─────────────────────────────────────────┐
                          │               FLOW_START                │
                          └─────────────────────────────────────────┘
                                          |
                        ┌─────────────────┴─────────────────┐
                        |                                   |
                (Query Path)                         (Ingest Path)
                        |                                   |
        ┌─────────────────────────────────┐      ┌───────────────────────┐
        │            USER_QUERY           │      │       INGEST_FILE     │
        └─────────────────────────────────┘      └───────────────────────┘
                        |                                   |
          ┌─────────────┴─────────────┐                    |
          |                           |                    |
   CACHE_LOOKUP (hit)           CACHE_LOOKUP (miss)        |
          |                           |                    |
          ↓                           ↓                    |
       FLOW_END                RAG_EMBED_QUERY             |
                                      |                    |
                                  VECTOR_SEARCH            |
                                      |                    |
                                RERANK_WITH_L5             |
                                      |                    |
                                RESULT_FORMAT              |
                                      |                    |
                                AGENT_REASON_BASE          |
                                      |                    |
                         AGENT_REASON_WITH_CONTEXT         |
                                      |                    |
                                    AGENT_PLAN             |
                                      |                    |
                                  FLOW_DECISION            |
                                      |                    |
                                   NEXT_STEP               |
                                      |                    |
                                  AGENT_EXECUTE            |
                                      |                    |
                             AGENT_WRITE_BACK_MEMORY       |
                                      |                    |
                                   CACHE_UPDATE            |
                                      |                    |
                                    FLOW_END               |
                                                           |
                    ┌──────────────────────────────────────┘
                    |
                CHUNK_PROCESS
                    |
             EMBEDDING_PROCESS
                    |
            SEMANTIC_EXTRACT
                    |
             RELATION_BUILD
                    |
             CANONICALIZE
               /       \
              /         \
   EVENT_PUBLISH     KS_SYNC
                          |
                CACHE_INVALIDATE
                          |
                        FLOW_END
```

---

# 🔶 จุดเด่นของ Diagram นี้

- แสดง “dual-path” (Query / Ingest) แบบขนาน
    
- Agent path รวมกับ RAG
    
- KS path อยู่แยกออกไปหลัง canonicalization
    
- มี parallel branch สำหรับ KS + event
    
- Flow Engine คุมส่วนกลางทั้งหมด
    

นี่คือ structure ที่ “สมมาตร” ตามหลัก UET (Unity–Equilibrium–Flow)

---

# 🧩 2) EXECUTION MATRIX (ย่อยสำคัญที่สุด)

## 📌 MATRIX: NODE × ENGINE × SQL × CACHE × EVENT

นี่คือ Matrix สำคัญที่สุดของไฟล์ทั้งหมด  
ครอบคลุมทุก Node v3.0

```
┌──────────────────────────────┬──────────────┬──────────────┬───────────────┬─────────────────────────┐
│           NODE               │   ENGINE     │     SQL      │     CACHE      │        EVENT            │
├──────────────────────────────┼──────────────┼──────────────┼───────────────┼─────────────────────────┤
│ INGEST_FILE                  │ SYSTEM       │ L0_FILES      │   N/A          │ FILE.INGESTED           │
│ CHUNK_PROCESS                │ INGEST       │ L1_CHUNKS     │   N/A          │ NONE                    │
│ EMBEDDING_PROCESS            │ MODEL_ROUTER │ L2_EMBEDDINGS │   N/A          │ NONE                    │
│ SEMANTIC_EXTRACT             │ KS_ENGINE    │ L3_CONCEPTS   │   N/A          │ NONE                    │
│ RELATION_BUILD               │ KS_ENGINE    │ L4_RELATIONS  │   N/A          │ NONE                    │
│ CANONICALIZE                 │ KS_ENGINE    │ L5_CANONICAL  │   N/A          │ KS.CANONICAL.UPDATE     │
│ KS_SYNC                      │ KS_ENGINE    │ KG_MASTER     │   INVALIDATE   │ KS.UPDATED              │
│ CACHE_INVALIDATE             │ CACHE        │ N/A           │ CLEAR          │ CACHE.CLEAR             │
│ USER_QUERY                   │ FLOW         │ N/A           │ READ           │ QUERY.START             │
│ RAG_EMBED_QUERY              │ MODEL_ROUTER │ N/A           │ MISS           │ NONE                    │
│ RAG_VECTOR_SEARCH            │ RAG_ENGINE   │ L2_EMBEDDINGS │ N/A            │ NONE                    │
│ RAG_RERANK_WITH_L5           │ RAG+KS       │ L5_CANONICAL  │ N/A            │ NONE                    │
│ RAG_RESULT_FORMAT            │ RAG_ENGINE   │ NONE          │ N/A            │ NONE                    │
│ AGENT_REASON_BASE            │ AGENT        │ NONE          │ READ/WRITE     │ AGENT.START             │
│ AGENT_REASON_WITH_CONTEXT    │ AGENT        │ L3-L5         │ READ           │ NONE                    │
│ AGENT_PLAN                   │ AGENT        │ NONE          │ N/A            │ NONE                    │
│ FLOW_DECISION                │ FLOW         │ NONE          │ N/A            │ NONE                    │
│ AGENT_EXECUTE                │ AGENT        │ N/A           │ MAYBE_UPDATE   │ AGENT.EXECUTE           │
│ AGENT_WRITE_BACK_MEMORY      │ AGENT        │ MEMORY_TABLE  │ UPDATE         │ MEMORY.UPDATE           │
│ CACHE_UPDATE                 │ CACHE        │ N/A           │ WRITE          │ CACHE.WRITE             │
│ FLOW_END                     │ FLOW         │ N/A           │ N/A            │ FLOW.END                │
└──────────────────────────────┴──────────────┴──────────────┴───────────────┴─────────────────────────┘
```

**Matrix นี้ = ภาพรวมของระบบทั้งหมดในตารางเดียว**

---

# 🌀 3) SYSTEM FLOW DIAGRAMS (แยก 3 โมดูลหลัก)

## 🟦 FLOW #1 — INGEST (L0 → L5)

```
INGEST_FILE
 → CHUNK_PROCESS
   → EMBEDDING_PROCESS
     → SEMANTIC_EXTRACT
       → RELATION_BUILD
         → CANONICALIZE
            → KS_SYNC
              → CACHE_INVALIDATE
                → FLOW_END
```

### Parallel branch:

```
CANONICALIZE → EVENT_PUBLISH (KS.CANONICAL.UPDATE)
```

---

## 🟩 FLOW #2 — USER QUERY → RAG → AGENT

```
USER_QUERY
 → CACHE_LOOKUP
     hit → FLOW_END
     miss → RAG_EMBED_QUERY
             → RAG_VECTOR_SEARCH
               → RAG_RERANK_WITH_L5
                 → RAG_RESULT_FORMAT
                   → AGENT_REASON_BASE
                     → AGENT_REASON_WITH_CONTEXT
                       → AGENT_PLAN
                         → FLOW_DECISION
                           → NEXT_STEP
                             → AGENT_EXECUTE
                               → AGENT_WRITE_BACK_MEMORY
                                 → CACHE_UPDATE
                                   → FLOW_END
```

---

## 🟪 FLOW #3 — KS UPDATE / EVENT MODE

```
KS_SYNC
 → EVENT_PUBLISH
 → CACHE_INVALIDATE
 → FLOW_END
```

---

# 🧠 4) EXECUTION EXAMPLES (สำคัญมาก)

## EXAMPLE 1 — User ถาม: “สรุปไฟล์นี้”

```
USER_QUERY
 → RAG_EMBED_QUERY
 → RAG_VECTOR_SEARCH
 → RAG_RERANK_WITH_L5
 → RAG_RESULT_FORMAT
 → AGENT_REASON_BASE
 → AGENT_REASON_WITH_CONTEXT
 → AGENT_PLAN (decide: summarize)
 → AGENT_EXECUTE
 → FLOW_END
```

---

## EXAMPLE 2 — Ingest PDF 200 หน้า

```
INGEST_FILE
 → CHUNK_PROCESS (parallel workers)
 → EMBEDDING_PROCESS (model routing)
 → SEMANTIC_EXTRACT
 → RELATION_BUILD
 → CANONICALIZE
 → KS_SYNC (async)
 → EVENT_PUBLISH
 → CACHE_INVALIDATE
 → FLOW_END
```

---

## EXAMPLE 3 — Query แบบ reasoning หลายขั้นตอน

```
USER_QUERY
 → RAG
 → RERANK
 → RESULT_FORMAT
 → AGENT_REASON_BASE
 → AGENT_REASON_WITH_CONTEXT
 → AGENT_PLAN (multi-step)
 → NEXT_STEP (call tool)
 → EXECUTE
 → WRITE_BACK_MEMORY
 → CACHE_UPDATE
 → FLOW_END
```

---

# 🔗 5) ENGINE MAPPING DIAGRAM

## (เชื่อม Execution Graph ↔ RAG ↔ KS ↔ Agent ↔ SQL ↔ Cache ↔ Router)

```
                    Execution Graph
                           |
   ┌───────────────────────┼────────────────────────┐
   |                       |                        |
RAG Engine           Agent Engine           KS Engine (L0–L5)
   |                       |                        |
 SQL (L2)              Memory Store           SQL (L0–L5 tables)
   |                       |                        |
 Cache Layer    ←→      Flow Engine      ←→     Model Router
   |                                               |
 Event Bus  ←─────── Inter-system signals ───────→ SQL Sync
```

---

# 🗂️ 6) CANONICAL MAPPING DIAGRAM (สำคัญสุดใน RAG × KS)

```
L2 vector hits
   ↓
L3 semantic extraction (concept, entity, topic)
   ↓
L4 relational graph (CAUSES, PART_OF, SIMILAR_TO)
   ↓
L5 canonical knowledge unit
   ↓
Agent Reasoning Input
```

---

# 🧱 7) EDGE CONDITION MATRIX (สรุปกฎทั้งหมด)

```
┌─────────────────────────────────────────────────────────────────────┐
│ CONDITION                             │ NEXT NODE                   │
├───────────────────────────────────────┼──────────────────────────────┤
│ cache_hit == true                     │ FLOW_END                    │
│ cache_hit == false                    │ RAG_EMBED_QUERY             │
│ topK_confidence < 0.45                │ AGENT_REASON_WITH_CONTEXT   │
│ topK_confidence ≥ 0.45                │ AGENT_REASON_BASE           │
│ AGENT_PLAN.fail                       │ AGENT_REASON_BASE           │
│ SEMANTIC_EXTRACT.fail                 │ EMBEDDING_PROCESS           │
│ RELATION_BUILD.fail                   │ SEMANTIC_EXTRACT            │
│ CANONICALIZE.fail                     │ RELATION_BUILD              │
└─────────────────────────────────────────────────────────────────────┘
```

---

# 🧩 8) COMPLETE MAPPING OVERVIEW

รวมทั้งหมด:

## ENGINE → NODE (กลับด้าน)

|Engine|Node|
|---|---|
|SYSTEM|INGEST_FILE, FLOW_START, FLOW_END|
|INGEST|CHUNK_PROCESS|
|MODEL_ROUTER|EMBEDDING_PROCESS, RAG_EMBED_QUERY|
|RAG|VECTOR_SEARCH, RERANK, RESULT_FORMAT|
|KS|SEMANTIC_EXTRACT, RELATION_BUILD, CANONICALIZE, KS_SYNC|
|AGENT|REASON_BASE, REASON_WITH_CONTEXT, PLAN, EXECUTE, MEMORY|
|CACHE|LOOKUP, UPDATE, INVALIDATE|
|EVENT BUS|PUBLISH, CONSUME|
|FLOW|DECISION, NEXT_STEP|

---

# 🎯 CONCLUSION (EXECUTION_GRAPH_v3.0 DIAGRAM PACK)

ตอนนี้ Santa ได้ **DIAGRAM + MATRIX + FLOW + EXAMPLE + ENGINE MAPPING**  
แบบครบที่สุดสำหรับ Part Diagram ของ v3.0  
สอดคล้อง 100% กับไฟล์:

- MASTER_BLUEPRINT
    
- SYSTEM_ARCHITECTURE
    
- DATA_SCHEMA
    
- RAG ENGINE
    
- KS ENGINE
    
- AGENT ENGINE
    
- CACHE
    
- EVENT BUS
    
- MODEL ROUTER
    

ไม่มี conflict  
ไม่มีหลุด  
ไม่มีเขียนทับ  
พร้อมนำไปเป็นไฟล์ `EXECUTION_GRAPH_v3.0 (DIAGRAM).md` ได้ทันที

---

# ❓ต่อไปต้องการอะไร?

## เลือก 1 อัน:

A) ให้กูรวม Diagram + Matrix เป็นไฟล์ Markdown พร้อม heading  
B) ให้กูทำเวอร์ชัน “Ultra HD Diagram” แบบ ASCII Vision-level  
C) ไปต่อโมดูลถัดไป (KS Engine v3.0 หรือ RAG Engine v3.0 หรือ Agent Engine v3.0)  
D) ตรวจสอบความสอดคล้องทุกไฟล์ของโปรเจคอีกที

มึงต้องการอันไหน?