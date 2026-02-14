# Event Bus Specification
## Layer D — System Nervous System

**Last Updated:** 2024-12-24  
**Status:** 📋 SPEC (Ready for Implementation)

---

## 1) Purpose

The Event Bus is the **central nervous system** of the UET platform. It enables:
- Real-time UI updates without polling
- Decoupled communication between components
- Audit trail of all system events
- Cache invalidation triggers

---

## 2) Event Types

### 2.1 Simulation Events

| Event | Payload | Trigger |
|-------|---------|---------|
| `SIM_INITIALIZED` | `{ runId, presetId, equations[], seed }` | After SimCore.init(preset) |
| `SIM_STARTED` | `{ runId, timestamp }` | After SimCore.play() |
| `SIM_PAUSED` | `{ runId, step, t }` | After SimCore.pause() |
| `SIM_STEP_COMPLETED` | `{ runId, step, t, dt }` | After each step |
| `SIM_RESET` | `{ runId }` | After SimCore.reset() |
| `SIM_ERROR` | `{ runId, error, traceId }` | On simulation error |

### 2.2 Persistence Events

| Event | Payload | Trigger |
|-------|---------|---------|
| `RUN_SAVED` | `{ runId, projectId }` | After POST /api/runs |
| `RUN_LOADED` | `{ runId }` | After GET /api/runs/:id |
| `SNAPSHOT_CREATED` | `{ runId, snapshotId }` | After snapshot save |
| `TELEMETRY_PERSISTED` | `{ runId, sampleCount }` | After telemetry batch save |

### 2.3 Invariant Events

| Event | Payload | Trigger |
|-------|---------|---------|
| `INVARIANT_PASSED` | `{ invariantId, step }` | Oracle check passed |
| `INVARIANT_FAILED` | `{ invariantId, step, expected, actual }` | Oracle check failed |
| `HEALTH_WARNING` | `{ type, message, step }` | SimulationHealth warning |

### 2.4 UI Events

| Event | Payload | Trigger |
|-------|---------|---------|
| `PANEL_TOGGLED` | `{ panel: 'left'|'right'|'dock', open: boolean }` | Panel show/hide |
| `MODAL_OPENED` | `{ modalId }` | Modal open |
| `MODAL_CLOSED` | `{ modalId }` | Modal close |

---

## 3) Event Bus Interface

```typescript
interface EventBus {
  // Publish event
  emit(event: EventType, payload: unknown): void;
  
  // Subscribe to event
  on(event: EventType, handler: (payload: unknown) => void): () => void;
  
  // Subscribe once
  once(event: EventType, handler: (payload: unknown) => void): void;
  
  // Get event history
  getHistory(filter?: { event?: EventType; runId?: string }): EventLog[];
}
```

---

## 4) Implementation Requirements

### 4.1 Frontend (Zustand/Context)

```typescript
// eventBus.ts
const eventBus = create<EventBusState>((set, get) => ({
  listeners: new Map(),
  history: [],
  
  emit: (event, payload) => {
    const entry = { event, payload, timestamp: Date.now() };
    set(s => ({ history: [...s.history, entry].slice(-1000) }));
    get().listeners.get(event)?.forEach(fn => fn(payload));
  },
  
  on: (event, handler) => {
    // ... subscription logic
  }
}));
```

### 4.2 Backend (SSE Stream)

```
GET /api/events/stream
Content-Type: text/event-stream

data: {"event":"SIM_STEP_COMPLETED","payload":{"runId":"...","step":100}}

data: {"event":"TELEMETRY_PERSISTED","payload":{"runId":"...","sampleCount":50}}
```

---

## 5) Persistence

All events MUST be logged to `EventLog` table:

```prisma
model EventLog {
  id        String   @id @default(cuid())
  eventType String   @map("event_type")
  payload   Json     @default("{}")
  runId     String?  @map("run_id")
  projectId String?  @map("project_id")
  createdAt DateTime @default(now()) @map("created_at")
  
  @@index([runId])
  @@index([eventType])
  @@map("event_logs")
}
```

---

## 6) Traceability

| Layer | Connection |
|-------|------------|
| A (UX) | User actions emit events |
| B (Frontend) | Components subscribe to events |
| C (Backend) | API endpoints emit persistence events |
| D (Engine) | SimCore emits simulation events |
| E (Database) | EventLog persists all events |

---

**Layer:** D — Flow Engine  
**Cross-refs:** [flow_control.md](./flow_control.md), [C_BACKEND/api_contract.md](../C_BACKEND/api_contract.md)
