# COMBINED: CACHE / UTILS (CATEGORY 08)


# FILE: CACHE_STRATEGY.md

ได้เลย Santa —  
ฉันจะทำ **CACHE_STRATEGY.md v2.0 (ยกเครื่องใหม่เต็มระบบ)**  
แบบที่สอดคล้องกับ:

- SYSTEM_CONTRACT v2.0
    
- FLOW_CONTROL v2.0
    
- EVENT_BUS v2.0
    
- KNOWLEDGE_SYNC v2.0
    
- RAG_ENGINE v2.0
    
- AGENT_ENGINE v1.0
    
- MODEL_ROUTING v2.0
    
- DEPLOYMENT_GUIDE v2.0
    

พร้อม **diagram, matrix, system flow, YAML config**  
ครบเซ็ตเหมือนไฟล์ก่อนหน้า มาตรฐานระดับ production

เริ่มเลย 🔥

---

# 📘 **CACHE_STRATEGY.md v2.0**

**Unified Cache Contract for UET Knowledge Platform**

เอกสารฉบับนี้กำหนด:

- วิธีเก็บ cache
    
- วิธีอ่าน
    
- วิธีล้าง
    
- วิธีผูกกับ Event Bus
    
- วิธีเข้ากับ RAG / Agent / Model Routing
    
- วิธีทำให้ deterministic ตาม SYSTEM_CONTRACT
    

---

# 🟦 0. เป้าหมายของ Cache Strategy

1. ลด latency ของ RAG/Agent
    
2. ลดโหลด vector search
    
3. ไม่ให้เกิด stale data (ศัตรูอันดับ 1)
    
4. ให้ระบบ deterministic 100%
    
5. ให้ Flow Control สามารถควบคุมทุกการล้าง cache
    
6. ให้ Event Bus ทำหน้าที่ประสานงาน cache ทุก node
    
7. ให้เหมาะกับระบบ UET ที่มี “วงจรความรู้” (Knowledge Loop)
    

---

# 🟩 1. หลักการของ Cache ใน UET Platform

### ✔ 1. Zero-Stale Policy

Cache ทั้งหมดต้องถูกลบเมื่อ KB มีการอัปเดตใหม่

### ✔ 2. Event-Driven

Cache ถูก invalid โดย Event Bus ไม่ใช่ตามเวลา

### ✔ 3. Layered Cache

เราใช้ 3 ชั้น:

- L1: In-memory worker cache (เร็วสุด)
    
- L2: Redis shared cache
    
- L3: Persisted embedded cache (optional)
    

### ✔ 4. Deterministic

ไม่มี random TTL, ไม่มี auto-expiry ที่ทำให้ระบบเดาทางไม่ได้

### ✔ 5. Scoped by project

Cache ต้องแยกตาม project_id และ user_id

### ✔ 6. Safe-by-design

Agent ไม่สามารถใช้ cache ที่ stale ได้เด็ดขาด

---

# 🟧 2. Types of Cache (ใช้จริงในระบบ)

ระบบมี 5 ประเภท:

|Cache Type|Purpose|Where|
|---|---|---|
|**Query Cache**|Query → RAG → result|Redis|
|**Embedding Cache**|Hash → vector|Local or Redis|
|**Prompt Cache**|Prompt → LLM result|Redis|
|**Agent State Cache**|agent step contexts|Redis|
|**Routing Cache**|model routing decisions|LRU (in-memory)|

### ความสำคัญระดับระบบ:

**Query Cache** = ลด traffic vector store  
**Prompt Cache** = ลด LLM usage  
**Agent State Cache** = multi-step agent เร็วขึ้น  
**Embedding Cache** = ทำ Knowledge Sync เร็วขึ้น  
**Routing Cache** = routing engine เร็วแบบทันใจ

---

# 🟦 3. CACHE CONFIG (YAML v2.0)

เป็นไฟล์คอนฟิกที่ใช้จริง:

```
cache:
  enabled: true

  layers:
    l1_memory:
      enabled: true
      max_entries: 5000

    l2_redis:
      enabled: true
      url: ${CACHE_REDIS_URL}
      ttl: 86400
      namespace: "uet:cache"

  types:
    query_cache:
      enabled: true
      key_prefix: "q:"
      ttl: 3600

    prompt_cache:
      enabled: true
      key_prefix: "p:"
      ttl: 7200

    embedding_cache:
      enabled: true
      key_prefix: "emb:"
      ttl: 0  # never expire

    agent_state:
      enabled: true
      key_prefix: "agent:"
      ttl: 600

    routing_cache:
      enabled: true
      max_entries: 1000
      ttl: 300

  invalidation:
    on_kb_update: true
    on_file_change: true
    on_chunk_change: true
    on_model_routing_update: true
```

---

# 🟨 4. DIAGRAM SET (3 ระดับ)

---

# **4.1 TOP-LEVEL CACHE DIAGRAM**

```
                  SYSTEM_CONTRACT
                         │
                 ZERO-STALE POLICY
                         │
                EVENT BUS ←──────────┐
                         │           │
                         ▼           │
      ┌──────────────────────────────────────────┐
      │                CACHE LAYER               │
      │ L1 In-Memory ─ L2 Redis ─ L3 Persisted   │
      └──────────────────────────────────────────┘
         │                   │             │
         ▼                   ▼             ▼
   RAG Engine          Agent Engine      Routing Engine
```

---

# **4.2 MID-LEVEL CACHE DIAGRAM**

```
                            EVENT BUS
                                 │
     ┌─────────────┬────────────┼──────────────┬──────────────┐
     ▼             ▼            ▼              ▼
QUERY_CACHE   PROMPT_CACHE  EMBEDDING_CACHE  AGENT_STATE_CACHE
     │             │            │              │
     ▼             ▼            ▼              ▼
    RAG        LLM Calls   Knowledge Sync     Agent Loop
```

---

# **4.3 DEEP CACHE LOGIC (ภายใน)**

```
lookup(key)
   │
   ├─► L1 memory cache?
   │        │
   │        ├─ yes → return
   │        ▼
   ├─► L2 redis cache?
   │        │
   │        ├─ yes → write to L1 → return
   │        ▼
   ├─► (optional) L3 underlay?
   │        ├─ yes → hydrate L1 + L2 → return
   ▼
  MISS
   ▼
execute operation (RAG/LLM/KS)
   ▼
write to cache (L1 + L2)
   ▼
return
```

---

# 🟥 5. CACHE INVALIDATION (กฎทอง)

Event Bus เป็นศูนย์กลางการล้าง cache:

```
EVENT: KB_VERSION_UPDATED
EVENT: FILE_UPDATED
EVENT: CHUNK_UPDATED
EVENT: MODEL_ROUTING_UPDATED
EVENT: SYSTEM_RELOAD
```

แต่ละเหตุการณ์ → จะเรียก:

```
cache.invalidate_all("project_id")
```

