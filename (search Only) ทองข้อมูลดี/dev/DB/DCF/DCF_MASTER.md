# Documentary Consistency Framework (DCF)
## UET Platform - Master Documentation Standard v1.0

> **กฎเหล็ก:** Doc ที่ไม่ผ่าน DCF = ห้ามเขียนแผน/โค้ด  
> **หลักคิด:** A → B → C → D → E ต้องไหลต่อเนื่อง ไม่ขัดแย้ง

---

## 📚 The A → E Framework

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DOCUMENTATION CONSISTENCY FRAMEWORK                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  │
│   │    A    │───▶│    B    │───▶│    C    │───▶│    D    │───▶│    E    │  │
│   │  UX/UI  │    │Frontend │    │Backend  │    │  Flow   │    │Database │  │
│   │ Intent  │    │Structure│    │Contract │    │ Engine  │    │Persist  │  │
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘  │
│        │                                                              │      │
│        └───────────────────── E → A ────────────────────────────────┘      │
│                        (Replay / Reopen verification)                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Layer Definitions

### A — UX / UI INTENT

> **คำถาม:** ผู้ใช้คิดอะไร / เห็นอะไร / ทำอะไรได้

| Covers | Examples |
|--------|----------|
| User expectations | "ผู้ใช้คาดหวังว่า..." |
| Page layouts | Home, Gallery, Lab layouts |
| Interactions | Click, drag, hover behaviors |
| Forbidden actions | "ห้ามทำ X เมื่อ Y" |

### B — FRONTEND STRUCTURE

> **คำถาม:** Component อะไร / State อะไร / Action อะไร

| Covers | Examples |
|--------|----------|
| Components | TopNav, LabShell, SimulationHUD |
| State management | Zustand stores, Context |
| Action IDs | data-action-id values |
| Layout constants | Widths, z-indices |

### C — BACKEND CONTRACT

> **คำถาม:** API อะไร / Validate อะไร / Return อะไร

| Covers | Examples |
|--------|----------|
| API endpoints | /api/runs, /api/projects |
| Request schemas | Body, params, headers |
| Response schemas | Success, error formats |
| Validation rules | Required fields, ranges |

### D — FLOW / ENGINE LOGIC

> **คำถาม:** ข้อมูลไหลยังไง / Engine ทำอะไร / Determinism

| Covers | Examples |
|--------|----------|
| Data flow | Input → Engine → Output |
| Simulation logic | SimCoreV4, equations |
| Test gates | L0-L5 verification |
| Determinism | Same input = same output |

### E — DATABASE / PERSISTENCE

> **คำถาม:** เก็บอะไร / ไม่เก็บอะไร / Replay ได้ไหม

| Covers | Examples |
|--------|----------|
| Schema | Tables, columns, types |
| Persistence policy | What to save, when |
| Replay rules | How to restore state |
| History | What's tracked |

---

## 📁 Required Directory Structure

```
docs/
├── DCF/                          # Documentary Consistency Framework
│   ├── DCF_MASTER.md             # This file
│   ├── DCF_AUDIT.md              # Verification results
│   └── DCF_CHANGELOG.md          # Changes across layers
│
├── A_UX_UI/
│   ├── intent.md                 # User expectations
│   ├── page_map.md               # All pages and layouts
│   ├── interaction_rules.md      # Click/drag/hover behaviors
│   └── forbidden_actions.md      # Things users cannot do
│
├── B_FRONTEND/
│   ├── component_map.md          # All components
│   ├── state_model.md            # Zustand/Context state
│   ├── action_map.md             # All action_ids
│   └── layout_contract.md        # Layout constants
│
├── C_BACKEND/
│   ├── api_contract.md           # All API endpoints
│   ├── validation_rules.md       # Input validation
│   └── error_handling.md         # Error responses
│
├── D_FLOW_ENGINE/
│   ├── flow_diagram.md           # Data flow diagrams
│   ├── runner_logic.md           # Simulation runner
│   ├── test_gate_logic.md        # L0-L5 gates
│   └── determinism_rules.md      # Reproducibility rules
│
├── E_DATABASE/
│   ├── schema.md                 # DB schema
│   ├── persistence_policy.md     # What to persist
│   └── replay_rules.md           # How to replay/restore
│
└── TRACEABILITY/
    ├── a_to_b.md                 # UX → Frontend mapping
    ├── b_to_c.md                 # Frontend → Backend mapping
    ├── c_to_d.md                 # Backend → Engine mapping
    ├── d_to_e.md                 # Engine → Database mapping
    └── e_to_a.md                 # Database → UX (reopen) mapping
```

---

## ✅ Verification Phases

### Phase V1: A ↔ B (UX/UI ↔ Frontend)

**คำถาม:**
- ทุก interaction ใน A มี component ใน B?
- ทุกปุ่มใน A มี action_id ใน B?
- **มี component ใน B ที่ไม่มีใน A ไหม?** (อันตราย!)

**Checklist:**
```
□ A ระบุปุ่ม/interaction ครบ
□ B มี component รองรับทุกอัน
□ ไม่มี component "ลอย ๆ" ที่ A ไม่เคยพูดถึง
```

❌ **FAIL:** B มีของที่ A ไม่พูด = Doc ไม่สอดคล้อง

---

### Phase V2: B ↔ C (Frontend ↔ Backend)

