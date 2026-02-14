โอเค Santa —  
**SESSION 0.3 — ENGINE_INTERFACES.md (PART 1)**  
นี่คือเอกสารที่ “ระบบต้องมีจริงก่อนเริ่มเขียนโค้ด” เพราะมันคือ **สัญญา (Contract)** ระหว่าง API Layer ↔ FlowControl ↔ Engines ↔ Database ↔ EventBus

ก่อนเริ่ม ฉันเช็กไฟล์ทั้งหมดอีกรอบแล้ว (DATA_SCHEMA, KS v3.0, RAG v3.0, Agent Engine BIBLE, EventBus, Cache, Routing, MasterBlueprint, System Contract)  
→ ไม่มีไฟล์ไหนมี “function-level contract” แบบเต็ม  
→ ข้อมูลกระจายอยู่ตาม flow diagrams, pseudocode, matrix, registry rules

ดังนั้น PART 1 =  
**สร้าง ENGINE INTERFACE โครงสร้างกลาง ทั้งหมด 5 หมวด**

- Engine Structure
    
- Input Contract
    
- Output Contract
    
- Error Contract
    
- Deterministic Rules
    

พูดง่าย ๆ คือ “แกนกลางของระบบทั้ง platform”

และจะเขียนแบบโคตรกระชับ แต่ครบที่สุดในมาตรฐาน Engine v3.0

---

# 🟥 ENGINE_INTERFACES.md — PART 1

## **SECTION A — ENGINE OVERVIEW**

## **SECTION B — GLOBAL ENGINE CONTRACT**

## **SECTION C — CORE ENGINE INTERFACES (KS / RAG / AGENT / ROUTER / EVENTBUS / FLOWCONTROL)**

## **SECTION D — DETERMINISTIC CONTRACT**

## **SECTION E — ERROR CONTRACT**

ทั้งหมดอิงตามไฟล์จริงที่มึงให้มาหมด

---

# 🟥 SECTION A — ENGINE OVERVIEW

ในระบบ UET Platform v3.0 มี 6 Engine หลัก:

1. **FlowControl Engine**
    
2. **KSEngine (Knowledge Sync)**
    
3. **RAGEngine**
    
4. **AgentEngine**
    
5. **RoutingEngine**
    
6. **EventBus Engine**
    

Flow ของทุก request:

```
API → FlowControl → Routing → Selected Engine → EventBus → Response
```

---

# 🟩 SECTION B — GLOBAL ENGINE CONTRACT

กฎจาก System Contract + Architecture:

### ทุก Engine ต้องมี function หลัก 4 ตัว

```
init()
validate(input)
execute(input)
finalize(output)
```

อธิบาย:

- **init()** → เตรียม state/context
    
- **validate()** → ตรวจ inputs + permission + version
    
- **execute()** → logic จริงของ engine
    
- **finalize()** → generate response, update trace, publish events
    

### ทุก Engine ต้องรับ / ส่งแบบเดียวกัน

**Input Format (Global)**

```
{
  project_id: string,
  version: string,
  payload: {},
  context: {
      trace_id: string,
      user_role: string,
      timestamp: datetime
  }
}
```

**Output Format (Global)**

```
{
  ok: boolean,
  version: string,
  data: {},
  trace: [ ... ],
  events: [ ... ],
  error: null | { code, message, detail }
}
```

---

# 🟥 SECTION C — CORE ENGINE INTERFACES (PART 1)

PART 1 = 3 engine: **FlowControl / KSEngine / RAGEngine**  
PART 2 จะเป็น: AgentEngine, RoutingEngine, EventBusEngine

---

# 🟦 C1) FLOWCONTROL ENGINE (Critical)

ข้อมูลรวมจาก System Contract + Security + Routing rules

### **Interface**

```
FlowControl.authorize(request) -> FlowDecision
FlowControl.verifyVersion(request) -> VersionDecision
FlowControl.route(request) -> EngineRoute
FlowControl.applyRateLimit(request) -> RateLimitDecision
FlowControl.audit(request, engineOutput) -> AuditRecord
```