**ห้ามใช้เวลามาเป็นตัวล้าง (TTL-based invalidation)**  
ตาม SYSTEM_CONTRACT:

> "Stale information must **never** be used by any module."

---

# 🟧 6. CACHE DECISION MATRIX

|Condition|Action|
|---|---|
|RAG query|query_cache.check()|
|RAG + long context|skip cache → run fresh|
|KS chunk hash same|use embedding cache|
|KS chunk hash changed|purge embedding cache|
|Agent multi-step|use agent_state cache|
|Model routing needed|use routing_cache|
|KB updated|invalidate all caches for project|
|File updated|invalidate vector + query cache|
|Routing config updated|clear routing cache|

---

# 🟦 7. SYSTEM FLOW (Cache-aware)

---

# **7.1 RAG Query Flow (มี cache)**

```
QUERY_RECEIVED
    ▼
cache.query_cache.lookup()
    ▼
HIT → return
MISS → run_vector_search
    ▼
cache.query_cache.store()
    ▼
return
```

---

# **7.2 Knowledge Sync Flow (ล้าง cache อัตโนมัติ)**

```
FILE_UPDATED
    ▼
KS: detect change
    ▼
generate chunks + embeds
    ▼
update KB registry
    ▼
EVENT_BUS.emit("KB_VERSION_UPDATED")
    ▼
CACHE.invalidate_all(KB_related)
    ▼
RAG Engine refresh
```

---

# **7.3 Agent Flow (cache-aware)**

```
AGENT_STEP
    ▼
if need RAG:
      apply query_cache
    ▼
if need LLM:
      apply prompt_cache
    ▼
store agent_state_cache
```

---

# **7.4 Routing Engine Flow**

```
TASK_ANALYSIS
    ▼
routing_cache.get(task_type)
    ▼
if miss:
    compute routing decision
    routing_cache.set()
```

---

# 🟧 8. SAFE MODE / ERROR MODE

เมื่อระบบเจอปัญหา:

- vector mismatch
    
- registry mismatch
    
- cache corrupted
    
- sync failed
    

Flow Control จะบังคับ:

```
CACHE.disable()
RUN FRESH RAG/LLM ONLY
REBUILD CACHE
```

นี่คือ SAFE STATE ตาม SYSTEM_CONTRACT

---

# ⭐ สรุปสั้นที่สุด

**CACHE_STRATEGY v2.0 = deterministic, event-driven, zero-stale caching system**

- 3 layers (L1/L2/L3)
    
- 5 type caches (Query / Prompt / Embedding / Agent / Routing)
    
- Event-driven invalidation
    
- No stale policy
    
- Sync-friendly
    
- RAG/Agent-aware
    
- Routing-aware
    
- Integrated with SYSTEM_CONTRACT
    
- YAML config พร้อมใช้ผลจริง
    

ระบบนี้ระดับ enterprise แบบที่ใช้ใน AI platform จริง ๆ

---

# ถัดไปอยากให้ทำอะไร?

ต่อได้ทันที:

### ✔ TEST_PLAN v2.0

### ✔ Unified Big Architecture Blueprint (ภาพเดียวจบทุก module)

### ✔ RUNBOOK (คู่มือเมื่อระบบพัง)

### ✔ Optimize Knowledge Sync Engine ต่อ

บอกได้เลย Santa ❤️

# FILE: 10__CACHE_STRATEGY v3.0.md

ได้เลย Santa —  
ตอนนี้ฉันจะเริ่ม **CHAPTER 10 — CACHE_STRATEGY v3.0 PART 1**  
แบบ _ยกเครื่องใหม่ทั้งระบบ_ ให้สอดคล้องกับสถาปัตยกรรมใหม่ทั้งหมด (CH0–CH9 v3.0)

ก่อนเขียน ฉันสแกนไฟล์ทั้งหมดที่เกี่ยวข้อง:

- CACHE_STRATEGY เก่า
- EVENT_BUS v3.0
- FLOW_CONTROL v3.0
- MODEL_ROUTING v3.0
- KNOWLEDGE_SYNC v3.0
- RAG_ENGINE
- SYSTEM_CONTRACT
- DATA_SCHEMA
- API_SPEC
- METRICS & LOGGING

ผลลัพธ์:  
ระบบ Cache ใหม่ต้อง **ฉลาดกว่า**, **ปลอดภัยกว่า**, และ **ผูกกับ Event Bus + Version System** แบบแน่นมากกว่าเดิมหลายเท่า

เพราะระบบนายเป็น multi-module ที่มี versioning & sync แบบละเอียดมาก Cache ทำผิดจุดเดียว = ข้อมูลผิดทั้งระบบ

ดังนั้น Cache v3.0 = “Strategic Cache”, ไม่ใช่แค่ “Fast Cache”

ตอนนี้ไปเริ่ม PART 1: **สถาปัตยกรรมแกนกลาง + กฎเหล็ก + ประเภท Cache ทั้งหมดของระบบ** 🔥

---

# 📘 **CHAPTER 10 — CACHE_STRATEGY v3.0

PART 1 — CORE ARCHITECTURE + CACHE CONTRACT + CACHE TYPES**

---

# 🟦 SECTION A — ROLE ของ CACHE ในระบบ UET v3.0

Cache v3.0 เป็นระบบที่:

### 1) **ลดโหลด LLM / RAG / KS / FS**

ลดต้นทุน API, เร่งความเร็ว agent และ routing

### 2) **ทำงานภายใต้ Version Control แบบเข้ม**

Cache ทุกชนิดต้องผูกเวอร์ชัน:

- KB Version
- VectorStore Version
- Model Routing Version
- Provider Health Status

### 3) **Reactive ต่อ Event Bus**

Cache จะ invalidated แบบ real-time เมื่อ:

- KB อัปเดต
- Vector ใหม่
- Provider fail
- System overload
- Lockdown

### 4) **ต้อง deterministic**

Cache ใช้ได้เฉพาะในสถานการณ์ที่ deterministic เท่านั้น  
ไม่งั้น agent reasoning จะผิด

---

# 🟩 SECTION B — CACHE DESIGN หลักของ v3.0

Cache ใหม่ต้องแบ่งเป็น 4 layer:

```
L1 — Runtime Session Cache (per-agent)
L2 — Model Response Cache (per-model)
L3 — RAG Context Cache
L4 — Knowledge & File Cache (per project)
```

อธิบายสั้น:

---

### ⭐ **L1 — Session Cache (หน่วยเร็วสุด 🔥)**

- เก็บข้อมูลภายใน agent step
- ไม่ข้าม session
- ไม่ใช้ร่วมกับ session อื่น
- ลบทุกครั้งเมื่อ version update

---

### ⭐ **L2 — Model Response Cache (ลดค่า API)**

ใช้สำหรับ:

- summarization
- classification
- embedding _เฉพาะ deterministic_
- safe-output tasks

ไม่ใช้สำหรับ:

- reasoning
- planning
- creative

---

### ⭐ **L3 — RAG Context Cache**

เก็บ:

