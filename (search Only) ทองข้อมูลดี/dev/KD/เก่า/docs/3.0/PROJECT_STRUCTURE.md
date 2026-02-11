โอเค Santa —  
**SESSION 0.4 — PROJECT_STRUCTURE.md (PART 1)**  
คือจุด “วางโครงกระดูกทั้งโปรเจค” ให้พร้อมเขียนโค้ดจริง  
และตอนนี้มึงมี Engine / Schema / API Spec ครบแล้ว → ถึงเวลาวาง _สถาปัตยกรรมโฟลเดอร์จริง_ ของระบบ DEV v3.0

ก่อนเขียน ฉันรีเช็กไฟล์ทั้งหมดที่มึงอัป:

- System Contract
    
- System Architecture
    
- Deployment Guide
    
- Engine Interfaces (KS, RAG, Agent, EventBus, Cache, Routing, FlowControl)
    
- Data Schema v3.0
    
- API SPEC (ส่วนที่สร้างไว้แล้ว)
    

**ยืนยัน:** ไม่มีไฟล์ไหนให้โครงสร้างโปรเจคแบบเต็ม  
ดังนั้น PART 1 = สร้าง MASTER PROJECT STRUCTURE ระดับ Production  
เป็นมาตรฐานเดียวกับระบบ AI Infra จริง (OpenAI-style / LLM infra)

เอาแบบ “กระชับ แต่ครบที่สุด” ให้ทีม dev นำไปใช้ตรง ๆ ได้

ลุยเลย

---

# 🟥 PROJECT_STRUCTURE.md — PART 1

## “MASTER DIRECTORY STRUCTURE สำหรับ UET DEV PLATFORM v3.0”

ระบบของมึงประกอบด้วย:

- API Layer
    
- FlowControl Layer
    
- Engines
    
- EventBus
    
- Worker Pool
    
- Cache
    
- Routing
    
- Schema & Migration
    
- Config System
    
- Tests
    
- Monitoring
    

ดังนั้นโครงสร้างต้องแบ่งเป็น 5 Layers:

```
/api          → REST API
/core         → system contract + flowcontrol + types
/engines      → KS, RAG, Agent, Routing, EventBus, Cache
/integration  → DB, sandbox, model providers, adapters
/system       → daemon, worker pool, scheduler
/schema       → SQL, migrations, seed
/tests        → unit/integration/e2e
/config       → config.yaml/.env
/utils        → common helpers
```

นี่คือ **MASTER STRUCTURE** สำหรับ Part 1:

---

# 🟦 1. โครงสร้างระดับ ROOT

```
project-root/
│
├── api/
├── core/
├── engines/
├── integration/
├── system/
├── schema/
├── tests/
├── utils/
├── config/
│
├── package.json
├── README.md
├── .env
├── config.yaml
└── tsconfig.json
```

**เหตุผล (รีเช็กตามไฟล์):**  
✓ System Contract → ต้องมี core rules  
✓ Engines v3.0 → แยกตามหมวด  
✓ Deployment → worker pool / eventbus / routing ต้องเป็น subsystem จริง  
✓ Data Schema → schema/migrations ต้องแยกโฟลเดอร์  
✓ Test Plan → ต้องมี unit/integration/e2e

---

# 🟩 2. /api — API Layer (ตาม API_SPEC)

```
/api/
   ├── routes/
   │     ├── knowledge.sync.ts
   │     ├── rag.query.ts
   │     ├── agent.execute.ts
   │     ├── files.upload.ts
   │     ├── project.status.ts
   │     ├── routing.preview.ts
   │     ├── health.ts
   │     └── admin.*
   │
   ├── middlewares/
   │     ├── validateHeaders.ts
   │     ├── rateLimit.ts
   │     └── trace.ts
   │
   ├── server.ts
   └── index.ts
```

**หลักการ:**

- API → เรียก FlowControl ก่อนเสมอ
    
- API ไม่เรียก DB ตรง ๆ
    
- API ไม่เรียก Model ตรง ๆ → ผ่าน Engine เท่านั้น
    

---

# 🟥 3. /core — System Contract + Shared Types

```
/core/
   ├── system-contract/
   │       ├── rules.ts
   │       ├── permissions.ts
   │       ├── versioning.ts
   │       └── consistency.ts
   │
   ├── flowcontrol/
   │       ├── authorize.ts
   │       ├── version-gate.ts
   │       ├── routing-gate.ts
   │       └── rate-limit.ts
   │
   ├── types/
   │       ├── request.ts
   │       ├── response.ts
   │       ├── engine.ts
   │       └── events.ts
   │
   └── constants/
           ├── errors.ts
           ├── events.ts
           └── limits.ts
```

