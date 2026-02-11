# API Contract & Interface Rules
## Layer C — Interface & RPC

**Version:** 1.0  
**Last Updated:** 2025-12-25  
**Layer:** C (Interface)

---

# 1. General Principles

## 1.1 JSON-RPC Style
All endpoints follow a strict Request/Response structure.
-   **Content-Type:** `application/json`
-   **Charset:** `utf-8`

## 1.2 Traceability (Mandatory)
Every request MUST include `x-trace-id` header for end-to-end tracing (A->E).

```http
x-trace-id: [uuid]-[action_id]
```

## 1.3 Standard Error Schema
All error responses must match this schema:

```json
{
  "success": false,
  "error": "Error Message",
  "code": "ERROR_CODE",
  "traceId": "..."
}
```

---

# 2. Endpoints

## 2.1 Graph Persistence

### `POST /api/graphs`
Save a graph layout.

-   **Body:** `NodeGraph` (see Layer D)
-   **Response:** `{ success: true, id: string }`

### `GET /api/graphs?projectId={id}`
Load graphs for a project.

-   **Response:** `{ success: true, data: NodeGraph[] }`

## 2.2 Simulation Runs

### `POST /api/runs`
Create a new simulation run record.

-   **Body:** `{ scenarioId, dt, totalTime, equations: [] }`
-   **Response:** `{ success: true, data: { runId } }`

### `POST /api/runs/{id}/telemetry`
Append telemetry samples to a run.

-   **Body:** `{ history: Sample[] }`
-   **Response:** `{ success: true }`

---

# 3. Validation Rules (Zod)

-   **Graph:** Must contain valid `nodes` and `edges` arrays.
-   **Equations:** Must match `EquationSpec` in Registry.
-   **Trace:** Missing `x-trace-id` will result in `400 Bad Request`.

---

**Status:** ✅ SPEC LOCKED
