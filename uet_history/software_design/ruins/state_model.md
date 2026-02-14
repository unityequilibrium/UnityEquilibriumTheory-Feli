# State Model
## Layer B — Complete State Ownership Contract

**Last Updated:** 2024-12-24  
**Layer:** B (Frontend)  
**Status:** ✅ Complete

---

## 🗃️ State Ownership Matrix

> **Rule:** ทุก data มี owner เดียว ห้ามซ้ำ

### Primary State Stores

| Data | Owner | Type | Persistence |
|------|-------|------|-------------|
| **Simulation** |
| particles[] | SimCoreV4 | runtime | DB (on save) |
| worldState.time | SimCoreV4 | runtime | DB (on save) |
| worldState.step | SimCoreV4 | runtime | DB (on save) |
| equations[] | simStoreV4 | zustand | DB (on save) |
| dt | simStoreV4 | zustand | DB (on save) |
| softening | simStoreV4 | zustand | DB (on save) |
| speed | simStoreV4 | zustand | None |
| seed | simStoreV4 | zustand | DB (on save) |
| **Telemetry** |
| telemetry.run | SimCoreV4 | runtime | DB (periodic) |
| telemetry.history | SimCoreV4 | runtime | DB (on save) |
| **UI Layout** |
| leftPanelOpen | LayoutContext | react context | None |
| rightPanelOpen | LayoutContext | react context | None |
| dockOpen | LayoutContext | react context | None |
| dimensionMode | SimulationHUD | local state | None |
| **User Preferences** |
| theme | localStorage | storage | localStorage |
| showFPS | localStorage | storage | localStorage |
| defaultUnits | localStorage | storage | localStorage |

---

## 🔄 Sync Rules

### SimCore ↔ simStore

```
simStore.equations → SimCoreV4.loadEquations()
simStore.dt → SimCoreV4.setDt()
simStore.softening → SimCoreV4.setSoftening()

SimCoreV4.worldState → simStore.worldState (on tick)
SimCoreV4.telemetry → simStore.telemetry (on tick)
```

### Store → DB

```
Save triggered by: output_save_snapshot action
Data saved:
  - simStore.worldState → runs.worldState
  - simStore.equations → runs.equations
  - simStore.seed → runs.seed
```

---

## 📍 State Flow Diagram

```
User Input (UI)
     │
     ▼
┌─────────────────┐
│   simStoreV4    │ ← Zustand (primary store)
│  - equations    │
│  - dt, softening│
│  - seed         │
└────────┬────────┘
         │ sync
         ▼
┌─────────────────┐
│   SimCoreV4     │ ← Physics engine (runtime)
│  - particles    │
│  - worldState   │
│  - telemetry    │
└────────┬────────┘
         │ notify
         ▼
┌─────────────────┐
│   Components    │ ← React (render)
│  - GraphDock    │
│  - MetricCards  │
│  - Canvas       │
└─────────────────┘
```

---

## ⚠️ Ownership Conflicts (Resolved)

| Conflict | Resolution |
|----------|------------|
| dt in UI vs Engine | Store is owner, Engine syncs |
| particles in multiple places | SimCoreV4 is owner, others read-only |
| panel states | LayoutContext only, never persist |

---

## 🔒 Rules

1. **Single owner** - ห้ามมี data อยู่หลายที่
2. **Clear direction** - Owner → Readers
3. **No circular deps** - Store → Engine → Components
4. **Persist explicitly** - เฉพาะ owner เป็นคน save

---

**Layer:** B — Frontend Structure