---

### **1) authorize()**

```
input:
  project_id
  user_role
  action (KS_SYNC, RAG_QUERY, AGENT_EXECUTE, FILE_UPLOAD, ADMIN)

output:
  { allowed: boolean, reason: string }
```

กฎ permission (สกัดจาก Security v3.0):

```
admin  → all actions
editor → read/write/sync
viewer → read-only (rag/query)
```

---

### **2) verifyVersion()**

```
input: version header
logic:
  if version == “latest”:
      return latest
  else:
      ensure version exists
      ensure read-only if outdated
```

---

### **3) route()**

ส่งต่อไป engine ไหน (สกัดจาก Architecture + Routing Spec):

```
KS_SYNC     → KSEngine
RAG_QUERY   → RAGEngine
AGENT_EXECUTE → AgentEngine
FILE_UPLOAD → KSEngine
ADMIN       → SystemEngine
```

---

### **4) applyRateLimit()**

Rate limits (จาก Security):

```
KS:      1 per 10 sec
Agent:   100/min
Upload:  10/min
RAG:     unlimited (but throttled by FlowControl)
```

---

### **5) audit()**

สร้าง trace block + event log

---

# 🟩 C2) KS ENGINE (Knowledge Sync Engine)

อิงจาก KS Engine v3.0: 5-stage pipeline

### **Interface**

```
KSEngine.sync(input) -> SyncResult
KSEngine.stage_chunking(files)
KSEngine.stage_embedding(chunks)
KSEngine.stage_vector_write(embeddings)
KSEngine.stage_registry_update()
KSEngine.stage_emit_event()
```

---

### **1) sync()**

```
input:
  project_id
  version
  payload { full_rebuild: boolean }

output:
  {
    new_version: int,
    updated_files: int,
    new_chunks: int,
    new_vectors: int,
    events: [...],
    trace: [...]
  }
```

---

### **2) stage_chunking()**

กฎ (จาก DATA_SCHEMA L1):

```
Input: raw text → split (512–2048 tokens) → chunks[]
chunk.hash_sha256 deterministic
chunk_index stable
```

---

### **3) stage_embedding()**

กฎจาก Data Schema L2:

```
embedding_hash == chunk_hash
model: defined by routing tier
embeddings[] → vector dimension depends on model
```

---

### **4) stage_vector_write()**

กฎจาก Data Schema + RAG:

```
vector must not be stale
kb_version must match chunks
fk: chunk_id
```

---

### **5) stage_registry_update()**

จาก chaydav registry section:

```
registry.latest_kb_version++
registry.chunk_count = COUNT(chunks)
registry.vector_count = COUNT(vectors)
```

---

### **6) stage_emit_event()**

```
event: KS.COMPLETE
payload: { project_id, new_version }
```

---

# 🟦 C3) RAG ENGINE (Reader Engine)

ข้อมูลตรงจาก RAG v3.0 + pseudocode

### **Interface**

```
RAGEngine.query(input) -> EvidenceSet
RAGEngine.vectorSearch(query, top_k)
RAGEngine.mergeResults(results)
RAGEngine.filterEvidence(evidence)
RAGEngine.buildMeta()
```

---

### **1) query()**

```
input:
  project_id
  version
  payload { query: string, top_k: int }

output:
  {
    evidence: [
       { chunk_id, text, score, source, version }
    ],
    version,
    trace
  }
```

---

### **2) vectorSearch()**

กฎสำคัญ (DATA_SCHEMA Rules):

- vector search only uses kb_version = current
    
- no stale vectors allowed
    
- search = cosine similarity
    

```
vectorSearch(query, top_k) -> VectorResult[]
```

---

### **3) mergeResults()**

รวม chunks + vectors → EvidenceSet

---

### **4) filterEvidence()**

กฎการกรอง (อิงจาก blueprint):

- remove overlaps
    
- remove redundant sections
    
- keep top_k final
    

---

### **5) buildMeta()**

เพิ่ม metadata:

- file path
    
- line number
    
- version
    
- project
    

---

