# Global Rules (Immutable)
## UET Platform - Rules That Cannot Be Violated

**Last Updated:** 2025-12-25  
**Status:** 🔒 LOCKED - ห้ามแก้ไขโดยไม่มี explicit approval

---

## 🏗️ R1: Platform Structure

### R1.1 Three Pages Only

```
/           → Home (3D portal)
/gallery    → Gallery (project browser)
/lab        → Lab (simulation workspace)
/dev        → Dev (system audit)
```

**❌ Forbidden:**
- สร้าง route ใหม่ (e.g., /demo, /test, /sandbox)
- สร้าง page ที่ไม่อยู่ในรายการ
- สร้าง "โลกแยก" สำหรับ features

### R1.2 Lab = One Shell

```
/lab ใช้ LabShell.tsx เท่านั้น
ทุกห้อง (room) render ใน shell เดียว
ห้ามสร้าง shell ใหม่สำหรับ room types ต่าง ๆ
```

### R1.3 Room Registry

```
ทุกห้องต้องอยู่ใน roomRegistry
ห้ามมีห้องที่ hardcode
Room types: test_lab, sim_3d (future: more)
```

### R1.4 Preset Registry

```
ทุก simulation preset ต้องอยู่ใน presetRegistry
ห้ามสร้าง preset นอก registry
Families: extension, archetype, physics, toy, 3d
Total: 62 presets (ref: gallery.html)
```

### R1.5 Controller Pattern (Overlays)

```
Nodes (Actors) = Live in Graph (Canvas)
Panels (Controllers) = Live in UI (Overlay)
Panels ACT upon Nodes via RPC/Store.
Panels are NOT Nodes.
```

---

## 🔘 R2: Button & Action Rules

### R2.1 Every Button Has action_id

```tsx
// ❌ WRONG
<button onClick={handleClick}>Click</button>

// ✅ CORRECT
<button 
  data-action-id="studio_add_equation"
  onClick={handleClick}
>
  Click
</button>
```

### R2.2 Every action_id Has Expected Effect

```
action_id → expected_effect → documented in BUTTON_ACTION_IDS.md
```

**No dead buttons allowed** - ทุกปุ่มต้องมีผลลัพธ์

### R2.3 Action Logging

```
ทุก action ต้อง loggable
actionLogger.log(action_id) ก่อน execute
```

---

## 💾 R3: Panel Ownership

### R3.1 Save/Export Location

```
Save Snapshot → Output Panel (Left) ONLY
Export JSON/CSV → Export Modal ONLY
ห้ามมี Save ที่อื่น
```

### R3.2 Input Location

```
Simulation params → Studio Panel (Right) ONLY
ห้ามปรับ sim params ใน Settings Modal
Settings Modal = read-only verification
```

---

## 🎲 R4: Determinism

### R4.1 Reproducibility Guarantee

```
Same input + Same seed = Same output
ทุกครั้ง ไม่มีข้อยกเว้น
```

### R4.2 Seed Management

```
1. Generate seed on run create
2. Save seed with run in DB
3. Use seed for all RNG
4. Restore seed on replay
```

### R4.3 Forbidden Non-determinism

```
❌ Math.random() without seed
❌ Date.now() in calculations
❌ External API in simulation loop
```

---

## 📊 R5: State Ownership

### R5.1 Single Source of Truth

| Data | Owner | Secondary | Persistence |
|------|-------|-----------|-------------|
| particles | SimCoreV4 | simStore | DB |
| equations | simStore | SimCoreV4 | DB |
| dt | simStore | SimCoreV4 | DB |
| panel states | LayoutContext | None | None |
| theme | localStorage | None | localStorage |

### R5.2 No Duplicate State

```
ห้ามมี state เดียวกันอยู่หลายที่
ถ้าจะ sync → ต้องระบุ owner ชัด
```

---

## 💽 R6: Persistence

### R6.1 Must Save

```
✅ worldState (particles, time, step)
✅ equations config
✅ seed
✅ notes
```

### R6.2 Must NOT Save

```
❌ panel open/close states
❌ theme preference (use localStorage)
❌ camera position (optional)
❌ animation frame state
```

### R6.3 Save Before Navigate

```
ถ้ามี unsaved changes → prompt user
ห้าม silent discard
```

---

## 🧪 R7: Testing

### R7.1 Gate Levels

```
L0: Static (compile)
L1: Runtime (start)
L2: Unit (logic)
L3: Integration (API)
L4: E2E (flow)
L5: Production (monitor)
```

### R7.2 Gate Requirements

```
L0 ต้องผ่านก่อน commit
L1-L2 ต้องผ่านก่อน PR
L3-L4 ต้องผ่านก่อน release
```

---

## 📝 R8: Documentation

### R8.1 Doc First

```
Doc ก่อน Code เสมอ
ถ้า Doc ไม่มี → ห้าม implement
```

### R8.2 No Orphan Features

```
ทุก feature ต้องถูก trace A → E
Feature ที่อยู่แค่ชั้นเดียว = orphan = ต้องแก้
```

### R8.3 DCF Compliance

```
ทุก doc ต้องอยู่ใน DCF layer
A/B/C/D/E ต้องครบ
Traceability ต้องชัดตาม [TRACEABILITY_MATRIX.md](./TRACEABILITY_MATRIX.md)
```

### R8.4 Traceability Matrix (A-E)

Any feature MUST map to all layers:

| Feature | A (UX) | B (UI) | C (API) | D (Engine) | E (DB) |
|:---|:---|:---|:---|:---|:---|
| **Graph Persistence** | Lifecycle | CanvasView | `/graphs` | GraphSpec | `NodeGraph` |
| **Simulation Run** | HUD/Output | SimHUD | `/runs` | SimCore | `Run` |
| **Telemetry** | Charts | MetricNode | `/telemetry` | MetricStream | `Sample` |

---

## 💻 R9: System Health

### R9.1 Disk Space Requirement

```
Minimum free disk space: 500MB
ถ้าน้อยกว่า → dev server จะ fail (ENOSPC)
ตรวจสอบด้วย: Get-PSDrive C | Select-Object Free
```

### R9.2 Pre-flight Check

```
ก่อนรัน dev server ต้องตรวจสอบ:
✅ Disk space > 500MB
✅ Port 3000 available
✅ PostgreSQL running (port 5432)
✅ Runtime: Bun installed
```

### R9.3 ENOSPC Recovery

```
ถ้าเจอ ENOSPC:
1. หยุด dev server
2. ลบ frontend/.next
3. เคลียร์ %TEMP%
4. รัน `bun run dev --filter frontend` ใหม่
```

---

## 🚫 Violations

**ถ้าละเมิด Global Rules:**

1. ❌ Code จะถูก reject
2. ❌ PR จะไม่ผ่าน
3. ❌ Feature จะถูก revert

**Process:**
1. Flag violation
2. Document in CHANGELOG
3. Create fix ticket
4. Revert if necessary

---

**🔒 Status: LOCKED**  
**Approvers:** System Architect + Lead Developer