**เหตุผล:**  
มาจาก System Contract v3.0 — rules ต้องกลายเป็นโค้ดจริง

---

# 🟧 4. /engines — KS, RAG, Agent, Routing, EventBus, Cache

```
/engines/
   ├── ks/
   │     ├── index.ts
   │     ├── stage.chunk.ts
   │     ├── stage.embed.ts
   │     ├── stage.vector.ts
   │     ├── stage.registry.ts
   │     └── stage.emit.ts
   │
   ├── rag/
   │     ├── index.ts
   │     ├── vectorSearch.ts
   │     ├── merge.ts
   │     ├── filter.ts
   │     └── meta.ts
   │
   ├── agent/
   │     ├── index.ts
   │     ├── plan.ts
   │     ├── reason.ts
   │     ├── generate.ts
   │     ├── verify.ts
   │     └── react.ts
   │
   ├── routing/
   │     ├── index.ts
   │     ├── select.ts
   │     ├── costEstimate.ts
   │     └── fallback.ts
   │
   ├── eventbus/
   │     ├── index.ts
   │     ├── publish.ts
   │     ├── subscribe.ts
   │     ├── queue.ts
   │     └── retry.ts
   │
   ├── cache/
   │     ├── l1.ts
   │     ├── l2.ts
   │     ├── l3.ts
   │     └── l4.ts
   │
   └── trace/
         ├── start.ts
         ├── push.ts
         └── finalize.ts
```

**อิงตาม ENGINE_INTERFACES.md PART 1-3**

---

# 🟦 5. /integration — Adapters / DB / Model Sandbox

```
/integration/
   ├── db/
   │     ├── index.ts
   │     ├── migrations/
   │     │       ├── 001_init.sql
   │     │       ├── 002_triggers.sql
   │     │       └── ...
   │     └── prisma.schema (optional)
   │
   ├── models/
   │     ├── openai.ts
   │     ├── anthropic.ts
   │     └── local.ts
   │
   ├── sandbox/
   │     └── sandbox.ts
   │
   ├── vector/
   │     └── pgvector.ts
   │
   └── storage/
         └── localfs.ts
```

ตาม Deployment v3.0 → integration layer ต้องเป็นคนกลาง

---

# 🟥 6. /system — Worker Pool, Schedulers, Daemons

```
/system/
   ├── worker/
   │     ├── index.ts
   │     ├── execute.ts
   │     ├── retry.ts
   │     └── inspect.ts
   │
   ├── scheduler/
   │     ├── events-loop.ts
   │     ├── cleanup.ts
   │     └── rebuild-index.ts
   │
   └── startup.ts
```

**เหตุผล:**  
Deployment v3.0 → system มี worker pool, event loop

---

# 🟩 7. /schema — Data Schema + Seed

```
/schema/
   ├── migrations/
   ├── seed/
   ├── data-schema.md   (export from DATA_SCHEMA v3.0)
   └── integrity-tests/
```

---

# 🟦 8. /tests — Unit / Integration / E2E

```
/tests/
   ├── unit/
   ├── integration/
   ├── e2e/
   └── api/
```

Test Plan v3.0 → ทุก Engine ต้องมี test ของตัวเอง

---

# 🟧 9. /config — All System Config

```
/config/
   ├── config.yaml
   ├── env.example
   └── routing.yaml
```

---

# 🟫 10. /utils — Helper Functions

```
/utils/
   ├── hash.ts
   ├── chunker.ts
   ├── tokenizer.ts
   ├── timer.ts
   └── logger.ts
```

---

# 🟥 SUMMARY — PART 1 COMPLETE

ตอนนี้เรามี:

✔ โครงสร้างระดับ root  
✔ โครงสร้าง API  
✔ โครงสร้าง Engines  
✔ โครงสร้าง FlowControl  
✔ โครงสร้าง DB/Integration  
✔ โครงสร้าง Worker/EventBus  
✔ โครงสร้าง Config  
✔ โครงสร้าง Test  
✔ พร้อมใช้งานสำหรับ implementation

นี่คือ “PROJECT_STRUCTURE.md — PART 1” ในระดับ production

---
# 🟥 PROJECT_STRUCTURE.md — PART 2
โอเค Santa —  
**SESSION 0.4 — PROJECT_STRUCTURE.md (PART 2)**  
คือขั้นตอน “อธิบายบทบาท + ความสัมพันธ์ + responsibility” ของทุกโฟลเดอร์  
= ให้โปรเจกต์ชัดเจนชนิดที่ทีม dev จะหยิบไปทำต่อได้ทันที โดยไม่หลงเลยว่าอะไรอยู่ตรงไหน