**คำถาม:**
- ทุก action ใน B ยิง API ไหม?
- ถ้ายิง → C มี API รองรับ?
- ถ้าไม่ยิง → ต้องระบุว่า local-only

**Checklist:**
```
□ ทุก action ใน B ระบุ destination (local / API)
□ ทุก API ใน C มี caller ใน B
□ ไม่มี API ที่ "ไม่รู้ว่าใครเรียก"
```

❌ **FAIL:** API ที่ไม่มี caller = เอกสารมั่ว

---

### Phase V3: C ↔ D (Backend ↔ Flow/Engine)

**คำถาม:**
- Backend ทำหน้าที่อะไร?
- Flow/Engine ทำหน้าที่อะไร?
- ใครเป็น source of truth?

**Checklist:**
```
□ ทุก API ใน C ชี้ไป logic ใน D
□ D ไม่รับ input ที่ C ไม่ validate
□ Rule สำคัญ (determinism, gate) ถูกพูดตรงกัน
```

❌ **FAIL:** C กับ D พูดคนละเรื่อง = ระบบพังแน่นอน

---

### Phase V4: D ↔ E (Flow ↔ Database)

**คำถาม:**
- Flow ไหนต้อง persist?
- Flow ไหนห้าม persist?
- Replay เอาข้อมูลจากไหน?

**Checklist:**
```
□ ทุก persistence decision ใน D มีคำตอบใน E
□ ไม่มีข้อมูลสำคัญที่ D ใช้ แต่ E ไม่เก็บ
□ Replay rules เขียนชัด
```

❌ **FAIL:** D ใช้ข้อมูลที่ E ไม่เก็บ = Replay พัง

---

### Phase V5: E ↔ A (Database ↔ UX/UI)

**คำถาม:**
- UX บอกว่าผู้ใช้ "จะเห็นอะไรตอนกลับมา"?
- DB เก็บพอไหมให้ UX แสดงสิ่งนั้น?

**Checklist:**
```
□ UX ทุก requirement มี field รองรับใน DB
□ ไม่มีข้อมูลใน DB ที่ UX ไม่เคยใช้เลย
□ History / Gallery / Reopen อธิบายได้จาก Doc
```

❌ **FAIL:** UX สัญญา แต่ DB เก็บไม่ครบ = โกหกผู้ใช้

---

## 🔗 Transitive Consistency (A → C → E)

**ตัวอย่าง:**
```
UX บอก: "ปุ่มนี้จำค่าได้"
   → Backend มี API save ไหม?
   → DB เก็บ field นี้จริงไหม?
```

**Checklist:**
```
□ A → C semantics ตรงกัน
□ C → E semantics ตรงกัน
□ A → E ไม่ขัดกัน
```

⚠️ **ถ้า A↔B ผ่าน, B↔C ผ่าน แต่ A↔E พัง = เอกสารยังใช้ไม่ได้**

---

## 🚦 Documentary Gate

### DOC PASS CRITERIA

เอกสารจะถือว่า "พร้อมไป implement" ก็ต่อเมื่อ:

```
✔ A–B–C–D–E ครบทุกส่วน
✔ ทุก Phase V1–V5 ผ่าน
✔ ไม่มี orphan concept (สิ่งที่อยู่แค่ชั้นเดียว)
✔ ไม่มี contradiction ระหว่างชั้น
```

### DOC FAIL = STOP

```
❌ ถ้าไม่ผ่าน → ห้ามเขียนแผน
❌ ถ้าไม่ผ่าน → ห้ามเขียนโค้ด
❌ ต้องแก้ Doc ก่อน
```

---

## 📊 Current Status Mapping

### Existing Docs → DCF Layers

| Existing Doc | DCF Layer | Status |
|--------------|-----------|--------|
| UI_BLUEPRINT.md | A | ⚠️ Partial |
| LAB_UI_DESIGN_SPEC.md | A + B | ⚠️ Mixed |
| COMPONENT_REGISTRY.md | B | ⚠️ Partial |
| BUTTON_ACTION_IDS.md | B | ✅ Good |
| SETTINGS_CONTRACT.md | B | ✅ Good |
| API_REFERENCE.md | C | ✅ Good |
| BACKEND_ARCHITECTURE.md | C + D | ⚠️ Mixed |
| SMART_SIMULATION_DESIGN.md | D | ⚠️ Partial |
| DATABASE_SCHEMA.md | E | ✅ Good |
| TRACEABILITY | - | ❌ Missing |

---

## 🎯 Action Items

### P0 - Create Missing Docs

1. [ ] `A_UX_UI/intent.md`
2. [ ] `A_UX_UI/forbidden_actions.md`
3. [ ] `D_FLOW_ENGINE/determinism_rules.md`
4. [ ] `E_DATABASE/replay_rules.md`
5. [ ] All TRACEABILITY docs

### P1 - Reorganize Existing

1. [ ] Split mixed docs (LAB_UI_DESIGN_SPEC → A + B)
2. [ ] Move content to correct layers
3. [ ] Add cross-references

### P2 - Run Verification

1. [ ] Phase V1: A ↔ B
2. [ ] Phase V2: B ↔ C
3. [ ] Phase V3: C ↔ D
4. [ ] Phase V4: D ↔ E
5. [ ] Phase V5: E ↔ A

---

**Last Updated:** 2024-12-24
**Version:** 1.0
