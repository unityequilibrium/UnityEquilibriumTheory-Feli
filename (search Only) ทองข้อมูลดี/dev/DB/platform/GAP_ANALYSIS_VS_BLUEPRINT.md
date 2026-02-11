# Gap Analysis: Current UET Lab vs Master Blueprint

> วิเคราะห์เชิงลึก: สถานะปัจจุบันเทียบกับ Blueprint มาตรฐานระดับ Production

---

## Executive Summary

**Master Blueprint** คือ architecture ระดับ Enterprise สำหรับ **Knowledge Management Platform** ประกอบด้วย 20 เอกสาร ครอบคลุม:
- System Contract (กฎสูงสุดของระบบ)
- Data Schema v2.0 (โครงสร้างข้อมูลทุกประเภท)
- API Spec v2.0 (Unified API ทุก endpoint)
- Event Bus (Nervous system ของระบบ)
- Flow Control (บังคับ sequence ทุก action)
- และอีก 15 subsystems

**ข้อสังเกต:** Master Blueprint ออกแบบสำหรับ **Knowledge Platform** ที่มี AI Agent, RAG, Knowledge Sync  
ในขณะที่ **UET Lab** เป็น **Physics Simulation Platform** → บางส่วนใช้ได้ บางส่วนต้องดัดแปลง

---

## 1. ARCHITECTURE PRINCIPLES COMPARISON

| หลักการ | Master Blueprint | UET Lab ปัจจุบัน | Gap |
|---------|-----------------|------------------|-----|
| **Deterministic Execution** | ✅ บังคับ seed, no randomness | ⚠️ มี seed แต่ยังไม่ enforce | ต้องเพิ่ม validation |
| **Version Control** | ✅ ทุกไฟล์ต้องมี version | ⚠️ Run มี version แต่ equations/presets ไม่มี | ต้องเพิ่ม versioning |
| **Event-Driven** | ✅ ทุก state change ประกาศ event | ❌ ไม่มี Event Bus | ต้องสร้าง Event Bus |
| **Zero-Stale Policy** | ✅ ข้อมูลต้อง fresh เสมอ | ⚠️ Telemetry buffer มี stale ได้ | ต้องเพิ่ม invalidation |
| **Flow Control** | ✅ ทุก action ผ่าน validation | ❌ ไม่มี Flow Control | ต้องสร้าง |
| **Permission Matrix** | ✅ Role-based ละเอียด | ❌ Hardcoded user/project | ต้องเพิ่ม auth |

---

## 2. DATA SCHEMA COMPARISON

### Master Blueprint Schema (12 Entities):
```
User → Project → File → FileVersion → Chunk → Embedding
                                    ↓
                              KBRegistry
                                    ↓
AgentRun → RoutingLog → EventLog
         ↓
    ErrorLog → Metrics → CacheEntry
```

### UET Lab Schema (9 Tables):
```
User → Project → Run → Snapshot
                    ↓
              TelemetrySample
                    ↓
              RunEquation ↔ EquationModule
                    ↓
              UnitMode → MetricRegistry
```

### Gap Analysis:

| Entity | Blueprint | UET Lab | Match |
|--------|-----------|---------|-------|
| User | ✅ | ✅ | ✅ |
| Project | ✅ | ✅ | ✅ |
| File/FileVersion | ✅ | ❌ (ไม่มี) | N/A สำหรับ sim |
| Chunk/Embedding | ✅ | ❌ (ไม่มี) | N/A สำหรับ sim |
| KBRegistry | ✅ | ⚠️ MetricRegistry (บางส่วน) | ❌ |
| Run/Simulation | ❌ | ✅ | ใช้ได้ |
| Snapshot | ❌ | ✅ | ✅ |
| TelemetrySample | ❌ | ✅ | ✅ |
| AgentRun | ✅ | ❌ | N/A |
| RoutingLog | ✅ | ❌ | N/A |
| EventLog | ✅ | ❌ | ต้องสร้าง |
| ErrorLog | ✅ | ❌ | ต้องสร้าง |
| Metrics | ✅ | ⚠️ TelemetrySample | ใกล้เคียง |
| CacheEntry | ✅ | ❌ | ต้องสร้าง |

---

## 3. API COMPARISON

### Master Blueprint API Categories:
```
/auth     - Authentication
/projects - Project management
/files    - File upload/management
/versions - Version control
/kb       - Knowledge Base
/rag      - Vector search
/agent    - AI Agent runs
/routing  - Model selection
/cache    - Cache management
/events   - Event stream/SSE
/metrics  - Performance tracking
/system   - Health check
```

### UET Lab API Categories:
```
/api/runs       - Run management ✅
/api/notes      - Notes CRUD ✅
/api/telemetry  - Time series data ✅
```

### Gap Summary:
| API Category | Blueprint | UET Lab | Priority |
|--------------|-----------|---------|----------|
| Auth | ✅ | ❌ Hardcoded | High |
| Projects | ✅ | ⚠️ Implicit | Medium |
| Runs | ❌ | ✅ | ✅ |
| Telemetry | ❌ | ✅ | ✅ |
| Notes | ❌ | ✅ | ✅ |
| Events/SSE | ✅ | ❌ | High |
| Metrics/Health | ✅ | ❌ | Medium |
| Cache | ✅ | ❌ | Low |

---

## 4. ENGINES COMPARISON

