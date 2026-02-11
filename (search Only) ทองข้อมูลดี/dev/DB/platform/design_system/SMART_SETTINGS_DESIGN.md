# Smart Simulation Settings Design
## UET Platform - Smart Settings Architecture v3.0

> **Key Insight:** Settings = Verification View, ไม่ใช่ Input Panel  
> **Rule:** ปรับค่าที่ Smart Input → Settings ดูว่า sync ถูกต้องไหม

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            SMART SYSTEM                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐             │
│   │ Smart Input  │───▶│ SimCoreV4    │───▶│ Smart Output │             │
│   │ (Studio)     │    │ (Engine)     │    │ (GraphDock)  │             │
│   └──────────────┘    └──────────────┘    └──────────────┘             │
│         │                    │                    │                     │
│         ▼                    ▼                    ▼                     │
│   ┌──────────────────────────────────────────────────────────┐         │
│   │                 SMART SETTINGS VIEW                      │         │
│   │              (Read-only Verification)                    │         │
│   │                                                          │         │
│   │   Input Value    Engine Value    Status                  │         │
│   │   ───────────    ────────────    ──────                  │         │
│   │   dt: 0.016      dt: 0.016      ✅ SYNC                  │         │
│   │   soft: 0.01     soft: 0.01     ✅ SYNC                  │         │
│   │   Newton: ON     Newton: RUN    ✅ SYNC                  │         │
│   │   UET: OFF       UET: ─         ✅ SYNC                  │         │
│   │                                                          │         │
│   │   ⚠️ ถ้าไม่ตรง = SYSTEM BUG!                              │         │
│   └──────────────────────────────────────────────────────────┘         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Setting Categories

### 1. Smart Input (Studio Panel - WRITE)

> **Location:** Right Panel → Studio section  
> **Purpose:** User adjusts simulation parameters here  
> **Action:** Changes propagate to SimCoreV4

| Setting | Input Control | Component |
|---------|---------------|-----------|
| dt | Slider | RightPanelContent |
| softening | Slider | RightPanelContent |
| speed | Slider | HUD or Studio |
| equations toggle | Checkbox | RightPanelContent |
| equation role | Dropdown | RightPanelContent |
| equation params | SmartParameterPanel | RightPanelContent |

### 2. Smart Settings View (Verification - READ-ONLY)

> **Location:** TopNav → ⚙️ → Simulation tab  
> **Purpose:** Verify that input → engine sync is working  
> **Action:** No editing, only displays status

| Displays | Input Value | Engine Value | Status |
|----------|-------------|--------------|--------|
| Time Step (dt) | from UI state | from SimCoreV4 | ✅/❌ |
| Softening | from UI state | from SimCoreV4 | ✅/❌ |
| Speed | from UI state | from SimCoreV4 | ✅/❌ |
| Active Equations | from store | from engine | ✅/❌ |

### 3. Platform Settings (Still Editable)

> **Location:** TopNav → ⚙️ → Platform tab  
> **Purpose:** User preferences (theme, units, display)  
> **Action:** Direct edit, saves to localStorage

---

## 🔄 Data Flow

```
USER INPUT (Studio Panel)
    │
    ▼
┌─────────────────────────┐
│     simStoreV4          │  ← Zustand store
│  - worldState.dt        │
│  - equations[]          │
│  - params               │
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│     SimCoreV4           │  ← Physics engine
│  - actualDt             │
│  - runningEquations     │
│  - engineParams         │
└─────────────────────────┘
    │
    ▼
SMART SETTINGS VIEW (Read-only)
    │
    ├── Compare: store.dt === engine.dt ?
    │       ✅ SYNC: Values match
    │       ❌ DESYNC: BUG DETECTED!
    │
    └── Show diagnostic info
```

---

## 🎯 UI Spec: Platform Settings Modal

```
┌─────────────────────────────────────────────────────────────┐
│  ⚙️ SETTINGS                                           ×   │
├─────────────────────────────────────────────────────────────┤
│  [🏛️ Platform] [🔬 Simulation] [ℹ️ About]                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ▸ PLATFORM TAB (Editable)                                  │
│  ────────────────────────────────────────────────────────   │
│  Theme              [● Dark] [○ Light]                      │
│  Show FPS           [✓]                                     │
│  Default Units      [SI ▼]                                  │
│                                                             │
│  ▸ SIMULATION TAB (Read-only Verification)                  │
│  ────────────────────────────────────────────────────────   │
│  CURRENT RUN PARAMETERS                                     │
│                                                             │
│  │ Parameter      │ Input    │ Engine   │ Status │         │
│  │────────────────│──────────│──────────│────────│         │
│  │ Time Step (dt) │ 0.0160   │ 0.0160   │ ✅     │         │
│  │ Softening      │ 0.0100   │ 0.0100   │ ✅     │         │
│  │ Speed          │ 1.0x     │ 1.0x     │ ✅     │         │
│  │ Integrator     │ verlet   │ verlet   │ ✅     │         │
│  │────────────────│──────────│──────────│────────│         │
│  │ Newton         │ ON       │ RUNNING  │ ✅     │         │
│  │ Einstein       │ OFF      │ IDLE     │ ✅     │         │
│  │ UET            │ OFF      │ IDLE     │ ✅     │         │
│                                                             │
│  ℹ️ Adjust parameters in Studio Panel (Right sidebar)       │
│     This view shows if values are correctly synced.         │
│                                                             │
│  [🔄 Refresh]                                    [Close]    │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚠️ Error States

### SYNC OK (✅)
```
Input: dt = 0.016
Engine: dt = 0.016
Status: ✅ SYNC
```

### DESYNC DETECTED (❌)
```
Input: dt = 0.016
Engine: dt = 0.032
Status: ❌ DESYNC - BUG!

[Report Issue] [Force Resync]
```

### Value Not Connected (⚠️)
```
Input: softening = 0.01
Engine: N/A
Status: ⚠️ NOT CONNECTED

Note: This parameter is not yet connected to the engine.
```

---

## 🔌 Integration with Smart System

| Smart Component | Role | Connection |
|-----------------|------|------------|
| **SmartParameterPanel** | Input equations params | → SimCoreV4 |
| **SmartUnit** | Display with correct units | → Settings View |
| **SmartPlotly** | Visualize output metrics | ← SimCoreV4 |
| **SmartSettings** | Verify sync status | ← Both stores |

---

## 📊 Implementation Checklist

### P0 - Connect Existing Inputs

- [ ] `sim.softening` → Connect slider to SimCoreV4
- [ ] Add action_ids to all input controls
- [ ] Verify dt slider → engine sync

### P1 - Create Settings Modal

- [ ] Create `PlatformSettingsModal` component
- [ ] Platform tab: theme, fps, units (editable)
- [ ] Simulation tab: read-only verification view
- [ ] Compare store values vs engine values
- [ ] Show sync status (✅/❌/⚠️)

### P2 - Error Handling

- [ ] Detect desync between input and engine
- [ ] Show warning banner if desync detected
- [ ] Add "Force Resync" button
- [ ] Log desync events for debugging

---

## 📝 Key Principles

1. **Single Source of Input** - ปรับค่าที่ Smart Input Panel เท่านั้น
2. **Settings = Verification** - ดูว่า sync ถูกไหม ไม่ใช่ที่ปรับ
3. **Desync = Bug** - ถ้าค่าไม่ตรง = ระบบมีปัญหา
4. **Smart Integration** - สอดคล้องกับ Smart System ทั้งหมด

---

**Last Updated:** 2024-12-24  
**Version:** 3.0 (Smart Settings = Verification View)
