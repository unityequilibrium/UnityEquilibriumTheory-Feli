# Schema
## Layer E — Database Tables

---

## 📊 Tables Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      PostgreSQL                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│   │   projects   │───▶│     runs     │───▶│  telemetry   │  │
│   └──────────────┘    └──────────────┘    └──────────────┘  │
│                              │                               │
│                              ▼                               │
│                       ┌──────────────┐                       │
│                       │    notes     │                       │
│                       └──────────────┘                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Table Definitions

### projects

| Column | Type | Purpose |
|--------|------|---------|
| id | uuid | Primary key |
| name | varchar(255) | Project name |
| description | text | Description |
| isPublic | boolean | Visibility |
| createdAt | timestamp | Created |
| updatedAt | timestamp | Last update |

### runs

| Column | Type | Purpose |
|--------|------|---------|
| id | uuid | Primary key |
| projectId | uuid | FK to projects |
| scenarioId | varchar | Room/scenario |
| runName | varchar(255) | Name |
| worldState | jsonb | Simulation state |
| equations | jsonb | Equation config |
| createdAt | timestamp | Created |
| updatedAt | timestamp | Last update |

### telemetry_samples

> **Note:** Table uses normalized structure (one row per metric per step) for efficient querying.

| Column | Type | Purpose | Prisma Type |
|--------|------|---------|-------------|
| id | cuid | Primary key | String @id |
| run_id | cuid | FK to runs | String |
| t | decimal | Simulation time | Decimal |
| step | bigint | Step number | BigInt |
| metric_id | varchar | Metric identifier | String |
| value | decimal | Metric value | Decimal |
| created_at | timestamp | Created | DateTime |

**Indexes:**
- `(run_id, step)` — Query by run and step
- `(run_id, metric_id)` — Query by run and metric

**Difference from old schema:**
- Old: `metrics: jsonb` (all metrics in one row)
- New: Normalized (one row per metric for flexibility)

### notes

| Column | Type | Purpose |
|--------|------|---------|
| id | uuid | Primary key |
| runId | uuid | FK to runs |
| content | text | Note text |
| createdAt | timestamp | Created |
| updatedAt | timestamp | Updated |

### node_graphs

> **Reference:** Architecture v2.0 "Universal Node Protocol"

| Column | Type | Purpose | Validation |
|--------|------|---------|------------|
| id | uuid | Primary key | cuid() |
| projectId | uuid | FK to projects | - |
| name | varchar(255) | Graph name | min(1) |
| layout | jsonb | Graph State | Must match `NodeGraph` spec |
| createdAt | timestamp | Created | - |
| updatedAt | timestamp | Last update | - |

**Structure of `layout`:**
```json
{
  "nodes": [ { "id": "...", "type": "...", "data": { ... } } ],
  "edges": [ { "id": "...", "source": "...", "target": "..." } ]
}
```
 
---

# 4. Persistence Policy

## 4.1 Snapshot vs Replay

-   **Snapshot (Graph):** Saves the *structure* (nodes/edges).
    -   Use for: Templates, Restore Points.
    -   Table: `NodeGraph`
-   **Replay (Run):** Saves the *execution* (seed/inputs).
    -   Use for: Reproducibility, Shareable Links.
    -   Table: `Run` + `Sample`

## 4.2 Minimal Viable Store

We only store what is needed to reconstruct the state (Determinism R4).

-   ✅ **Store:** Seed, Inputs, Eq Params.
-   ❌ **Do Not Store:** Computed Intermediates (positions of 10k particles) unless recording telemetry.

---

**Status:** ✅ SPEC LOCKED
**Source:** [DATABASE_SCHEMA.md](../../platform/DATABASE_SCHEMA.md)  
**Layer:** E — Database/Persistence
