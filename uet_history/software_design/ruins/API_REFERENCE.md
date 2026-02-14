# API Reference

> **Related Documents:**
> - [SMART_INDEX](design_system/SMART_INDEX.md) ← Smart System Master
> - [SMART_DATA_DICTIONARY](SMART_DATA_DICTIONARY.md) ← Metric Definitions
> - [DATABASE_SCHEMA](DATABASE_SCHEMA.md) ← Table Structures
> - [BACKEND_ARCHITECTURE](BACKEND_ARCHITECTURE.md) ← Server Design

> Complete REST API documentation for UET Lab platform  
> **Last Updated: 2024-12-24** (Smart System Integration)

---

## Base URL

```
Development: http://localhost:3000/api
Production:  https://uet-lab.example.com/api
```

---

## Authentication

> ⚠️ Currently using hardcoded demo credentials

```typescript
const DEFAULT_PROJECT_ID = 'default_project';
const DEFAULT_USER_ID = 'demo_user';
```

**TODO (Phase 4):** Implement proper JWT authentication

---

## Standard Response Schema ✅ NEW (Phase 1)

All API responses follow this format:

**Success:**
```json
{
    "success": true,
    "data": {...},
    "meta": {
        "timestamp": "2024-12-23T12:00:00.000Z"
    }
}
```

**Error:**
```json
{
    "success": false,
    "error": {
        "id": "err_abc123",
        "type": "VALIDATION_ERROR",
        "message": "scenarioName is required"
    },
    "meta": {
        "timestamp": "2024-12-23T12:00:00.000Z"
    }
}
```

**Error Types:** `VALIDATION_ERROR` | `NOT_FOUND` | `PERMISSION_DENIED` | `SIMULATION_ERROR` | `INVARIANT_VIOLATION` | `PERSISTENCE_ERROR` | `SYSTEM_ERROR`

---

