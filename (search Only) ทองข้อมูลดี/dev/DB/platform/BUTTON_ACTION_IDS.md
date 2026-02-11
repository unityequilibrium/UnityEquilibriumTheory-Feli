# Button Action IDs Registry
## UET Platform - Complete Action ID Specification

> **Source of Truth:** ทุกปุ่มในระบบต้องมี action_id ที่นี่  
> **Rule:** ปุ่มที่ไม่มี action_id = ต้องเพิ่ม หรือ ลบทิ้ง

---

## 📋 Action ID Format

```
[area]_[action]_[target?]

Examples:
- hud_play
- topnav_nav_gallery
- studio_add_equation
- dock_toggle_energy
```

---

## 🎯 By Area

### TopNav (`topnav_*`)

| action_id | Label | Component | Expected Effect | Implementation |
|-----------|-------|-----------|-----------------|----------------|
| `topnav_home` | UET Logo | TopNav | Navigate to / | ⚠️ Add ID |
| `topnav_nav_home` | HOME | TopNav | Navigate to / | ⚠️ Add ID |
| `topnav_nav_gallery` | GALLERY | TopNav | Navigate to /gallery | ⚠️ Add ID |
| `topnav_nav_lab` | LAB | TopNav | Navigate to /lab | ⚠️ Add ID |
| `topnav_nav_diagnostics` | DIAGNOSTICS | TopNav | Navigate to /diagnostics | ⚠️ Add ID |
| `topnav_export` | EXPORT | TopNav | Open ExportModal | ⚠️ Add ID |
| `topnav_settings` | ⚙️ | TopNav | Open SettingsModal | ❌ Need Modal |

---

### HUD (`hud_*`)

| action_id | Label | Component | Expected Effect | Implementation |
|-----------|-------|-----------|-----------------|----------------|
| `hud_play` | ▶ | SimulationHUD | Start simulation | ✅ Done |
| `hud_pause` | ⏸ | SimulationHUD | Pause simulation | ✅ Done |
| `hud_step_forward` | ⏭ | SimulationHUD | Single step forward | ✅ Done |
| `hud_reset` | ⟲ | SimulationHUD | Reset to initial state | ✅ Done |
| `hud_dimension_2d` | 2D | SimulationHUD | Switch to 2D view | ⚠️ Not connected |
| `hud_dimension_3d` | 3D | SimulationHUD | Switch to 3D view | ⚠️ Not connected |
| `hud_dimension_4d` | 4D | SimulationHUD | Switch to 4D view | ⚠️ Not connected |

---

### Panel Controls (`panel_*`, `dock_*`)

| action_id | Label | Component | Expected Effect | Implementation |
|-----------|-------|-----------|-----------------|----------------|
| `panel_left_hide` | [◀ HIDE] | LabShell | Close left panel | ⚠️ Add ID |
| `panel_left_show` | [▶ SHOW OUTPUT] | LabShell | Open left panel | ⚠️ Add ID |
| `panel_right_hide` | [HIDE ▶] | LabShell | Close right panel | ⚠️ Add ID |
| `panel_right_show` | [SHOW STUDIO ◀] | LabShell | Open right panel | ⚠️ Add ID |
| `dock_hide` | [HIDE ▼] | GraphDock | Close bottom dock | ⚠️ Add ID |
| `dock_show` | [▲ SHOW GRAPHS] | LabShell | Open bottom dock | ⚠️ Add ID |
| `dock_clear` | × Clear | GraphDock | Clear telemetry data | ⚠️ Add ID |

---

### Output Panel (`output_*`)

| action_id | Label | Component | Expected Effect | Implementation |
|-----------|-------|-----------|-----------------|----------------|
| `output_save_snapshot` | 💾 Save Snapshot | LeftPanelContent | Save current simulation state to DB | ⚠️ Add ID |

---


### Dock/Telemetry (`dock_*`)

| action_id | Label | Component | Expected Effect | Implementation |
|-----------|-------|-----------|-----------------|----------------|
| `dock_toggle_[metric]` | Metric checkbox | GraphDock | Show/hide metric line | ⚠️ Add ID |
| `dock_tab_live` | Live Graph | GraphDock | Show live telemetry | ❌ Not implemented |
| `dock_tab_energy` | Energy | GraphDock | Show energy graphs | ❌ Not implemented |
| `dock_tab_momentum` | Momentum | GraphDock | Show momentum graphs | ❌ Not implemented |

---

### Export Modal (`export_*`)

| action_id | Label | Component | Expected Effect | Implementation |
|-----------|-------|-----------|-----------------|----------------|
| `export_json` | Export JSON | ExportModal | Download simulation as JSON | ⚠️ Add ID |
| `export_csv` | Export CSV | ExportModal | Download telemetry as CSV | ⚠️ Add ID |
| `export_close` | Close/× | ExportModal | Close modal | ⚠️ Add ID |

---

### Notes (`notes_*`)

| action_id | Label | Component | Expected Effect | Implementation |
|-----------|-------|-----------|-----------------|----------------|
| `notes_add` | + NEW NOTE | NotesTab | Create new note | ⚠️ Add ID |
| `notes_save` | Save | NotesTab | Save note to DB | ⚠️ Add ID |
| `notes_delete` | Delete | NotesTab | Delete note | ⚠️ Add ID |
| `notes_select_[id]` | Note item | NotesTab | Select note to edit | ⚠️ Add ID |

