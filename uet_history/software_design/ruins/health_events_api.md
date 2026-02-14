# Health and Events API Specification
## Layer C — System Monitoring Endpoints

**Last Updated:** 2024-12-24  
**Status:** 📋 SPEC (Ready for Implementation)

---

## 1) Purpose

Add system monitoring and real-time event streaming endpoints:
- Health check for deployment/monitoring
- Metrics for performance tracking
- SSE stream for real-time UI updates

---

## 2) New Endpoints

### 2.1 GET /api/health

System health check endpoint.

**Request:**
```
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "0.8.5",
  "uptime": 86400,
  "database": "connected",
  "timestamp": "2024-12-24T16:00:00Z",
  "checks": {
    "database": { "status": "ok", "latency": 12 },
    "simCore": { "status": "ok" }
  }
}
```

**Status Codes:**
- `200` — All systems healthy
- `503` — Service degraded (include failing checks)

---

### 2.2 GET /api/events/stream

Server-Sent Events (SSE) for real-time updates.

**Request:**
```
GET /api/events/stream?runId=xxx
Accept: text/event-stream
```

**Response:**
```
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

event: SIM_STEP_COMPLETED
data: {"runId":"abc123","step":100,"t":1.5}

event: TELEMETRY_PERSISTED
data: {"runId":"abc123","sampleCount":50}

event: INVARIANT_FAILED
data: {"invariantId":"energy_conservation","step":150}
```

**Supported Events:**
- `SIM_STARTED`, `SIM_PAUSED`, `SIM_STEP_COMPLETED`, `SIM_RESET`
- `RUN_SAVED`, `SNAPSHOT_CREATED`, `TELEMETRY_PERSISTED`
- `INVARIANT_PASSED`, `INVARIANT_FAILED`, `HEALTH_WARNING`

---

### 2.3 GET /api/events

Get event history for a run.

**Request:**
```
GET /api/events?runId=xxx&limit=100
```

**Response:**
```json
{
  "events": [
    {
      "id": "evt_123",
      "eventType": "SIM_STARTED",
      "payload": { "runId": "abc123" },
      "createdAt": "2024-12-24T16:00:00Z"
    }
  ],
  "total": 250,
  "hasMore": true
}
```

---

### 2.4 POST /api/errors

Log errors with traceId.

**Request:**
```json
{
  "traceId": "550e8400-e29b-41d4-a716-446655440000",
  "errorType": "API_ERROR",
  "message": "Failed to save run",
  "detail": {
    "endpoint": "/api/runs",
    "status": 500
  },
  "runId": "abc123"
}
```

**Response:**
```json
{
  "id": "err_xyz",
  "traceId": "550e8400-e29b-41d4-a716-446655440000",
  "createdAt": "2024-12-24T16:00:00Z"
}
```

---

### 2.5 GET /api/metrics/project/:id

Get project-level metrics.

**Request:**
```
GET /api/metrics/project/proj_123
```

**Response:**
```json
{
  "projectId": "proj_123",
  "totalRuns": 42,
  "totalSteps": 125000,
  "totalSimulationTime": 3600.5,
  "lastRunAt": "2024-12-24T15:30:00Z",
  "errorCount": 3,
  "averageRunDuration": 85.7
}
```

---

## 3) Standard Response Schema

All API responses MUST follow this schema:

### Success Response

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "timestamp": "2024-12-24T16:00:00Z",
    "requestId": "req_abc123"
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "type": "VALIDATION_ERROR",
    "message": "Invalid runId format",
    "traceId": "550e8400-e29b-41d4-a716-446655440000",
    "details": { ... }
  },
  "meta": {
    "timestamp": "2024-12-24T16:00:00Z",
    "requestId": "req_abc123"
  }
}
```

---

## 4) Error Types

| Type | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid input |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | State conflict |
| `INTERNAL_ERROR` | 500 | Server error |
| `SERVICE_UNAVAILABLE` | 503 | Dependency down |

---

## 5) Traceability

| Layer | Responsibility |
|-------|----------------|
| A (UX) | User triggers actions |
| B (Frontend) | Connects to SSE stream |
| C (Backend) | Serves health/events/errors APIs |
| D (Engine) | Emits events to stream |
| E (Database) | Persists logs |

---

**Layer:** C — Backend  
**Cross-refs:** [api_contract.md](./api_contract.md), [D_FLOW_ENGINE/event_bus.md](../D_FLOW_ENGINE/event_bus.md)