### Master Blueprint มี 6 Engines:
1. **File Engine** - จัดการไฟล์
2. **Knowledge Sync Engine** - Parse→Chunk→Embed→Registry
3. **RAG Engine** - Vector search
4. **Agent Engine** - AI reasoning
5. **Flow Control Engine** - Sequence validation
6. **Event Bus** - Central nervous system

### UET Lab มี 2 Engines:
1. **SimCoreV4** - Physics simulation ✅
2. **TelemetryService** - Data buffering ✅

### Gap:
| Engine | Blueprint | UET Lab | Action |
|--------|-----------|---------|--------|
| File Engine | ✅ | ❌ | N/A สำหรับ sim |
| Knowledge Sync | ✅ | ⚠️ MetricRegistry | Partial |
| RAG Engine | ✅ | ❌ | N/A สำหรับ sim |
| Agent Engine | ✅ | ❌ | N/A สำหรับ sim |
| SimCore | ❌ | ✅ | UET-specific |
| Flow Control | ✅ | ❌ | **ต้องสร้าง** |
| Event Bus | ✅ | ❌ | **ต้องสร้าง** |
| Oracle/Invariants | ❌ | ✅ | UET-specific |
| Test Runner | ❌ | ✅ | UET-specific |

---

## 5. WHAT UET LAB SHOULD ADOPT

### 🔴 Critical (Must Have):

1. **Event Bus**
   - ระบบประกาศ events: `RUN_STARTED`, `STEP_COMPLETED`, `INVARIANT_FAILED`, `TELEMETRY_PERSISTED`
   - UI subscribe to events แทน polling
   - Cache invalidation ผ่าน events

2. **Flow Control**
   - Validate sequence: Init→Play→Pause→Save
   - ห้าม Save ก่อน Init
   - ห้าม Export ถ้า Run ยังไม่จบ

3. **Event/Error Logging**
   - Add `EventLog` table
   - Add `ErrorLog` table
   - Log ทุก action ที่สำคัญ

4. **Authentication**
   - แทน hardcoded user/project
   - JWT tokens
   - Role-based permissions

### 🟡 High Priority (Should Have):

5. **Response Schema มาตรฐาน**
   ```json
   {
     "success": boolean,
     "data": {...},
     "error": { "id", "type", "message" }
   }
   ```

6. **Health/Metrics API**
   - `/api/health`
   - `/api/metrics`

7. **SSE for Real-time Updates**
   - `/api/events/stream`
   - UI ใช้แทน polling telemetry

### 🟢 Nice to Have:

8. **Cache Layer with TTL**
9. **Version Tracking for Presets**
10. **Audit Trail for all saves**

---

## 6. RECOMMENDED SCHEMA ADDITIONS

```prisma
// Add Event Bus support
model EventLog {
  id          String   @id @default(cuid())
  eventType   String   @map("event_type")
  actorType   String   @map("actor_type") // 'user' | 'system'
  actorId     String?  @map("actor_id")
  projectId   String?  @map("project_id")
  runId       String?  @map("run_id")
  payload     Json     @default("{}")
  createdAt   DateTime @default(now()) @map("created_at")
  
  @@index([projectId])
  @@index([runId])
  @@index([eventType])
  @@map("event_logs")
}

model ErrorLog {
  id          String   @id @default(cuid())
  errorType   String   @map("error_type")
  message     String
  detail      Json?
  projectId   String?  @map("project_id")
  runId       String?  @map("run_id")
  createdAt   DateTime @default(now()) @map("created_at")
  
  @@index([projectId])
  @@index([runId])
  @@map("error_logs")
}
```

---

## 7. RECOMMENDED API ADDITIONS

```
// New endpoints needed
GET  /api/health              - System health
GET  /api/events/stream       - SSE real-time events  
GET  /api/events?runId=xxx    - Event history
POST /api/errors              - Log errors
GET  /api/metrics/project/:id - Project metrics
```

---

## 8. PRIORITY MATRIX

| Item | Effort | Impact | Priority |
|------|--------|--------|----------|
| Fix API field names | Low | High | 🔴 P0 |
| Add endedAt to schema | Low | Medium | 🔴 P0 |
| Add EventLog table | Medium | High | 🔴 P1 |
| Add ErrorLog table | Medium | High | 🔴 P1 |
| Implement Event Bus | High | High | 🟡 P2 |
| Implement Flow Control | High | High | 🟡 P2 |
| Add Auth system | High | Medium | 🟡 P2 |
| Add SSE streaming | Medium | Medium | 🟢 P3 |
| Add Health API | Low | Low | 🟢 P3 |

---

## 9. CONCLUSION

**Master Blueprint** เป็น architecture ระดับ Enterprise สำหรับ Knowledge Platform  

**UET Lab** สามารถ adopt บางส่วนได้:
- ✅ Event Bus concept
- ✅ Flow Control concept
- ✅ Event/Error Logging
- ✅ Unified Response Schema
- ✅ Health/Metrics API

**ไม่จำเป็นต้อง adopt:**
- ❌ RAG Engine (UET ใช้ physics simulation ไม่ใช่ text search)
- ❌ Agent Engine (UET ไม่มี AI reasoning แบบ LLM)
- ❌ Knowledge Sync (UET ใช้ MetricRegistry แทน)
- ❌ File/Chunk/Embedding (ไม่มี document processing)

**Next Steps:**
1. Fix critical API issues ก่อน
2. Add EventLog/ErrorLog tables
3. Implement basic Event Bus
4. Add Flow Control validation
5. Add Authentication

---

**Document Version:** 1.0  
**Last Updated:** 2024-12-23
