# Smart Sync System Specification
## Unified Room↔Equation↔Params↔Unit Synchronization

**Last Updated:** 2024-12-25  
**Purpose:** Single Source of Truth for Smart Sync System

---

# ═══════════════════════════════════════════════════════════════
# LAYER A: UX/UI Intent & Interaction Rules
# ═══════════════════════════════════════════════════════════════

## A.1 User Goals

| User wants to... | Smart Sync provides... |
|------------------|------------------------|
| เปลี่ยน scenario | Room Selector (in NavBar) |
| เรียนรู้ตามสาขาวิชา | Subject filter (Physics, Economics, etc.) |
| เพิ่ม/ลบสมการ | EQUATIONS panel + Modal |
| ปรับ parameters | PARAMS panel (grouped) |
| เปลี่ยน unit | Unit dropdown |

## A.2 NavBar UX Design (Redesign 2025-12-25)

### Problem: Redundancy
```
OLD (ซ้ำ 3 แห่ง):
[ROOM: Solar System] [LAB] ... LAB / SOLAR SYSTEM
     ↑ ซ้ำ 1          ↑ ซ้ำ 2         ↑ ซ้ำ 3
```

### Solution: ChatGPT-style Room Selector
```
NEW:
[UET] [HOME] [GALLERY] [☀️ Solar System ▾]
                              ↓ dropdown
                       ┌─────────────────────────┐
                       │ 🔬 PHYSICS              │
                       │   ☀️ Solar System     ✓ │
                       │   🔮 Three-Body         │
                       │                         │
                       │ 📈 ECONOMICS        →   │
                       │   💹 Stock Market       │
                       │                         │
                       │ 🌍 GEOSIM           →   │
                       │   🚗 Bangkok Traffic    │
                       └─────────────────────────┘
```

### Subject/Discipline Categories (12 สาขาวิชา)

| Order | Subject | Icon | Target Faculty |
|-------|---------|------|----------------|
| 1 | **Physics** | 🔬 | คณะวิทยาศาสตร์ |
| 2 | **Quantum Physics** | ⚛️ | คณะวิทยาศาสตร์ |
| 3 | **Chemistry** | 🧪 | คณะวิทยาศาสตร์ |
| 4 | **Biology** | 🧬 | คณะวิทยาศาสตร์ |
| 10 | **Engineering** | ⚡ | คณะวิศวกรรมศาสตร์ (Traffic/Urban) |
| 20 | **Economics** | 💼 | คณะเศรษฐศาสตร์ |
| 21 | **Psychology** | 🧠 | คณะจิตวิทยา |
| 30 | **Medical/Neuro** | 🏥 | คณะแพทยศาสตร์ |
| 40 | **CS/AI** | 💻 | คณะวิศวกรรมคอมพิวเตอร์ |
| 50 | **Geography** | 🌍 | คณะภูมิศาสตร์ (Real-world Sim) |
| 60 | **Mathematics** | 📐 | คณะคณิตศาสตร์ (Misc) |
| 99 | **Testing** | 🔧 | QA/Validation |

## A.3 Selection Cascade

```
USER ACTION → SelectionStore → UI UPDATE

┌──────────┐    ┌──────────┐    ┌──────────┐
│   ROOM   │───▶│ EQUATION │───▶│  PARAMS  │
│  Select  │    │  Sync    │    │  Sync    │
└──────────┘    └──────────┘    └──────────┘
```

## A.4 Interaction Rules

| Rule | Description |
|------|-------------|
| IR1 | Room change resets equations to defaultModules + UET |
| IR2 | UET cannot be removed (core equation) |
| IR3 | Modal filters by room.type + category |
| IR4 | Params grouped by equation name |
| IR5 | **NEW:** Room dropdown replaces LAB button |
| IR6 | **NEW:** Rooms grouped by Subject in dropdown |

---

# ═══════════════════════════════════════════════════════════════
# LAYER B: Frontend Shell/State/Action Contracts
# ═══════════════════════════════════════════════════════════════

## B.1 SelectionStore Schema

