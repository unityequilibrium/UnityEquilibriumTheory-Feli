# UET LAB - PRODUCTION ROADMAP v1.0

> **แผนพัฒนาเพื่อขยายสู่ระดับ Production**  
> ผสมผสาน UET Lab + Master Blueprint Enterprise Architecture

---

## 📋 EXECUTIVE SUMMARY

**เป้าหมาย:** พัฒนา UET Lab จากระดับ Prototype → Production-Ready Platform ที่สามารถ scale ได้

**Timeline Estimate:** 8-12 สัปดาห์

**Phases:**
1. **Foundation Fix** (Week 1-2) - แก้ไข critical issues
2. **Architecture Core** (Week 3-4) - Event Bus + Flow Control
3. **Single Shell** (Week 5-6) - Registries + RoomRouter
4. **Security Layer** (Week 7-8) - Auth + Permissions
5. **Production Polish** (Week 9-12) - Metrics, Monitoring, Deployment

---

# PHASE 1: FOUNDATION FIX 🔴
> **Priority: CRITICAL** | Week 1-2 | 15 Tasks

## 1.1 Fix Database Schema

### Actions:
```prisma
// Add to schema.prisma

// 1. Add endedAt to Run
model Run {
  ...existing...
  endedAt   DateTime?  @map("ended_at")
}

// 2. Create EventLog
model EventLog {
  id          String   @id @default(cuid())
  eventType   String   @map("event_type")
  actorType   String   @map("actor_type") // 'user' | 'system' | 'simulation'
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

// 3. Create ErrorLog
model ErrorLog {
  id          String   @id @default(cuid())
  errorType   String   @map("error_type")
  message     String
  stack       String?
  detail      Json?
  projectId   String?  @map("project_id")
  runId       String?  @map("run_id")
  createdAt   DateTime @default(now()) @map("created_at")
  
  @@index([projectId])
  @@index([errorType])
  @@map("error_logs")
}

// 4. Separate Notes model
model Note {
  id        String   @id @default(cuid())
  runId     String   @map("run_id")
  title     String
  content   String
  t         Decimal?  // simulation time reference
  step      BigInt?   // step reference
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")
  
  run Run @relation(fields: [runId], references: [id], onDelete: Cascade)
  
  @@index([runId])
  @@map("notes")
}
```

### Checklist:
- [ ] Add `endedAt` to Run model
- [ ] Create `EventLog` model
- [ ] Create `ErrorLog` model
- [ ] Create `Note` model (separate from metadata)
- [ ] Run `npx prisma migrate dev --name add_production_tables`
- [ ] Update seed.ts

## 1.2 Fix API Routes

### `runs/route.ts` Fix:
```typescript
// BEFORE (WRONG)
data: {
    unitMode: 'physical',       // ❌
    codeVersion: 'oracle-v1',   // ❌
    createdBy: DEFAULT_USER_ID, // ❌
}

// AFTER (CORRECT)
data: {
    unitModeId: 'physical',         // ✅
    equationVersion: 'oracle-v1',   // ✅
    userId: DEFAULT_USER_ID,        // ✅
    name: scenarioName || `Run ${Date.now()}`, // ✅ Required
}
```

### Checklist:
- [ ] Fix `runs/route.ts` POST - correct field names
- [ ] Fix `runs/route.ts` PATCH - add endedAt
- [ ] Add missing `name` field to run creation
- [ ] Implement standard response schema
- [ ] Add error logging to all routes

## 1.3 Standard Response Schema

### Implement in all API routes:
```typescript
// lib/api/response.ts
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    id: string;
    type: string;
    message: string;
    detail?: unknown;
  };
  meta?: {
    timestamp: string;
    requestId?: string;
  };
}

export function success<T>(data: T): ApiResponse<T> {
  return {
    success: true,
    data,
    meta: { timestamp: new Date().toISOString() }
  };
}

export function error(type: string, message: string, detail?: unknown): ApiResponse<never> {
  return {
    success: false,
    error: { id: cuid(), type, message, detail },
    meta: { timestamp: new Date().toISOString() }
  };
}
```

### Checklist:
- [ ] Create `lib/api/response.ts`
- [ ] Update all API routes to use standard response
- [ ] Create error type constants

---

# PHASE 2: ARCHITECTURE CORE 🟠
> **Priority: HIGH** | Week 3-4 | 12 Tasks

## 2.1 Event Bus

