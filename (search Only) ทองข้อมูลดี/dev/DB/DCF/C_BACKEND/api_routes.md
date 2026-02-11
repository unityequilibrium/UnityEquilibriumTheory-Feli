# API Routes Specification
## Layer C - Backend Contract

**Version:** 1.0  
**Last Updated:** 2025-12-25  
**Layer:** C (Backend)

---

## 1. Route Overview

| Route | Method | Purpose | Status |
|-------|--------|---------|--------|
| `/api/registry` | GET | Get metrics & equations | ✅ |
| `/api/runs` | GET/POST | List/create runs | ✅ |
| `/api/runs/[id]` | GET/PUT/DELETE | CRUD single run | ✅ |
| `/api/telemetry` | GET | Get telemetry data | ✅ |
| `/api/notes` | GET/POST | CRUD notes | ✅ |
| `/api/events` | GET | Get event logs | ✅ |
| `/api/errors` | POST | Log errors | ✅ |
| `/api/health` | GET | Health check | ✅ |
| `/api/projects` | GET/POST | List/create projects | ✅ |
| `/api/metrics` | GET | Get metric registry | ✅ |
| `/api/canvas/chat` | POST | AI chat | ✅ |

---

## 2. Registry API

### GET /api/registry

**Response:**
```typescript
{
  metrics: MetricDefinition[];
  equations: EquationModule[];
}
```

---

## 3. Runs API

### GET /api/runs

**Query:**
```
?projectId=string
?limit=number
?offset=number
```

**Response:**
```typescript
{
  runs: Run[];
  total: number;
}
```

### POST /api/runs

**Body:**
```typescript
{
  projectId: string;
  name: string;
  scenarioId: string;
  equations: string[];
  config?: object;
}
```

---

## 4. Telemetry API

### GET /api/telemetry

**Query:**
```
?runId=string (required)
?metricId=string
```

**Response:**
```typescript
{
  samples: TelemetrySample[];
}
```

---

## 5. Notes API

### GET /api/notes

**Query:**
```
?runId=string (required)
```

### POST /api/notes

**Body:**
```typescript
{
  runId: string;
  title: string;
  content: string;
  t?: number;
  step?: number;
}
```

---

## 6. Events API

### GET /api/events

**Query:**
```
?projectId=string
?runId=string
?eventType=string
```

---

## 7. Errors API

### POST /api/errors

**Body:**
```typescript
{
  errorType: string;
  message: string;
  stack?: string;
  projectId?: string;
  runId?: string;
}
```

---

## 8. Health API

### GET /api/health

**Response:**
```typescript
{
  status: 'ok' | 'error';
  database: boolean;
  timestamp: number;
}
```

---

## 9. Projects API

### GET /api/projects

**Response:**
```typescript
{
  projects: Project[];
}
```

### POST /api/projects

**Body:**
```typescript
{
  name: string;
  description?: string;
}
```

---

## 10. Traceability

| This Doc | Links To |
|----------|----------|
| Routes | frontend/src/app/api/* |
| Models | E_DATABASE/schema.md |
| Validation | validation_rules.md |

---

**Status:** ✅ SPEC LOCKED
