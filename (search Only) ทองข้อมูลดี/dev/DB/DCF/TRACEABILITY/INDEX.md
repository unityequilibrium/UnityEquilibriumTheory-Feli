# TRACEABILITY
## Cross-Layer Mapping Documents

> **Purpose:** พิสูจน์ว่า A→B→C→D→E ไหลต่อเนื่อง ไม่มี orphan concepts

---

## 📁 Documents in this Layer

| Document | Purpose |
|----------|---------|
| [a_to_b.md](a_to_b.md) | UX → Frontend mapping |
| [b_to_c.md](b_to_c.md) | Frontend → Backend mapping |
| [c_to_d.md](c_to_d.md) | Backend → Engine mapping |
| [d_to_e.md](d_to_e.md) | Engine → Database mapping |
| [e_to_a.md](e_to_a.md) | Database → UX (reopen) mapping |

---

## ✅ Verification Status

| Phase | Check | Status | Updated |
|-------|-------|--------|---------|
| V1 | A ↔ B | ✅ Pass | 2024-12-24 |
| V2 | B ↔ C | ✅ Pass | 2024-12-24 |
| V3 | C ↔ D | ✅ Pass | 2024-12-24 |
| V4 | D ↔ E | ✅ Pass | 2024-12-24 |
| V5 | E ↔ A | ✅ Pass | 2024-12-24 |

> ✅ **All layers verified.** 

---

## 🆕 Preset Registry Mapping

| Flow | Path | Status |
|------|------|--------|
| gallery.html → presetRegistry | 62 presets | ✅ |
| presetRegistry → SimCore | equations[] | ✅ |
| preset.id → SIM_INITIALIZED | event payload | ✅ |
| Global R1.4 | Registry rule | ✅ |

---

## 📐 Equation Module Mapping

| Category | Implemented | Spec | Status |
|----------|-------------|------|--------|
| Core | 3 (newton, einstein, uet) | 3 | ✅ |
| Extensions | 6 | 6 | ✅ |
| Physics | 4 | 4 | ✅ |
| Toys | 11 | 11 | ✅ |
| 3D | 1 | 1 | ✅ |
| **Total** | **26** | **26** | ✅ |

---

## 🖼️ Canvas Node Module Mapping (NEW)

| Layer | Doc | Content | Status |
|-------|-----|---------|--------|
| A | canvas_view_toggle.md | Toggle UX spec | ✅ |
| B | button_action_ids.md | action_id map | ✅ |
| C | canvas_chat_api.md | AI Chat API contract | ✅ |
| D | telemetry_service.md | Real-time updates | ✅ |
| D | node_canvas_architecture.md | Node system design | ✅ |
| REG | graph_presets_spec.md | Room → Graph presets | ⚠️ 2/62 |

### Canvas Flow

```
A (Toggle UX) → B (action_id) → C (API) → D (Telemetry) → E (N/A)
                                       ↓
                              D (NodeSpec) → E (Persistence)
```

---

## 🔄 Cross-Reference

See [DCF_AUDIT.md](../DCF_AUDIT.md) for detailed verification results.