### Design:
```typescript
// lib/eventBus/types.ts
export type EventType = 
  // Simulation Events
  | 'RUN_CREATED'
  | 'RUN_STARTED'
  | 'RUN_PAUSED'
  | 'RUN_COMPLETED'
  | 'RUN_FAILED'
  // Step Events
  | 'STEP_COMPLETED'
  | 'TELEMETRY_PUSHED'
  | 'TELEMETRY_PERSISTED'
  // Validation Events
  | 'INVARIANT_CHECK'
  | 'INVARIANT_PASSED'
  | 'INVARIANT_FAILED'
  // Data Events
  | 'SNAPSHOT_SAVED'
  | 'NOTE_CREATED'
  | 'NOTE_UPDATED'
  // Cache Events
  | 'CACHE_INVALIDATED';

export interface AppEvent {
  type: EventType;
  actorType: 'user' | 'system' | 'simulation';
  actorId?: string;
  projectId?: string;
  runId?: string;
  payload: Record<string, unknown>;
  timestamp: number;
}
```

### Implementation:
```typescript
// lib/eventBus/eventBus.ts
class EventBus {
  private listeners: Map<EventType | '*', Set<(event: AppEvent) => void>>;
  private persistQueue: AppEvent[] = [];
  
  emit(event: AppEvent): void {
    // Notify listeners
    this.listeners.get(event.type)?.forEach(fn => fn(event));
    this.listeners.get('*')?.forEach(fn => fn(event));
    
    // Queue for persistence
    this.persistQueue.push(event);
    
    // Log important events
    if (this.shouldPersist(event.type)) {
      this.persistEvent(event);
    }
  }
  
  subscribe(type: EventType | '*', listener: (e: AppEvent) => void): () => void {
    // returns unsubscribe function
  }
  
  private shouldPersist(type: EventType): boolean {
    const persistTypes: EventType[] = [
      'RUN_CREATED', 'RUN_COMPLETED', 'RUN_FAILED',
      'INVARIANT_FAILED', 'SNAPSHOT_SAVED'
    ];
    return persistTypes.includes(type);
  }
}

export const eventBus = new EventBus();
```

### Checklist:
- [ ] Create `lib/eventBus/types.ts`
- [ ] Create `lib/eventBus/eventBus.ts`
- [ ] Create `lib/eventBus/index.ts`
- [ ] Integrate with SimCoreV4 to emit events
- [ ] Integrate with TelemetryService
- [ ] Create `/api/events` endpoint
- [ ] Add SSE support for real-time

## 2.2 Flow Control

### Design:
```typescript
// lib/flowControl/stateMachine.ts
export type SimState = 
  | 'IDLE'
  | 'INITIALIZING'
  | 'READY'
  | 'RUNNING'
  | 'PAUSED'
  | 'COMPLETED'
  | 'FAILED';

export type SimAction =
  | 'INIT'
  | 'PLAY'
  | 'PAUSE'
  | 'RESUME'
  | 'STOP'
  | 'SAVE'
  | 'RESET';

export const VALID_TRANSITIONS: Record<SimState, SimAction[]> = {
  IDLE: ['INIT'],
  INITIALIZING: [],  // Wait for completion
  READY: ['PLAY', 'RESET'],
  RUNNING: ['PAUSE', 'STOP'],
  PAUSED: ['RESUME', 'STOP', 'SAVE'],
  COMPLETED: ['SAVE', 'RESET'],
  FAILED: ['RESET'],
};

export function canTransition(current: SimState, action: SimAction): boolean {
  return VALID_TRANSITIONS[current]?.includes(action) ?? false;
}
```

### Checklist:
- [ ] Create `lib/flowControl/stateMachine.ts`
- [ ] Create `lib/flowControl/flowValidator.ts`
- [ ] Integrate with SimStoreV4
- [ ] Add pre-action validation
- [ ] Emit events on state transitions

## 2.3 Error Handling

### Design:
```typescript
// lib/errors/types.ts
export type ErrorType = 
  | 'SIMULATION_ERROR'      // NaN/Inf detected
  | 'INVARIANT_VIOLATION'   // Physics broke
  | 'PERSISTENCE_ERROR'     // DB/API failed
  | 'VALIDATION_ERROR'      // Invalid input
  | 'PERMISSION_ERROR'      // Not authorized
  | 'SYSTEM_ERROR';         // Unknown

// lib/errors/handler.ts
export async function handleError(
  error: Error,
  type: ErrorType,
  context: { runId?: string; projectId?: string }
): Promise<void> {
  // 1. Log to console
  console.error(`[${type}]`, error);
  
  // 2. Emit event
  eventBus.emit({
    type: 'RUN_FAILED',
    actorType: 'system',
    payload: { errorType: type, message: error.message },
    timestamp: Date.now(),
    ...context
  });
  
  // 3. Persist to DB
  await fetch('/api/errors', {
    method: 'POST',
    body: JSON.stringify({ type, message: error.message, ...context })
  });
}
```

### Checklist:
- [ ] Create `lib/errors/types.ts`
- [ ] Create `lib/errors/handler.ts`
- [ ] Create `/api/errors` endpoint
- [ ] Integrate with SimCoreV4
- [ ] Add error boundaries in React

