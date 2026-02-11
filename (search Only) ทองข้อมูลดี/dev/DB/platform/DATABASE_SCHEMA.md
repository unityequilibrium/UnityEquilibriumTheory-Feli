# Database Schema Reference

> **Related Documents:**
> - [SMART_DATA_DICTIONARY](SMART_DATA_DICTIONARY.md) ← Metric Definitions
> - [SMART_INDEX](design_system/SMART_INDEX.md) ← Smart System Master
> - [API_REFERENCE](API_REFERENCE.md) ← REST API

> Complete reference for all database tables and relationships  
> **Last Updated: 2024-12-24** (Smart System Integration)

---

## Quick Reference

| Table | Primary Purpose | Key Relations | Status |
|-------|-----------------|---------------|--------|
| `users` | User accounts | → projects, runs | ✅ |
| `projects` | Workspaces | → runs | ✅ |
| `unit_modes` | Unit display modes | → runs | ✅ |
| `equation_modules` | Physics equations | ↔ runs (N:M) | ✅ |
| `runs` | Simulation instances | → snapshots, telemetry, notes | ✅ |
| `run_equations` | Run↔Equation join | FK to runs, modules | ✅ |
| `snapshots` | Checkpoint states | ← runs | ✅ |
| `telemetry_samples` | Time series data | ← runs | ✅ |
| `metric_registry` | Metric definitions | (standalone) | ✅ |
| `notes` | Run annotations | ← runs | ✅ **NEW** |
| `event_logs` | Event Bus persistence | (standalone) | ✅ **NEW** |
| `error_logs` | Error tracking | (standalone) | ✅ **NEW** |

---

## Table: `users`

```sql
CREATE TABLE users (
    id          TEXT PRIMARY KEY,
    email       TEXT UNIQUE NOT NULL,
    name        TEXT,
    created_at  TIMESTAMP DEFAULT NOW(),
    updated_at  TIMESTAMP
);
```

---

## Table: `projects`

```sql
CREATE TABLE projects (
    id          TEXT PRIMARY KEY,
    owner_id    TEXT REFERENCES users(id) ON DELETE CASCADE,
    name        TEXT NOT NULL,
    slug        TEXT UNIQUE NOT NULL,
    config      JSONB DEFAULT '{}',
    created_at  TIMESTAMP DEFAULT NOW(),
    updated_at  TIMESTAMP
);

CREATE INDEX idx_projects_owner ON projects(owner_id);
```

---

## Table: `runs` ⭐ (Core Table)

```sql
CREATE TABLE runs (
    id                TEXT PRIMARY KEY,
    project_id        TEXT REFERENCES projects(id) ON DELETE CASCADE,
    user_id           TEXT REFERENCES users(id),
    unit_mode_id      TEXT REFERENCES unit_modes(id),
    name              TEXT NOT NULL,
    seed              BIGINT,
    status            TEXT DEFAULT 'running',  -- running, paused, completed, failed
    duration_ms       BIGINT,
    total_steps       BIGINT,
    equation_version  TEXT,
    container_hash    TEXT,
    metadata          JSONB DEFAULT '{}',
    started_at        TIMESTAMP,
    ended_at          TIMESTAMP,               -- ✅ ADDED in Phase 1
    created_at        TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_runs_project ON runs(project_id);
CREATE INDEX idx_runs_user ON runs(user_id);
CREATE INDEX idx_runs_unit_mode ON runs(unit_mode_id);
```

---

## Table: `notes` ✅ NEW (Phase 1)

```sql
CREATE TABLE notes (
    id          TEXT PRIMARY KEY,
    run_id      TEXT REFERENCES runs(id) ON DELETE CASCADE,
    title       TEXT NOT NULL,
    content     TEXT NOT NULL,
    t           DECIMAL,                    -- simulation time reference
    step        BIGINT,                     -- step reference
    created_at  TIMESTAMP DEFAULT NOW(),
    updated_at  TIMESTAMP
);

CREATE INDEX idx_notes_run ON notes(run_id);
```

