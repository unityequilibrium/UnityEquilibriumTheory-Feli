# Backend Architecture Documentation

> **Related Documents:**
> - [SMART_INDEX](design_system/SMART_INDEX.md) ← Smart System Master
> - [SMART_DATA_DICTIONARY](SMART_DATA_DICTIONARY.md) ← Metric Definitions
> - [API_REFERENCE](API_REFERENCE.md) ← REST API Docs
> - [DATABASE_SCHEMA](DATABASE_SCHEMA.md) ← Table Definitions

> เอกสารอธิบายระบบหลังบ้านทั้งหมด: Database, API, Services, Data Flow  
> **Last Updated: 2024-12-24** (Smart System Integration)

---

## 1. SYSTEM OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ FRONTEND (Next.js App Router)                                               │
│                                                                             │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│ │ SimCoreV4    │→ │ EventBus     │→ │ TelemetryService │→ │ API Routes │  │
│ │ (Engine)     │  │ (Phase 2)    │  │ (Buffer+Batch)│  │ (REST)       │    │
│ └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
│        ↓                 ↓                                   │              │
│ ┌──────────────┐  ┌──────────────┐                           │              │
│ │ FlowControl  │  │ ErrorHandler │                           │              │
│ │ (Phase 2)    │  │ (Phase 2)    │                           │              │
│ └──────────────┘  └──────────────┘                           │              │
│                                                              │              │
│ ┌──────────────────────────────────────────────────┐         │              │
│ │ Registries (Phase 3)                             │         │              │
│ │ • roomRegistry    • testRegistry    • metricRegistry       │              │
│ └──────────────────────────────────────────────────┘         │              │
└──────────────────────────────────────────────────────│───────│──────────────┘
                                                       │       │
                                                       ▼       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ DATABASE (PostgreSQL via Prisma ORM)                                        │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│ │ users        │  │ projects     │  │ runs         │  │ snapshots    │     │
│ │ unit_modes   │  │ equations    │  │ notes ✅     │  │ telemetry    │     │
│ │ event_logs ✅│  │ error_logs ✅│  │              │  │ samples      │     │
│ └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. DATABASE SCHEMA (PostgreSQL + Prisma)

### 2.1 Entity Relationship Diagram

```
┌──────────┐      ┌───────────┐      ┌─────────┐      ┌───────────────┐
│   User   │──1:N─│  Project  │──1:N─│   Run   │──1:N─│   Snapshot    │
└──────────┘      └───────────┘      └─────────┘      └───────────────┘
                                          │
                                          │──1:N─→ TelemetrySample
                                          │──1:N─→ Note ✅ (Phase 1)
                                          │──N:M─→ EquationModule
                                          │         (via RunEquation)
                                          └───→ UnitMode (FK)

[Standalone Tables]
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  EventLog    │  │  ErrorLog    │  │MetricRegistry│
│  (Phase 1)   │  │  (Phase 1)   │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
```

### 2.2 Table Descriptions

| Table | Purpose | Key Fields | Status |
|-------|---------|------------|--------|
| `users` | ผู้ใช้งาน | id, email, name | ✅ |
| `projects` | โปรเจค/workspace | id, ownerId, slug, config | ✅ |
| `unit_modes` | โหมดหน่วย (PHY/UET) | id, name, color | ✅ |
| `equation_modules` | สมการที่รองรับ | id, slug, category, canCouple | ✅ |
| `runs` | การรันแต่ละครั้ง | id, seed, status, **endedAt**, metadata | ✅ Fixed |
| `run_equations` | สมการที่ใช้ในแต่ละ run | runId, moduleId, role, config | ✅ |
| `snapshots` | Checkpoint states | runId, t, step, stateJson, hash | ✅ |
| `telemetry_samples` | Time series data | runId, t, step, metricId, value | ✅ |
| `metric_registry` | นิยาม metrics | id, label, unit, plotGroup | ✅ |
| `notes` | Run annotations | runId, title, content, t, step | ✅ **NEW** |
| `event_logs` | Event Bus persistence | eventType, actorType, payload | ✅ **NEW** |
| `error_logs` | Error tracking | errorType, message, stack | ✅ **NEW** |

### 2.3 Key Schema Features

**✅ ใช้งานได้:**
- Run เชื่อม N:M กับ EquationModule ผ่าน RunEquation
- Snapshot เก็บ stateJson สำหรับ replay
- TelemetrySample indexed ด้วย (runId, step) และ (runId, metricId)
- MetricRegistry ใน DB sync กับ JSON registry
- **Notes model แยก** (Phase 1) ✅
- **EventLog สำหรับ audit trail** (Phase 1) ✅
- **ErrorLog สำหรับ error tracking** (Phase 1) ✅
- **endedAt field** (Phase 1) ✅