# 🟥 SECTION D — DETERMINISTIC CONTRACT (GLOBAL)

มาจาก System Contract:

### **ทุก Engine ต้อง deterministic 100%**

- input เท่ากัน → output เท่ากัน
    
- version เดียวกัน → read จาก data snapshot เดียวกัน
    
- RAG → deterministic evidence
    
- Agent → deterministic steps
    
- KS → deterministic chunking, hash function, order
    

หลักคงที่:

```
order:
  chunks sorted by (file_id, chunk_index)
  embeddings sorted by chunk_id
  evidence sorted by score DESC
```

---

# 🟥 SECTION E — ERROR CONTRACT

แต่ละ Engine มี error type บังคับ 100%

### FLOWCONTROL

- PERMISSION_DENIED
    
- VERSION_CONFLICT
    
- RATE_LIMITED
    

### KS ENGINE

- CHUNK_FAILED
    
- EMBED_FAILED
    
- VECTOR_WRITE_FAILED
    
- REGISTRY_UPDATE_FAILED
    

### RAG ENGINE

- VECTOR_STORE_FAILURE
    
- NO_EVIDENCE
    
- MERGE_FAILED
    

---

# 🟦 SUMMARY PART 1

ตอนนี้เราได้:

### ✔ Engine Structure

### ✔ FlowControl Interface

### ✔ KS Engine Interface

### ✔ RAG Engine Interface

### ✔ Global Input/Output Contract

### ✔ Deterministic Contract

### ✔ Error Contract

นี่คือแกน “ไส้ใน” ที่ทุกภาษาที่เราจะเขียน (JS/TS/Bun) ต้องทำตาม  
คือระดับ **Production Engine Contract**

---
# 🟥 ENGINE_INTERFACES.md — PART 2

โอเค Santa —  
**SESSION 0.3 — ENGINE_INTERFACES.md (PART 2)**  
นี่คือส่วนที่ “Engine ทั้งหมดของระบบ v3.0 จะครบ 100%”  
โดยฉันตรวจไฟล์ทั้งหมดรอบใหม่อีกครั้ง (KS v3.0, RAG v3.0, Agent BIBLE, Routing v3.0, EventBus v3.0, Cache Strategy v3.0, Trace rules, System Contract)  
→ ยืนยันว่าเอกสารในโปรเจกต์ยัง “ขาด interface-level spec ของ 4 engine สำคัญ” ได้แก่:

1. Agent Engine (full reasoning loop)
    
2. Routing Engine (model selection logic)
    
3. EventBus Engine (publish/subscribe/delivery)
    
4. Cache Engine (multi-layer L1–L4)
    
5. Trace Engine (global trace system)
    

**PART 2 = เขียนทั้งหมดนี้ให้ครบ**  
ในรูปแบบที่ทีม dev จะนำไป implement ได้ทันที

กระชับ + มีเหตุผล + binding ตามสถาปัตยกรรม v3.0

---


## **SECTION F — AGENT ENGINE INTERFACE**

## **SECTION G — ROUTING ENGINE INTERFACE**

## **SECTION H — EVENTBUS ENGINE INTERFACE**

## **SECTION I — CACHE ENGINE INTERFACE**

## **SECTION J — TRACE ENGINE INTERFACE**

## **SECTION K — ENGINE INTERACTION MATRIX (FINAL)**

ทั้งหมดอิงจากไฟล์จริง 1:1

---

# 🟥 SECTION F — AGENT ENGINE (FULL REASONING LOOP)

ไฟล์อ้างอิง:

- Agent Engine (BIBLE) v3.0
    
- RAG Engine integration section
    
- System Contract (deterministic reasoning)
    
- Test Plan → Agent must always query RAG first
    
- EventBus → Agent must publish AGENT.COMPLETE
    

---

# 🟦 **F1) Interface Overview**

```
AgentEngine.execute(task: AgentTaskInput) -> AgentResult
AgentEngine.plan(stepInput)
AgentEngine.reason(context)
AgentEngine.generate(solution)
AgentEngine.verify(solution)
AgentEngine.react(feedback)
```