```typescript
interface SelectionState {
    // State
    roomId: string;              // 'solarSystem'
    enabledEquations: string[];  // ['uet', 'newton']
    presetId: string | null;     // 'solarSystemV2'
    unitMode: UnitMode;          // 'physical'
    
    // Actions
    setRoom: (roomId: string) => void;
    addEquation: (id: string) => void;
    removeEquation: (id: string) => void;
    setPreset: (presetId: string) => void;
    setUnitMode: (mode: UnitMode) => void;
}
```

## B.2 Sync Rules

### R1: Room Change
```
TRIGGER: User selects room from dropdown
ACTION:
  1. roomId = selected
  2. enabledEquations = ['uet', ...room.defaultModules]
  3. presetId = room.defaultPreset
  4. Trigger EQUATIONS panel update
  5. Trigger PARAMS panel update
```

### R2: Add Equation
```
TRIGGER: User clicks "+ Add" and selects equation
ACTION:
  1. enabledEquations.push(id)
  2. Recalculate visible params
  3. Update PARAMS panel
```

### R3: Remove Equation
```
TRIGGER: User clicks ✕ on equation
GUARD: id !== 'uet'
ACTION:
  1. enabledEquations = enabledEquations.filter(x => x !== id)
  2. Remove equation's params from PARAMS panel
```

### R4: Unit Mode Change
```
TRIGGER: User changes unit dropdown
ACTION:
  1. Convert displayed values to new unit
  2. Update all param labels
  3. Update telemetry displays
```

### R5: Category Filter
```
TRIGGER: User opens Add Equation modal
FILTER: Show equation ONLY IF:
  1. Category compatible with room.type
  2. Extensions require UET enabled
  3. Not already in enabledEquations
```

## B.3 Category Compatibility Matrix

| Category | sim3d | geosim | test |
|----------|-------|--------|------|
| core | ✅ | ✅ | ✅ |
| extensions | ✅* | ❌ | ✅* |
| physics | ✅ | ❌ | ✅ |
| toys | ❌ | ✅ | ✅ |

*Requires UET enabled

---

# ═══════════════════════════════════════════════════════════════
# LAYER C: API Contract (Client-Only)
# ═══════════════════════════════════════════════════════════════

Smart Sync is client-side only. No API calls required for:
- Room selection
- Equation enable/disable
- Param changes

API calls occur only for:
- Save to Gallery (POST /api/snapshot)
- Load from Gallery (GET /api/snapshot/:id)

---

# ═══════════════════════════════════════════════════════════════
# LAYER D: Engine/Telemetry/Determinism
# ═══════════════════════════════════════════════════════════════

## D.1 Engine Integration

```
SelectionStore.enabledEquations → SimCoreV4.setActiveEquations()
                               → Engine reconfigures
                               → Telemetry updates
```

## D.2 Determinism Rules

| Rule | Description |
|------|-------------|
| DR1 | Same room + preset = same initial state |
| DR2 | Same equations = same physics |
| DR3 | Preset applies AFTER room change |

---

# ═══════════════════════════════════════════════════════════════
# LAYER E: Persistence Policy
# ═══════════════════════════════════════════════════════════════

## E.1 What is Saved

| Data | Saved? | Location |
|------|--------|----------|
| roomId | ✅ | Snapshot JSON |
| enabledEquations | ✅ | Snapshot JSON |
| param values | ✅ | Snapshot JSON |
| body positions | ✅ | Snapshot JSON |
| unitMode | ❌ | Display only |

## E.2 Replay Requirements

To replay a snapshot:
1. Load roomId → triggers R1
2. Apply enabledEquations → may differ from room default
3. Apply param values
4. Apply body positions

---

# ═══════════════════════════════════════════════════════════════
# ACTION MAP
# ═══════════════════════════════════════════════════════════════

| action_id | Element | Expected Effect | Owner |
|-----------|---------|-----------------|-------|
| `room_select` | Room dropdown | R1: Reset equations | SelectionStore |
| `equation_add` | + Add button | Open modal | Modal |
| `equation_add_confirm` | Add Selected | R2: Add to list | SelectionStore |
| `equation_toggle` | Checkbox | Enable/disable | SelectionStore |
| `equation_remove` | ✕ button | R3: Remove | SelectionStore |
| `equation_role` | Role dropdown | Change role | SelectionStore |
| `param_change` | Slider/input | Update value | SimCoreV4 |
| `unit_change` | Unit dropdown | R4: Convert | SelectionStore |

