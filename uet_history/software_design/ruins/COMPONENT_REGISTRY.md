# Component Registry
## UET Platform - Complete Component Documentation

> **Source of Truth:** ทุก component ในระบบต้องมี entry ที่นี่  
> **Rule:** ถ้าไม่มีใน registry = ไม่ควรมีในโค้ด

---

## 📁 Directory Structure Overview

```
frontend/src/
├── app/                    # Next.js pages
│   ├── page.tsx           # Home page
│   ├── gallery/page.tsx   # Gallery page
│   ├── lab/page.tsx       # Lab page
│   ├── diagnostics/page.tsx
│   └── api/               # API routes
├── components/            # Shared components
│   ├── shared/
│   │   └── TopNav.tsx
│   └── gallery/
│       └── SystemTicker.tsx
├── features/              # Feature-specific components
│   ├── simulation/        # Lab simulation features
│   ├── units/             # Unit display components
│   └── rooms/             # Room type components
├── shell/                 # App shell components
│   ├── LabShell.tsx
│   ├── AppTokens.ts
│   └── IconButton.tsx
├── lib/                   # Utilities and core logic
│   ├── SimCoreV4.ts      # Simulation engine
│   ├── simStoreV4.ts     # Zustand store
│   └── equations/        # Physics equations
└── contexts/             # React contexts
    └── LayoutContext.tsx
```

---

## 🏠 Pages

### Home Page (`app/page.tsx`)

| Property | Value |
|----------|-------|
| **Route** | `/` |
| **Doc Reference** | GRID_LAYOUT_DESIGN_SYSTEM.md (Portal Pattern) |
| **Components Used** | TopNav, SystemTicker |
| **Buttons** | Quick Start cards (4) |
| **Status** | ⚠️ Interactions not fully documented |

**Action IDs Required:**
- `home_quickstart_solar` - Open Solar System preset
- `home_quickstart_galaxy` - Open Galaxy preset
- `home_quickstart_custom` - Open custom simulation
- `home_quickstart_tutorial` - Open tutorial

---

### Gallery Page (`app/gallery/page.tsx`)

| Property | Value |
|----------|-------|
| **Route** | `/gallery` |
| **Doc Reference** | GRID_LAYOUT_DESIGN_SYSTEM.md (Browser Pattern) |
| **Components Used** | TopNav, ProjectCard, SystemTicker |
| **Status** | ⚠️ Filter/Card interactions not documented |

**Action IDs Required:**
- `gallery_filter_all` - Show all projects
- `gallery_filter_[category]` - Filter by category
- `gallery_card_open` - Open project in Lab
- `gallery_card_delete` - Delete project
- `gallery_add_project` - Open add modal

---

### Lab Page (`app/lab/page.tsx`)

| Property | Value |
|----------|-------|
| **Route** | `/lab` |
| **Doc Reference** | LAB_UI_DESIGN_SPEC.md, GRID_LAYOUT_DESIGN_SYSTEM.md |
| **Shell** | LabShell.tsx |
| **Components Used** | TopNav, SimulationHUD, GraphDock, Left/Right panels |
| **Status** | ✅ Layout documented, ⚠️ some buttons missing action_ids |

---

### Diagnostics Page (`app/diagnostics/page.tsx`)

| Property | Value |
|----------|-------|
| **Route** | `/diagnostics` |
| **Doc Reference** | GRID_LAYOUT_DESIGN_SYSTEM.md (Utility Pattern) |
| **Components Used** | TopNav |
| **Status** | ✅ Basic, minimal interactions |

---

## 🧩 Shell Components

### TopNav (`components/shared/TopNav.tsx`)

| Property | Value |
|----------|-------|
| **Doc Reference** | GRID_LAYOUT_DESIGN_SYSTEM.md |
| **Props** | `roomTitle?: string`, `onToggleExport?: () => void` |
| **Used By** | All pages |
| **Z-Index** | 50 |

**Buttons & Action IDs:**

