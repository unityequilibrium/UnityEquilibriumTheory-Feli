# D → E Traceability
## Flow/Engine Logic → Database/Persistence

---

## 🔗 Engine Data → Database Mappings

| D: Engine Data | E: Database Field | Persisted? |
|----------------|-------------------|------------|
| worldState.particles | runs.worldState.particles | ✅ |
| worldState.time | runs.worldState.time | ✅ |
| worldState.step | runs.worldState.step | ✅ |
| equations[] | runs.equations | ✅ |
| telemetry snapshot | telemetry.metrics | ✅ |
| dt setting | runs.equations (embedded) | ✅ In config |
| softening | runs.metadata | ⚠️ Should persist |
| seed | runs.seed (BigInt) | ✅ Persisted |

---

## ⚠️ Gaps

| D Uses | E Stores? | Issue |
|--------|-----------|-------|
| initial conditions | Only current | No step-0 snapshot |
| parameter history | No | No audit trail |