---

# ═══════════════════════════════════════════════════════════════
# REGISTRIES
# ═══════════════════════════════════════════════════════════════

## Room Registry

| Field | Type | Required |
|-------|------|----------|
| room_id | string | ✅ |
| type | 'sim3d' \| 'geosim' \| 'test' | ✅ |
| title | string | ✅ |
| defaultModules | string[] | ✅ |
| defaultMetrics | string[] | ✅ |
| defaultPreset | string | ❌ |
| geoConfig | object | geosim only |

## Equation Registry

| Field | Type | Required |
|-------|------|----------|
| id | string | ✅ |
| name | string | ✅ |
| category | string | ✅ |
| parameters | EquationParameter[] | ✅ |
| outputs | EquationOutput[] | ✅ |

## Subject Registry (NEW)

| Field | Type | Description |
|-------|------|-------------|
| id | string | 'physics', 'economics', etc. |
| name | string | \"🔬 Physics\" |
| icon | string | Emoji or icon class |
| order | number | Display order in dropdown |

### Default Subjects (12 categories)

| Subject ID | Icon | Name | Rooms |
|------------|------|------|-------|
| `physics` | 🔬 | Physics | solarSystem, threeBody, uetTest |
| `quantum` | ⚛️ | Quantum Physics | (future) |
| `chemistry` | 🧪 | Chemistry | (future) |
| `biology` | 🧬 | Biology | (future) |
| `engineering` | ⚡ | Engineering | geoSimBangkok, trafficShibuya |
| `economics` | 💼 | Economics | stockMarket |
| `psychology` | 🧠 | Psychology | (future) |
| `medical` | 🏥 | Medical/Neuro | neuralSleep |
| `cs` | 💻 | CS/AI | llmDynamics |
| `geography` | 🌍 | Geography | geoSimPM25, geoSimFlood |
| `mathematics` | 📐 | Mathematics | (future) |
| `test` | 🔧 | Testing | testGates |

---

# ═══════════════════════════════════════════════════════════════
# TRACEABILITY
# ═══════════════════════════════════════════════════════════════

## Cross-Layer Matrix

| Layer A (UX) | Layer B (FE) | Layer D (Engine) |
|--------------|--------------|------------------|
| IR1 Room reset | R1 setRoom | DR1 initial state |
| IR2 UET locked | R3 guard | DR2 same physics |
| IR3 Modal filter | R5 category | - |
| IR4 Params grouped | B.1 schema | - |

## Doc ↔ Code Mapping

| Doc Section | Code File |
|-------------|-----------|
| B.1 SelectionStore | lib/stores/SelectionStore.ts |
| R1-R5 Rules | SelectionStore actions |
| Action Map | LabShell.tsx data-action-id |
| Room Registry | registries/roomRegistry.ts |
| Equation Registry | lib/equations/registry.ts |

---

# ═══════════════════════════════════════════════════════════════
# GLOBAL RULES ALIGNMENT
# ═══════════════════════════════════════════════════════════════

| Global Rule | This Doc |
|-------------|----------|
| 3 Pages only | ✅ No routes |
| One shell /lab | ✅ UI in LabShell |
| Rooms from registry | ✅ R1, Room dropdown |
| Save in OUTPUT only | ✅ Layer E |
| No dead buttons | ✅ Action Map |

---

# ═══════════════════════════════════════════════════════════════
# IMPLEMENTATION FILES
# ═══════════════════════════════════════════════════════════════

| File | Change | Priority |
|------|--------|----------|
| `lib/stores/SelectionStore.ts` | Create new | 🔴 |
| `shell/LabShell.tsx` | Add Room dropdown | 🔴 |
| `shell/LabShell.tsx` | Fix ✕ button | 🔴 |
| `components/modals/AddEquationModal.tsx` | Add R5 filter | 🔴 |
| `components/panels/ParamsPanel.tsx` | Group by equation | 🟡 |

