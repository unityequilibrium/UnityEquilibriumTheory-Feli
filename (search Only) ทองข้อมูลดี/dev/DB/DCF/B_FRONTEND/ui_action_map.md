# UI Action Map (Complete)
## UET Platform - All Buttons & Actions

**Last Updated:** 2024-12-24  
**Layer:** B (Frontend)  
**Total Actions:** 67

---

## 📊 Summary

| Area | Count | Has action_id | Status |
|------|-------|---------------|--------|
| TopNav | 7 | 7 | ✅ |
| HUD | 7 | 7 | ✅ |
| Panel Controls | 6 | 6 | ✅ |
| Studio (Right Panel) | 12 | 12 | ✅ |
| Output (Left Panel) | 3 | 3 | ✅ |
| Dock | 8 | 8 | ✅ |
| Export Modal | 4 | 4 | ✅ |
| Notes | 5 | 5 | ✅ |
| Home | 5 | 5 | ✅ |
| Gallery | 10 | 10 | ✅ |
| **Total** | **67** | **67** | **✅** |

---

## 🔝 TopNav Actions

| action_id | Label | Location | Effect | States | Owner |
|-----------|-------|----------|--------|--------|-------|
| `topnav_logo_home` | UET Logo | TopNav left | Navigate to / | normal, hover | A |
| `topnav_nav_home` | HOME | TopNav center | Navigate to / | normal, hover, active | A |
| `topnav_nav_gallery` | GALLERY | TopNav center | Navigate to /gallery | normal, hover, active | A |
| `topnav_nav_lab` | LAB | TopNav center | Navigate to /lab | normal, hover, active | A |
| `topnav_nav_diagnostics` | DIAGNOSTICS | TopNav center | Navigate to /diagnostics | normal, hover, active | A |
| `topnav_export` | EXPORT | TopNav right | Open ExportModal | normal, hover, disabled | B |
| `platform_settings_open` | ⚙️ | TopNav right | Open PlatformSettingsModal | normal, hover | B |

---

## 🎮 HUD Actions

| action_id | Label | Location | Effect | States | Owner |
|-----------|-------|----------|--------|--------|-------|
| `hud_play` | ▶ | HUD center | Start simulation | normal, active | D |
| `hud_pause` | ⏸ | HUD center | Pause simulation | normal, active | D |
| `hud_step_forward` | ⏭ | HUD center | Single step | normal, disabled | D |
| `hud_reset` | ⟲ | HUD center | Reset to initial | normal, disabled | D |
| `hud_dimension_2d` | 2D | HUD center | Switch to 2D view | normal, selected | B |
| `hud_dimension_3d` | 3D | HUD center | Switch to 3D view | normal, selected | B |
| `hud_dimension_4d` | 4D | HUD center | Switch to 4D view | normal, selected | B |

---

## 📋 Panel Control Actions

| action_id | Label | Location | Effect | States | Owner |
|-----------|-------|----------|--------|--------|-------|
| `panel_left_hide` | [◀ HIDE] | Left Panel header | Close left panel | normal | B |
| `panel_left_show` | [▶ SHOW OUTPUT] | Left edge | Open left panel | normal | B |
| `panel_right_hide` | [HIDE ▶] | Right Panel header | Close right panel | normal | B |
| `panel_right_show` | [◀ SHOW STUDIO] | Right edge | Open right panel | normal | B |
| `dock_show` | [▲ SHOW GRAPHS] | Bottom edge | Open bottom dock | normal | B |
| `dock_hide` | [▼ HIDE] | Dock header | Close bottom dock | normal | B |

---

## 🔬 Studio (Right Panel) Actions

| action_id | Label | Location | Effect | States | Owner |
|-----------|-------|----------|--------|--------|-------|
| `sim_add_equation` | [+ Add Equation] | Studio header | Open AddEquationModal | normal, hover | B |
| `sim_equation_toggle_{id}` | Checkbox | Equation row | Enable/disable equation | checked, unchecked | D |
| `sim_equation_role_{id}` | Dropdown | Equation row | Change equation role | normal | D |
| `sim_equation_remove_{id}` | × | Equation row | Remove equation | normal, hover | D |
| `sim_slider_dt` | DT Slider | Quick Params | Change time step | normal, dragging | D |
| `sim_slider_softening` | Softening | Quick Params | Change softening | normal, dragging | D |
| `sim_slider_speed` | Speed | Quick Params | Change playback speed | normal, dragging | D |
| `sim_param_{key}` | Param input | Smart Params | Change equation param | normal, editing | D |
| `sim_expand_advanced` | Advanced ▼ | Studio footer | Show/hide advanced | collapsed, expanded | B |
| `sim_integrator_select` | Integrator | Advanced | Change integrator | normal | D |
| `sim_seed_input` | Seed | Advanced | Set random seed | normal, editing | D |
| `sim_seed_randomize` | 🎲 | Advanced | Generate new seed | normal | D |