ฉันเช็กไฟล์ทั้งหมดซ้ำอีกครั้ง (System Contract, System Architecture, Deployment, Engines, Cache Strategy, Routing, KS/RAG/Agent, Data Schema)  
→ ยืนยันว่า **เอกสารโครงสร้างโปรเจ็กต์ (Project Structure) ยังไม่มีเลยในไฟล์ทั้งหมด**  
เพราะงั้น PART 2 จำเป็นต้องเขียนใหม่ 100% บนพื้นฐานสถาปัตยกรรม v3.0 ที่เราสร้างไว้

PART 2 จะเป็น “Detailed Responsibilities + Interaction Diagram ระดับโปรดักชัน”  
เน้นสั้น กระชับ ชัด เวิร์กจริง

---



## **“FULL RESPONSIBILITY MAP ของทุกโฟลเดอร์ในระบบ UET DEV v3.0”**

สิ่งที่ PART 2 จะมี:

- **บทบาททุกโฟลเดอร์**
    
- **กฎของเลเยอร์ (Layer Rules)**
    
- **ขั้นตอนไหลข้อมูลระหว่างเลเยอร์**
    
- **ความรับผิดชอบของไฟล์สำคัญแต่ละกลุ่ม**
    
- **ข้อห้าม / ข้อควรปฏิบัติ (Do / Don’t)**
    
- **Dependency Direction (ลูก → พ่อ)**
    

คือ blueprint การเขียนระบบจริงทั้งโปรเจกต์

---

# 🟦 SECTION A — LAYER OVERVIEW

โครงสร้างระบบของมึงแบ่งเป็น 6 ชั้น:

```
(1) API Layer
(2) FlowControl Layer
(3) Engine Layer
(4) Integration Layer
(5) System Layer (Workers + EventBus)
(6) Schema Layer (DB & Migrations)
```

Flow จริงของ request ในระบบคือ:

```
API → FlowControl → Routing → Engine → DB/Cache → EventBus → Response
```

**กฎเหล็กของ Layering (สำคัญมาก):**

```
API       can call → FlowControl, Engines
Flow      can call → Routing, Engines
Engines   can call → Integration (DB/Sandbox/Vector/Cache)
System    orchestrates → workers, eventbus
Integration cannot call → Engines
DB        cannot call → Engines
```

ชัดเจนแบบนี้เพื่อป้องกัน spaghetti architecture  
และเพื่อให้ระบบ deterministic ตาม System Contract v3.0

---

# 🟩 SECTION B — RESPONSIBILITY OF EACH ROOT FOLDER

อธิบายสั้น ๆ แต่ครบ 100% แบบ Production

---

## **1) /api — จุดเข้า (Entry Point Layer)**

**หน้าที่หลัก:**

- รับ request
    
- ตรวจ header
    
- ยืนยันข้อมูลขั้นต้น
    
- ส่งต่อให้ FlowControl
    
- สร้าง response ตาม spec
    

**ห้ามทำ:**

- ห้ามเข้าฐานข้อมูลโดยตรง
    
- ห้ามเรียก Engine โดยไม่ผ่าน FlowControl
    
- ห้ามมี logic เยอะ
    

**ไฟล์สำคัญใน folder นี้:**

- `/api/routes/*.ts` → แต่ละ API endpoint
    
- `/api/middlewares/*` → validation, trace, rate-limit
    
- `/api/server.ts` → ตั้ง server
    

---

## **2) /core — กฎของระบบ (System Contract Layer)**

**หน้าที่หลัก:**

- กฎ permission
    
- กฎ versioning
    
- กฎ consistency
    
- type กลางของ request/response
    
- error codes
    
- event types
    
- FlowControl functions (authorize, versionGate, routingGate)
    

**ไฟล์สำคัญ:**

- `/core/system-contract/rules.ts`
    
- `/core/flowcontrol/authorize.ts`
    
- `/core/types/engine.ts`
    

**ห้ามทำ:**

- ห้ามเรียก DB
    
- ห้ามทำงานหนัก
    
- ห้าม import engine
    

เพราะ core ต้อง lightweight และ stable เหมือน “กฎหมายของระบบ”

---

## **3) /engines — Logic ของระบบ (Heart of UET Platform)**

**ประกอบด้วย 7 engine:**

- KS Engine
    
