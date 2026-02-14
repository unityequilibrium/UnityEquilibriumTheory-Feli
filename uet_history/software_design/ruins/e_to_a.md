# E → A Traceability
## Database/Persistence → UX/UI Intent (Reopen)

---

## 🔗 UX Promise → Database Support

| A: UX Promise | E: DB Support | Status |
|---------------|---------------|--------|
| "See saved projects in Gallery" | projects.* | ✅ |
| "Resume simulation" | runs.worldState | ✅ |
| "See telemetry history" | telemetry.* | ✅ |
| "View notes" | notes.* | ✅ |
| "Remember my settings" | localStorage | ✅ (not DB) |
| "Replay exact same run" | NO seed saved | ❌ |

---

## 🔄 Reopen Flow

```
User opens project from Gallery
    ↓
API loads runs.worldState
    ↓
SimCoreV4.init(worldState)
    ↓
Canvas shows restored state
    ↓
User can resume
```

---

## ⚠️ Gaps

| A Promise | E Missing |
|-----------|-----------|
| Exact replay | No seed saved |
| Same behavior | No determinism guarantee |
