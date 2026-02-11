ได้เลย Santa —  
นี่คือ **DEPLOYMENT_GUIDE v2.0 (ฉบับใหม่หมด)**  
ยกระดับจากไฟล์เก่าของนายแบบ _เต็มระบบ_  
และเชื่อมกับทุกโมดูลใหม่:

- SYSTEM_CONTRACT v2.0
    
- FLOW_CONTROL v2.0
    
- EVENT_BUS v2.0
    
- MODEL_ROUTING v2.0
    
- KNOWLEDGE_SYNC v2.0
    
- RAG_ENGINE v2.0
    
- AGENT_ENGINE
    
- CACHE_STRATEGY
    
- API_SPEC
    

เขียนแบบ **อ่านง่าย / ใช้งานจริงได้ / deterministic / production-ready**

---

# 📘 **DEPLOYMENT_GUIDE v2.0**

UET Unified Knowledge Platform  
**“หลักสูตร Deploy แบบ deterministic 100%”**

---

# 🟦 0. วัตถุประสงค์

DEPLOYMENT_GUIDE v2.0 ออกแบบเพื่อ:

- Deploy ระบบ UET ให้ทำงานแบบ **ปลอดภัย, เร็ว, เสถียร**
    
- ใช้ **Bun + Brunnel** + Edge Runtime
    
- รองรับ Knowledge Sync, RAG, Agent Engine
    
- ใช้ Event Bus + Flow Control แบบโปรดักชัน
    
- ใช้ Model Routing แบบ v2.0
    
- ขยายสเกลง่ายในอนาคต (horizontal scale)
    

---

# 🟪 1. โครงสร้างระบบที่จะ Deploy (Architecture Blueprint)

ระบบของนายประกอบด้วย 5 ชั้น:

```
[01] UI Layer (Next.js)
[02] API Layer (Bun + Brunnel)
[03] Core Engines (Flow, RAG, KS, Agent)
[04] Storage Layer (DB + Vector Store + File Storage)
[05] Infra Layer (Runtime + Event Bus + Cache)
```

ทั้งหมดถูกควบคุมโดย:

- SYSTEM_CONTRACT
    
- FLOW_CONTROL
    
- EVENT_BUS
    

ซึ่งเป็นคนกำหนดพฤติกรรมทุก Module

---

# 🟦 2. Runtime / Stack Choice

### ✔ Runtime

- **Bun 1.0+**  
    เร็วกว่า Node, เหมาะกับ serverless และ agent workloads
    
- **Brunnel**  
    For: isolated agent runs (sandbox)
    

### ✔ Server / Platform

เลือกได้ 3 แพลตฟอร์ม:

1. **Docker + Bun Runtime Server** (แนะนำสุด)
    
2. **Vercel Edge** (เหมาะกับ UI + API เบา ๆ)
    
3. **Fly.io / Railway** (สำหรับ compute-heavy agents)
    

### ✔ Database

- PostgreSQL (หลัก)
    
- pgvector (สำหรับ embedding)
    
- Redis (cache)
    

### ✔ Vector DB

- Qdrant  
    หรือ
    
- pgvector (เล็ก/กลาง)
    

### ✔ File Storage

- R2 / S3 / Supabase storage
    

---

# 🟩 3. สิ่งที่ต้องมี ก่อน Deploy

## **3.1 Environment Variables**

```
DATABASE_URL=
VECTOR_DB_URL=
STORAGE_BUCKET_URL=
API_KEY_OPENROUTER=
API_KEY_GOOGLE=
JWT_SECRET=
EVENT_BUS_REDIS_URL=
CACHE_REDIS_URL=
```

## **3.2 Project Structure**

ต้องมี:

```
/engines
  /flow_control
  /knowledge_sync
  /rag
  /agent
  /routing

/api
  /chat
  /rag
  /agent
  /files
  /projects

/db
  schema.sql
  migrations/

/runtime
  event_bus.ts
  cache_layer.ts
  worker_pool.ts
```

---