---

## 📊 Output (Left Panel) Actions

| action_id | Label | Location | Effect | States | Owner |
|-----------|-------|----------|--------|--------|-------|
| `output_save_snapshot` | 💾 Save Snapshot | Output header | Save run to DB | normal, loading | C |
| `output_metric_toggle_{metric}` | Checkbox | Metric list | Show/hide metric | checked, unchecked | B |
| `output_metric_expand_{metric}` | Metric row | Metric list | Expand metric details | collapsed, expanded | B |

---

## 📈 Dock Actions

| action_id | Label | Location | Effect | States | Owner |
|-----------|-------|----------|--------|--------|-------|
| `dock_clear` | × Clear | Dock header | Clear telemetry | normal | D |
| `dock_tab_live` | Live Graph | Dock tabs | Show live telemetry | selected, unselected | B |
| `dock_tab_energy` | Energy | Dock tabs | Show energy graph | selected, unselected | B |
| `dock_tab_momentum` | Momentum | Dock tabs | Show momentum graph | selected, unselected | B |
| `dock_tab_phase` | Phase Space | Dock tabs | Show phase plot | selected, unselected | B |
| `dock_toggle_{metric}` | Metric line | Legend | Toggle line visibility | visible, hidden | B |
| `dock_export` | Export | Dock header | Export graph data | normal | C |
| `dock_fullscreen` | ⛶ | Dock header | Expand dock | normal, expanded | B |

---

## 📤 Export Modal Actions

| action_id | Label | Location | Effect | States | Owner |
|-----------|-------|----------|--------|--------|-------|
| `export_json` | Export JSON | Modal | Download run as JSON | normal, loading | C |
| `export_csv` | Export CSV | Modal | Download telemetry CSV | normal, loading | C |
| `export_png` | Export PNG | Modal | Save canvas as image | normal, loading | B |
| `export_close` | × | Modal | Close modal | normal | B |

---

## 📝 Notes Actions

| action_id | Label | Location | Effect | States | Owner |
|-----------|-------|----------|--------|--------|-------|
| `notes_add` | + NEW NOTE | Notes section | Create new note | normal | C |
| `notes_select_{id}` | Note item | Note list | Select note | normal, selected | B |
| `notes_save` | Save | Note editor | Save note to DB | normal, loading, disabled | C |
| `notes_delete_{id}` | Delete | Note editor | Delete note | normal, confirm | C |
| `notes_cancel` | Cancel | Note editor | Cancel editing | normal | B |

---

## 🏠 Home Page Actions

| action_id | Label | Location | Effect | States | Owner |
|-----------|-------|----------|--------|--------|-------|
| `home_quickstart_solar` | Solar System | Quick Start | Open lab with solar | normal, hover | A |
| `home_quickstart_galaxy` | Galaxy | Quick Start | Open lab with galaxy | normal, hover | A |
| `home_quickstart_custom` | Custom | Quick Start | Open lab blank | normal, hover | A |
| `home_quickstart_tutorial` | Tutorial | Quick Start | Open tutorial | normal, hover | A |
| `home_recent_{id}` | Recent project | Recent section | Open project | normal, hover | A |

---

## 🖼️ Gallery Page Actions

| action_id | Label | Location | Effect | States | Owner |
|-----------|-------|----------|--------|--------|-------|
| `gallery_add_project` | + New Project | Gallery header | Open create modal | normal | C |
| `gallery_search` | Search | Gallery header | Filter projects | normal, active | B |
| `gallery_filter_all` | All | Filter tabs | Show all projects | selected, unselected | B |
| `gallery_filter_{category}` | Category | Filter tabs | Filter by category | selected, unselected | B |
| `gallery_sort_select` | Sort dropdown | Gallery header | Change sort order | normal | B |
| `gallery_card_open_{id}` | Project card | Card grid | Open in Lab | normal, hover | A |
| `gallery_card_menu_{id}` | ⋮ | Card | Open card menu | normal | B |
| `gallery_card_rename_{id}` | Rename | Card menu | Rename project | normal | C |
| `gallery_card_duplicate_{id}` | Duplicate | Card menu | Copy project | normal, loading | C |
| `gallery_card_delete_{id}` | Delete | Card menu | Delete project | normal, confirm | C |

---

## 📋 Owner Legend

| Owner | Description |
|-------|-------------|
| A | UX/UI only (navigation, selection) |
| B | Frontend state change |
| C | Backend API call |
| D | Engine/Flow logic |
| E | Database persistence |

---

**Status:** ✅ All 67 actions documented