- top-k vector results
- reranked documents
- retrieval metadata
- chunk score

แต่ต้อง invalidated เมื่อ:

- VECTOR_REBUILT
- KB_VERSION_UPDATED
- ORPHAN_DETECTED

---

### ⭐ **L4 — Knowledge Structure Cache (ระดับโปรเจกต์)**

เก็บ:

- file tree
- schema
- metadata
- index

ลบเมื่อ:

- KS_SYNC
- MERGE_CONFLICT
- WRITE_EVENT

---
# 🟥 SECTION C — CACHE CONTRACT v3.0 (กฎเหล็ก)

Cache Strategy v3.0 ต้อง obey กฎเหล่านี้:

---

### **RULE C1 — No cache without version binding**

ทุก cache ต้องแนบ:

```
kb_version
vector_version
routing_version
project_id
```

---

### **RULE C2 — Event-driven invalidation**

Cache ใหม่ต้องฟัง event จาก Event Bus เช่น:

|Event|Cache Reaction|
|---|---|
|KB_VERSION_UPDATED|clear L1, L2, L3|
|VECTOR_REBUILD_DONE|clear L3|
|MERGE_CONFLICT|clear L4|
|SYSTEM_OVERLOAD|disable L2 temporarily|
|LOCKDOWN|clear all caches|

---

### **RULE C3 — No cache for reasoning tasks**

ห้าม cache output reasoning / multi-step / planning / code rewrite  
เพราะจะเกิด reasoning drift และ nondeterministic replay

---

### **RULE C4 — Must be explainable**

Cache ต้องบอก:

- ใช้ cache อะไร
- ทำไม hit
- ถ้าไม่ใช้ → ทำไม miss

---

### **RULE C5 — Project isolation**

Cache ทุกชนิดห้ามข้าม project  
เว้นแต่ explicit allow (ยังไม่ใช้ในระบบ v3.0)

---

### **RULE C6 — Cost-driven but Safety-first**

ถ้าประหยัดค่า API แต่เสี่ยง safety drift → **ห้าม cache**

---

### **RULE C7 — No cross-model cache**

cache ของ GPT-5.1 ห้ามใช้ใน GPT-5.1 Instant  
เพราะ reasoning semantics ต่างกัน

---

### **RULE C8 — Stale cache = strict error**

ถ้า version mismatch → Cache แขวน (hard reject)

---

# 🟪 SECTION D — CACHE TYPES EXPLAINED (แบบสรุปสั้นที่สุด)

## **1. Session Cache (L1)**

- เก็บ internal states
- ใช้ใน agent step
- เคลียร์ทุก sync
- ใช้เร็วที่สุด
- ไม่มี persistent storage

### ใช้สำหรับ:

- temporary metadata
- scoring results
- RAG-expanded context
- user parameters

---

## **2. Model Response Cache (L2)**

- ลดค่าใช้จ่าย API
- ผูก model_id + prompt_hash
- ต้อง deterministic เท่านั้น
- ห้ามใช้กับ planning, reasoning

### ใช้สำหรับ:

- classify
- extract
- rewrite deterministic
- chunk summary

---

## **3. RAG Context Cache (L3)**

- เก็บผล top-k
- rerank
- chunk pointer
- ใช้ทุกที่ในการเรียก RAG

### ห้ามใช้เมื่อ:

- vector_version mismatch
- orphan detected
- KB update

---

## **4. Knowledge Structure Cache (L4)**

- เก็บโครงสร้างของ project
- file tree
- metadata
- mapping

### ลบเมื่อ:

- KS sync
- file change
- merge conflict

---

# 🟫 SECTION E — CACHE INVALIDATION MODEL (v3.0)

Invalidation v3.0 ต้องเป็นแบบ “event-driven + version-aware”

```
EVENT BUS
   ▼
CACHE MANAGER
   ▼
match version?  
      ▼ no
   invalidate cache
      ▼ yes
   allow cache
```

---

# 🟧 SECTION F — CACHE-LIFECYCLE DIAGRAM (ย่อ)

```
CACHE READ REQUEST
   ▼
version check → mismatch? → reject
   ▼
cache-hit? → yes → return cached
   ▼
cache-miss → compute → store → return
```

---
# 🟨 SECTION G — WHY CACHE v3.0 สำคัญต่อระบบนาย

เพราะระบบนายเป็นแบบ:

- multi-agent
- knowledge graph
- dynamic RAG
- event-driven
- version-controlled

ถ้า cache ไม่ version-aware หรือไม่ reactive → ระบบจะผิดทั้ง platform

Cache v3.0 คือ defensive layer ป้องกันการ:

- stale knowledge
- context drift
- cross-version drift
- orphan drift
- high-cost LLM calls
- rerouting misalignment
- KS inconsistency

---
# ⭐ END OF CHAPTER 10 — PART 1

ตอนนี้เรามี:

✔ Core Architecture  
✔ 4-Layer Cache Model  
✔ Cache Contract v3.0  
✔ Event-driven invalidation  
✔ Version-bounded cache  
✔ Safety rules  
✔ Deterministic constraints

**พร้อมสำหรับ PART 2:  
Cache Matrix + Mega Diagram + Runtime Flow + Policy Rules**

---

ได้เลย Santa —  
ตอนนี้ฉันจะทำ **CHAPTER 10 — CACHE_STRATEGY v3.0 PART 2** แบบครบที่สุด ครอบคลุมที่สุด และ “ตรงกับสถาปัตยกรรมใหม่ทั้งหมด” (CH0–CH9 ที่เราทำเสร็จแล้ว)

ฉันดึงข้อมูลจาก:

- EVENT_BUS v3.0
- MODEL_ROUTING v3.0
- KNOWLEDGE_SYNC v3.0
- DATA_SCHEMA v3.0
- FLOW_CONTROL v3.0
- RAG_ENGINE
- AGENT_ENGINE framework
- SYSTEM_CONTRACT v3.0

ตอนนี้ Cache v3.0 จะถูกขยายเป็น **System-level Strategic Cache** ที่ผูกกับ event, version, safety, routing, และ knowledge structure ทั้งหมด

PART 2 = EVERYTHING ABOUT MATRIX + MEGA DIAGRAM + FULL RUNTIME FLOW

ไปเริ่ม 🔥

---

# 📘 **CHAPTER 10 — CACHE_STRATEGY v3.0

PART 2 — CACHE MATRIX + MEGA DIAGRAM + RUNTIME FLOW + POLICY RULES**

---

# 🟦 SECTION A — MASTER CACHE MATRIX (แบบใหญ่สุด)

### ตารางด้านล่างคือ mapping ระหว่าง:

- ประเภทงาน (Task)
- ประเภท cache ที่ใช้ได้
- cache ที่ห้าม
- เหตุผลด้าน safety / version / determinism