**Purpose:** Store annotations/notes for runs separately from metadata.

---

## Table: `event_logs` ✅ NEW (Phase 1)

```sql
CREATE TABLE event_logs (
    id          TEXT PRIMARY KEY,
    event_type  TEXT NOT NULL,              -- 'RUN_CREATED', 'RUN_COMPLETED', etc.
    actor_type  TEXT NOT NULL,              -- 'user', 'system', 'simulation'
    actor_id    TEXT,
    project_id  TEXT,
    run_id      TEXT,
    payload     JSONB DEFAULT '{}',
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_event_logs_project ON event_logs(project_id);
CREATE INDEX idx_event_logs_run ON event_logs(run_id);
CREATE INDEX idx_event_logs_type ON event_logs(event_type);
```

**Purpose:** Persist important events from Event Bus for audit trail.

**Event Types:**
- `RUN_CREATED`, `RUN_STARTED`, `RUN_COMPLETED`, `RUN_FAILED`
- `INVARIANT_FAILED`, `SNAPSHOT_SAVED`, `ERROR_OCCURRED`

---

## Table: `error_logs` ✅ NEW (Phase 1)

```sql
CREATE TABLE error_logs (
    id          TEXT PRIMARY KEY,
    error_type  TEXT NOT NULL,              -- 'SIMULATION_ERROR', 'INVARIANT_VIOLATION', etc.
    message     TEXT NOT NULL,
    stack       TEXT,
    detail      JSONB,
    project_id  TEXT,
    run_id      TEXT,
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_error_logs_project ON error_logs(project_id);
CREATE INDEX idx_error_logs_type ON error_logs(error_type);
```

**Error Types:**
- `SIMULATION_ERROR` - NaN/Inf detected
- `INVARIANT_VIOLATION` - Physics conservation broken
- `PERSISTENCE_ERROR` - DB/API failed
- `VALIDATION_ERROR` - Invalid input
- `SYSTEM_ERROR` - Unknown errors

---

## Table: `snapshots`

```sql
CREATE TABLE snapshots (
    id            TEXT PRIMARY KEY,
    run_id        TEXT REFERENCES runs(id) ON DELETE CASCADE,
    t             DECIMAL NOT NULL,
    step          BIGINT NOT NULL,
    hash          TEXT NOT NULL,      -- SHA256 of state
    state_json    JSONB,              -- Full world state
    is_checkpoint BOOLEAN DEFAULT FALSE,
    metadata      JSONB DEFAULT '{}',
    created_at    TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_snapshots_run ON snapshots(run_id);
CREATE INDEX idx_snapshots_run_t ON snapshots(run_id, t);
```

---

## Table: `telemetry_samples`

```sql
CREATE TABLE telemetry_samples (
    id          TEXT PRIMARY KEY,
    run_id      TEXT REFERENCES runs(id) ON DELETE CASCADE,
    t           DECIMAL NOT NULL,
    step        BIGINT NOT NULL,
    metric_id   TEXT NOT NULL,       -- 'total_energy', 'kinetic_energy', etc.
    value       DECIMAL NOT NULL,
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_telemetry_run_step ON telemetry_samples(run_id, step);
CREATE INDEX idx_telemetry_run_metric ON telemetry_samples(run_id, metric_id);
```

---

## Migration History

```
migrations/
├── 20241223_initial/
│   └── migration.sql
└── 20241223_add_production_tables/    ✅ NEW
    └── migration.sql                   (added EventLog, ErrorLog, Note, endedAt)
```

**Commands:**
```bash
# Generate from schema
npx prisma migrate dev --name <name>

# Apply migrations
npx prisma migrate deploy

# Reset (DESTROYS DATA)
npx prisma migrate reset
```

---

## Phase 1 Changes Summary

| Change | Status |
|--------|--------|
| Add `ended_at` to `runs` | ✅ DONE |
| Create `notes` table | ✅ DONE |
| Create `event_logs` table | ✅ DONE |
| Create `error_logs` table | ✅ DONE |

---

**Document Version:** 2.0  
**Last Updated:** 2024-12-23

