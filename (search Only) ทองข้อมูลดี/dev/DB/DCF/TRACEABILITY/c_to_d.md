# C → D Traceability
## Backend Contract → Flow/Engine Logic

---

## 🔗 API → Engine Mappings

| C: Endpoint | D: Engine Logic |
|-------------|-----------------|
| POST /api/runs (create) | DB insert only |
| PATCH /api/runs (save) | Read from SimCoreV4.worldState |
| GET /api/runs/[id] | Returns saved worldState |
| (Frontend) Play | SimCoreV4.run() |
| (Frontend) Pause | SimCoreV4.pause() |
| (Frontend) Step | SimCoreV4.step() |
| (Frontend) Reset | SimCoreV4.reset() |

---

## 📍 Source of Truth

| Data | Source of Truth |
|------|-----------------|
| Live worldState | SimCoreV4 (runtime) |
| Saved worldState | Database (persisted) |
| Equations config | simStoreV4 (runtime) |

---

## ⚠️ Gaps

| Issue | Status |
|-------|--------|
| Determinism rules | Not validated in API |
| Seed management | Not implemented |
