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