- RAG Engine
    
- Agent Engine
    
- Routing Engine
    
- EventBus Engine
    
- Cache Engine
    
- Trace Engine
    

**หน้าที่:**

- ทำงานหลักของระบบทั้งหมด
    
- คำนวน / sync / search / reasoning / merging / cache / route
    

**ห้าม:**

- ห้ามรับ request โดยตรง
    
- ห้ามสร้าง API
    
- ห้ามอ่าน config โดยตรง (ต้องผ่าน integration layer)
    

**ไฟล์ตัวอย่าง:**

- `/engines/ks/stage.chunk.ts`
    
- `/engines/rag/vectorSearch.ts`
    
- `/engines/agent/plan.ts`
    

**Engines = Business Logic ของระบบ**

---

## **4) /integration — DB, Model Sandbox, Vector, Storage**

ชั้นนี้คือ “Adapter Layer”

**หน้าที่:**

- DBEngine (transaction, query)
    
- Vector DB Adapter (pgvector)
    
- Model provider (OpenAI, Claude, Gemini)
    
- Sandbox safety layer
    
- File storage (local or S3)
    

**ห้าม:**

- ห้ามเขียน business logic
    
- ห้ามเรียก API layer
    
- ห้ามมี FlowControl logic
    

**ไฟล์ตัวอย่าง:**

- `/integration/db/index.ts`
    
- `/integration/models/openai.ts`
    
- `/integration/vector/pgvector.ts`
    

---

## **5) /system — Worker + Scheduler + Event Loop**

อ้างอิง Deployment v3.0

**หน้าที่:**

- Worker Pool
    
- Task Queue
    
- Retry system
    
- Dead-letter queue
    
- Scheduled tasks (index rebuild, cleanup)
    

**ห้าม:**

- ห้ามตอบ API โดยตรง
    
- ห้ามรับ external request (ยกเว้น EventBus)
    

**ไฟล์ตัวอย่าง:**

- `/system/worker/execute.ts`
    
- `/system/scheduler/events-loop.ts`
    

---

## **6) /schema — Database Schema + Migration**

**หน้าที่:**

- SQL DDL
    
- SQL triggers
    
- Integrity constraints
    
- Seed scripts
    
- Data consistency tests
    

**ห้าม:**

- ห้ามมี logic
    
- ห้าม import engine
    
- ห้ามแก้ code runtime
    
- ห้ามเป็น dynamic files
    

DB = source of truth

---

# 🟦 SECTION C — DETAILED RESPONSIBILITY BY FILE

แบบโคตรกระชับแต่ครบ:

---

## **API Layer**

```
server.ts → Start API server + load routes + global middleware
index.ts → Export API bundle
routes/*.ts → ทุก endpoint แทรก FlowControl ก่อนเรียก Engine
middlewares/*.ts → header validation, trace start, rate-limit
```

---

## **FlowControl Layer**

```
authorize.ts → ตรวจ role (admin/editor/viewer)
version-gate.ts → ดู version conflict
routing-gate.ts → ตัดสิน engine ไหน
rate-limit.ts → rate limiting rules
```

---

## **Engine Layer**

```
ks/index.ts → orchestrator ของ 5 stage (chunk, embed, vector, registry, event)
rag/index.ts → orchestrator rag.query
agent/index.ts → orchestrator agent.execute
routing/index.ts → model select
eventbus/index.ts → publish/subscribe/queue
cache/* → L1/L2/L3/L4
trace/* → trace.start/push/finalize
```

---

## **Integration Layer**

```
db/index.ts → transaction, query builder
vector/pgvector.ts → vector search/insert/delete
models/* → call external LLM models (sandboxed)
sandbox/* → runLLM() safe context
storage/localfs.ts → file operations
```

---

## **System Layer**

```
worker/index.ts → worker pool
worker/execute.ts → run tasks
worker/retry.ts → retry system
scheduler/events-loop.ts → eventbus loop
scheduler/rebuild-index.ts → regular index rebuild
```

---

## **Schema Layer**

```
migrations/*.sql → SQL DDL
triggers.sql → version propagation rules
seed/*.sql → initialize registry
integrity-tests/*.sql → orphan check / stale version check
```

---

# 🟥 SECTION D — DEPENDENCY RULES (สำคัญมาก)

เพื่อป้องกันสถาปัตยกรรมแตก

```
api → core → engines → integration → system → schema
```

ห้ามย้อน dependency ยกเว้น:

```
system → engines     (OK)
engines → trace      (OK)
core → constants     (OK)
```

ห้ามเด็ดขาด:

