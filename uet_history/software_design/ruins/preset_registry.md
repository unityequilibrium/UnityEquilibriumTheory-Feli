# Preset Registry
## Layer B — Frontend Registry Contract

> **Rule:** ทุก simulation preset ต้องอยู่ใน presetRegistry
> **Source of Truth:** `frontend/src/registries/presetRegistry.ts`

---

## 📋 Registry Interface

```typescript
interface SimPreset {
    id: string;           // Unique ID (e.g., 'einstein_binary')
    familyId: string;     // Category (extension|archetype|physics|toy|3d)
    subFamily?: string;   // Sub-category (e.g., 'coffee', 'traffic')
    name: string;         // Display name
    description: string;  // Short description
    thumbnail: string;    // Path to thumbnail
    tags: PresetTag[];    // PASS|WARN|FAIL|VIZ_ONLY
    equations: EquationConfig[];  // Required modules
    simParams: SimParams;         // Simulation parameters
    initialState: InitialStateConfig;
    metrics: string[];    // Tracked metrics
}

interface SimFamily {
    id: string;
    name: string;
    icon: string;
    order: number;
}
```

---

## 🎯 Families (5)

| id | name | icon | Count |
|----|------|------|-------|
| `extension` | UET Extensions | 🚀 | 6 |
| `archetype` | Archetype Demos | 🎬 | 5 |
| `physics` | Physics & Advanced | 🔬 | 12 |
| `toy` | Toy Models | 🎮 | 35 |
| `3d` | 3D Simulations | 🌐 | 4 |
| **Total** | | | **62** |

---

## 🔌 API Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `getFamilies()` | `SimFamily[]` | All families sorted by order |
| `getByFamily(id)` | `SimPreset[]` | Presets in family |
| `getBySubFamily(fam, sub)` | `SimPreset[]` | Filter by subfamily |
| `get(id)` | `SimPreset` | Single preset |
| `getAll()` | `SimPreset[]` | All presets |
| `search(query)` | `SimPreset[]` | Search by name/desc/id |
| `count()` | `number` | Total preset count |

---

## 🔗 Integration Points

| Layer | Integration |
|-------|-------------|
| B (Gallery) | PresetCard reads from `getByFamily()` |
| B (Modal) | Modal reads from `get(presetId)` |
| D (SimCore) | `init(preset)` → enables `preset.equations` |
| D (Event) | `SIM_INITIALIZED` includes `preset.id` |

---

## ⚠️ Constraints (from Global Rules)

1. **R1.3**: All presets MUST be in registry (no hardcode)
2. **R2.1**: Gallery cards MUST have `data-action-id="gallery_preset_open"`
3. **R4.1**: Same preset + seed = same result (determinism)

---

**Layer:** B — Frontend Structure