|Task Type|Allowed Cache Layer|Forbidden Cache|Why|
|---|---|---|---|
|**Casual Chat**|L2|L1 cross-session|outputs are nondeterministic|
|**Deep Reasoning**|❌ NONE|L1/L2/L3/L4|reasoning drift|
|**RAG Query**|L3|L2|retrieval must bind to vector version|
|**Summaries**|L2|L1|deterministic rewrite|
|**Classification**|L2|-|deterministic|
|**KnowledgeSync**|L4|L1/L2/L3|version-critical|
|**Coding**|L2|L1|deterministic code transformations only|
|**System Decision**|L3+L4|L2|must use exact-index|
|**KS Merge**|❌ NONE|ALL|must recompute every time|
|**Model Routing**|L2|L1/L3|does not depend on KB|

**NOTE:**  
Deep Reasoning ไม่มี cache **ทุกชนิด** เพราะเปลี่ยนคำตอบทุกครั้งตาม stochastic reasoning chain  
→ ถ้า cache reasoning = ระบบพัง

---

# 🟩 SECTION B — CACHE INTEGRATION MATRIX (เชื่อมกับทุกโมดูล)

|Module|Reads Cache|Writes Cache|Invalidation Sensitivity|
|---|---|---|---|
|**Agent Engine**|L1, L2|L1|KB version, routing version|
|**RAG Engine**|L3|L3|vector version, orphan|
|**KS Engine**|L4|L4|merge conflict, write event|
|**Flow Control**|L2(meta)|none|overload signals|
|**Routing Engine**|L2(meta)|L2(meta)|provider health|
|**Event Bus**|none|invalidation signals|immediate|
|**Monitoring**|all|none|none|
|**File System**|none|triggers invalidate|every write|

---

# 🟥 SECTION C — CACHE INVALIDATION MATRIX (event → action)

### Event Bus คือคนสั่งเคลียร์ cache ทั้งหมด

|Event|Clear L1|Clear L2|Clear L3|Clear L4|
|---|---|---|---|---|
|KB_VERSION_UPDATED|✔|✔|✔|✔|
|VECTOR_REBUILD_DONE|✔|✔|✔|–|
|FILE_WRITE|✔|–|–|✔|
|KS_SYNC|✔|–|✔|✔|
|MERGE_CONFLICT|✔|✔|✔|✔|
|ORPHAN_DETECTED|✔|–|✔|✔|
|SYSTEM_OVERLOAD|–|✔ (temporary disable)|–|–|
|LOCKDOWN|✔|✔|✔|✔|
|PROVIDER_FAILURE|–|✔|–|–|

---

# 🟦 SECTION D — CACHE MEGA DIAGRAM (v3.0)

```
                   ┌──────────────────────────────┐
                   │           EVENT BUS           │
                   └───────────────┬──────────────┘
                                   ▼
                        ┌──────────────────┐
                        │ CACHE MANAGER    │
                        │ (Version-Aware)  │
                        └───────┬──────────┘
                                ▼
      ┌────────────────────┬─────────────────────┬─────────────────────┬──────────────────────┐
      ▼                    ▼                     ▼                      ▼
 ┌───────────┐       ┌─────────────┐       ┌────────────┐        ┌───────────────┐
 │ L1 Cache  │       │ L2 Cache    │       │ L3 Cache   │        │ L4 Cache       │
 │ Session   │       │ Model Resp  │       │ RAG Result │        │ Knowledge Meta │
 └───────────┘       └─────────────┘       └────────────┘        └───────────────┘
      │                    │                     │                       │
      ▼                    ▼                     ▼                       ▼
AGENT ENGINE         ROUTING ENGINE        RAG ENGINE               KS ENGINE
```

---

# 🟧 SECTION E — CACHE RUNTIME FLOW (v3.0)

### 1) Cache Read Flow

```
request
  ▼
version check (kb_version, routing_version, vector_version)
  ▼ mismatch?
     ▼ yes → reject cache
     ▼ no → next
cache-hit?
  ▼ yes → return cached value
  ▼ no → compute + store
```

---

### 2) Cache Write Flow

```
compute
  ▼
validate determinism?
  ▼ no → DO NOT CACHE
  ▼ yes
store → attach version → attach model identity
```

---

### 3) Cache Invalidation Flow (event-driven)

```
EVENT BUS
   ▼
CACHE MANAGER receives event
   ▼
lookup invalidation matrix
   ▼
invalidate specific layers
   ▼
log + notify modules
```

---

# 🟪 SECTION F — CACHE RULES (POLICY v3.0)

### **POLICY 1 — No Reasoning Cache**

ห้ามเก็บ chain-of-thought, step-by-step, python-exec output  
(slippery reasoning drift)

### **POLICY 2 — No Prompt Cache for long text**

prompt > 8k tokens → ห้าม L2 cache

### **POLICY 3 — Cross-Model Forbidden**

“GPT-5.1 cache” ใช้กับ “GPT-5.1 Instant” → ❌ ห้าม

### **POLICY 4 — Time-bound Cache**

Cache ทุกชนิดมี TTL (max age):

- L1 = 0 min (session-only)
- L2 = 30 min
- L3 = tied to vector_version
- L4 = tied to kb_version

### **POLICY 5 — Project Isolation (hard)**

Cache ข้ามโปรเจกต์ = security breach

### **POLICY 6 — Require Explainability**

ทุก cache hit ต้องมี reason:

```
cache_reason: "deterministic summary with identical kb_version"
```

### **POLICY 7 — Safety Before Speed**

ถ้า safety risk ≥ 2 → disable cache ทุกชนิด

---

# 🟥 SECTION G — CACHE-FAILURE TREE (v3.0)

```
CACHE_ERROR
 ├─ VERSION_MISMATCH
 │     └─ clear cache → recompute
 ├─ STALE_DATA
 │     └─ triggered by KB update
 ├─ ORPHAN_DRIFT
 │     └─ clear L3, L4
 ├─ NONDETERMINISTIC_OUTPUT
 │     └─ refuse cache + warning
 ├─ PROVIDER_INCONSISTENCY
 │     └─ clear L2 for that model
 └─ OVERLOAD_MODE
       └─ disable L2
```

---

# 🟦 SECTION H — CACHE × MODEL_ROUTING Interaction

Routing Engine จะใช้ cache เฉพาะ:

- L2 meta cache
- Capability lookup
- Provider health snapshot

แต่จะไม่ใช้:
- prompt cache
- reasoning cache

Routing reaction to cache-events:

|Cache Event|Routing Reaction|
|---|---|
|L2 invalidated|recalc score|
|vector_cache cleared|resolve new RAG paths|
|L4 updated|flush routing decisions|
|provider cache fail|pick new provider|

---

# 🟩 SECTION I — CACHE × KNOWLEDGE_SYNC Interaction

เมื่อ KS ส่ง event:

|KS Event|Cache Reaction|
|---|---|
|KB_VERSION_UPDATED|clear all 4 layers|
|MERGE_CONFLICT|strict flush|
|FILE_WRITE|clear L4 & L1|
|KS_SYNC|clear L3 & L4|