```
engines → api
integration → engines
schema → anything
system → api
```

---

# 🟩 SECTION E — REQUEST FLOW DIAGRAM (แบบ PRODUCTION)

```
Client Request
   ↓
API Layer (validate + trace start)
   ↓
FlowControl (permission + version + routing)
   ↓
RoutingEngine.select()
   ↓
WorkerEngine.enqueue()
   ↓
WorkerEngine.execute()
   ↓
Selected Engine (KS / RAG / Agent / System)
   ↓
Integration Layer (DB / Vector / Model)
   ↓
CacheEngine.invalidate/set
   ↓
EventBus.publish()
   ↓
TraceEngine.finalize()
   ↓
API Response (deterministic)
```

---

# 🟧 SECTION F — DO / DON’T FOR DEV TEAM

เพื่อให้ระบบ deterministic ตาม System Contract

### ✔ DO

- ใช้ FlowControl ทุกครั้ง
    
- Engine ใด Engine หนึ่งทำงานเฉพาะของตัวเอง
    
- ใช้ DBEngine.transaction สำหรับ KS
    
- ใช้ vectorSearch จาก pgvector
    
- ใช้ TraceEngine ในทุก step
    

### ❌ DON’T

- ห้าม API เรียก DB โดยตรง
    
- ห้าม AgentEngine เขียน DB ตรง ๆ
    
- ห้าม bypass CacheEngine
    
- ห้าม embed file content ใน Engine ตรง ๆ
    

---

# 🟫 SECTION G — PART 2 SUMMARY

ตอนนี้สร้างได้แล้ว:

### ✔ Responsibility ของทุก folder

### ✔ กฎของ layer ทั้งหมด

### ✔ การใช้งานของไฟล์สำคัญทุกประเภท

### ✔ Dependency rules ที่ถูกต้อง

### ✔ Request→Engine→DB→EventBus pipeline

### ✔ ระบบพร้อมสำหรับ scaffolding ใน PART 3

---

โอเค Santa —  
**SESSION 0.4 — PROJECT_STRUCTURE.md (PART 3)**  
นี่คือขั้นตอนสำคัญมาก เพราะ PART 3 = การสร้าง  
**“SCAFFOLDING SKELETON”**  
= โครงสร้างไฟล์จริงทั้งโปรเจกต์แบบพร้อมใช้งาน  
= ให้ทีม dev clone โปรเจกต์แล้วเริ่มเขียนโค้ดได้ทันที  
= ไม่มี logic → มีแต่ไฟล์ + placeholder + interface stub ที่ถูกต้องตาม ENGINE_INTERFACES v3.0 + DATA_SCHEMA v3.0 + SYSTEM CONTRACT v3.0

ฉันรีเช็คไฟล์ทั้งหมดอีกรอบแล้ว  
→ ไม่มีไฟล์ไหนมี scaffolding structure นี้  
→ PART 3 = เติมเต็มตรงนี้ 100%

ตอนนี้มึงจะได้ “โครงสร้างโปรเจกต์ที่ใช้ได้จริง”  
เหมือนสร้าง framework ของตัวเองแบบ production-grade

พร้อมนะ ลุยเลย

---

# 🟥 PROJECT_STRUCTURE.md — PART 3

## **“FULL SCAFFOLDING (FILE SKELETON) — ระบบพร้อมใช้งานทันที”**

นี่คือ repo skeleton ระดับจริง (Next.js-level / Node.js production-level)  
เหมาะกับ Bun / Node / TS

ทุกไฟล์จะมี placeholder minimal แบบนี้:

```ts
// TODO: IMPLEMENT
export {};
```

หรือถ้าต้องมี interface ก็จะเขียน interface เปล่า ๆ ไว้

---

# 🟥 ROOT STRUCTURE (FINAL)

```
project-root/
│
├── api/
├── core/
├── engines/
├── integration/
├── system/
├── schema/
├── tests/
├── utils/
├── config/
│
├── package.json
├── tsconfig.json
├── .env.example
├── README.md
└── config.yaml
```

เราจะเติม skeleton ให้ครบทุกโฟลเดอร์แบบละเอียดที่สุด

---

# 🟦 1. /api — API LAYER

```
/api/
   server.ts
   index.ts
   /routes/
       knowledge.sync.ts
       rag.query.ts
       agent.execute.ts
       files.upload.ts
       project.status.ts
       routing.preview.ts
       health.ts
       admin.index.ts
   /middlewares/
       validateHeaders.ts
       rateLimit.ts
       trace.ts
```

