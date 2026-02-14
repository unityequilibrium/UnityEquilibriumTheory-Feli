# Master System Integration & Alignment Report

**Status:** 🟠 PARTIALLY DECOUPLED
**Date:** 2025-12-24
**Scope:** Frontend (React/Zustand), Backend (Next.js/Prisma), Database (PostgreSQL), Scripts (Python/JAX)

## 1. System-Wide Audit Summary

The Smart System is currently composed of three highly functional but **disconnected** islands. While each layer is architecturally sound, they do not share data effectively, leading to "Ephemeral Runs" (frontend) and "Invisible Batch Data" (scripts).

| Layer | Primary Driver | Storage Type | Interaction Mode |
|-------|----------------|--------------|------------------|
| **Interactive UI** | `SimCoreV4` (JS) | In-Memory / LocalStorage | Ephemeral (Lost on refresh) |
| **Data Platform** | Next.js API | PostgreSQL (Prisma) | Inert (Tables exist but are empty) |
| **Research Engine** | Python Scripts | CSV / JSON (Filesystem) | Offline (Not accessible via UI) |

## 2. Component-Level Gaps

### 2.1 Frontend ↔ Database Disconnect
- **Hardcoded Registries**: `ROOMS` and `METRICS` are hardcoded in `src/registries/`. The database tables `MetricRegistry` and `EquationModule` are essentially redundant right now.
- **Run Persistence**: There is no "Save" or "Auto-Save" logic in `SimCoreV4`. Every "Play" creates a new local UUID that is never synced to the `/api/runs` table.
- **Project Configuration**: The Gallery loads "Project Cards," but editing them only updates local state, not the Prisma `Project` table.

### 2.2 Scripts ↔ Web Implementation Gap
- **Ledger Incompatibility**: Python scripts produce `dt_ladder_ledger.csv`. The web `/api/metrics` endpoint expects to read from PostgreSQL. 
- **In-Browser vs Offline Physics**: `SimCoreV4` JS results may diverge slightly from `run_uet_jax.py` due to floating-point differences or integrator implementations. There is no "Drift Verification" between the two.

### 2.3 Feature "Dead Zones"
- **Gallery Replay**: The Gallery feature is designed to replay runs, but because frontend runs aren't saved to SQL, the Gallery only shows static "Demo Cards."
- **Export System**: The "Export to JSON" feature is implemented in the UI, but there is no corresponding "Import from JSON" to re-instantiate a simulation state.

## 3. Recommended Convergence Roadmap

### Phase 1: The Persistence Bridge (Immediate)
1.  **Sync SimCore to API**: Update `SimCoreV4.init()` and `SimCoreV4.step()` (sampled) to send data to `POST /api/runs`.
2.  **Telemetry Flush**: Implement a background service that flushes the 200 Telemetry points from memory to the `TelemetrySample` table.

### Phase 2: Dynamic Catalog (Standardization)
1.  **Unified Registry API**: Create a single `GET /api/registry` that returns combined data from `MetricRegistry` and `EquationModule` tables.
2.  **API-Driven UI**: Replace hardcoded `ROOMS` in the frontend with a fetch-on-boot from the API.

### Phase 3: Offline-to-Online Loop (Advanced)
1.  **Ingestion Tool**: Create a Python script or API route to import `dt_ladder_ledger.csv` files into the Prisma DB so that batch research results appear in the web Dashboard.
2.  **Cross-Library Verification**: Automate a "Kepler Check" between JS and Python outputs to ensure physics consistency across platforms.

## 4. Specific File Reinforcements

- **Modify** `SimCoreV4.ts`: Add `SyncService` call points.
- **Modify** `MetricRegistryService`: Add `fetch()` logic for DB-backed metrics.
- **New** `src/lib/SyncManager.ts`: Handle the lifecycle of syncing local runs to the backend.
- **New** `scripts/db_import.py`: Bridge the gap between CSV ledgers and PostgreSQL.

---
**Verdict:** The system is "ready to connect." Most of the hard work (Core physics, DB schema, UI design) is done. The final step is wiring the data flow.