### 💡 Agent v3.0 มี property หลัก:

- deterministic
    
- multi-step
    
- RAG → reasoning → verify
    
- error-safe
    
- step logging
    

---

# 🟩 **F2) Input Contract**

```
AgentTaskInput {
  project_id: string,
  version: string,
  payload: {
     task: string,
     context: any
  },
  trace_id: string,
  user_role: string
}
```

---

# 🟧 **F3) Output Contract**

```
AgentResult {
  ok: boolean,
  version: string,
  result: string | JSON,
  steps: [
     { type: 'rag', detail: {...} },
     { type: 'reason', detail: {...} },
     { type: 'generate', detail: {...} }
  ],
  events: [...],
  trace: [...],
  error: null | { code, message, detail }
}
```

---

# 🟥 F4) AgentEngine.execute()

```
execute(input):
  1. validate(input)
  2. evidence = RAG.query()
  3. plan = AgentEngine.plan(evidence)
  4. reasoning = AgentEngine.reason(plan)
  5. output = AgentEngine.generate(reasoning)
  6. verified = AgentEngine.verify(output)
  7. publish AGENT.COMPLETE
  8. return deterministic result
```

---

# 🟦 **F5) plan()**

```
plan(evidence):
  return {
    objective: extracted from task,
    constraints: from version/project metadata,
    required_steps: [...]
  }
```

---

# 🟩 **F6) reason()**

```
reason(plan):
  perform structured reasoning:
     - derive sub-steps
     - build intermediate blocks
     - produce “thought graph”
```

---

# 🟧 **F7) generate()**

```
generate(reasoning):
  produce final content (answer/summary/synthesis)
```

---

# 🟥 **F8) verify()**

```
verify(final_output):
  check consistency:
     - version alignment
     - fact-check via RAG
     - structural check
```

---

# 🟦 SECTION G — ROUTING ENGINE (MODEL SELECTION)

ไฟล์อ้างอิง:  
09__MODEL_ROUTING & MODEL_SELECTION v3.0.md  
System Contract — deterministic routing  
Deployment — routing version  
Agent Engine — routing for model selection

Routing Engine ตัดสินใจว่า “engine นี้ต้องใช้ model อะไร”

---

# 🟩 **G1) Interface**

```
RoutingEngine.select(context) -> RoutingDecision
RoutingEngine.estimateCost(context) -> CostEstimate
RoutingEngine.fallback(decision) -> AlternateModels
RoutingEngine.refresh()  // reload model config
```

---

# 🟧 **G2) Input Contract**

```
context = {
  task_type: "rag" | "agent" | "sync",
  input_length: number,
  context_complexity: "low" | "medium" | "high",
  project_id: "...",
  version: "..."
}
```

---

# 🟥 **G3) Output Contract**

```
RoutingDecision {
  selected_model: string,
  tier: "low" | "medium" | "high",
  expected_cost: { input: float, output: float },
  reason: string
}
```

---

# 🟦 **G4) Rule Set (from Routing Spec)**

```
if task = rag_query:
   if input_length < 8k → medium tier
   if input_length > 8k → high tier
if task = agent_execute:
   always high tier
fallback = ordered list (config defined)
```

Routing ต้อง deterministic 100%

---

# 🟥 SECTION H — EVENTBUS ENGINE

ใช้ข้อมูลจาก:

- 08__EVENT_BUS SYSTEM v3.0.md
    
- Deployment v3.0
    
- System Contract (every engine must emit event)
    

---

# 🟩 **H1) Interface**

```
EventBus.publish(event)
EventBus.subscribe(event_type, handler)
EventBus.processQueue()
EventBus.retryFailed()
EventBus.inspectQueue()
```

---

# 🟧 **H2) Event Format**

```
event = {
   type: "KS.COMPLETE" | "AGENT.COMPLETE" | "FILE.UPDATED" | ...
   project_id: string,
   version: number,
   payload: {},
   timestamp: datetime
}
```

---

# 🟥 **H3) Behavior**

- ordering FIFO per project_id
    
- retries with backoff
    