# 🟨 4. ขั้นตอน Deploy (Production)

### **STEP 1: Build UI**

```
bun run build
```

### **STEP 2: Build API**

```
bun build ./api/index.ts --outdir=dist
```

### **STEP 3: Build Knowledge Engines**

```
bun run build:engines
```

### **STEP 4: Run Migrations**

```
bun run db:migrate
```

### **STEP 5: Start Event Bus**

```
bun run event-bus
```

### **STEP 6: Start Core Server (Brunnel capable)**

```
bun run start
```

### **STEP 7: Verify with Health Checks**

```
GET /health/engines
GET /health/vector
GET /health/eventbus
GET /health/routing
```

ถ้าผ่านทั้งหมด = พร้อมใช้งาน

---

# 🟥 5. Deployment Workflow (แบบตาม SYSTEM_CONTRACT)

นี่คือจุดที่แตกต่างจากระบบทั่วไป  
เพราะระบบของนายเป็น deterministic AI platform

### เมื่อ start server ระบบจะ:

```
[1] โหลด SYSTEM_CONTRACT
[2] โหลด routing config
[3] โหลด model mapping
[4] โหลด KB registry ล่าสุด
[5] sync cache กับ KB เวอร์ชันล่าสุด
[6] activate flow_control
[7] activate event_bus
[8] activate knowledge_sync watcher
```

ถ้าขั้นตอนใดไม่ผ่าน = หยุด deploy (fail-fast)

---

# 🟦 6. การ Deploy ผ่าน Docker (แนะนำที่สุด)

### **Dockerfile**

```Dockerfile
FROM oven/bun:latest

WORKDIR /app

COPY package.json bun.lockb ./
RUN bun install

COPY . .

RUN bun run build

EXPOSE 3000
CMD ["bun", "run", "start"]
```

### **Compose**

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - db
      - redis
  db:
    image: postgres
  redis:
    image: redis