---

### Home Page (`home_*`)

| action_id | Label | Component | Expected Effect | Implementation |
|-----------|-------|-----------|-----------------|----------------|
| `home_quickstart_solar` | Solar System | Home | Open lab with solar preset | ⚠️ Add ID |
| `home_quickstart_galaxy` | Galaxy | Home | Open lab with galaxy preset | ⚠️ Add ID |
| `home_quickstart_custom` | Custom | Home | Open lab with blank | ⚠️ Add ID |
| `home_quickstart_tutorial` | Tutorial | Home | Open tutorial flow | ⚠️ Add ID |

---

### Gallery Page (`gallery_*`)

| action_id | Label | Component | Expected Effect | Implementation |
|-----------|-------|-----------|-----------------|----------------|
| `gallery_filter_all` | All | Gallery | Show all projects | ⚠️ Add ID |
| `gallery_filter_[category]` | Category | Gallery | Filter by category | ⚠️ Add ID |
| `gallery_card_open_[id]` | Card click | Gallery | Open project in Lab | ⚠️ Add ID |
| `gallery_card_delete_[id]` | Delete | Gallery | Delete project | ⚠️ Add ID |
| `gallery_add_project` | + Add | Gallery | Open AddProjectModal | ⚠️ Add ID |

---

### Platform Settings Modal (`platform_settings_*`) - TO BE CREATED

> **Trigger:** TopNav → ⚙️ Settings button  
> **Scope:** Global platform preferences

| action_id | Label | Component | Expected Effect | Implementation |
|-----------|-------|-----------|-----------------|----------------|
| `platform_settings_open` | ⚙️ | TopNav | Open PlatformSettingsModal | ❌ Need Modal |
| `platform_settings_close` | Close/× | PlatformSettingsModal | Close modal | ❌ Not implemented |
| `platform_settings_save` | Save & Close | PlatformSettingsModal | Save to localStorage | ❌ Not implemented |
| `platform_settings_reset` | Reset All | PlatformSettingsModal | Reset to defaults | ❌ Not implemented |
| `platform_settings_theme_dark` | Dark | PlatformSettingsModal | Set dark theme | ❌ Not implemented |
| `platform_settings_theme_light` | Light | PlatformSettingsModal | Set light theme | ❌ Not implemented |
| `platform_settings_toggle_fps` | Show FPS | PlatformSettingsModal | Toggle FPS display | ❌ Not implemented |
| `platform_settings_toggle_grid` | Show Grid | PlatformSettingsModal | Toggle grid overlay | ❌ Not implemented |

---

### Simulation Settings (`sim_*`) - IN STUDIO PANEL

> **Location:** Right Panel → Studio section (ไม่ใช่ modal, อยู่ใน panel)  
> **Scope:** Per-room/per-run simulation parameters

| action_id | Label | Component | Expected Effect | Implementation |
|-----------|-------|-----------|-----------------|----------------|
| `sim_slider_dt` | DT Slider | RightPanelContent | Change time step | ⚠️ Add ID |
| `sim_slider_softening` | Softening Slider | RightPanelContent | Change softening param | ⚠️ Add ID, ❌ Not connected |
| `sim_equation_toggle_[id]` | Checkbox | RightPanelContent | Enable/disable equation | ⚠️ Add ID |
| `sim_equation_role_[id]` | Dropdown | RightPanelContent | Change equation role | ⚠️ Add ID |
| `sim_add_equation` | [+ Add Equation] | RightPanelContent | Open AddEquationModal | ❌ Need Modal |
| `sim_expand_advanced` | Advanced ▼ | RightPanelContent | Show integrator/seed | ❌ Not implemented |
| `sim_integrator_[type]` | Integrator | RightPanelContent | Change integrator | ❌ Not implemented |
| `sim_seed_input` | Seed | RightPanelContent | Set random seed | ❌ Not implemented |

---

## 📊 Implementation Status Summary

| Status | Count | Notes |
|--------|-------|-------|
| ✅ Implemented with ID | 4 | HUD play/pause/step/reset |
| ⚠️ Missing ID | 45+ | Need to add data-action-id |
| ❌ Not Implemented | 15+ | Need modal/feature first |

---

## 🎯 Priority Implementation Order

### P0 - Add IDs to Working Buttons (Today)

1. TopNav navigation buttons (6)
2. Panel show/hide buttons (6)
3. Save Snapshot button (1)
4. Export modal buttons (3)

### P1 - Connect Existing UI (This Week)

1. Dimension toggle → Renderer
2. Sliders → Engine

### P2 - Create Missing Modals

1. SettingsModal
2. AddEquationModal

---

## 📝 How to Add action_id

```tsx
<button
    data-action-id="studio_add_equation"
    onClick={handleAddEquation}
>
    + Add Equation
</button>
```

With logging:

```tsx
import { actionLogger } from '@/lib/ActionLogger';

<button
    data-action-id="studio_add_equation"
    onClick={() => {
        actionLogger.log('studio_add_equation');
        handleAddEquation();
    }}
>
    + Add Equation
</button>
```
