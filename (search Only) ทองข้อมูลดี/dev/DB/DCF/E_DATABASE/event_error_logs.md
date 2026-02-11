# Event and Error Log Schema
## Layer E — Persistence for Logging

**Last Updated:** 2024-12-24  
**Status:** 📋 SPEC (Ready for Implementation)

---

## 1) Purpose

Add logging tables to support:
- Event Bus persistence
- Error tracking with traceId
- Audit trail for debugging and replay

---

## 2) New Tables

### 2.1 EventLog

Stores all events emitted by the Event Bus.

```prisma
model EventLog {
  id        String   @id @default(cuid())
  
  // Event identification
  eventType String   @map("event_type")  // e.g., "SIM_STARTED", "RUN_SAVED"
  payload   Json     @default("{}")       // Event-specific data
  
  // Context
  projectId String?  @map("project_id")
  runId     String?  @map("run_id")
  userId    String?  @map("user_id")
  
  // Actor
  actorType String   @default("system") @map("actor_type")  // 'user' | 'system'
  actorId   String?  @map("actor_id")
  
  // Timestamp
  createdAt DateTime @default(now()) @map("created_at")
  
  // Relations
  project   Project? @relation(fields: [projectId], references: [id])
  run       Run?     @relation(fields: [runId], references: [id])
  
  @@index([projectId])
  @@index([runId])
  @@index([eventType])
  @@index([createdAt])
  @@map("event_logs")
}
```

### 2.2 ErrorLog

Stores all errors with traceId for debugging.

```prisma
model ErrorLog {
  id        String   @id @default(cuid())
  
  // Error identification
  traceId   String   @map("trace_id")     // UUID from ErrorService
  errorType String   @map("error_type")   // e.g., "API_ERROR", "ENGINE_ERROR"
  message   String                         // Human-readable message
  
  // Details
  stack     String?                        // Stack trace
  detail    Json?                          // Additional context
  
  // Context
  projectId String?  @map("project_id")
  runId     String?  @map("run_id")
  endpoint  String?                        // API endpoint if applicable
  
  // Severity
  severity  String   @default("error")     // 'warning' | 'error' | 'critical'
  
  // Timestamp
  createdAt DateTime @default(now()) @map("created_at")
  
  // Relations
  project   Project? @relation(fields: [projectId], references: [id])
  run       Run?     @relation(fields: [runId], references: [id])
  
  @@index([traceId])
  @@index([projectId])
  @@index([runId])
  @@index([errorType])
  @@index([createdAt])
  @@map("error_logs")
}
```

---

## 3) Relation Updates

Add to existing models:

```prisma
// In Project model, add:
model Project {
  // ... existing fields
  eventLogs  EventLog[]
  errorLogs  ErrorLog[]
}

// In Run model, add:
model Run {
  // ... existing fields
  eventLogs  EventLog[]
  errorLogs  ErrorLog[]
}
```

---

## 4) Query Patterns

### 4.1 Get Events for a Run

```sql
SELECT * FROM event_logs 
WHERE run_id = ? 
ORDER BY created_at DESC 
LIMIT 100;
```

### 4.2 Get Errors by TraceId

```sql
SELECT * FROM error_logs 
WHERE trace_id = ?;
```

### 4.3 Get Recent Errors

```sql
SELECT * FROM error_logs 
WHERE project_id = ? 
AND created_at > NOW() - INTERVAL '24 hours'
ORDER BY created_at DESC;
```

---

## 5) Retention Policy

| Log Type | Retention | Reason |
|----------|-----------|--------|
| EventLog | 30 days | Debugging + audit |
| ErrorLog | 90 days | Support + debugging |

Implement cleanup job:
```sql
DELETE FROM event_logs WHERE created_at < NOW() - INTERVAL '30 days';
DELETE FROM error_logs WHERE created_at < NOW() - INTERVAL '90 days';
```

---

## 6) Traceability

| Layer | Responsibility |
|-------|----------------|
| B (Frontend) | ErrorService generates traceId |
| C (Backend) | POST /api/errors persists to ErrorLog |
| D (Engine) | Event Bus emits events |
| E (Database) | EventLog/ErrorLog persist all data |

---

**Layer:** E — Database  
**Cross-refs:** [D_FLOW_ENGINE/event_bus.md](../D_FLOW_ENGINE/event_bus.md), [schema.md](./schema.md)