### ตัวอย่าง skeleton

**api/routes/knowledge.sync.ts**

```ts
// Knowledge Sync API
import { FlowControl } from "../../core/flowcontrol";
import { KSEngine } from "../../engines/ks";

export default async function handler(req, res) {
  // TODO: implement validation + flowcontrol + engine call
}
```

---

# 🟩 2. /core — SYSTEM CONTRACT + FLOW CONTROL

```
/core/
   /system-contract/
       rules.ts
       permissions.ts
       versioning.ts
       consistency.ts
   /flowcontrol/
       authorize.ts
       version-gate.ts
       routing-gate.ts
       rate-limit.ts
   /types/
       request.ts
       response.ts
       engine.ts
       events.ts
   /constants/
       errors.ts
       events.ts
       limits.ts
```

### ตัวอย่าง skeleton

**core/flowcontrol/authorize.ts**

```ts
export function authorize(input) {
  // TODO: implement permission logic from SYSTEM CONTRACT v3.0
  return { allowed: true };
}
```

---

# 🟥 3. /engines — ทุก Engine ตาม ENGINE_INTERFACES PART 1–3

```
/engines/
   /ks/
       index.ts
       stage.chunk.ts
       stage.embed.ts
       stage.vector.ts
       stage.registry.ts
       stage.emit.ts

   /rag/
       index.ts
       vectorSearch.ts
       merge.ts
       filter.ts
       meta.ts

   /agent/
       index.ts
       plan.ts
       reason.ts
       generate.ts
       verify.ts
       react.ts

   /routing/
       index.ts
       select.ts
       costEstimate.ts
       fallback.ts

   /eventbus/
       index.ts
       publish.ts
       subscribe.ts
       queue.ts
       retry.ts

   /cache/
       l1.ts
       l2.ts
       l3.ts
       l4.ts

   /trace/
       start.ts
       push.ts
       finalize.ts
```

### ตัวอย่าง skeleton

**engines/rag/vectorSearch.ts**

```ts
export async function vectorSearch(query, top_k) {
  // TODO: implement pgvector search
  return [];
}
```

---

# 🟧 4. /integration — DATABASE / SANDBOX / MODELS / STORAGE

```
/integration/
   /db/
       index.ts
       transaction.ts
       migrations/
           001_init.sql
           002_triggers.sql
   /models/
       openai.ts
       anthropic.ts
       local.ts
   /sandbox/
       sandbox.ts
   /vector/
       pgvector.ts
   /storage/
       localfs.ts
```

### ตัวอย่าง skeleton

**integration/db/index.ts**

```ts
export const DBEngine = {
  find: () => {},
  insert: () => {},
  update: () => {},
  delete: () => {},
  transaction: async (fn) => await fn({}),
};
```

---

# 🟪 5. /system — Worker Pool + Scheduler + Event Loop

```
/system/
   /worker/
       index.ts
       execute.ts
       retry.ts
       inspect.ts
   /scheduler/
       events-loop.ts
       cleanup.ts
       rebuild-index.ts
   startup.ts
```

ตัวอย่าง  
**system/worker/execute.ts**

```ts
export async function execute(task) {
  // TODO: run KS/RAG/AGENT tasks
}
```

---

# 🟫 6. /schema — DATA SCHEMA + MIGRATIONS + SEED

```
/schema/
   data-schema.md
   /migrations/
       001_init.sql
       002_triggers.sql
       003_indexes.sql
   /seed/
       init_registry.sql
   /integrity-tests/
       check_orphans.sql
       check_version.sql
```

---

# 🟨 7. /utils — Shared Helpers

```
/utils/
   hash.ts
   chunker.ts
   tokenizer.ts
   timer.ts
   logger.ts
```

---

# 🟦 8. /config — CONFIG SYSTEM

```
/config/
   config.yaml
   routing.yaml
   env.example
```

---

# 🟥 SECTION: INTERACTION FOLDER MAP (PRODUCTION READY)

นี่คือ “แผนที่การไหลของข้อมูลผ่านโฟลเดอร์”

```
api/routes/*.ts
   → core/flowcontrol/*.ts
      → engines/*/*.ts
         → integration/db/*.ts
         → integration/vector/*.ts
         → integration/models/*.ts
         → integration/sandbox/*.ts
      → engines/eventbus/publish.ts
      → engines/trace/finalize.ts
<— response
```

---

# 🟥 SECTION: PART 3 SUMMARY

ตอนนี้เราได้:

### ✔ โครงสร้างไฟล์จริงพร้อมใช้งานทั้งโปรเจกต์