**⚠️ ยังต้องทำ (Phase 4+):**
- Authentication/JWT
- Multi-tenant support (ยังใช้ hardcoded IDs)

---

## 3. API ROUTES

### 3.1 Overview

```
/api/
├── runs/
│   ├── route.ts      # POST (create), GET (list)
│   └── [id]/
│       └── route.ts  # GET (one), PATCH (update), DELETE
├── notes/
│   ├── route.ts      # GET (list), POST (create)
│   └── [id]/
│       └── route.ts  # PUT (update), DELETE
└── telemetry/
    └── route.ts      # POST (batch insert), GET (query)
```

### 3.2 Route Details

#### `POST /api/runs`
```typescript
// Request
{
  scenarioId: string,
  scenarioName: string,
  gate: string,
  seed?: number,
  dt: number,
  totalTime: number,
  equations: { id: string, role: string, enabled: boolean }[]
}

// Response
{ success: true, runId: string }
```

#### `GET /api/runs`
```typescript
// Query: ?limit=50&status=completed&gate=G2

// Response
{
  success: true,
  runs: [{
    id: string,
    seed: string,
    status: string,
    metadata: object,
    equations: [...],
    snapshots: [...]
  }],
  count: number
}
```

#### `POST /api/telemetry`
```typescript
// Request (Batch insert)
{
  samples: [{
    runId: string,
    t: number,
    step: number,
    metricId: string,
    value: number
  }, ...]
}

// Response
{ success: true, inserted: number }
```

#### `GET /api/telemetry`
```typescript
// Query: ?runId=xxx&metricId=total_energy&limit=1000

// Response
{
  runId: string,
  metrics: {
    "total_energy": [{ t, step, value }, ...],
    "kinetic_energy": [...]
  }
}
```

### 3.3 Issues Found

| Issue | Location | Description |
|-------|----------|-------------|
| ❌ | `runs/route.ts:30` | ใช้ `unitMode: 'physical'` แต่ schema ต้องการ `unitModeId` |
| ❌ | `runs/route.ts:33` | ใช้ `createdBy` แต่ schema ใช้ `userId` |
| ❌ | `runs/route.ts:32` | ใช้ `codeVersion` แต่ schema ใช้ `equationVersion` |
| ⚠️ | All routes | Hardcoded `DEFAULT_PROJECT_ID` และ `DEFAULT_USER_ID` |
| ⚠️ | Notes routes | Notes เก็บใน Run.metadata แทนที่จะมี Notes model แยก |

---

## 4. SERVICES LAYER

### 4.1 TelemetryService

**Type:** Singleton  
**Location:** `lib/services/telemetryService.ts`

```
                  ┌────────────────────┐
   SimCoreV4 ────→│  TelemetryService  │
                  │                    │
                  │ • subscribe()      │
                  │ • push(packet)     │
                  │ • getTimeSeries()  │
                  │ • flush()          │
                  └─────────┬──────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
     ┌──────────┐   ┌──────────────┐  ┌────────────┐
     │ Buffer   │   │ Listeners    │  │ Persistence│
     │ (in-mem) │   │ (callbacks)  │  │ (batch API)│
     └──────────┘   └──────────────┘  └────────────┘
```

**Key Features:**
- ✅ Buffering: เก็บ 1000 samples per metric in memory
- ✅ Pub/Sub: Subscribe to real-time updates
- ✅ Batch Persistence: Auto-flush ทุก 5 วินาที
- ✅ Trim old data: ไม่ให้ memory overflow

**⚠️ Issues:**
- Buffer size hardcoded (1000)
- Persistence interval hardcoded (5000ms)
- No retry mechanism if API fails

### 4.2 PersistenceService

**Location:** `lib/services/persistenceService.ts`

- ✅ Save to Gallery (DB)
- ✅ Export (CSV/JSON/HTML)
- ⚠️ Relies on Run.metadata for gallery info

### 4.3 NotesService

**Location:** `lib/services/notesService.ts`

- ✅ CRUD via API
- ✅ Autosave with debounce (1 second)
- ✅ Local cache
- ⚠️ Notes stored in Run.metadata, not separate table

---

## 5. DATA FLOW DIAGRAMS

### 5.1 Simulation Run Flow

