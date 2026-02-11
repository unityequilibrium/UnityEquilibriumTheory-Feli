# B → C Traceability
## Frontend Structure → Backend Contract

---

## 🔗 Action → API Mappings

| B: Action | Calls API? | C: Endpoint |
|-----------|------------|-------------|
| `hud_play` | No | - |
| `hud_pause` | No | - |
| `hud_step_forward` | No | - |
| `hud_reset` | No | - |
| `output_save_snapshot` | Yes | POST /api/runs/[id]/telemetry |
| `output_unit_select_*` | No | - |
| `gallery_load_replay` | No | (nav → /lab?runId=...) |
| `gallery_new_project` | Yes | POST /api/projects |
| `notes_add` | Yes | POST /api/notes |
| `notes_save` | Yes | PATCH /api/notes/[id] |
| `notes_delete` | Yes | DELETE /api/notes/[id] |
| `export_json` | Yes | GET /api/runs/[id]/export |
| `gallery_card_open` | No | GET (on page load) |
| `gallery_add_project` | Yes | POST /api/projects |

---

## ✅ All API Calls Traced

Every frontend action that calls API has corresponding endpoint in C.

---

## ⚠️ Orphan APIs (C without B caller)

| Endpoint | Status |
|----------|--------|
| POST /api/ai/chat | Not used in current UI |
| POST /api/ai/oracle | Not used in current UI |