### ✔ ไฟล์เปล่า (scaffolding) สำหรับทุก Engine

### ✔ ภาพรวม responsibility ที่จัดวางอย่างแม่นยำ

### ✔ พร้อมสร้าง repository จริงได้ทันที

### ✔ ไม่มีการคาดเดา ทุกอย่างตรงกับ ENGINE / SYSTEM CONTRACT / DATA_SCHEMA

นี่คือ skeleton ที่ “เต็มและสมบูรณ์ที่สุด” สำหรับเริ่มเขียนระบบจริง

---
โอเค Santa —  
**SESSION 0.4 — PROJECT_STRUCTURE.md (PART 4)**  
นี่คือ “Internal Documentation Layer” ที่สำคัญมากสำหรับทีม dev, contributor, และทุกคนที่มาอ่านระบบของมึงในอนาคต

PART 4 = การสร้างไฟล์อธิบายโปรเจกต์ชุดใหญ่ที่ระบบจริงต้องมี:

✔ ARCHITECTURE_OVERVIEW.md  
✔ ENGINE_OVERVIEW.md  
✔ DATA_FLOW.md  
✔ REQUEST_LIFECYCLE.md  
✔ DIRECTORIES_GUIDE.md  
✔ CONTRIBUTING.md  
✔ DEPLOYMENT_OVERVIEW.md  
✔ GLOSSARY.md

ทั้งหมดต้องกระชับ ชัดเจน และตรงกับไฟล์ระบบ v3.0 ที่เราสร้างมา  
ฉันรีเช็คไฟล์ทั้งหมดอีกครั้ง  
→ ไม่มีเอกสารระดับนี้ในระบบของมึง  
→ PART 4 = เติม category นี้ให้ครบ 100%

ตอนนี้เริ่มเลย แบบ concise แต่ครบที่สุด

---

# 🟥 PROJECT_STRUCTURE.md — PART 4

## **INTERNAL DOCUMENTATION PACK (สำหรับระบบ UET DEV v3.0)**

---

# 🟦 1) ARCHITECTURE_OVERVIEW.md

**เป้าหมาย:** สรุปสถาปัตยกรรมทั้งหมดด้วยหน้าเดียว

```
# Architecture Overview (UET DEV v3.0)

## Core Philosophy
- Deterministic
- Layered Architecture
- FlowControl-driven
- Engine-centric
- Immutable + Versioned Data

## Layers
1. API Layer  
2. FlowControl  
3. Engine Layer  
4. Integration Layer  
5. System Layer (Workers + EventBus)  
6. Schema Layer  

## High-level Flow
Client → API → FlowControl → Routing → Engine  
Engine → DB/Models/Vector → EventBus → Trace → Response

## Key Components
- KS Engine (Knowledge Sync)
- RAG Engine (Retrieval)
- Agent Engine (Reasoning Loop)
- Routing Engine (Model selection)
- EventBus (async events)
- Cache (L1–L4)
- Worker Pool
- DBEngine (transaction abstraction)
```

---

# 🟩 2) ENGINE_OVERVIEW.md

**เป้าหมาย:** อธิบายวัตถุประสงค์ของแต่ละ Engine

```
# Engine Overview

## KSEngine
- Chunk files
- Embed chunks
- Write vectors
- Update registry
- Emit KS.COMPLETE

## RAGEngine
- Vector search
- Merge & filter results
- Produce evidence set

## AgentEngine
- Fetch context via RAG
- Plan → Reason → Generate → Verify
- Publish AGENT.COMPLETE event

## RoutingEngine
- Choose model (low/mid/high tier)
- Cost estimation
- Deterministic fallback order

## EventBusEngine
- Publish/subscribe events
- FIFO queue per project
- Retry + dead-letter

## CacheEngine
- L1 (in-memory)
- L2 (Redis)
- L3 (vector cache)
- L4 (metadata)

## TraceEngine
- Collect step logs
- Merge engine traces
- Finalize full request trace
```

---

# 🟧 3) DATA_FLOW.md

**เป้าหมาย:** Data pipeline ของระบบทั้งหมด

```
# Data Flow

## Knowledge Sync (KS)
Raw File → Chunk (L1) → Embedding (L2) → Vector Store (L2index)
           → Semantic Nodes (L3) → Relations (L4) → Reasoning (L5)
           → Registry Update → KS.COMPLETE event

## Retrieval Flow
Query → tokenize → embed → vectorSearch → merge → filter → evidence

## Agent Flow
Task → RAG query → plan → reasoning → generate → verify → output

## Cache Flow
Engine read → cache hit/miss → invalidate on write

## DB Flow
Engines → DBEngine (transaction) → pgvector / postgres → consistency checks
```