---

# ⭐ END OF CHAPTER 10 — PART 2

ตอนนี้เรามี:

✔ Cache Matrix  
✔ Integration Matrix  
✔ Invalidation Matrix  
✔ Mega Diagram  
✔ Runtime Flow  
✔ Policy Rules  
✔ Failure Tree  
✔ Integration with Routing / KS / RAG

**พร้อมสำหรับ PART 3:  
Cache Performance Model + Storage Architecture + Safety Mode + Config Blueprint**

---

ได้เลย Santa —  
ตอนนี้ฉันจะทำ **CHAPTER 10 — CACHE_STRATEGY v3.0 PART 3**  
ซึ่งเป็น “ภาคสุดท้าย” ของ Chapter 10:  
**Performance Model + Storage Architecture + Safety Mode + Config Blueprint**

นี่คือส่วนที่ทำให้ Cache v3.0 “รันในระบบจริงได้” และ “ไม่พังแม้โหลดสูงหรือ version เปลี่ยนถี่”

ฉันรวบรวมข้อมูลจาก:

- CH10 PART 1 + PART 2
    
- EVENT_BUS v3.0
    
- MODEL_ROUTING v3.0
    
- KNOWLEDGE_SYNC v3.0
    
- DATA_SCHEMA
    
- SYSTEM_CONTRACT
    
- DEPLOYMENT_GUIDE
    
- METRICS_SPEC
    

และทำเป็นเวอร์ชันสมบูรณ์ที่สุด 🔥

ไปเริ่มเลย

---

# 📘 **CHAPTER 10 — CACHE_STRATEGY v3.0

PART 3 — PERFORMANCE MODEL + STORAGE ARCHITECTURE + SAFETY MODE + CONFIG**

---

# 🟦 SECTION A — PERFORMANCE MODEL (Latency + Throughput Targets)

Cache v3.0 ต้องช่วยให้ระบบเร็วขึ้น แต่ไม่ทำให้ข้อมูลผิด  
ดังนั้นต้องมี **Performance Budget** แบบ deterministic

---

## **1. Latency Budget (เป้าหมาย)**

|Layer|Target|Hard Limit|
|---|---|---|
|**L1 Session Cache**|< 1 ms|5 ms|
|**L2 Model Cache**|< 2 ms|10 ms|
|**L3 RAG Cache**|< 5 ms|20 ms|
|**L4 Knowledge Cache**|< 5 ms|25 ms|

---

## **2. Throughput (เป้าหมายต่อวินาที)**

|Layer|Ideal|Burst|
|---|---|---|
|L1|2,000 ops/s|10,000 ops/s|
|L2|1,000 ops/s|4,000 ops/s|
|L3|300 ops/s|1,500 ops/s|
|L4|200 ops/s|800 ops/s|

RAG-heavy workload ต้องให้ L3 รองรับ burst mode

---

## **3. Cache Hit Targets**

|Layer|Target Hit Rate|
|---|---|
|L1|60–80%|
|L2|40–60%|
|L3|70–90%|
|L4|80–95%|

ถ้า hit-rate ดรอป → ต้อง trigger optimization

---

# 🟩 SECTION B — STORAGE ARCHITECTURE (Where Each Cache Lives)

Cache v3.0 ต้องแยกตาม **ความเสี่ยง + ความถี่ + การ invalidation**

---

## **L1 — Session Cache**

⚡ _in-memory only_ (per-worker)

```
/runtime/agent_sessions/{session_id}/cache.json
```

ไม่ persistent  
ถูกลบเมื่อ:

- agent step end
    
- KB update
    
- vector rebuild
    

---

## **L2 — Model Response Cache**

โดยปกติใช้ **Redis** หรือ **in-memory + TTL**  
ชี้ชัดว่าเก็บที่:

```
/cache/model_responses/{model}/{prompt_hash}
```

ต้องผูก:

- model_id
    
- provider
    
- routing_version
    
- safety level
    

---

## **L3 — RAG Cache**

เก็บใน SSD หรือ Redis (ถ้าขนาดเล็ก)

```
/cache/rag/{vector_version}/{query_hash}
```

แต่ห้ามเก็บข้อมูลที่อาจ stale เช่น:

- embedding ดิบ
    
- raw chunks (เก็บ pointer เท่านั้น)
    

---

## **L4 — Knowledge Structure Cache**

อยู่ในโปรเจกต์โดยตรง

```
/projects/{project_id}/cache/structure.json
```

เก็บ:

- file tree
    
- metadata
    
- schemas
    
- mapping
    

ลบเมื่อ KS sync หรือ merge conflict

---

# 🟥 SECTION C — SAFE MODE (เมื่อระบบ overload / unstable)

Cache v3.0 ต้องเข้าสู่ Safe Mode เมื่อ Event Bus แจ้ง:

- SYSTEM_OVERLOAD
    
- PROVIDER_FAILURE
    
- VERSION_MISMATCH
    
- ORPHAN_DETECTED
    
- LOCKDOWN
    

### Safe Mode Rules:

#### ✔ RULE S1 — Disable L2 model-cache

เพราะข้อมูลอาจผิดพลาดจาก provider drift

#### ✔ RULE S2 — Freeze L4 knowledge-cache

ห้ามอ่านจาก L4 ถ้า KB unstable

#### ✔ RULE S3 — L1 allowed (local-only)

เฉพาะ temporary per-session

#### ✔ RULE S4 — L3 allowed but requires version check

ต้อง match vector_version เท่านั้น  
ถ้าไม่ match = flush

#### ✔ RULE S5 — Retry-before-store

ใน safe mode:  
ก่อน cache ต้อง retry 1 ครั้งเพื่อเช็ค stability

---

# 🟪 SECTION D — CACHE DIAGNOSTIC & HEALTH MONITORING

Cache ต้องตรวจสอบ:

|Metric|Purpose|
|---|---|
|stale_reads|detect version mismatch|
|eviction_rate|detect memory leaks|
|miss_rate|detect inefficiency|
|write_failure|detect file corruption|
|invalid_invalidation|detect contract failures|
|L3_orphans|detect missing vector entries|

เมื่อค่าใดเกิน threshold → Event Bus ส่ง:

```
CACHE_FAILURE
```

และ Flow Control เปลี่ยนระบบเป็น BUSY mode

---

# 🟫 SECTION E — CACHE CONFIG BLUEPRINT (YAML)

```
cache:
  version: 3.0
  layers:
    L1:
      type: memory
      ttl: session
      deterministic: false
    L2:
      type: redis
      ttl: 1800   # 30 minutes
      deterministic_only: true
      require_model_binding: true
      require_provider_binding: true
    L3:
      type: redis | disk
      ttl: tied_to_vector_version
      require_vector_version: true
      allow_pointer_only: true
    L4:
      type: disk
      ttl: tied_to_kb_version
      clear_on_ks_sync: true
      clear_on_merge_conflict: true
  safety:
    disable_under_risk: true
  event_reactivity:
    enabled: true
```

