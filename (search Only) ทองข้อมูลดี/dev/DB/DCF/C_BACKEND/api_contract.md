# API Contract
## Layer C — All API Endpoints

---

## 📡 Endpoints Summary

### Runs API

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| GET | /api/runs | List all runs | No |
| POST | /api/runs | Create new run | No |
| GET | /api/runs/[id] | Get single run | No |
| PATCH | /api/runs/[id] | Update run | No |
| DELETE | /api/runs/[id] | Delete run | No |

### Telemetry API

| Method | Endpoint | Purpose | Auth | Required Headers |
|--------|----------|---------|------|------------------|
| POST | /api/runs/[id]/telemetry | Save telemetry history | No | x-trace-id |
| GET | /api/runs/[id]/telemetry | Get telemetry data | No | x-trace-id |

#### POST /api/runs/[id]/telemetry

**Request:**
```json
{
  "history": [
    {
      "t": 1.5,
      "step": 100,
      "values": {
        "energy_total": 123.45,
        "momentum_total": 0.001
      }
    }
  ]
}
```

**Response (201):**
```json
{
  "runId": "cmj...",
  "samplesAdded": 5
}
```

**Required Headers:**
- `x-trace-id`: UUID for audit trail (Extreme Audit compliance)

---

#### GET /api/runs/[id]/telemetry

**Required Headers:**
- `x-trace-id`: Mandatory for all telemetry access.

**Response (200):**
Returns raw telemetry samples. Grouping/formatting for Plotly is handled in Layer B.
```json
{
  "runId": "...",
  "samples": [
    { "t": 0.1, "step": "0", "metricId": "energy", "value": 1.0 }
  ]
}
```

### Projects API

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| GET | /api/projects | List projects | No |
| POST | /api/projects | Create project | No |
| GET | /api/projects/[id] | Get project | No |
| PATCH | /api/projects/[id] | Update project | No |
| DELETE | /api/projects/[id] | Delete project | No |

### Notes API

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| GET | /api/notes | List notes | No |
| POST | /api/notes | Create note | No |
| PATCH | /api/notes/[id] | Update note | No |
| DELETE | /api/notes/[id] | Delete note | No |

### AI API

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| POST | /api/ai/chat | Chat with AI | No |
| POST | /api/ai/oracle | Query Oracle | No |

---

## 🛡️ Validation & Error Semantics (DCF Rules)

Every C-Layer request MUST adhere to the following audit rules:

### 1. Mandatory Traceability
- **Header:** `x-trace-id` (UUID v4)
- **Violation:** `403 Forbidden` + `ERR_C1_NO_TRACE`

### 2. Error Code Schema
All errors return a standard JSON body:
```json
{
  "error": "Short description",
  "code": "ERR_[LAYER]_[CODE]",
  "traceId": "uuid-..."
}
```

| Code | Layer | Meaning |
|:---|:---|:---|
| `ERR_C1_AUTH` | Interface | Unauthorized access attempt |
| `ERR_C2_VALIDATION` | Interface | Schema validation failed |
| `ERR_D4_STABILITY` | Engine | Physical simulation instability |
| `ERR_D5_DETERMINISM` | Engine | Determinism check failed (R4.1) |
| `ERR_E6_PERSISTENCE` | Database | Failed to commit to DB (E-Layer) |

### 3. Rate Limiting
- **Telemetry:** 1000 requests/min per traceId.
- **AI Chat:** 50 requests/min per traceId.

---

## 🔗 Full Details

See [API_REFERENCE.md](../../platform/API_REFERENCE.md)

---

**Layer:** C — Backend Contract