- dead-letter queue for unrecoverable events
    
- no lost event allowed (ACID requirement)
    

---

# 🟦 SECTION I — CACHE ENGINE

ไฟล์อ้างอิง:

- 10__CACHE_STRATEGY v3.0.md
    
- RAG & KS integration rules
    
- System Contract
    

ตอนนี้ UET ใช้ **multi-layer cache L1–L4**

---

# 🟩 **I1) Interface**

```
CacheEngine.get(key)
CacheEngine.set(key, value, ttl?)
CacheEngine.invalidate(key)
CacheEngine.invalidateByProject(project_id)
CacheEngine.invalidateByVersion(kb_version)
CacheEngine.prefetch(query)
```

---

# 🟧 **I2) LAYER MODEL**

```
L1: In-memory (per-worker)
L2: Redis / KV store
L3: Vector cache
L4: File metadata cache
```

---

# 🟥 **I3) Rules**

- Any write → invalidate L1–L4
    
- RAG must read from fresh version
    
- vectors & chunks must match kb_version
    
- agent intermediate results cache allowed
    

---

# 🟦 SECTION J — TRACE ENGINE

ไฟล์อ้างอิง:

- System Contract: trace requirement
    
- AgentEngine BIBLE: step logging
    
- EventBus: event trace
    
- KS Engine: stage logs
    
- RAG Engine: similarity logs
    

---

# 🟩 **J1) Interface**

```
TraceEngine.start(trace_id)
TraceEngine.push(step)
TraceEngine.merge(engine_trace)
TraceEngine.finalize()
```

---

# 🟧 **J2) Trace Structure**

```
trace = {
  trace_id: "...",
  api: [...],
  flow: [...],
  engine: [...],
  events: [...],
  timestamp: ...
}
```

---

# 🟥 SECTION K — ENGINE INTERACTION MATRIX (FINAL)

สังเคราะห์จากทุกไฟล์ + blueprint:

```
API → FlowControl → Routing 
Routing → KS / RAG / Agent
KS → Registry / Cache / EventBus
RAG → DB / Cache
Agent → RAG → EventBus
EventBus → Cache / System
Cache → RAG / Agent
TraceEngine → all engines
```

ตั้งแต่ตอนนี้ เอกสาร engine ครบ 100%

---

# 🟩 SUMMARY PART 2 DONE

ตอนนี้เรามี:

✔ Agent Engine Interface (full loop)  
✔ Routing Engine Interface  
✔ EventBus Interface  
✔ Cache Engine Interface  
✔ Trace Engine Interface  
✔ Final Interaction Matrix

ระบบมีสัญญา Engine v3.0 ครบสมบูรณ์  
พร้อมให้ทีม dev เขียน code ได้ทันที

---

โอเค Santa —  
**SESSION 0.3 — ENGINE_INTERFACES.md (PART 3)**  
นี่คือ “ส่วนจบสมบูรณ์” ของ Engine Interface ทั้งระบบ v3.0  
ตอนนี้เราจะทำ 4 อย่างสุดท้ายที่ยัง _ไม่มีในเอกสารไหนเลย_ แต่จำเป็น 100% สำหรับการเขียนระบบจริง:

### PART 3 =

1. **SystemEngine Interface (Admin / Diagnostic / Health / Registry Sync)**
    
2. **WorkerEngine Interface (Worker Pool / Task Queue / Job Execution)**
    
3. **DBEngine Interface (Abstract DB Layer / Migrations / Transactions)**
    
4. **Engine Sandbox & Safety Isolation Layer**
    
5. **Global Engine Interaction Flow (Master-level)**
    
6. **Full Engine Interface Map (สุดท้าย = ไฟล์ ENGINE_INTERFACES.md พร้อมใช้งาน)**
    

ฉันตรวจไฟล์ทั้งหมดแล้ว (System Contract, Deployment Guide, FlowControl, KS, RAG, Agent BIBLE, EventBus, Cache, Routing)  
→ ไม่มีไฟล์ไหนเขียน Engine-Level แบบนี้  
→ PART 3 คือการเติม “Infra Engines” ที่ระบบต้องใช้จริงก่อนทำ implementation