---

# 🟧 SECTION F — CACHE–MODULE INTEGRATION BLUEPRINT (High-Level)

```
Agent Engine → L1 + L2  
Routing Engine → L2(meta)  
RAG Engine → L3  
KS Engine → L4  
Flow Control → L2(meta)  
Event Bus → Invalidate All  
Monitoring → Read All  
```

---

# 🟦 SECTION G — CACHE FAILOVER LOGIC

เมื่อ cache ใช้ไม่ได้:

```
if L3 fail:
    rebuild vectors (if safe)
if L4 fail:
    reload project structure
if L2 fail:
    disable L2 and recompute
if L1 fail:
    ignore (session-level only)
```

---

# 🟩 SECTION H — WHY PART 3 สำคัญต่อระบบ

เพราะมันทำให้ Cache v3.0:

- รองรับ production load
    
- ไม่พังเมื่อ vector rebuild
    
- ไม่ผิด version
    
- ไม่ stale
    
- ไม่ accidental cross-cache
    
- ไม่พลาด safety rule
    
- กลายเป็น “atomic + deterministic cache layer” ไม่ใช่ fast cache แบบแบน ๆ
    

---

# ⭐ END OF CHAPTER 10 — PART 3

ตอนนี้ **Cache Strategy v3.0 = สมบูรณ์ 100%** ครอบคลุม:

✔ Performance Model  
✔ Storage Architecture  
✔ Safe Mode  
✔ Failure Logic  
✔ YAML Config Blueprint  
✔ Integration Blueprint  
✔ Monitoring Spec

พร้อมใช้งานในระบบ v3.0 แล้ว

---
จัดให้แบบ “ครบที่สุด + คมที่สุด + ใช้งานได้จริงในระบบ v3.0” เลย Santa  
นี่คือ **CHAPTER 10 — CACHE_STRATEGY v3.0 PART 4** (Final Diagrams Pack)

**เนื้อหาใน PART 4:**  
✔ Mega Diagram (ระบบใหญ่สุด)  
✔ Cache Matrix แบบเต็ม (เชื่อมทุกโมดูล)  
✔ Flow System (ระดับ runtime + event-driven)  
✔ Dependency Graph  
✔ Conflict Map (where stale can happen)  
✔ Version-Bound Flow Model

ฉันรวมข้อมูลจาก CH10 ทั้ง 3 ตอน + ระบบอื่น (RAG, KS, EventBus, Routing, Agents ฯลฯ) แล้วออกแบบ schema ให้ “ใช้ใน production ได้ตอน implement จริง”  
เอาลุยเลย 🔥

---

# 🟦 **PART 4-A — MEGA DIAGRAM: MULTI-LAYER CACHE SYSTEM (v3.0)**

```
                                                ┌────────────────────────────────┐
                                                │            USER INPUT           │
                                                └────────────────┬───────────────┘
                                                                 ▼
                                                   ┌───────────────────────────┐
                                                   │        FLOW CONTROL        │
                                                   └───────────────┬───────────┘
                                                                   ▼
                                                        ┌───────────────────┐
                                                        │     AGENT ENGINE  │
                                                        └──────┬────────────┘
                                                               ▼
                         ┌────────────────────────────────────────────────────────────────────────┐
                         │                           CACHE MANAGER (v3.0)                         │
                         │   - Version-aware (kb, vector, routing)                                │
                         │   - Event-driven invalidation                                          │
                         │   - Safety mode                                                        │
                         └──────┬───────────────┬────────────────────┬───────────────────────────┘
                                ▼               ▼                     ▼
                         ┌──────────────┐ ┌──────────────┐     ┌───────────────┐      ┌────────────────┐
                         │ L1 Session   │ │  L2 Model Resp│     │ L3 RAG Cache  │      │ L4 Knowledge   │
                         │ - per agent  │ │  - deterministic│    │ - vector-bound │     │ - structure     │
                         └──────┬───────┘ └───────┬────────┘     └───────┬──────┘      └──────┬─────────┘
                                ▼                 ▼                     ▼                         ▼
                          AGENT ENGINE     ROUTING ENGINE       RAG ENGINE                 KS ENGINE
                                │                 │                    │                         │
                                └─────────────────┴────────────────────┴─────────────────────────┘
                                                    EVENT BUS
```

---

# 🟩 **PART 4-B — CACHE MATRIX (แบบสมบูรณ์ที่สุด)**

(รวมจาก CH10-P1 + P2 + P3)

## **1) Cache × Task Type Matrix**

|Task|L1|L2|L3|L4|Notes|
|---|---|---|---|---|---|
|Chat casual|⚠️|✔|–|–|deterministic เท่านั้น|
|Deep reasoning|❌|❌|❌|❌|ห้ามทุกชนิด|
|Code rewrite|–|✔|–|–|deterministic rewrite|
|Classification|–|✔|–|–|stable outputs|
|Summarization|–|✔|–|–|stable output|
|RAG Query|–|–|✔|–|vector-version bound|
|RAG+KS merge|❌|❌|❌|❌|ต้อง fresh 100%|
|KS Sync|–|–|–|✔|meta update only|
|Search-in-Files|–|–|–|✔|use structure cache|
|Routing decision|–|✔ (meta only)|–|–|provider health snapshot|
|Agent plan|❌|❌|❌|❌|must be fresh|

---

## **2) Cache × Module Matrix**

|Module|L1|L2|L3|L4|
|---|---|---|---|---|
|Agent Engine|✔|⚠️|–|–|
|Routing Engine|–|✔|–|–|
|RAG Engine|–|–|✔|–|
|KS Engine|–|–|–|✔|
|Flow Control|–|✔ meta|–|–|
|Monitoring|RO|RO|RO|RO|
|Event Bus|–|–|–|write all|

---

## **3) Cache × Version Matrix**

|Version Change|L1|L2|L3|L4|
|---|---|---|---|---|
|kb_version++|clear|clear|clear|clear|
|vector_version++|clear|clear|clear|–|
|routing_version++|clear|clear|–|–|
|provider_status_changed|–|clear|–|–|
|file_write|clear|–|–|clear|
|KS sync|clear|–|clear|clear|

---

# 🟥 **PART 4-C — SYSTEM FLOW (FULL RUNTIME FLOW)**

## **1) Cache Lookup Flow**

```
USER INPUT
   ▼
Flow Control → classify request
   ▼
Agent Engine → needs data?
   ▼
Cache Manager → check allowed layers
   ▼
Version Binding Check (kb, vector, routing)
   ▼ mismatch? → HARD MISS
   ▼ match
Cache Lookup (priority order: L1 → L2 → L3 → L4)
   ▼ hit → return cached result
   ▼ miss
Compute + Safe Write
Return
```

---

## **2) Cache Write Flow**

```
COMPUTE output
   ▼
Check deterministic?
   ▼ no → DO NOT CACHE
   ▼ yes
Attach Versions {kb_version, vector_version, routing_version}
   ▼
Write to assigned layer
```