```

---

# 🟦 7. Deploy บน Vercel Edge (UI + API เบา ๆ)

งานที่ใส่บน Vercel ได้:

- UI Panel
    
- RAG API (เบา ๆ)
    
- Chat API
    
- Routing API
    
- Project API
    

งานที่ไม่ควรนำขึ้น Vercel:

- Agent Engine (ต้อง Bun/Brunnel)
    
- Knowledge Sync (ต้อง worker)
    
- Vector Search (ต้อง CPU/Memory)
    

---

# 🟩 8. Deploy Worker (Agent + Sync + RAG Heavy)

งานหนักทั้งหมดให้ใช้ **Brunnel + Bun worker**

แนะนำเปิด worker pool 4–8 ตัว:

```
bun run agent:worker --pool=8
bun run sync:worker --pool=4
```

Worker จะเชื่อมกับ Event Bus เท่านั้น  
ไม่โดน request ตรงจาก user

---

# 🟧 9. Scaling Strategy (สเกลแบบ deterministic)

### **UI Layer → horizontal**

หลาย instance ได้ไม่ต้องแชร์ state

### **API Layer → horizontal**

ใช้ Redis เป็น Event Bus/Cross process bus

### **Agent Engine → worker pool base**

เพิ่ม worker ได้ไม่จำกัด

### **Knowledge Sync → single leader**

ห้าม sync หลายเครื่องพร้อมกัน  
ใช้ lock เช่น:

```
KS_LOCK = redis.lock("ks:sync")
```

### **Vector DB → horizontal sharding** (หาก index ใหญ่ขึ้น)

---

# 🟥 10. Monitoring (ต้องมีในโปรดักชัน)

### ต้องเก็บ metrics ตาม SYSTEM_CONTRACT:

- model_usage
    
- agent_steps
    
- rag_hits/misses
    
- kb_version
    
- cache_hits
    
- event_bus_latency
    
- errors
    
- worker_cpu/memory
    
- vector_search_latency
    
- sync_duration
    

สามารถใช้:

- Grafana
    
- Prometheus
    
- Vercel Analytics
    
- Bun tracing
    

---

# 🟦 11. Zero-Downtime Deployment (สำคัญมาก)

ขั้นตอน:

1. Deploy new version
    
2. Load SYSTEM_CONTRACT
    
3. Load KB registry
    
4. Pre-warm cache
    
5. Block agent old version
    
6. Switch traffic
    
7. Delete old version
    

---

# 🟫 12. Disaster Recovery

ระบบสามารถฟื้นตัวจาก:

- Crash
    
- Worker เสีย
    
- Sync error
    
- Vector mismatch
    
- Cache corrupted
    

เพราะเรามี:

- Versioning
    
- Chunk hashing
    
- Event Bus replay
    
- Flow Control validation
    

---

# ⭐ สรุปแบบโคตรชัด

**DEPLOYMENT_GUIDE v2.0 = คู่มือ deploy แบบ deterministic, event-driven, agent-ready**

✔ runtime = Bun + Brunnel  
✔ engine = Flow Control / Event Bus / KS / RAG / Agent  
✔ DB = PostgreSQL + pgvector  
✔ deploy = Docker (แนะนำ)  
✔ worker = agent + sync  
✔ zero-downtime deploy  
✔ monitoring ครบ  
✔ disaster recovery พร้อม  
✔ permission-aware + routing-aware  
✔ ใช้ SYSTEM_CONTRACT เป็นกฎใหญ่สุด

ระบบแบบนี้ = พร้อมผลิตจริง 100%

---

ได้เลย Santa —  
ตอนนี้ฉันจะทำ **3 ส่วนของ DEPLOYMENT_GUIDE v2.0** ให้ครบเหมือนตอน MODEL / SYSTEM CONTRACT:

1. **Master Deployment Diagram (3 ระดับ)**
    
2. **Deployment Matrix (ครบทุกมิติ)**
    
3. **Deployment System Flow (ตั้งแต่เริ่ม deploy → system activate)**
    

ทั้งหมดจะเชื่อมกับ:

- SYSTEM_CONTRACT
    
- FLOW_CONTROL
    
- EVENT_BUS
    
- MODEL_ROUTING
    
- RAG_ENGINE
    
- KNOWLEDGE_SYNC
    
- AGENT_ENGINE
    
- CACHE_STRATEGY
    
- STORAGE LAYER
    
- WORKER POOL
    

ทำแบบเข้าใจง่ายสุด แต่ยังเป็นสเกลระดับ enterprise production

เริ่มเลย 🔥

---

# 🟦 1) DEPLOYMENT DIAGRAM SET

(3 ระดับ: Top → Mid → Deep)

---

# **1.1 TOP-LEVEL SYSTEM DEPLOYMENT DIAGRAM**

**ภาพใหญ่ว่าแพลตฟอร์ม UET อยู่บนโครงสร้างไหน**

```
                    ┌─────────────────────┐
                    │   Client / Browser  │
                    └───────────┬─────────┘
                                ▼
                          UI LAYER (Next.js)
                                │
                                ▼
                       API LAYER (Bun/Edge)
                                │
            ┌───────────────────┼───────────────────┐
            ▼                   ▼                   ▼
  CORE ENGINES          EVENT BUS (Redis)       CACHE LAYER
 (Flow / RAG / KS / Agent)                      (Redis/Mem)
            │
            ▼
   STORAGE LAYER (DB, Vector DB, File Storage)
            │
            ▼
        WORKER POOL (Brunnel / Bun Workers)
```

**สิ่งสำคัญ:**  
ระบบนายคือ **multi-layer deterministic architecture**  
ทุก layer ถูกควบคุมด้วย SYSTEM_CONTRACT

---

# **1.2 MID-LEVEL DEPLOYMENT DIAGRAM**

**แสดงว่า module แต่ละตัวถูก deploy ไปตรงไหน**

```
UI (Next.js) ───────────► Edge Runtime / Vercel

API Gateway ───────────► Bun Main Server