---

# PHASE 3: SINGLE SHELL ARCHITECTURE 🟡
> **Priority: HIGH** | Week 5-6 | 18 Tasks

## 3.1 Create Registries

### roomRegistry.ts:
```typescript
// registries/roomRegistry.ts
export interface RoomDefinition {
  room_id: string;
  type: 'sim3d' | 'test_terminal';
  title: string;
  description: string;
  tags: string[];
  defaultModules: string[];
  defaultMetrics: string[];
  defaultPreset?: string;
  permissions: {
    saveToDB: boolean;
    export: boolean;
    edit: boolean;
  };
}

export const ROOMS: RoomDefinition[] = [
  {
    room_id: 'solarSystem',
    type: 'sim3d',
    title: 'Solar System',
    description: 'N-body simulation of solar system',
    tags: ['sim', 'planetary', 'demo'],
    defaultModules: ['newtonian'],
    defaultMetrics: ['total_energy', 'kinetic_energy', 'potential_energy'],
    defaultPreset: 'solarSystem',
    permissions: { saveToDB: true, export: true, edit: true }
  },
  {
    room_id: 'testGates',
    type: 'test_terminal',
    title: 'Test Gates',
    description: 'Run validation test scenarios G0-G4',
    tags: ['test', 'validation', 'gates'],
    defaultModules: ['newtonian'],
    defaultMetrics: ['energy_drift', 'angular_momentum_drift', 'test_status'],
    permissions: { saveToDB: true, export: true, edit: false }
  }
];
```

### testRegistry.ts:
```typescript
// registries/testRegistry.ts
export interface TestGateDefinition {
  gate_id: 'G0' | 'G1' | 'G2' | 'G3' | 'G4';
  name: string;
  description: string;
  scenarios: string[];
  tolerances: {
    energyDrift: number;
    angularMomentumDrift: number;
    positionError?: number;
  };
}

export const TEST_GATES: TestGateDefinition[] = [
  {
    gate_id: 'G0',
    name: 'Sanity',
    description: 'Determinism + No NaN',
    scenarios: ['sanity_determinism', 'sanity_no_nan'],
    tolerances: { energyDrift: 0, angularMomentumDrift: 0 }
  },
  // ... G1-G4
];
```

### Checklist:
- [ ] Create `registries/` directory
- [ ] Create `registries/roomRegistry.ts`
- [ ] Move metrics to `registries/metricRegistry.ts`
- [ ] Create `registries/testRegistry.ts`
- [ ] Create `registries/index.ts` barrel export

## 3.2 Create Shell Components

### LabShell.tsx:
```typescript
// shell/LabShell.tsx
interface LabShellProps {
  roomId: string;
  children: React.ReactNode; // RoomRouter output
}

export function LabShell({ roomId, children }: LabShellProps) {
  const [selectedMetrics, setSelectedMetrics] = useState<string[]>([]);
  const [dockOpen, setDockOpen] = useState(true);
  
  return (
    <div className="fixed inset-0 flex flex-col bg-[#050508]">
      <TopNav roomId={roomId} />
      
      <div className="flex-1 flex overflow-hidden">
        <LeftOutputPanel 
          selectedMetrics={selectedMetrics}
          onToggleMetric={...}
        />
        
        <main className="flex-1">
          {children}
        </main>
        
        <RightStudioPanel />
      </div>
      
      <GraphDock 
        selectedMetrics={selectedMetrics}
        isOpen={dockOpen}
      />
    </div>
  );
}
```

### Checklist:
- [ ] Create `shell/` directory
- [ ] Create `shell/AppTokens.ts`
- [ ] Create `shell/LabShell.tsx`
- [ ] Add room selector to TopNav
- [ ] Add URL sync (`/lab?room=xxx`)

## 3.3 Create RoomRouter

### RoomRouter.tsx:
```typescript
// features/rooms/RoomRouter.tsx
interface RoomRouterProps {
  roomId: string;
}

export function RoomRouter({ roomId }: RoomRouterProps) {
  const room = getRoomById(roomId);
  
  switch (room?.type) {
    case 'sim3d':
      return <Sim3DRoom room={room} />;
    case 'test_terminal':
      return <TestTerminalRoom room={room} />;
    default:
      return <div>Room not found</div>;
  }
}
```

### Checklist:
- [ ] Create `features/rooms/` directory
- [ ] Create `features/rooms/RoomRouter.tsx`
- [ ] Create `features/rooms/Sim3DRoom.tsx`
- [ ] Create `features/rooms/TestTerminalRoom.tsx`

## 3.4 Migrate Components