| Button | action_id | expected_effect | Status |
|--------|-----------|-----------------|--------|
| UET Logo | `topnav_home` | Navigate to / | ⚠️ Missing |
| Home | `topnav_nav_home` | Navigate to / | ⚠️ Missing |
| Gallery | `topnav_nav_gallery` | Navigate to /gallery | ⚠️ Missing |
| Lab | `topnav_nav_lab` | Navigate to /lab | ⚠️ Missing |
| Diagnostics | `topnav_nav_diagnostics` | Navigate to /diagnostics | ⚠️ Missing |
| Export | `topnav_export` | Open ExportModal | ⚠️ Missing |
| Settings ⚙️ | `topnav_settings` | Open SettingsModal | ❌ Not implemented |

---

### LabShell (`shell/LabShell.tsx`)

| Property | Value |
|----------|-------|
| **Doc Reference** | LAB_UI_DESIGN_SPEC.md |
| **Props** | `children: React.ReactNode` |
| **Provides** | LayoutProvider context |
| **Contains** | Left/Right panels, Bottom dock, floating buttons |

**Panel Settings:**

| Setting | Key | Type | Default | Persistence |
|---------|-----|------|---------|-------------|
| Left Panel | `layout.leftOpen` | boolean | false | UI-only |
| Right Panel | `layout.rightOpen` | boolean | true | UI-only |
| Bottom Dock | `layout.dockOpen` | boolean | false | UI-only |

**Buttons & Action IDs:**

| Button | action_id | expected_effect | Status |
|--------|-----------|-----------------|--------|
| [◀ HIDE] (left) | `panel_left_hide` | Close left panel | ⚠️ Missing |
| [HIDE ▶] (right) | `panel_right_hide` | Close right panel | ⚠️ Missing |
| [▶ SHOW OUTPUT] | `panel_left_show` | Open left panel | ⚠️ Missing |
| [SHOW STUDIO ◀] | `panel_right_show` | Open right panel | ⚠️ Missing |
| [▲ SHOW GRAPHS] | `dock_show` | Open bottom dock | ⚠️ Missing |
| 💾 Save Snapshot | `output_save_snapshot` | Save current state | ⚠️ Missing |
| [+ Add Equation] | `studio_add_equation` | Open AddEquationModal | ❌ Not implemented |

---

## 🎛️ Simulation Components

### SimulationHUD (`features/simulation/SimulationHUD.tsx`)

| Property | Value |
|----------|-------|
| **Doc Reference** | LAB_UI_DESIGN_SPEC.md |
| **Props** | None (uses store) |
| **Z-Index** | 30 |

**Buttons & Action IDs:**

| Button | action_id | expected_effect | Status |
|--------|-----------|-----------------|--------|
| ▶ Play | `hud_play` | Start simulation | ✅ |
| ⏸ Pause | `hud_pause` | Pause simulation | ✅ |
| ⏭ Step | `hud_step_forward` | Single step | ✅ |
| ⟲ Reset | `hud_reset` | Reset simulation | ✅ |
| 2D | `hud_dimension_2d` | Switch to 2D view | ⚠️ Not connected |
| 3D | `hud_dimension_3d` | Switch to 3D view | ⚠️ Not connected |
| 4D | `hud_dimension_4d` | Switch to 4D view | ⚠️ Not connected |

**Settings:**

| Setting | Key | Type | Default | Persistence |
|---------|-----|------|---------|-------------|
| Dimension Mode | `ui.dimensionMode` | enum(2D,3D,4D) | 3D | UI-only |

---

### GraphDock (`features/simulation/GraphDock.tsx`)

| Property | Value |
|----------|-------|
| **Doc Reference** | SMART_PLOTLY_DESIGN.md |
| **Props** | `isOpen`, `onToggle`, `mode`, `runId?`, `defaultMetrics` |
| **Z-Index** | 20 |

**Buttons & Action IDs:**

| Button | action_id | expected_effect | Status |
|--------|-----------|-----------------|--------|
| [HIDE ▼] | `dock_hide` | Close dock | ⚠️ Missing |
| × Clear | `dock_clear` | Clear telemetry | ⚠️ Missing |
| Metric toggles | `dock_toggle_[metric]` | Toggle graph line | ⚠️ Missing |

---

### MetricCards (`features/simulation/MetricCards.tsx`)