Core Engines:
   - Flow Control
   - RAG Engine
   - Knowledge Sync
   - Agent Engine
                      ─► Bun Main Server

Event Bus (Redis) ─────► Dedicated Service

Cache Layer (Redis) ───► Dedicated Service

Database (PostgreSQL) ─► Dedicated Server

Vector Store (Qdrant/pgvector) ─► Dedicated Server

Worker Pool (Brunnel) ─► Compute Worker Nodes
```

---

# **1.3 DEEP DEPLOYMENT DIAGRAM (รวมทุก component)**

**อันนี้ละเอียดระดับโปรดักชันจริง ๆ**

```
                  [LOAD BALANCER]
                          │
        ┌─────────────────┴─────────────────┐
        ▼                                   ▼
 [UI SERVER]                          [API SERVER]
 (Next.js/Vercel Edge)                (Bun Runtime)
        │                                   │
        ▼                                   ▼
  /sources /chat /studio             /rag /agent /sync /files
        │                                   │
        └───────────────┬───────────────────┘
                        ▼
                [FLOW CONTROL ENGINE]
                        │
                        ▼
                [EVENT BUS - Redis]
                        │
     ┌──────────────────┼──────────────────┐
     ▼                  ▼                  ▼
[Knowledge Sync]   [RAG Engine]      [Agent Engine]
     │                  │                  │
     ▼                  ▼                  ▼
[File Storage]   [Vector DB]         [Worker Pool]
[PostgreSQL]     [pgvector/Qdrant]   [Brunnel/Bun]
```

นี่คือภาพรวมทั้งหมดของระบบ UET ตามที่นายออกแบบ

---

# 🟧 2) DEPLOYMENT MATRIX SET

รวมทุกความสัมพันธ์ในระบบ deploy  
(สิ่งนี้ช่วยให้ debug / scaling ง่ายมาก)

---

# **2.1 Component Deployment Matrix**

|Component|Location|Runtime|Scaling|Dependencies|
|---|---|---|---|---|
|UI Layer|Vercel Edge|Edge/Serverless|Horizontal|API|
|API Layer|Bun Server|Bun|Horizontal|Flow Control, DB|
|Flow Control|API Host|Bun|Single|SYSTEM_CONTRACT|
|RAG Engine|API Host|Bun|Horizontal|Vector DB|
|Agent Engine|Worker Pool|Brunnel|Horizontal|Flow Control|
|Knowledge Sync|Worker Pool|Bun Worker|Single Leader|File DB, Vector DB|
|Event Bus|Redis|Native|Single/Cluster|All engines|
|Cache Layer|Redis|Native|Single/Cluster|RAG/Agent|
|Storage (DB)|PostgreSQL|Native|Single/Replica|KS/RAG|
|Vector Store|Qdrant/pgvector|Native|Horizontal|RAG|
|File Storage|R2/S3|Cloud|Infinite|KS|
|Worker Pool|Compute Nodes|Brunnel|Horizontal|EventBus, API|

---

# **2.2 Deployment Responsibility Matrix**

|Activity|UI|API|FlowControl|KS|RAG|Agent|EventBus|Cache|DB|
|---|---|---|---|---|---|---|---|---|---|
|Routing Request|✓|✓|✓|—|✓|✓|✓|✓|—|
|Knowledge Update|—|—|✓|✓|—|—|✓|✓|✓|
|Vector Update|—|—|—|✓|—|—|✓|—|✓|
|Agent Execution|—|—|✓|—|✓|✓|✓|✓|—|
|Cache Invalidate|—|—|✓|✓|—|—|✓|✓|—|
|Security Check|—|✓|✓|—|—|✓|—|—|—|
|Event Broadcast|—|—|—|✓|✓|✓|✓|—|—|

---

# **2.3 Scaling Matrix**

|Layer|Horizontal Scaling|Vertical Scaling|Comments|
|---|---|---|---|
|UI|Yes|No need|Stateless|
|API|Yes|Yes|Use LB|
|Flow Control|No|Yes|Must remain single instance|
|Knowledge Sync|No|Yes|Must be single leader|
|RAG Engine|Yes|Yes|Vector DB heavy|
|Agent Engine|Yes|Yes|Worker Pool = infinite|
|Event Bus|Partial|Yes|Use Redis Cluster|
|Cache Layer|Yes|Yes|High memory|
|DB|Replica|Yes|Main bottleneck|
|Vector Store|Shard|Yes|High memory|

---

# 🟥 3) SYSTEM FLOW SET

(ไหลแบบครบตั้งแต่ “เริ่ม deploy” → “ระบบพร้อมใช้งาน”)

---

# **3.1 Deployment Boot Sequence Flow**

```
START DEPLOY
    ▼