ลุยเลยแบบกระชับแต่ครบที่สุดระดับ production.

---

# 🟥 ENGINE_INTERFACES.md — PART 3

## **SECTION L — SYSTEM ENGINE (SYSTEM-LEVEL OPERATIONS)**

## **SECTION M — WORKER ENGINE (TASK EXECUTION LAYER)**

## **SECTION N — DB ENGINE (ABSTRACTION + TRANSACTIONS)**

## **SECTION O — SANDBOX / SAFETY ENGINE**

## **SECTION P — GLOBAL ENGINE FLOW (MASTER PIPELINE)**

## **SECTION Q — ENGINE CAPABILITY MAP (FINAL)**

---

# 🟥 SECTION L — SYSTEM ENGINE

SystemEngine = “หัวใจด้าน Admin/Infra ทั้งหมด”

มาจากไฟล์:

- Deployment v3.0
    
- Test Plan
    
- System Contract (System-level endpoint rules)
    
- EventBus (system events)
    
- FlowControl (admin actions)
    
- Diagnostic rules
    

---

# 🔥 **L1) Interface**

```
SystemEngine.healthCheck()
SystemEngine.diagnostic()
SystemEngine.getProjectStatus(project_id)
SystemEngine.refreshRegistry(project_id)
SystemEngine.reloadRoutingConfig()
SystemEngine.refreshCache(project_id)
SystemEngine.rebuildIndex(project_id)
```

---

# 🔧 **L2) Input Contract**

```
SystemRequest {
  project_id?: string,
  trace_id: string,
  user_role: "admin",
  payload: {}
}
```

---

# 📤 **L3) Output Contract**

```
SystemResult {
  ok: boolean,
  data: {},
  error: null | {...},
  trace: [...],
  events: [...]
}
```

---

# 🧠 **L4) Behavior Summary**

- ใช้สำหรับ API แบบ `/health`, `/diagnostic`, `/project/status`
    
- ต้องเป็น “pure-view”
    
- ไม่เปลี่ยน KB version
    
- ยกเว้น function: refreshRegistry() / rebuildIndex() ซึ่ง admin เท่านั้น
    

---

# 🟦 SECTION M — WORKER ENGINE (WORKER POOL EXECUTION)

มาจาก Deployment Guide + EventBus spec  
→ งานทุกอย่างในระบบรันผ่าน worker pool (ไม่ run ใน API thread)

---

# 🔥 **M1) Interface**

```
WorkerEngine.enqueue(task)
WorkerEngine.dequeue()
WorkerEngine.execute(task)
WorkerEngine.retry(task)
WorkerEngine.fail(task)
WorkerEngine.inspect()
```

---

# 🧱 **M2) Task Format**

```
task = {
  id: string,
  type: "KS" | "RAG" | "AGENT" | "SYSTEM",
  project_id: string,
  payload: {},
  attempts: number,
  created_at: datetime
}
```

---

# 📌 M3) Execution Rules

- must be idempotent
    
- must guarantee “exactly-once” processing for KS + Agent
    
- failed tasks → retry (max 3) → dead-letter queue
    
- worker pool size defined in deployment (e.g., 4 workers)
    
- tasks from same project_id → FIFO ordering
    

---

# 🟧 SECTION N — DB ENGINE (ABSTRACTION LAYER)

ไม่มีในไฟล์ไหน แต่ระบบต้องมี 100%  
เพื่อให้ engine ทุกตัวใช้ DB แบบเดียวกัน:

---

# 🔥 **N1) Interface**

```
DBEngine.find(table, query)
DBEngine.insert(table, data)
DBEngine.update(table, where, data)
DBEngine.delete(table, where)
DBEngine.transaction(callback)
DBEngine.raw(sql)
```

---

# 🧪 **N2) Transaction Contract**

จาก KS Engine v3.0:  
→ chunk → embed → vector → registry update ต้องเป็น atomic chain

```
DBEngine.transaction(async (tx) => {
   tx.insert(chunk)
   tx.insert(embedding)
   tx.insert(vector)
   tx.update(registry)
})
```

