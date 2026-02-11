# Telemetry Service Specification
## Layer D - Real-time Node Updates

**Version:** 1.0  
**Last Updated:** 2025-12-25  
**Layer:** D (Flow/Engine)

---

## 1. Purpose

ส่ง real-time updates ของ node status จาก simulation engine ไปยัง Canvas View

---

## 2. Architecture

```
SimCore → TelemetryService → Socket.IO → useTelemetry → CanvasView
                 ↓
            Mock fallback (dev)
```

---

## 3. Events

### Server → Client

| Event | Payload | Purpose |
|-------|---------|---------|
| `telemetry` | `TelemetryEvent` | Node status update |
| `node-patch` | `NodePatch` | Node data change |

### Event Types

```typescript
interface TelemetryEvent {
    nodeId: string;
    status: 'idle' | 'running' | 'blocked' | 'throttled' | 'error';
    trace: {
        lastOutput: unknown;
        latency: number;
    };
    timestamp: number;
}

interface NodePatch {
    nodeId: string;
    path: string;
    value: unknown;
}
```

---

## 4. Connection

| Config | Value |
|--------|-------|
| Protocol | WebSocket |
| Default URL | `ws://localhost:3001` |
| Transport | websocket |
| Reconnection | true |
| Max attempts | 5 |

---

## 5. Mock Mode (Development)

เมื่อไม่มี server:

```typescript
startMockTelemetry(nodeIds, intervalMs = 800)
```

Behavior:
- Cycle nodes through: `idle → running → running → running → idle`
- Random values for lastOutput
- Random latency 0-10ms

---

## 6. Budget Integration

```typescript
// Report to budgetManager
budgetManager.reportExecution(nodeId, cpuMs, gpuMs);

// Check throttle
if (budgetManager.shouldThrottle(nodeId)) {
    skip telemetry;
}
```

---

## 7. Determinism

> **WARNING**: Telemetry is READ-ONLY

| ✅ Allowed | ❌ Forbidden |
|-----------|-------------|
| Read node status | Modify simulation state |
| Display metrics | Affect calculation |
| Log events | Change seed |

---

## 8. Traceability

| This Doc | Links To |
|----------|----------|
| TelemetryEvent | D_FLOW_ENGINE/node_contract.md TraceHooks |
| Budget | D_FLOW_ENGINE/node_canvas_architecture.md §6 |
| Implementation | frontend/src/lib/telemetryService.ts |
| Hook | frontend/src/hooks/useTelemetry.ts |

---

**Status:** ✅ SPEC LOCKED