```
[User clicks Play]
      │
      ▼
┌─────────────────┐
│ SimCoreV4.play()│
└────────┬────────┘
         │
         ▼ (every step)
┌─────────────────────┐
│ compute forces      │
│ update positions    │
│ compute outputs     │
└────────┬────────────┘
         │
         ▼
┌────────────────────────┐
│ telemetryService.push()│
│ {run_id, t, step,      │
│  metrics: {E, K, U...}}│
└────────┬───────────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌─────────────┐
│Buffer  │ │Notify       │
│(local) │ │Listeners    │
└────────┘ │(UI update)  │
           └─────────────┘
         │
         ▼ (every 5s)
┌─────────────────────────┐
│ POST /api/telemetry     │
│ (batch insert)          │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ PostgreSQL              │
│ telemetry_samples table │
└─────────────────────────┘
```

### 5.2 Save to Gallery Flow

```
[User clicks Save]
      │
      ▼
┌───────────────────────────┐
│ persistenceService        │
│ .saveToGallery()          │
└───────────┬───────────────┘
            │
            ▼
┌───────────────────────────┐
│ PATCH /api/runs/{id}      │
│ {                         │
│   status: 'completed',    │
│   metadata: {             │
│     savedToGallery: true, │
│     galleryThumbnail: ... │
│   }                       │
│ }                         │
└───────────┬───────────────┘
            │
            ▼
┌───────────────────────────┐
│ PostgreSQL                │
│ UPDATE runs               │
│ SET metadata = {...}      │
└───────────────────────────┘
```

### 5.3 Replay Flow

```
[User opens Gallery item]
      │
      ▼
┌────────────────────────┐
│ GET /api/runs/{id}     │
│ include: snapshots,    │
│          equations     │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ Reconstruct WorldState │
│ from snapshot.stateJson│
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ SimCoreV4.resume()     │
│ with restored state    │
└────────────────────────┘
```

---

## 6. ISSUES SUMMARY

### 6.1 Critical (Must Fix)

| # | Issue | Impact | Fix |
|---|-------|--------|-----|
| 1 | API field names don't match schema | Runs won't create | Update API to use correct field names |
| 2 | Missing `endedAt` in schema | Can't track run end time | Add field to Prisma schema |

### 6.2 Medium (Should Fix)

| # | Issue | Impact | Fix |
|---|-------|--------|-----|
| 3 | Notes in metadata | Performance/query issues | Create separate Notes model |
| 4 | Hardcoded project/user IDs | No multi-tenant support | Add auth context |
| 5 | No retry for persistence | Data loss if API fails | Add retry queue |

### 6.3 Low (Nice to Have)

| # | Issue | Impact | Fix |
|---|-------|--------|-----|
| 6 | Magic numbers (buffer sizes) | Hard to tune | Move to config |
| 7 | No compression for telemetry | High storage | Add compression option |

---

## 7. RECOMMENDED SCHEMA UPDATES

```prisma
// Add to Run model
endedAt  DateTime?  @map("ended_at")

// New Notes model (instead of metadata)
model Note {
  id        String   @id @default(cuid())
  runId     String   @map("run_id")
  title     String
  content   String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  run Run @relation(fields: [runId], references: [id], onDelete: Cascade)
  
  @@map("notes")
}
```

---

## 9. AUTHENTICATION LAYER ✅ (Phase 4)

### 9.1 Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│ Auth System (lib/auth/)                                             │
│                                                                     │
│ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│ │ types.ts    │  │permissions.ts│  │ context.tsx │  │middleware.ts│ │
│ │ Role, User  │  │ hasPermission│  │ AuthProvider│  │ requireAuth │ │
│ │ Permission  │  │ hasMinRole   │  │ useAuth()   │  │ withAuth()  │ │
│ └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### 9.2 Role Hierarchy

| Role | Level | Description |
|------|-------|-------------|
| `guest` | 0 | View only, no actions |
| `user` | 1 | Basic simulation/save |
| `power` | 2 | Access all runs |
| `admin` | 3 | Full system access |

### 9.3 Permission Matrix

| Permission | Guest | User | Power | Admin |
|------------|-------|------|-------|-------|
| `sim:view` | ✅ | ✅ | ✅ | ✅ |
| `sim:run` | ❌ | ✅ | ✅ | ✅ |
| `sim:save` | ❌ | ✅ | ✅ | ✅ |
| `runs:view_all` | ❌ | Own | ✅ | ✅ |
| `runs:delete_all` | ❌ | Own | ✅ | ✅ |
| `admin:panel` | ❌ | ❌ | ❌ | ✅ |

### 9.4 Usage in React

```typescript
// In components
import { useAuth } from '@/lib/auth';

function MyComponent() {
    const { user, can, isAuthenticated } = useAuth();
    
    if (!isAuthenticated) return <Login />;
    if (!can('sim:run')) return <Unauthorized />;
    
    return <Simulation />;
}
```

