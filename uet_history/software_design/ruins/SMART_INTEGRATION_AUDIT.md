# Full System Integration Audit (Smart System)

This report analyzes the alignment between the **Frontend (Smart Simulation UI)** and the **Backend (Next.js API & Prisma Database)**.

## 1. Executive Summary

The current system has a **strong architectural foundation** (Equation-agnostic design, Prisma schema for runs/modules), but suffers from **Implementation Gaps**. Most "Smart" logic currently lives entirely in the browser (Local-only), meaning simulation data is not persisted to the database, and presets are hardcoded.

## 2. Integration Gap Analysis

| Feature | Frontend Status | Backend Status | Alignment Gap |
|---------|-----------------|----------------|---------------|
| **Presets** | Hardcoded in `SimCoreV4.ts` | No preset table in DB | **CRITICAL**: Presets require code redeploy to update. |
| **Run Management** | Local UUID; No POST to API | `Run` table exists | **HIGH**: Runs are not saved to DB. History lost on refresh. |
| **Telemetry** | 200 pts in memory (history) | `TelemetrySample` table ready | **HIGH**: No persistence for high-res simulation data. |
| **Unit Preferences** | LocalStorage (`useUnitSystem`) | No preference table | **MEDIUM**: Preferences don't sync across devices. |
| **Equation Catalog** | `EquationRegistry` (JS) | `EquationModule` table | **MEDIUM**: No sync between JS metadata and DB records. |
| **Simulation Sync** | Local SimCoreV4 (JS) | Batch scripts (Python/JAX) | **LOW**: Dual-engine approach is valid, but results might differ. |

## 3. Detailed Observations

### 3.1 Preset Management
- **Inconsistency**: `SimCoreV4.ts` contains `PRESETS` object with `solarSystem`, `binaryStar`, etc.
- **Risk**: Adding a new project or scenario requires modifying the engine code rather than a user saving a project to the DB.
- **Recommendation**: Create `Preset` model in Prisma and implement `GET /api/registry/presets`.

### 3.2 Run Persistence
- **Discovery**: `SimCoreV4` generates a random UUID on `init()` but never communicates it to `/api/runs`.
- **Impact**: The "Gallery" and "Replay" features are currently disconnected from actual simulation activity.
- **Recommendation**: Implement a `RunService` that calls `POST /api/runs` when "Play" is clicked for the first time.

### 3.3 Unit System Synchronization
- **Discovery**: The `MetricRegistry` exists in DB, but the "Active Units" and "Lens mode" are strictly LocalStorage.
- **Recommendation**: Implement `POST /api/preferences` to save user-specific unit configurations (e.g., "Default everything to UET units").

## 4. Proposed Alignment Roadmap (Priority Order)

### Level 1: Foundation (Data Persistence)
- Implement `POST /api/runs` to register a local run in the DB.
- Implement `POST /api/runs/{id}/samples` to periodically flush `telemetry.history` to the DB.

### Level 2: Smart Registry
- Implement `GET /api/registry/equations` to populate `availableEquations` from the DB catalog.
- Implement `GET /api/registry/presets` to move hardcoded constants to the DB.

### Level 3: User Personalization
- Implement `UserPreference` table to store `useUnitSystem` state globally.

## 5. System Correctness Verification
- [x] Prisma Schema (Run, EquationModule, TelemetrySample) - **READY**
- [ ] API Endpoints (Registry, Preferences) - **MISSING**
- [ ] Frontend-to-Backend Sync Logic - **MISSING**