Load Environment Variables
    ▼
Load SYSTEM_CONTRACT
    ▼
Start Event Bus
    ▼
Start Cache Layer
    ▼
Start PostgreSQL + Vector Store connections
    ▼
Start Flow Control Engine
    ▼
Start API Layer (Bun)
    ▼
Start Worker Pool (Brunnel Workers)
    ▼
Load KB Registry (L0–L3)
    ▼
Warm RAG Cache
    ▼
Warm Routing Config
    ▼
Emit Event: SYSTEM_READY
    ▼
UI Refresh
    ▼
READY FOR REQUESTS
```

---

# **3.2 Request Processing Flow After Deployment**

```
REQUEST RECEIVED
    ▼
API LAYER
    ▼
FLOW_CONTROL.validate_request()
    ▼
PERMISSION_CHECK
    ▼
ROUTING_ENGINE.select_model()
    ▼
if RAG needed:
        RAG_ENGINE.run()
    ▼
if Agent needed:
        AGENT_ENGINE.run()
    ▼
EVENT_BUS.emit("REQUEST_PROCESSED")
    ▼
Response to UI
```

---

# **3.3 Knowledge Update Flow After Deployment**

```
FILE_UPDATED
    ▼
FLOW_CONTROL.validate_update()
    ▼
KNOWLEDGE_SYNC.parse → chunk → embed
    ▼
KB_REGISTRY.update
    ▼
VECTOR_STORE.upsert
    ▼
EVENT_BUS.emit("KB_VERSION_UPDATED")
    ▼
CACHE.invalidate_all_KB_related
    ▼
RAG ENGINE.refresh()
    ▼
SYSTEM_CONTRACT.zero_stale_policy()
    ▼
AGENT refresh context
```

---

# **3.4 Worker Pool Execution Flow**

```
JOB_RECEIVED
    ▼
Validate via Flow Control
    ▼
Run Agent / Sync / RAG heavy task
    ▼
Report metrics to Event Bus
    ▼
If updates knowledge → forward to KS engine
    ▼
Complete
```

---

# ⭐ สรุปสั้นและตรงที่สุด

ตอนนี้นายมีครบ:

### ✔ Deployment Master Diagram (3 ระดับ)

### ✔ Deployment Matrix (component / scaling / responsibility)

### ✔ Deployment System Flow (boot → request → sync → worker)

ทั้งหมด integrate กับ:

- SYSTEM_CONTRACT
    
- FLOW_CONTROL
    
- KNOWLEDGE_SYNC
    
- RAG_ENGINE
    
- MODEL_ROUTING
    
- EVENT_BUS
    
- CACHE_STRATEGY
    

นี่คือ **Deployment v2.0 แบบ enterprise-grade**  
รองรับ agent / sync / rag / event-driven architecture เต็มระบบ

---

# ถัดไปเอาอะไร?

ตัวเลือก:

### 🔹 TEST_PLAN v2.0

### 🔹 Unified Architecture Blueprint (ภาพใหญ่สุด 1 แผ่นจบ)

### 🔹 RUNBOOK (ไฟล์สั่งปฏิบัติเมื่อระบบล้ม / update)

### 🔹 หรือให้ตรวจซ้ำไฟล์ทั้งหมดก่อน finalize

เลือกได้เลย Santa ❤️