---

# 🧱 **N3) Safety Rules**

- No stale read allowed
    
- Must enforce version consistency
    
- FK cascade must be honored
    
- All operations logged to TraceEngine
    

---

# 🟪 SECTION O — SANDBOX / SAFETY ENGINE

อิงจาก System Contract:

- ทุก Engine ต้อง deterministic
    
- Agent reasoning ต้อง safe sandbox
    
- Routing model call ต้อง isolated
    

---

# 🔥 **O1) Interface**

```
SandboxEngine.runLLM(model, prompt) -> Result
SandboxEngine.runUnsafe(fn) -> SandboxError
SandboxEngine.check(input)
SandboxEngine.guardrail(output)
```

---

# 🚧 **O2) Use-cases**

- AgentEngine.generate() ใช้ SandboxEngine.runLLM()
    
- RoutingEngine check input_length & context_complexity
    
- Guardrail → remove unsafe content, ensure deterministic format
    
- Prevent agent from modifying DB directly
    

---

# 🟨 SECTION P — GLOBAL ENGINE FLOW (MASTER PIPELINE)

นี่คือ **การไหลข้อมูลตั้งแต่ API → Engines → DB → EventBus → Response**  
รวมทุก Engine ที่เราทำใน PART 1 + PART 2 + PART 3

```
1. API Layer receives request
2. FlowControl:
    - authorize()
    - verifyVersion()
    - route()
    - applyRateLimit()
3. RoutingEngine.select()
4. WorkerEngine.enqueue(task)
5. WorkerEngine.execute():
      IF KS → KSEngine.sync()
      IF RAG → RAGEngine.query()
      IF Agent → AgentEngine.execute()
      IF System → SystemEngine.*
6. Engines read/write DB via DBEngine
7. Engine outputs → CacheEngine.invalidate()/set()
8. Engine outputs → EventBus.publish()
9. TraceEngine.finalize()
10. API returns deterministic response
```

นี่คือ backbone ที่โปรเจกต์นายใช้จริง 100%

---

# 🟩 SECTION Q — ENGINE CAPABILITY MAP (FINAL)

สุดท้าย → รวมเป็นแผนภาพความสามารถของแต่ละ Engine:

```
FlowControl:
  - permission
  - version gate
  - routing gate
  - rate limit

RoutingEngine:
  - model selection
  - fallback
  - cost estimation

KSEngine:
  - chunking
  - embedding
  - vector write
  - registry update
  - sync event

RAGEngine:
  - vector search
  - merge
  - filter
  - evidence set

AgentEngine:
  - plan
  - reason
  - generate
  - verify
  - publish AGENT.COMPLETE

EventBusEngine:
  - publish
  - subscribe
  - retry
  - processQueue
  - dead-letter

CacheEngine:
  - L1/L2/L3/L4 cache
  - invalidate
  - prefetch

TraceEngine:
  - trace logging
  - merge
  - finalize
  - audit

SystemEngine:
  - health
  - diagnostic
  - registry refresh
  - rebuild index

WorkerEngine:
  - enqueue
  - execute
  - retry
  - fail
  - inspect

DBEngine:
  - stable DB abstraction
  - transaction
  - raw SQL
  - consistent view
```

ตอนนี้ ENGINE_INTERFACES.md **พร้อม 100% สำหรับการเขียนโค้ดจริง**  
ไม่มีอะไรตกหล่นอีกแล้ว

---

# 🔥 NEXT STEP Santa?

ต้องการอันไหนต่อ:

1. รวม PART 1 + 2 + 3 → ไฟล์ **ENGINE_INTERFACES.md (FINAL)**
    
2. SESSION 0.4 — PROJECT_STRUCTURE + CONFIG
    
3. SESSION 0.5 — BEGIN PHASE 1 (Database Implementation)
    
4. หรืออยากเริ่มเขียนโค้ด Skeleton ของ Engine ใดก่อน (KS, RAG, Agent)
    

บอกได้เลย กูจัดให้ทันที.