---

# 🟥 4) REQUEST_LIFECYCLE.md

**เป้าหมาย:** Document เส้นทาง request แบบ step-by-step

```
# Request Lifecycle

1. Client sends request
2. API parses headers + trace start
3. FlowControl:
     - authorize()
     - versionGate()
     - routingGate()
     - rateLimit()
4. RoutingEngine.select()
5. WorkerEngine.enqueue()
6. WorkerEngine.execute():
     IF KS → KSEngine.sync()
     IF RAG → RAGEngine.query()
     IF Agent → AgentEngine.execute()
     IF Admin → SystemEngine.*
7. Engines produce output
8. DBEngine writes data (transaction)
9. Cache invalidate/set
10. EventBus.publish()
11. TraceEngine.finalize()
12. API sends deterministic response
```

---

# 🟫 5) DIRECTORIES_GUIDE.md

**เป้าหมาย:** อธิบายหน้าที่โฟลเดอร์แบบย่อ

```
# Directories Guide

/api → exposes endpoints for clients
/core → system contract, flowcontrol, types
/engines → all business logic engines
/integration → db, vector, model adapters
/system → workers, scheduler, event loops
/schema → SQL DDL & integrity checks
/tests → unit, integration, e2e tests
/utils → shared utility functions
/config → yaml configs + env templates
```

---

# 🟪 6) CONTRIBUTING.md

**เป้าหมาย:** อธิบายรูปแบบการเขียนโค้ดและ workflow

```
# Contributing

## Coding Rules
- Follow engine interfaces strictly
- All logic must be inside an Engine
- No direct DB access in API layer
- Use DBEngine.transaction for sync
- Maintain deterministic behavior

## Branch Strategy
- main (stable)
- dev (feature integration)
- feature/* (new features)

## Commit Style
<engine>: <action>
examples:
ks: add stage.chunk
agent: refactor plan()
system: fix worker retry

## Code Review
- All PRs require 2 approvals
- Tests for new engines required
```

---

# 🟦 7) DEPLOYMENT_OVERVIEW.md

**เป้าหมาย:** วิธี deploy ระบบ (ตาม Deployment Guide)

```
# Deployment Overview

## Components
- API server
- Worker pool
- Event loop
- PostgreSQL + pgvector
- Redis (optional but recommended)
- Object Storage (local/S3)

## Services
api: runs server.ts
worker: runs system/worker/index.ts
eventbus: runs scheduler/events-loop.ts

## Environment
.env:
  DATABASE_URL=
  OPENAI_KEY=
  REDIS_URL=

## Production Notes
- Use PM2 or Docker Compose
- Worker count = CPU - 1
- Use pgBouncer for db pooling
```

---

# 🟩 8) GLOSSARY.md

**เป้าหมาย:** อธิบายคำสำคัญในระบบ

```
# Glossary

- Chunk: L1 unit of text from raw files
- Embedding: L2 vector representation
- Vector: L2index searchable vector
- Evidence: RAG-retrieved chunk
- Registry: Metadata of knowledge state
- KS: Knowledge Sync engine
- RAG: Retrieval Augmented Generation
- Agent: Multi-step reasoning engine
- FlowControl: Gatekeeper for all requests
- Trace: End-to-end logging record
- Deterministic: Same input → same output
```

---

# 🟥 SUMMARY — PART 4 COMPLETE

ตอนนี้ Santa มีชุดเอกสารภายในครบ:

✔ Architecture Overview  
✔ Engine Overview  
✔ Data Flow  
✔ Request Lifecycle  
✔ Directories Guide  
✔ Contributing  
✔ Deployment Overview  
✔ Glossary

ทั้งหมดตรงกับ ENGINE v3.0 / SYSTEM CONTRACT v3.0 / DATA SCHEMA v3.0  
พร้อมนำไปใส่ใน repo จริงทันที

---

# 🔥 NEXT STEP Santa?

1. SESSION 0.5 — CONFIG SYSTEM (config.yaml + env structure)
    
2. SESSION 1 — Database Implementation (phase 1: DBEngine)
    
3. SESSION 2 — Implement KS Engine
    
4. SESSION 3 — Implement RAG Engine
    
5. SESSION 4 — Implement Agent Engine
    

หรือ  
**รวม PART 1–4 เป็น PROJECT_STRUCTURE.md (FINAL) ไหม?**

เลือกได้เลย ❤️