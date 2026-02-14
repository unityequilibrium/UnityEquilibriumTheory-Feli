# Settings & Parameters Contract
## UET Platform - Complete Settings Specification v3.0

> **Source of Truth:** ทุก setting ในระบบต้องมี contract ที่นี่  
> **Smart Design:** See [SMART_SETTINGS_DESIGN.md](design_system/SMART_SETTINGS_DESIGN.md)  
> **Key Rule:** Sim Settings = READ-ONLY verification, Input via Smart Studio Panel

---

## 🏛️ Settings Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         UET PLATFORM                                │
├──────────────────────────────┬──────────────────────────────────────┤
│   PLATFORM SETTINGS (⚙️)     │     SIMULATION SETTINGS (🔬)         │
│   (TopNav → SettingsModal)   │     (Right Panel → Studio)           │
├──────────────────────────────┼──────────────────────────────────────┤
│  • Theme (dark/light)        │  • dt (time step)                    │
│  • Language                  │  • Integrator                        │
│  • Default units             │  • Softening                         │
│  • Notification prefs        │  • Speed                             │
│  • Startup page              │  • Equations on/off                  │
│  • Grid visibility           │  • Equation parameters               │
│  • FPS display               │  • Seed                              │
├──────────────────────────────┼──────────────────────────────────────┤
│  Storage: LocalStorage       │  Storage: Run/Session/DB             │
│  Scope: User-wide            │  Scope: Per-Room/Per-Run             │
└──────────────────────────────┴──────────────────────────────────────┘
```

---

## 📋 Setting Levels

| Level | Description | Storage | Scope |
|-------|-------------|---------|-------|
| **Platform** | User preferences, global UI | LocalStorage | User-wide |
| **UI State** | Panel states, temporary | React state | Session |
| **Run Parameter** | Sim settings, not persisted | SimCore state | Per-run |
| **Persisted Run** | Sim settings, saved with run | Database | Per-run |

---

# 🏛️ PLATFORM SETTINGS

> **Location:** TopNav → ⚙️ Settings button  
> **Modal:** PlatformSettingsModal  
> **Persistence:** LocalStorage

## Platform Settings Spec

### Appearance

| Key | Type | Default | Options | Notes |
|-----|------|---------|---------|-------|
| `platform.theme` | enum | 'dark' | dark, light | ❌ Not implemented |
| `platform.accentColor` | string | '#4ecdc4' | hex color | ❌ Not implemented |
| `platform.showFPS` | boolean | true | - | Current: always shows |

### Defaults

| Key | Type | Default | Options | Notes |
|-----|------|---------|---------|-------|
| `platform.defaultUnits` | enum | 'SI' | SI, CGS, Natural | ❌ Not implemented |
| `platform.startupPage` | enum | 'home' | home, gallery, lab | ❌ Not implemented |
| `platform.defaultRoom` | string | 'sim3d' | room_id | ❌ Not implemented |

### Display

| Key | Type | Default | Notes |
|-----|------|---------|-------|
| `platform.showGrid` | boolean | true | Grid overlay in canvas |
| `platform.showOrbits` | boolean | false | Orbit trails |
| `platform.showLabels` | boolean | true | Object labels |
| `platform.antialiasing` | boolean | true | 3D antialiasing |

### Notifications

| Key | Type | Default | Notes |
|-----|------|---------|-------|
| `platform.showWarnings` | boolean | true | SmartWarning overlay |
| `platform.soundEffects` | boolean | false | ❌ Not implemented |

---

## Platform Settings Modal UX Spec

```
┌─────────────────────────────────────────────────────┐
│  ⚙️ PLATFORM SETTINGS                           ×  │
├─────────────────────────────────────────────────────┤
│  [Appearance] [Defaults] [Display] [About]          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  APPEARANCE                                         │
│  ─────────────────────────────────────────────────  │
│  Theme                                              │
│  ○ Dark   ● Light                                   │
│                                                     │
│  Accent Color                                       │
│  [■ Cyan] [■ Purple] [■ Green] [■ Orange]           │
│                                                     │
│  Show FPS Counter                                   │
│  [✓]                                                │
│                                                     │
├─────────────────────────────────────────────────────┤
│  [Reset All]                        [Save & Close]  │
└─────────────────────────────────────────────────────┘
```

**Action IDs:**

| Button | action_id | Expected Effect |
|--------|-----------|-----------------|
| Close × | `platform_settings_close` | Close modal |
| Reset All | `platform_settings_reset` | Reset to defaults |
| Save & Close | `platform_settings_save` | Save to localStorage |
| Theme toggle | `platform_settings_theme_[value]` | Change theme |

---

# 🔬 SIMULATION SETTINGS

> **Location:** Right Panel → Studio section  
> **Already exists in:** RightPanelContent  
> **Persistence:** SimCore state (per-run) or DB (when saved)

## Simulation Settings Spec

### Core Parameters (Always Visible in Studio)

| Key | Type | Default | Range | Level | Component |
|-----|------|---------|-------|-------|-----------|
| `sim.dt` | number | 0.016 | 0.001-0.1 | Run param | RightPanelContent |
| `sim.speed` | number | 1.0 | 0.1-10 | Run param | SimCoreV4 |
| `sim.softening` | number | 0.01 | 0.001-0.1 | Run param | ⚠️ Not connected |

### Advanced Parameters (Expandable Section)

| Key | Type | Default | Options | Level | Notes |
|-----|------|---------|---------|-------|-------|
| `sim.integrator` | enum | 'verlet' | verlet, rk4, euler | Run param | ❌ Not implemented |
| `sim.seed` | number | random | 0-999999 | Persisted | ❌ Not implemented |
| `sim.maxIterations` | number | 100000 | 1000-1M | Run param | ❌ Not implemented |

### Equation Parameters

| Key | Type | Default | Level | Notes |
|-----|------|---------|-------|-------|
| `eq.[id].enabled` | boolean | varies | Persisted | ✅ Implemented |
| `eq.[id].role` | enum | 'coupled' | Persisted | ✅ Implemented |
| `eq.[id].params.*` | number | varies | Run param | ⚠️ Via SmartParameterPanel |

---

## Right Panel Studio Section Layout

```
┌─────────────────────────────────────────────────────┐
│  ⚡ ACTIVE EQUATIONS                                │
│  ┌─────────────────────────────────────────────────┐│
│  │ ☑ Newtonian Mechanics    [Driver   ▼]         ││
│  │ ☑ General Relativity     [Coupled  ▼]         ││
│  │ ☐ Unified Equilibrium    [Observer ▼]         ││
│  └─────────────────────────────────────────────────┘│
│  [+ Add Equation]                                   │
│                                                     │
│  ─────────────────────────────────────────────────  │
│  📊 QUICK PARAMETERS                                │
│  DT (Time Step)                         0.0160      │
│  [==========●==============================]        │
│                                                     │
│  Softening                              0.010       │
│  [==========●==============================]        │
│                                                     │
│  ─────────────────────────────────────────────────  │
│  ⚙️ SMART PARAMETERS                                │
│  [Expandable SmartParameterPanel content]           │
│                                                     │
│  ─────────────────────────────────────────────────  │
│  📝 NOTES                                           │
│  [NotesTab content]                                 │
└─────────────────────────────────────────────────────┘
```

**Action IDs for Simulation Settings:**

| Button | action_id | Expected Effect |
|--------|-----------|-----------------|
| DT slider | `sim_slider_dt` | Change time step |
| Softening slider | `sim_slider_softening` | Change softening |
| Equation checkbox | `sim_equation_toggle_[id]` | Enable/disable |
| Role dropdown | `sim_equation_role_[id]` | Change role |
| + Add Equation | `sim_add_equation` | Open equation modal |

---

# � UI STATE SETTINGS

> **Level:** UI-only (React state, not persisted)  
> **Scope:** Current session only

| Key | Type | Default | Component | Notes |
|-----|------|---------|-----------|-------|
| `ui.leftPanelOpen` | boolean | false | LayoutContext | ✅ Implemented |
| `ui.rightPanelOpen` | boolean | true | LayoutContext | ✅ Implemented |
| `ui.dockOpen` | boolean | false | LayoutContext | ✅ Implemented |
| `ui.dimensionMode` | enum | '3D' | SimulationHUD | ✅ UI only, ⚠️ not connected |
| `ui.activeNoteId` | string? | null | NotesTab | Session only |
| `ui.selectedMetrics` | string[] | [] | GraphDock | Session only |

---

# 📊 Implementation Status Summary

## Platform Settings

| Setting | Documented | Implemented | Connected |
|---------|------------|-------------|-----------|
| Theme | ✅ | ❌ | ❌ |
| Accent Color | ✅ | ❌ | ❌ |
| Show FPS | ✅ | ⚠️ Hardcoded | ❌ |
| Default Units | ✅ | ❌ | ❌ |
| Show Grid | ✅ | ❌ | ❌ |
| Show Warnings | ✅ | ⚠️ Hardcoded | ❌ |

**Overall:** 0% implemented (modal doesn't exist)

## Simulation Settings

| Setting | Documented | Implemented | Connected |
|---------|------------|-------------|-----------|
| dt | ✅ | ✅ | ✅ |
| speed | ✅ | ⚠️ Via HUD | ✅ |
| softening | ✅ | ✅ UI | ❌ Engine |
| integrator | ✅ | ❌ | ❌ |
| seed | ✅ | ❌ | ❌ |
| equations | ✅ | ✅ | ✅ |

**Overall:** 60% implemented

## UI State

| Setting | Documented | Implemented |
|---------|------------|-------------|
| Panel states | ✅ | ✅ |
| Dimension mode | ✅ | ⚠️ UI only |

**Overall:** 80% implemented

---

# 🎯 Priority Implementation

## P0 - Today

1. ✅ Document separation complete
2. [ ] Connect `sim.softening` to engine
3. [ ] Add action_ids to all sim sliders

## P1 - This Week

1. [ ] Create `PlatformSettingsModal` component
2. [ ] Implement localStorage for platform settings
3. [ ] Connect dimension toggle to renderer

## P2 - Nice to Have

1. [ ] Theme switching
2. [ ] Integrator selection
3. [ ] Seed input

---

**Last Updated:** 2024-12-24  
**Version:** 2.0 (Platform vs Simulation split)