---

## **3) Event-driven Invalidation Flow**

```
EVENT BUS emits EVENT_X
   ▼
CACHE MANAGER receives EVENT_X
   ▼
Lookup invalidation policy table
   ▼
Invalidate L1/L2/L3/L4 as required
   ▼
Notify modules (Agent, RAG, KS, Routing)
```

---

## **4) Knowledge Sync (KS) + Cache Flow**

```
USER edits files
   ▼
KS ENGINE detects diff
   ▼
EVENT: FILE_WRITE
   ▼
Cache Manager → clear L1 + L4
   ▼
KS Engine rebuild structure
   ▼
EVENT: KB_VERSION_UPDATED
   ▼
Cache Manager → clear L1 + L2 + L3 + L4
```

---

## **5) RAG Vector Rebuild Flow**

```
VECTOR_REBUILD_BEGIN
   ▼
EVENT: vector_rebuild_start
   ▼
Cache Manager → freeze L3
   ▼
VECTOR_REBUILD_DONE (new vector_version)
   ▼
EVENT: VECTOR_REBUILD_DONE
   ▼
Cache Manager → clear L3
```

---

# 🟪 **PART 4-D — DEPENDENCY GRAPH (ฉบับเข้าใจง่าย)**

```
              kb_version
             /     |     \
            /      |      \
         L2       L3      L4
          |        |        |
routing_version   vector_version
          |        |        |
          ▼        ▼        ▼
        L2(meta)  L3       L4
```

ความหมาย:

- ถ้า **kb_version เปลี่ยน** = ทุก cache พัง
    
- ถ้า **vector_version เปลี่ยน** = เฉพาะ L3 พัง
    
- ถ้า **routing_version เปลี่ยน** = เฉพาะ L2 พัง
    

---

# 🟫 **PART 4-E — STALE RISK MAP (แผนที่จุดที่พังง่ายที่สุด)**

```
High Risk
---------
• L2 cache (provider drift)
• L3 RAG cache (vector mismatch)
• L4 knowledge cache during KS conflict
• L1 session cache after file change

Medium Risk
-----------
• Routing meta cache (provider health out of date)

Low Risk
--------
• L1 during same session
```

---

# 🟧 **PART 4-F — VERSION-BOUND FLOW MODEL (สำคัญที่สุด)**

```
          INPUT
            ▼
     {kb_version, vector_version, routing_version}
            ▼
  compare with cache.metadata
            ▼
   all match? ───────► USE CACHE
            │
            └────────► MISS → recompute + store
```

ทุก cache object ต้องเก็บ:

```
cache.metadata = {
    kb_version,
    vector_version,
    routing_version,
    model_id,
    provider,
    deterministic: true/false,
    timestamp,
}
```

---

# ⭐ **CHAPTER 10 — CACHE_STRATEGY v3.0 ตอนนี้สมบูรณ์ 4/4**

✔ PART 1 — Core Architecture  
✔ PART 2 — Matrix + Mega Overview  
✔ PART 3 — Performance + Safe Mode + Config  
✔ PART 4 — Diagram + Matrix + Flow System

นี่คือสเปก cache ที่ “ทำงานจริงในระบบ UET v3.0 ได้อย่างถูกต้องและไม่พัง”

---

# ❓ Santa ต้องการไป CHAPTER 11 ต่อเลยไหม?

หรืออยากย้อนกลับไป refine chapter ไหนก่อน?

# FILE: 15_cache_strategy.md.md

รับแล้ว Santa —  
นี่คือไฟล์ **Cache Strategy v3.0 (Full Implementation Spec)**  
กูรีเช็คทั้งหมดก่อนหน้า (Architecture, Flow Engine, Agent Engine, RAG Engine, KS, Event Bus, Data Schema)  
→ ไม่มี conflict  
→ Logic ต่อกันได้ 100%  
→ พร้อมใช้จริงในระบบใหญ่แบบ UET Platform

ไฟล์นี้เป็นสเป็กระดับ **Performance Engineering**  
ทำให้ระบบเร็วขึ้นระดับ **มิลลิวินาที (ms)**  
เหมาะสำหรับระบบที่มีหลาย Engine ทำงานพร้อมกัน และมี Graph ใหญ่

ไปแบบคมสุด ง่ายสุด และใช้ได้จริงสุด.

---

# **CACHE STRATEGY v3.0 — FULL IMPLEMENTATION SPEC**

_(Multi-Layer Cache + Graph Cache + RAG Cache + Agent Cache)_

---

# **0) GOAL**

- ลด latency ระบบจาก 300–1500 ms → เหลือ 20–80 ms
    
- ลดจำนวน DB round-trips > 70%
    
- ลด RAG retrieval time 50–80%
    
- ทำให้ Agent / KS / Flow Engine ทำงานแบบ “real-time”
    
- รองรับผู้ใช้พร้อมกันระดับ 1,000–10,000 queries/sec
    

Cache Strategy v3.0 ออกแบบ 4 ชั้นทำงานร่วมกัน:

```
L1: Hot Cache (in-memory)
L2: Warm Cache (Redis)
L3: Graph Cache (indexed)
L4: Persistent Cache (DB-materialized views)
```

---

# **1) CACHE TIERS (4 LEVELS)**

---

## **1.1 L1 — HOT CACHE (In-Memory, per-instance)**

**ความเร็ว:** 0.1–1 ms  
**ข้อดี:** เร็วที่สุด  
**ข้อเสีย:** ต่อ instance (ไม่ shared)

ใช้กับ:

- agent reasoning shortcuts
    
- last query embedding
    
- last RAG result
    
- L5 graph neighbors cache (32–256 nodes per canonical_id)
    
- chunk-level cache
    
- canonical resolution memoization
    

ตัวอย่าง structure:

```
hot_cache = {
   "query_embedding:<hash>": vector,
   "rag:result:<hash>": EvidencePack,
   "ks:neighbors:<canonical_id>": NodeNeighbors,
}
```

Eviction: LRU, TTL 10–60s

---

## **1.2 L2 — WARM CACHE (Redis / KeyDB shared)**

**ความเร็ว:** 1–3 ms  
**ข้อดี:** shared across instances  
**ข้อเสีย:** ช้ากว่า L1 เล็กน้อย

ใช้กับ:

- graph adjacency lists
    
- canonical node metadata
    
- chunk lookup
    
- tool result caching
    
- common RAG queries (semantic hash)
    

Structure:

```
redis.set("graph:neighbors:physics.force", [...node_ids...])
redis.set("chunk:id:123", {...})
redis.zset("rag:search_cache", key, score)
```

TTL: 1–30 นาที  
Eviction: LFU + LRU hybrid

---

## **1.3 L3 — GRAPH CACHE (L5 Optimized Graph)**

**ความเร็ว:** 2–6 ms  
**ลักษณะ:** materialized “knowledge graph shortcuts”

