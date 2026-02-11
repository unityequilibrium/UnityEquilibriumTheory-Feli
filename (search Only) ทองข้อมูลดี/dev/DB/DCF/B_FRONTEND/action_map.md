# Action Map
## Layer B - All Action IDs (Traceable to Engine)

**Version:** 1.1  
**Last Updated:** 2025-12-25  
**Layer:** B (Frontend)

---

## Summary

| Category | Count | Primary Layer |
|----------|-------|---------------|
| Lab Shell | 29 | B/D |
| Simulation HUD | 3 | D |
| Graph Dock | 2 | D |
| GeoSim | 4 | B/D |
| Export Modal | 4 | E |
| Notes | 3 | E |
| Units | 2 | C |
| Room Selector | 2 | B |
| TopNav | 5 | B |
| Gallery | 8 | C/E |
| Canvas/Dev | 10 | B/C/D |
| **Total** | **72** | **Full Stack** |

---

## Lab Shell (Controller Layer)

| action_id | Component | Effect | Layer |
|-----------|-----------|--------|-------|
| `panel_left_hide` | LabShell | Hide left panel | B |
| `panel_left_show` | LabShell | Show left panel | B |
| `panel_right_hide` | LabShell | Hide right panel | B |
| `panel_right_show` | LabShell | Show right panel | B |
| `quick_save_gallery` | LabShell | Quick save to gallery | E |
| `quick_export` | LabShell | Open export modal | B |
| `quick_history` | LabShell | Show history | B |
| `quick_params` | LabShell | Show params | B |
| `quick_initial` | LabShell | Show initial conditions | B |
| `quick_notes` | LabShell | Show notes | B |
| `dock_show` | LabShell | Show graph dock | B |
| `view_canvas` | LabShell | Switch to canvas view | B |
| `view_normal` | LabShell | Switch to normal view | B |
| `output_tab_toggle_metrics` | LabShell | Toggle metrics tab | B |
| `output_tab_toggle_actions` | LabShell | Toggle actions tab | B |
| `output_tab_toggle_history` | LabShell | Toggle history tab | B |
| `output_save_gallery` | LabShell | Save to gallery | E |
| `output_export` | LabShell | Export data | E |
| `studio_tab_toggle_equations` | LabShell | Toggle equations tab | B |
| `studio_tab_toggle_params` | LabShell | Toggle params tab | B |
| `studio_tab_toggle_initial` | LabShell | Toggle initial tab | B |
| `studio_tab_toggle_notes` | LabShell | Toggle notes tab | B |
| `sim_equation_toggle_{id}` | LabShell | Toggle equation | D |
| `sim_equation_role_{id}` | LabShell | Change equation role | D |
| `equation_remove` | LabShell | Remove equation | D |
| `sim_add_equation` | LabShell | Add new equation | D |
| `sim_slider_dt` | LabShell | Adjust dt slider | D |
| `sim_slider_softening` | LabShell | Adjust softening | D |
| `studio_randomize` | LabShell | Randomize initial | D |

---

## Simulation HUD (Runtime Layer)

| action_id | Component | Effect | Layer |
|-----------|-----------|--------|-------|
| `hud_play_pause` | SimulationHUD | Play/pause simulation | D |
| `hud_step_forward` | SimulationHUD | Step forward | D |
| `hud_reset` | SimulationHUD | Reset simulation | D |

---

## Graph Dock (Flow Layer)

| action_id | Component | Effect | Layer |
|-----------|-----------|--------|-------|
| `dock_hide` | GraphDock | Hide graph dock | B |
| `dock_clear` | GraphDock | Clear graphs | D |

---

## GeoSim (Specialized Layer)

| action_id | Component | Effect | Layer |
|-----------|-----------|--------|-------|
| `geosim_zoom_in` | GeoSimCanvas | Zoom in map | B |
| `geosim_zoom_out` | GeoSimCanvas | Zoom out map | B |
| `geosim_center` | GeoSimCanvas | Center map | B |
| `geosim_toggle_layer` | GeoSimCanvas | Toggle layer | D |

---

## Export & Notes (Persistence Layer)

| action_id | Component | Effect | Layer |
|-----------|-----------|--------|-------|
| `export_csv` | ExportModal | Export as CSV | E |
| `export_json` | ExportModal | Export as JSON | E |
| `notes_delete_{id}` | NotesTab | Delete note | E |

---

## Modals (Traceability Layer)

| action_id | Component | Effect | Layer |
|-----------|-----------|--------|-------|
| `add_equation_close` | AddEquationModal | Close modal | B |
| `add_equation_filter_{cat}`| AddEquationModal | Filter equations | B |
| `add_equation_select_{id}`| AddEquationModal | Select equation | B |
| `add_equation_cancel` | AddEquationModal | Cancel addition | B |
| `add_equation_confirm` | AddEquationModal | Confirm addition | D |
| `platform_settings_close` | PlatformSettingsModal | Close settings | B |
| `settings_theme_{theme}` | PlatformSettingsModal | Change theme | B |
| `settings_ui_scale` | PlatformSettingsModal | Adjust UI scale | B |
| `settings_show_fps` | PlatformSettingsModal | Toggle FPS counter | B |
| `settings_autosave` | PlatformSettingsModal | Adjust autosave | B |
| `settings_telemetry_history`| PlatformSettingsModal| Adjust history size| B |
| `settings_reset` | PlatformSettingsModal | Reset defaults | B |
| `settings_done` | PlatformSettingsModal | Save and close | B |
| `modal_smart_close` | SmartSettingsModal | Close modal | B |
| `smart_dt_adjust` | SmartSettingsModal | Toggle auto-dt | B |
| `smart_target_fps` | SmartSettingsModal | Select target FPS | B |
| `smart_nan_detect` | SmartSettingsModal | Toggle NaN detect | B |
| `smart_graph_autoscale` | SmartSettingsModal | Toggle autoscale | B |
| `smart_anomaly_highlight` | SmartSettingsModal | Toggle highlight | B |
| `modal_smart_apply` | SmartSettingsModal | Apply settings | B |
| `modal_preset_close` | PresetPreviewModal | Close preview | B |
| `modal_preset_launch` | PresetPreviewModal | Launch preset | D |

---

## Canvas & Audit (System Layer)

| action_id | Component | Effect | Layer |
|-----------|-----------|--------|-------|
| `graph_save` | CanvasView | Persist graph to DB | C→E |
| `graph_load_latest` | CanvasView | Restore latest graph | C→E |
| `ai_chat_send` | AIChatNode | Send message to AI | C→D |
| `dev_node_select` | DevPage | Inspect system module | B |
| `dev_refresh` | DevPage | Rescan dependencies | D |

---

## Traceability Links

| Level | Document |
|-------|----------|
| **Matrix** | [TRACEABILITY_MATRIX.md](./TRACEABILITY_MATRIX.md) |
| **Rules** | [global_rules.md](./global_rules.md) |
| **API** | [C_BACKEND/api_contract.md](../C_BACKEND/api_contract.md) |

---

**Status:** ✅ AUDIT READY