| Property | Value |
|----------|-------|
| **Doc Reference** | LAB_UI_DESIGN_SPEC.md |
| **Props** | `metrics: string[]` |
| **Status** | ✅ Display only, no interactions |

---

### SmartParameterPanel (`features/simulation/components/SmartParameterPanel.tsx`)

| Property | Value |
|----------|-------|
| **Doc Reference** | SMART_SYSTEM_DESIGN.md |
| **Status** | ⚠️ Needs button action_ids |

---

### ExportModal (`features/simulation/components/ExportModal.tsx`)

| Property | Value |
|----------|-------|
| **Doc Reference** | ❌ Not fully documented |
| **Props** | `isOpen`, `onClose` |

**Buttons & Action IDs:**

| Button | action_id | expected_effect | Status |
|--------|-----------|-----------------|--------|
| Export JSON | `export_json` | Download JSON | ⚠️ Missing |
| Export CSV | `export_csv` | Download CSV | ⚠️ Missing |
| Close | `export_close` | Close modal | ⚠️ Missing |

---

### NotesTab (`features/simulation/components/NotesTab.tsx`)

| Property | Value |
|----------|-------|
| **Doc Reference** | ❌ Not documented |
| **Props** | `runId?: string` |

**Buttons & Action IDs:**

| Button | action_id | expected_effect | Status |
|--------|-----------|-----------------|--------|
| + NEW NOTE | `notes_add` | Create new note | ⚠️ Missing |
| Save Note | `notes_save` | Save current note | ⚠️ Missing |
| Delete Note | `notes_delete` | Delete note | ⚠️ Missing |

---

### SmartWarning (`features/simulation/components/SmartWarning.tsx`)

| Property | Value |
|----------|-------|
| **Doc Reference** | ❌ Not documented |
| **Purpose** | Display validation warnings overlay |
| **Status** | Display only |

---

## 🏠 Room Components

### TestLabRoom (`features/simulation/TestLabRoom.tsx`)

| Property | Value |
|----------|-------|
| **Doc Reference** | ❌ **CRITICAL - NOT DOCUMENTED** |
| **Size** | 19KB |
| **Purpose** | Main 3D simulation renderer |
| **Status** | ❌ Needs full documentation |

**Required Documentation:**
- [ ] Component purpose and architecture
- [ ] Props interface
- [ ] Three.js scene structure
- [ ] Interaction handlers
- [ ] connection to SimCoreV4

---

### Sim3DRoom (`features/simulation/Sim3DRoom.tsx`)

| Property | Value |
|----------|-------|
| **Doc Reference** | ❌ Not documented |
| **Size** | 2.5KB |
| **Status** | ❌ Needs documentation |

---

## 🔧 Utility Components

### IconButton (`shell/IconButton.tsx`)

| Property | Value |
|----------|-------|
| **Doc Reference** | ❌ Not documented |
| **Props** | Standard button props + icon |
| **Status** | Generic, low priority |

---

### SystemTicker (`components/gallery/SystemTicker.tsx`)

| Property | Value |
|----------|-------|
| **Doc Reference** | Partially in UI_BLUEPRINT.md |
| **Purpose** | Scrolling system status display |
| **Status** | Display only |

---

## 📊 Summary

### Documentation Status

| Status | Count | Components |
|--------|-------|------------|
| ✅ Fully Documented | 6 | TopNav, LabShell (layout), MetricCards, GraphDock, SimulationHUD (partial), API |
| ⚠️ Partial | 8 | SmartParameterPanel, ExportModal, Home, Gallery, etc. |
| ❌ Not Documented | 6 | TestLabRoom, Sim3DRoom, NotesTab, SmartWarning, IconButton, MiniMetricBadge |

### Action ID Status

| Status | Count |
|--------|-------|
| ✅ Implemented | 4 (HUD play/pause/step/reset) |
| ⚠️ Missing ID | ~40 |
| ❌ Not Implemented | 3 (Settings modal, Add Equation modal, dimension toggle) |

---

**Next Step:** Create BUTTON_ACTION_IDS.md with all action_ids as single source of truth