## Endpoints Overview

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/runs` | Create new run | ✅ |
| GET | `/runs` | List runs | ✅ |
| GET | `/runs/{id}` | Get single run | ✅ |
| PATCH | `/runs/{id}` | Update run | ✅ |
| DELETE | `/runs/{id}` | Delete run | ✅ |
| POST | `/telemetry` | Batch insert samples | ✅ |
| GET | `/telemetry` | Query time series | ✅ |
| GET | `/notes` | List notes for run | ✅ |
| POST | `/notes` | Create note | ✅ |
| PUT | `/notes/{id}` | Update note | ✅ |
| DELETE | `/notes/{id}` | Delete note | ✅ |
| **POST** | `/events` | Batch persist events | ✅ |
| **GET** | `/events` | Query event history | ✅ |
| **POST** | `/errors` | Log an error | ✅ |
| **GET** | `/errors` | Query error history | ✅ |
| **GET** | `/health` | System health check | ✅ |
| **HEAD** | `/health` | Simple alive check | ✅ |
| **GET** | `/metrics` | Application metrics | ✅ |
| **GET** | `/registry` | Get all metric definitions | ✅ **SMART** |
| **GET** | `/registry/{id}` | Get single metric | ✅ **SMART** |
| **GET** | `/equations` | List all equations | ✅ **SMART** |
| **GET** | `/equations/{id}` | Get equation details | ✅ **SMART** |
| **GET** | `/preferences` | Get user unit preferences | ✅ **SMART** |
| **PUT** | `/preferences` | Update unit preferences | ✅ **SMART** |

---

## Runs API

### Create Run

```http
POST /api/runs
Content-Type: application/json
```

**Request:**
```json
{
    "scenarioId": "kepler_2body_circular",
    "scenarioName": "Kepler 2-Body Circular",
    "gate": "G2",
    "seed": 12345,
    "dt": 0.01,
    "totalTime": 100,
    "equations": [
        { "id": "newtonian", "role": "driver", "enabled": true },
        { "id": "uet", "role": "observer", "enabled": false }
    ]
}
```

**Response (201):**
```json
{
    "success": true,
    "runId": "clq1234abcd",
    "message": "Run created successfully"
}
```

**Error (500):**
```json
{
    "success": false,
    "error": "Failed to create run"
}
```

---

### List Runs

```http
GET /api/runs?limit=50&status=completed&gate=G2
```

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| limit | int | 50 | Max results |
| status | string | - | Filter by status |
| gate | string | - | Filter by test gate |

**Response (200):**
```json
{
    "success": true,
    "runs": [
        {
            "id": "clq1234abcd",
            "name": "Kepler Test",
            "seed": "12345",
            "status": "completed",
            "durationMs": "5230",
            "totalSteps": "10000",
            "metadata": { "gate": "G2" },
            "equations": [
                { "moduleId": "newtonian", "role": "driver", "enabled": true }
            ],
            "snapshots": [
                { "t": "100.0", "step": "10000" }
            ],
            "createdAt": "2024-12-23T12:00:00Z"
        }
    ],
    "count": 1
}
```

---

### Get Single Run

```http
GET /api/runs/{id}
```

**Response (200):**
```json
{
    "success": true,
    "run": {
        "id": "clq1234abcd",
        "name": "Kepler Test",
        "seed": "12345",
        "status": "completed",
        "metadata": {...},
        "equations": [...],
        "snapshots": [
            {
                "id": "snap123",
                "t": "50.0",
                "step": "5000",
                "stateJson": {...}
            }
        ]
    }
}
```

---

### Update Run

```http
PATCH /api/runs/{id}
Content-Type: application/json
```

**Request:**
```json
{
    "status": "completed",
    "durationMs": 5230,
    "totalSteps": 10000,
    "metadata": {
        "gate": "G2",
        "scenarioId": "kepler_2body_circular",
        "failureReason": null,
        "invariantReports": [...]
    },
    "counterexample": {
        "t": 50.5,
        "step": 5050,
        "bodies": [...],
        "seed": 12345,
        "params": { "G": 1 }
    }
}
```

**Response (200):**
```json
{
    "success": true,
    "message": "Run updated successfully"
}
```

---

## Telemetry API

### Batch Insert Samples

```http
POST /api/telemetry
Content-Type: application/json
```

**Request:**
```json
{
    "samples": [
        {
            "runId": "clq1234abcd",
            "t": 1.0,
            "step": 100,
            "metricId": "total_energy",
            "value": -2534.11
        },
        {
            "runId": "clq1234abcd",
            "t": 1.0,
            "step": 100,
            "metricId": "kinetic_energy",
            "value": 2483.85
        }
    ]
}
```

**Response (200):**
```json
{
    "success": true,
    "inserted": 2
}
```

---

### Query Time Series

```http
GET /api/telemetry?runId=clq1234abcd&metricId=total_energy&limit=1000
```

**Query Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| runId | string | ✅ | Run ID |
| metricId | string | ❌ | Filter by metric |
| limit | int | ❌ | Max samples (default: 1000) |

**Response (200):**
```json
{
    "runId": "clq1234abcd",
    "metrics": {
        "total_energy": [
            { "t": 1.0, "step": 100, "value": -2534.11 },
            { "t": 2.0, "step": 200, "value": -2534.09 }
        ],
        "kinetic_energy": [
            { "t": 1.0, "step": 100, "value": 2483.85 },
            { "t": 2.0, "step": 200, "value": 2483.90 }
        ]
    }
}
```

---

## Notes API

### List Notes

```http
GET /api/notes?runId=clq1234abcd
```

**Response (200):**
```json
{
    "notes": [
        {
            "id": "note123",
            "runId": "clq1234abcd",
            "title": "Observation",
            "content": "Energy drift is minimal",
            "createdAt": "2024-12-23T12:30:00Z",
            "updatedAt": "2024-12-23T12:30:00Z"
        }
    ]
}
```

---

### Create Note

```http
POST /api/notes
Content-Type: application/json
```

**Request:**
```json
{
    "runId": "clq1234abcd",
    "id": "note123",
    "title": "Observation",
    "content": "Energy drift is minimal",
    "createdAt": "2024-12-23T12:30:00Z",
    "updatedAt": "2024-12-23T12:30:00Z"
}
```

**Response (200):**
```json
{
    "success": true,
    "note": {...}
}
```

---

### Update Note

```http
PUT /api/notes/{id}
Content-Type: application/json
```

**Request:**
```json
{
    "runId": "clq1234abcd",
    "title": "Updated Title",
    "content": "Updated content",
    "updatedAt": "2024-12-23T12:35:00Z"
}
```

---

### Delete Note

```http
DELETE /api/notes/{id}?runId=clq1234abcd
```

**Response (200):**
```json
{
    "success": true
}
```

---

## Events API ✅ NEW (Phase 1)

### Batch Persist Events

```http
POST /api/events
Content-Type: application/json
```

**Request:**
```json
{
    "events": [
        {
            "id": "evt_abc123",
            "type": "RUN_CREATED",
            "actorType": "user",
            "actorId": "demo_user",
            "projectId": "default_project",
            "runId": "clq1234abcd",
            "payload": { "name": "Solar System Test" },
            "timestamp": 1703318400000
        }
    ]
}
```

**Response (200):**
```json
{
    "success": true,
    "data": {
        "inserted": 1,
        "message": "Persisted 1 events"
    }
}
```

---

### Query Event History

```http
GET /api/events?runId=clq1234abcd&type=RUN_CREATED&limit=100
```

**Query Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| runId | string | ❌ | Filter by run |
| projectId | string | ❌ | Filter by project |
| type | string | ❌ | Filter by event type |
| limit | int | ❌ | Max results (default: 100) |

**Response (200):**
```json
{
    "success": true,
    "data": {
        "events": [...],
        "count": 10
    }
}
```

---

## Errors API ✅ NEW (Phase 1)

### Log an Error

```http
POST /api/errors
Content-Type: application/json
```

**Request:**
```json
{
    "type": "SIMULATION_ERROR",
    "message": "NaN detected in velocity calculation",
    "stack": "Error: NaN detected...",
    "context": {
        "runId": "clq1234abcd",
        "projectId": "default_project",
        "component": "SimCore",
        "action": "step"
    }
}
```

**Response (200):**
```json
{
    "success": true,
    "data": {
        "id": "errlog_xyz789",
        "message": "Error logged successfully"
    }
}
```

---

### Query Error History

```http
GET /api/errors?runId=clq1234abcd&type=SIMULATION_ERROR&limit=50
```

**Query Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| runId | string | ❌ | Filter by run |
| projectId | string | ❌ | Filter by project |
| type | string | ❌ | Filter by error type |
| limit | int | ❌ | Max results (default: 50) |

**Response (200):**
```json
{
    "success": true,
    "data": {
        "errors": [...],
        "count": 5
    }
}
```

---

## Error Responses

All endpoints return errors using the Standard Response Schema:

```json
{
    "success": false,
    "error": {
        "id": "err_abc123",
        "type": "VALIDATION_ERROR",
        "message": "Description of what went wrong"
    },
    "meta": {
        "timestamp": "2024-12-23T12:00:00.000Z"
    }
}
```

| Status Code | Error Type | Meaning |
|-------------|------------|---------|
| 400 | VALIDATION_ERROR | Missing/invalid parameters |
| 404 | NOT_FOUND | Resource doesn't exist |
| 403 | PERMISSION_DENIED | Not authorized |
| 500 | SYSTEM_ERROR | Internal server error |

---

## Rate Limits

> ⚠️ Not implemented yet (Phase 5)

Recommended limits:
- `/telemetry` POST: 100 req/min (batch of 1000 samples each)
- `/events` POST: 60 req/min
- All other endpoints: 60 req/min

---

## Health API ✅ (Phase 5)

### System Health Check

```http
GET /api/health
GET /api/health?detailed=true
```

**Response (200):**
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

**Status Values:**
| Status | HTTP Code | Meaning |
|--------|-----------|---------|
| `healthy` | 200 | All checks pass |
| `degraded` | 200 | Some checks warn |
| `unhealthy` | 503 | Critical check failed |

### Simple Alive Check

```http
HEAD /api/health
```

**Response:** 200 if alive, 503 if database unavailable

---

## Metrics API ✅ (Phase 5)

### Application Metrics

```http
GET /api/metrics
```

**Response (200):**
```json
{
    "success": true,
    "data": {
        "timestamp": "2024-12-23T12:00:00.000Z",
        "uptime": 3600,
        "database": {
            "runs": { "count": 123, "lastCreated": "2024-12-23T11:00:00.000Z" },
            "snapshots": { "count": 456 },
            "telemetry": { "count": 78900 },
            "events": { "count": 234 },
            "errors": { "count": 12 }
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

---

## Changes Summary

| Phase | Change | Status |
|-------|--------|--------|
| Phase 1 | Standard Response Schema | ✅ DONE |
| Phase 1 | `/api/events` POST/GET | ✅ DONE |
| Phase 1 | `/api/errors` POST/GET | ✅ DONE |
| Phase 5 | `/api/health` GET/HEAD | ✅ DONE |
| Phase 5 | `/api/metrics` GET | ✅ DONE |

---

**Document Version:** 3.0  
**Last Updated:** 2024-12-23  
**Status:** Phase 1-5 Complete ✅