### Checklist:
- [ ] Create `features/metrics/` directory
- [ ] Move MetricCard → `features/metrics/`
- [ ] Move MetricCardList → `features/metrics/`
- [ ] Move GraphDock → `features/metrics/`
- [ ] Create `features/panels/` directory
- [ ] Move LeftOutputPanel → `features/panels/`
- [ ] Move RightStudioPanel → `features/panels/`
- [ ] Update `/lab/page.tsx` to use LabShell
- [ ] Update all imports

---

# PHASE 4: SECURITY LAYER 🟢
> **Priority: MEDIUM** | Week 7-8 | 10 Tasks

## 4.1 Authentication

### Design:
```typescript
// lib/auth/types.ts
export type Role = 'guest' | 'user' | 'power' | 'admin';

export interface User {
  id: string;
  email: string;
  name: string;
  role: Role;
}

export interface AuthContext {
  user: User | null;
  isAuthenticated: boolean;
  can: (action: string) => boolean;
}
```

### Permission Matrix:
| Action | Guest | User | Power | Admin |
|--------|-------|------|-------|-------|
| View Sim | ✅ | ✅ | ✅ | ✅ |
| Run Sim | ❌ | ✅ | ✅ | ✅ |
| Save to DB | ❌ | ✅ | ✅ | ✅ |
| Export | ❌ | ✅ | ✅ | ✅ |
| View All Runs | ❌ | Own | ✅ | ✅ |
| Delete Runs | ❌ | Own | ✅ | ✅ |
| Admin Panel | ❌ | ❌ | ❌ | ✅ |

### Checklist:
- [ ] Create `lib/auth/types.ts`
- [ ] Create `lib/auth/context.tsx`
- [ ] Create `lib/auth/permissions.ts`
- [ ] Implement JWT validation
- [ ] Add auth middleware to API routes
- [ ] Create login page (optional - can defer)

---

# PHASE 5: PRODUCTION POLISH 🔵
> **Priority: LOW** | Week 9-12 | 15 Tasks

## 5.1 Health & Metrics API

### Checklist:
- [ ] Create `/api/health` endpoint
- [ ] Create `/api/metrics` endpoint
- [ ] Add performance tracking
- [ ] Add telemetry aggregation

## 5.2 Monitoring & Logging

### Checklist:
- [ ] Structured logging format
- [ ] Error tracking integration
- [ ] Performance monitoring
- [ ] Uptime monitoring

## 5.3 Testing

### Checklist:
- [ ] Unit tests for SimCore
- [ ] Integration tests for API
- [ ] E2E tests for critical flows
- [ ] Test coverage report

## 5.4 Deployment

### Checklist:
- [ ] Docker configuration
- [ ] CI/CD pipeline
- [ ] Environment configs
- [ ] Database migration strategy

---

# PROJECT TIMELINE

```
Week 1-2:  PHASE 1 (Foundation Fix)      ████████████
Week 3-4:  PHASE 2 (Architecture Core)   ████████████
Week 5-6:  PHASE 3 (Single Shell)        ████████████
Week 7-8:  PHASE 4 (Security Layer)      ████████████
Week 9-12: PHASE 5 (Production Polish)   ████████████████████████
```

---

# MIGRATION STRATEGY

## ทำได้ทีละขั้น (Incremental)

1. **Week 1:** Fix API routes ก่อน → ระบบยังใช้งานได้
2. **Week 2:** Add EventLog/ErrorLog → ยังไม่กระทบ existing code
3. **Week 3-4:** Event Bus + Flow Control → เป็น layer ใหม่ ไม่แก้ existing
4. **Week 5-6:** Single Shell → refactor progressive
5. **Week 7-8:** Auth → สามารถ bypass ได้ถ้ายังไม่พร้อม
6. **Week 9+:** Polish → ทำเมื่อ core เสร็จ

## Backward Compatibility

- ทุก Phase ต้อง**ไม่ break existing functionality**
- ใช้ Feature Flags สำหรับ features ใหม่
- Database migration ต้อง non-destructive

---

# SUCCESS CRITERIA

## Phase 1 Complete:
- [ ] API routes ทำงานถูกต้อง
- [ ] EventLog/ErrorLog tables exist
- [ ] Standard response format used

## Phase 2 Complete:
- [ ] eventBus.emit() works
- [ ] State machine validates transitions
- [ ] Errors logged to DB

## Phase 3 Complete:
- [ ] Single `/lab` route with room switching
- [ ] 3 registries exist and used
- [ ] All components in features/

## Phase 4 Complete:
- [ ] JWT auth works
- [ ] Permissions enforced

## Phase 5 Complete:
- [ ] Health check returns OK
- [ ] Docker deployment works
- [ ] Test coverage > 70%

---

**Document Version:** 1.0  
**Created:** 2024-12-23  
**Status:** APPROVED FOR EXECUTION
