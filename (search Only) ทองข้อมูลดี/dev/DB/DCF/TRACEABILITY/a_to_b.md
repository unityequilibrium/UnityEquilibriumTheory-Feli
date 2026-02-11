# A → B Traceability
## UX/UI Intent → Frontend Structure

---

## 🔗 Page Mappings

| A: Page Intent | B: Component |
|----------------|--------------|
| Home page | `app/page.tsx` |
| Gallery page | `app/gallery/page.tsx` |
| Lab page | `app/lab/page.tsx` + `LabShell.tsx` |
| Diagnostics | `app/diagnostics/page.tsx` |

---

## 🔗 Interaction → Component Mappings

| A: Interaction | B: Component | Status |
|----------------|--------------|--------|
| Play simulation | `SimulationHUD` → `hud_play` | ✅ |
| Pause simulation | `SimulationHUD` → `hud_pause` | ✅ |
| Step forward | `SimulationHUD` → `hud_step_forward` | ✅ |
| Reset simulation | `SimulationHUD` → `hud_reset` | ✅ |
| Open Settings | `TopNav` → `platform_settings_open` | ⚠️ No modal |
| Save snapshot | `LeftPanelContent` → `output_save_snapshot` | ⚠️ Missing ID |
| Add equation | `RightPanelContent` → `sim_add_equation` | ❌ No modal |
| Change dt | `RightPanelContent` slider | ⚠️ Missing ID |

---

## ⚠️ Orphan Components (B without A)

| Component | Issue |
|-----------|-------|
| SystemTicker | Not mentioned in UX docs |
| MiniMetricBadge | Not mentioned in UX docs |

---

## ⚠️ Missing Components (A without B)

| A Intent | Missing |
|----------|---------|
| PlatformSettingsModal | Not created |
| AddEquationModal | Not created |