### 9.5 Usage in API Routes

```typescript
// In API routes
import { requireAuth, requirePermission, withAuth } from '@/lib/auth';

// Option 1: Manual check
export async function GET(request: NextRequest) {
    const userOrResponse = requireAuth(request);
    if (!isUser(userOrResponse)) return userOrResponse;
    
    const user = userOrResponse;
    // ... use user
}

// Option 2: Wrapper
export const GET = withAuth(async (request, user) => {
    // user is guaranteed to exist
    return jsonSuccess({ user });
});
```

### 9.6 Demo Mode

- ตั้ง `AUTH_DEMO_MODE=true` (default ใน development)
- ใช้ Demo User (role: power) โดยไม่ต้อง login
- Production: ตั้ง `AUTH_DEMO_MODE=false` และใช้ JWT

---

## 10. PRODUCTION POLISH ✅ (Phase 5)

### 10.1 Health Check API

**Endpoint:** `GET /api/health`

```json
{
    "status": "healthy",
    "timestamp": "2024-12-23T12:00:00.000Z",
    "version": "0.1.0",
    "uptime": 3600,
    "checks": {
        "database": { "status": "pass", "latencyMs": 5 },
        "memory": { "status": "pass", "message": "Heap: 64MB / 128MB (50%)" }
    }
}
```

**Options:**
- `?detailed=true` - Include full check details
- `HEAD /api/health` - Simple alive check for load balancers

### 10.2 Metrics API

**Endpoint:** `GET /api/metrics`

```json
{
    "success": true,
    "data": {
        "timestamp": "2024-12-23T12:00:00.000Z",
        "uptime": 3600,
        "database": {
            "runs": { "count": 123, "lastCreated": "..." },
            "snapshots": { "count": 456 },
            "telemetry": { "count": 78900 }
        },
        "simulation": {
            "activeRuns": 2,
            "completedRuns": 100,
            "failedRuns": 5,
            "avgDurationMs": 5230
        },
        "system": {
            "memoryUsedMB": 64,
            "memoryTotalMB": 128,
            "nodeVersion": "v20.10.0"
        }
    }
}
```

### 10.3 Structured Logging

**Location:** `lib/logger.ts`

```typescript
import { logger, createLogger } from '@/lib/logger';

// Global logger
logger.info('Server started', { port: 3000 });

// Context-specific logger
const log = createLogger('SimCore');
log.debug('Step computed', { step: 100, t: 1.0 });
log.error('Simulation failed', error, { runId: 'xxx' });
```

**Output:**
- Development: Readable colored output
- Production: JSON format for log aggregation

### 10.4 Docker Deployment

**Files:**
- `frontend/Dockerfile` - Multi-stage Next.js build
- `docker-compose.yml` - Full stack setup
- `.env.example` - Environment template

**Quick Start:**
```powershell
# Copy environment
cp .env.example .env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f frontend

# Stop
docker-compose down
```

**Services:**
| Service | Port | Description |
|---------|------|-------------|
| `db` | 5432 | PostgreSQL database |
| `frontend` | 3000 | Next.js application |
| `prisma-studio` | 5555 | Database GUI (dev profile only) |

---

## 11. IMPLEMENTATION SUMMARY

### Files Created per Phase

| Phase | Module | Files |
|-------|--------|-------|
| Phase 1 | Database | schema.prisma changes, Note/EventLog/ErrorLog models |
| Phase 1 | API | lib/api/response.ts, /api/events, /api/errors |
| Phase 2 | Event Bus | lib/eventBus/types.ts, eventBus.ts, index.ts |
| Phase 2 | Flow Control | lib/flowControl/stateMachine.ts, index.ts |
| Phase 2 | Errors | lib/errors/handler.ts, index.ts |
| Phase 3 | Registries | registries/roomRegistry.ts, testRegistry.ts, index.ts |
| Phase 3 | Shell | shell/AppTokens.ts, LabShell.tsx, index.ts |
| Phase 3 | Rooms | features/rooms/RoomRouter.tsx, index.ts |
| Phase 4 | Auth | lib/auth/types.ts, permissions.ts, context.tsx, middleware.ts |
| Phase 5 | Health | /api/health, /api/metrics |
| Phase 5 | Deploy | Dockerfile, docker-compose.yml, .env.example |
| Phase 5 | Logging | lib/logger.ts |

---

**Document Version:** 2.0  
**Last Updated:** 2024-12-23  
**Status:** Phase 1-5 Complete ✅