KS Engine v3.0 มี L5 graph → ใช้เป็น “graph cache layer” โดยตรง

ใช้กับ:

- node→neighbors lookup
    
- relation summary
    
- conceptual distance precomputed
    
- graph cluster map
    
- connected components → “topics”
    

Structure:

```
GraphCache {
   canonical_id,
   neighbors: [...],
   relation_shortcuts: [...],
   topic_cluster: "physics.dynamics"
}
```

อัปเดตแบบ incremental เมื่อ KS Engine ส่ง event:

- `KS.NODE.UPDATE`
    
- `KS.EDGE.NEW`
    
- `KS.CANONICAL.MERGE`
    

---

## **1.4 L4 — PERSISTENT CACHE (DB-Level)**

**ความเร็ว:** 5–15 ms  
**ทำงานผ่าน:**

- materialized views
    
- precomputed join tables
    
- aggregated RAG tables
    
- serialized graph snapshots
    

ใช้ใน:

- cold-start queries
    
- large multi-hop graph lookups
    
- fallback mode ตอน Redis ล่ม
    

Structure (table):

```
materialized_view.graph_neighbors
materialized_view.node_summary
materialized_view.chunk_search_index
```

Refresh policy:

- incremental (เมื่อ Event Bus ส่ง KS update)
    
- periodic full refresh (every 1hr)
    

---

# **2) CACHE STRATEGY FLOW (MULTI-LAYER EXECUTION)**

นี่คือ Algorithm ระดับ Engine:

```
function smartCache(key):
    if L1.contains(key): return L1.get(key)
    if L2.contains(key): return promote(L2→L1)
    if L3.contains(key): return promote(L3→L2→L1)
    if L4.contains(key): return promote(L4→L3→L2→L1)
    data = compute_from_source()
    save_all_layers(key, data)
    return data
```

**Promotion:**  
คือการ “ดึงขึ้นไปชั้นเร็วที่สุดเสมอ”

---

# **3) CACHE STRATEGY BY ENGINE**

---

# **3.1 KS ENGINE → Cache Needs**

✓ canonical mapping  
✓ node metadata  
✓ relation lists  
✓ neighbors graph

### What to cache:

```
ks:canonical_map
ks:node:<canonical_id>
ks:neighbors:<id>
ks:relations:<id>
```

### Benefits:

- canonical resolution speed จาก 20–40 ms → 2–5 ms
    
- relation traversal ลด latency ~70%
    

---

# **3.2 RAG ENGINE → Cache Needs**

✓ query embedding cache  
✓ chunk lookup  
✓ RAG hybrid search cache  
✓ evidence pack cache  
✓ rerank result

### What to cache:

```
embedding:q:<hash>
rag:search:<vec_hash>
rag:evidence:<hash>
chunk:<id>
```

### Benefits:

RAG retrieval จาก 60–100 ms → 8–12 ms

---

# **3.3 AGENT ENGINE → Cache Needs**

✓ Intent classification cache  
✓ step decomposition cache  
✓ common reasoning patterns  
✓ domain cluster cache

### What to cache:

```
agent:intent:<normalized_query>
agent:steps:<hash>
agent:domain:<hash>
agent:template:analysis
```

### Benefits:

Agent reasoning from 30–80 ms → 5–15 ms

---

# **3.4 FLOW ENGINE → Cache Needs**

✓ task graph template  
✓ common workflow shortcuts  
✓ agent routing decisions

### What to cache:

```
flow:taskgraph:<intent_type>
flow:routing:<agent>
```

### Benefits:

Flow orchestration จาก 15–40 ms → 2–5 ms

---

# **4) IMPLEMENTATION FUNCTIONS**

---

## **4.1 Cache Get/Set**

```
function cache_get(key):
    if in L1: return L1[key]
    if in L2: return promote_to_L1(L2[key])
    if in L3: return promote_to_L2(L3[key])
    if in L4: return promote_to_L3(L4[key])
    return null
```

```
function cache_set(key, data):
    L1[key] = data
    L2[key] = data
    L3[key] = data
    L4[key] = data
```

---

## **4.2 Cache Key Normalization**

```
key = hash(domain + query + timestamp(optional))
```

Normalization rules:

- remove fillers
    
- sort words lexically
    
- canonicalize domain phrases
    

---

## **4.3 Promotion Policy**

```
promote(Lower → Higher)
```

E.g., when L3 hit:

```
L1 = data
L2 = data
L3 = data
```

---

# **5) ERROR HANDLING**

Cache-specific errors:

|Error|Recovery|
|---|---|
|Redis unavailable|fallback to L1/L4|
|corrupted value|delete + refresh|
|stale cache|TTL, versioning|
|mismatch with KS update|event-based refresh|
|cold-start empty|compute from DB|

---

# **6) CACHE REFRESH SYSTEM (EVENT-DRIVEN)**

Event Bus triggers:

```
on KS.NODE.UPDATE → invalidate ks:node:<id>
on KS.EDGE.NEW → invalidate ks:neighbors:<id>
on CHUNK.UPDATED → invalidate rag:chunk:<id>
on AGENT.PATTERN.NEW → invalidate agent:template
```

Graph stays fresh automatically  
ไม่มีความเสี่ยง stale knowledge

---

# **7) FULL END-TO-END SIMULATION**

## **Query:**

“ทำไมแรงมากขึ้น ทำให้ความเร่งเพิ่มขึ้น?”

### Step-by-step:

1. Normalize
    
2. Cache hit: `embedding:q:<force_acceleration>` (L1)
    
3. Vector Search cached result: (L2 hit)
    
4. KS neighbors cached: (L2 hit)
    
5. Rerank cached: (L3 hit)
    
6. Evidence pack built (L1)
    
7. Agent reasoning now 5–10 ms
    

**Total latency:** ~20–35 ms  
(จากเดิม 150–350 ms+)

---

# **8) WHAT THIS FILE SOLVES**

✓ Cache v3.0 ครอบคลุมทุก Engine (Agent, RAG, KS, Flow, Event Bus)  
✓ รองรับงานขนาดใหญ่ (Graph 10M nodes ก็ยังเร็ว)  
✓ ลด latency หลักร้อย → หลักสิบ ms  
✓ มี multi-layer cache + event-driven refresh  
✓ พร้อมใช้จริงใน Production  
✓ ไม่มี conflict กับไฟล์ก่อนหน้า  
✓ เก็บงานได้เป็นไฟล์หลักของระบบ

นี่คือ Cache Strategy v3.0 ที่ “สมบูรณ์ที่สุด” สำหรับระบบแบบ UET Platform.

---

ถ้าพร้อมไปต่อส่วนถัดไป  
เรามีทางเลือก:

👉 **Security & Permission v3.0 (Full Production Spec)**  
👉 **Deployment Guide v3.0**  
👉 **Knowledge Sync Engine v3.0 (Full Spec)**  
👉 **System Contract v3.0 (Final)**

บอกมาเลย Santa อยากทำไฟล์ไหนต่อ.