# Change Management & Doc-First Workflow
## UET Platform - Development Process Standard v1.0

> **กติกาเหล็ก:** Doc เป็นของจริง โค้ดเป็นการ "implement doc"  
> ทุก change ต้องมี Change ID และ "บันทึกใน Doc" ก่อน

---

## 📋 Iron Rules

1. **Doc เป็น Source of Truth** - โค้ดเป็นการ implement doc
2. **ทุก change ต้องมี Change ID** และบันทึกใน Doc ก่อน
3. **ห้ามสร้างโลกใหม่** (route/page/demo) ถ้า doc ไม่สั่ง
4. **ทุกปุ่มต้องมี action_id** และ expected_effect ตั้งแต่ใน Doc
5. **เปลี่ยน UX/UI = อัปเดต Design Tokens / Component Contract ใน Doc ก่อนเสมอ**

---

## 🔄 Change Flow (Doc-First - 2 รอบ)

### รอบ 1: Update Doc (ก่อนแตะโค้ด)

#### 1.1 Change Card (บังคับทุก change)

```markdown
## CHG-XXX: [Short Title]

| Field | Value |
|-------|-------|
| **Change ID** | CHG-XXX |
| **Change Type** | UI/Interaction \| Setting \| Layout \| Data flow \| API \| DB |
| **What** | เพิ่ม/ย้าย/เปลี่ยนอะไร (1-2 บรรทัด) |
| **Why** | ทำเพื่ออะไร |
| **Where** | หน้าไหน/ส่วนไหน (Home/Lab/Gallery + panel ไหน) |
| **Buttons/Controls** | รายการปุ่ม/ฟิลด์ที่จะเพิ่ม/แก้ |
| **DoD** | เสร็จคือเห็นอะไร/กดแล้วเกิดอะไร |
| **Risks** | มีอะไรพังได้ |
```

#### 1.2 UX Spec Update (ตำแหน่ง + พฤติกรรม)

| Field | Description |
|-------|-------------|
| **Location** | TopNav / Left / Right / HUD / Dock |
| **Label** | ชื่อที่แสดง |
| **action_id** | data-action-id value |
| **expected_effect** | กดแล้วเกิดอะไร |
| **States** | disabled / loading / error |
| **Constraints** | ข้อห้าม (เช่น Save/Export ต้องอยู่ Output เท่านั้น) |

#### 1.3 Component Contract Update (สำหรับ Setting)

| Field | Description |
|-------|-------------|
| **setting_key** | เช่น `sim.integrator` หรือ `ui.dock.open` |
| **type** | boolean / enum / number / string |
| **default** | ค่าเริ่มต้น |
| **validation/range** | ขอบเขตที่ยอมรับ |
| **applies_to** | room type ไหน (sim3d / test_terminal / both) |
| **persistence** | เก็บไหม (DB / local / none) |

---

### รอบ 2: Implement ตาม Doc

#### Checklist (แตะเท่าที่เกี่ยว)

##### A) UX/UI ↔ FE
- [ ] เพิ่ม UI element ตามตำแหน่งใน doc
- [ ] ใส่ `data-action-id` + log event ได้
- [ ] กดแล้ว state เปลี่ยนตาม expected_effect
- [ ] ไม่เพิ่ม route/page ใหม่ถ้า doc ไม่สั่ง

##### B) FE ↔ BE (ถ้า setting ต้องเรียก backend)
- [ ] endpoint มี/ใช้ถูก
- [ ] request/response schema ตรงกับ doc
- [ ] error shown ใน UI

##### C) BE ↔ Flow/Engine (ถ้า setting กระทบการรัน)
- [ ] engine รับ param นี้จริง
- [ ] deterministic ไม่พัง (อย่างน้อยใน gate mode)
- [ ] telemetry/validation ยังทำงาน

##### D) Flow ↔ DB (ถ้าต้อง persist)
- [ ] migration ถ้าจำเป็น
- [ ] save/reopen ยังได้ผลเดิม
- [ ] เก็บเฉพาะที่ doc บอกให้เก็บ

##### E) DB ↔ UX/UI (reopen/restore)
- [ ] เปิดกลับมาเห็น setting/สถานะถูก
- [ ] ค่า default ถูกถ้าไม่มี record

---

## 📊 Setting Levels (ต้องระบุทุกครั้ง)

| Level | Examples | Persistence |
|-------|----------|-------------|
| **UI-only** | dock open/close, theme, glass effect | None (state only) |
| **Run parameter** | speed, camera mode, dt | Session only |
| **Persisted config** | integrator, modules, seed | DB / Gallery / Snapshot |

> ⚠️ **ถ้าไม่ระบุระดับ = AI จะเดาเองแล้วพัง**

---

## 📝 Change Log

### Active Changes

| Change ID | Type | What | Status |
|-----------|------|------|--------|
| CHG-001 | Layout | Fixed Canvas + Overlay Panels | ✅ Complete |
| CHG-002 | UI | Move Settings to TopNav | ✅ Complete |
| CHG-003 | UI | Right Panel vertical layout | ✅ Complete |
| CHG-004 | UI | HUD 2D/3D/4D toggle | ✅ Complete |
| CHG-005 | UI | Right Panel sliders (DT, Softening) | ✅ Complete |
| CHG-006 | Design | Smart Settings = Verification View | ✅ Complete |

---

## CHG-001: Fixed Canvas + Overlay Panels

| Field | Value |
|-------|-------|
| **Change ID** | CHG-001 |
| **Change Type** | Layout |
| **What** | เปลี่ยน Lab layout จาก react-resizable-panels เป็น Fixed Canvas + CSS Overlay Panels |
| **Why** | Canvas ต้องไม่ resize เมื่อ panels เปิด/ปิด (ตาม design spec) |
| **Where** | Lab page - LabShell.tsx |
| **Buttons/Controls** | [HIDE], [SHOW OUTPUT], [SHOW STUDIO], [SHOW GRAPHS] |
| **DoD** | Canvas อยู่กับที่, panels slide in/out |
| **Risks** | None |

**Component Contract:**

| Setting Key | Type | Default | Persistence |
|-------------|------|---------|-------------|
| `layout.leftOpen` | boolean | false | UI-only |
| `layout.rightOpen` | boolean | true | UI-only |
| `layout.dockOpen` | boolean | false | UI-only |

---

## CHG-002: Move Settings to TopNav

| Field | Value |
|-------|-------|
| **Change ID** | CHG-002 |
| **Change Type** | UI/Interaction |
| **What** | ย้าย Settings gear icon จาก HUD ไป TopNav (มุมขวา) |
| **Why** | Settings ควรอยู่ TopNav ไม่ใช่ HUD (ตาม reference design) |
| **Where** | TopNav.tsx (เพิ่ม), SimulationHUD.tsx (ลบ) |
| **Buttons/Controls** | Settings button ⚙️ |
| **DoD** | Settings อยู่ที่ TopNav ข้าง Export |
| **Risks** | None |

**UX Spec:**

| Field | Value |
|-------|-------|
| Location | TopNav (right, after Export) |
| Label | ⚙️ (icon only) |
| action_id | `platform_settings_open` |
| expected_effect | Opens PlatformSettingsModal with verification view |
| States | normal, hover, active |

---

## CHG-003: Right Panel Vertical Layout

| Field | Value |
|-------|-------|
| **Change ID** | CHG-003 |
| **Change Type** | Layout |
| **What** | เปลี่ยน Right Panel จาก Tabs เป็น Vertical scroll |
| **Why** | แสดงทุก section พร้อมกัน (Equations, Params, Notes) |
| **Where** | Lab > Right Panel (RightPanelContent) |
| **Buttons/Controls** | N/A (ลบ tabs) |
| **DoD** | Scroll ลงเห็นทุก section |
| **Risks** | None |

---

## CHG-004: HUD 2D/3D/4D Toggle

| Field | Value |
|-------|-------|
| **Change ID** | CHG-004 |
| **Change Type** | UI/Interaction |
| **What** | เพิ่ม Dimension toggle (2D/3D/4D) ใน HUD |
| **Why** | สลับ visualization mode |
| **Where** | SimulationHUD.tsx |
| **Buttons/Controls** | 2D, 3D, 4D buttons |
| **DoD** | กดแล้ว highlight selection |
| **Risks** | Canvas render mode ยังไม่ implement |

**UX Spec:**

| Field | Value |
|-------|-------|
| Location | HUD (center, after counters) |
| Labels | 2D, 3D, 4D |
| action_id | `hud_dimension_2d`, `hud_dimension_3d`, `hud_dimension_4d` |
| expected_effect | Change visualization mode (TODO: link to renderer) |
| States | selected, unselected |

**Component Contract:**

| Setting Key | Type | Default | Persistence |
|-------------|------|---------|-------------|
| `ui.dimensionMode` | enum(2D,3D,4D) | 3D | UI-only |

---

## CHG-005: Right Panel Sliders

| Field | Value |
|-------|-------|
| **Change ID** | CHG-005 |
| **Change Type** | UI/Interaction + Setting |
| **What** | เพิ่ม DT slider และ Softening slider ใน Right Panel |
| **Why** | Quick access to simulation parameters |
| **Where** | Lab > Right Panel > Quick Parameters section |
| **Buttons/Controls** | DT slider, Softening slider |
| **DoD** | ลาก slider แล้วค่าเปลี่ยน |
| **Risks** | Softening ยังไม่เชื่อม engine |

**Component Contract:**

| Setting Key | Type | Default | Range | Persistence |
|-------------|------|---------|-------|-------------|
| `sim.dt` | number | 0.016 | 0.001-0.1 | Run parameter |
| `sim.softening` | number | 0.01 | 0.001-0.1 | Run parameter |

---

## CHG-006: Smart Settings = Verification View

| Field | Value |
|-------|-------|
| **Change ID** | CHG-006 |
| **Change Type** | Design / Architecture |
| **What** | Redesign Settings: ปรับค่าที่ Smart Input Panel → Settings เป็น Read-only Verification View |
| **Why** | สอดคล้องกับ Smart System, ตรวจสอบได้ว่า Input-Engine sync ถูกต้อง |
| **Where** | design_system/SMART_SETTINGS_DESIGN.md (new) |
| **Buttons/Controls** | N/A (architecture change) |
| **DoD** | Settings Modal แสดง: Input Value vs Engine Value + ✅/❌ Status |
| **Risks** | None (doc change only) |

**Key Principle:**

```
Input Panel (Studio) → Engine → Settings View (Verify)
      WRITE              SYNC       READ-ONLY
      
ถ้า Input ≠ Engine = ❌ BUG DETECTED!
ถ้า Input = Engine = ✅ SYNC OK
```

**Docs Updated:**
- Created: SMART_SETTINGS_DESIGN.md
- Updated: SMART_FULL_SYSTEM.md (8 docs)
- Updated: SMART_INDEX.md (9 docs)
- Updated: LAB_UI_DESIGN_SPEC.md
- Updated: SETTINGS_CONTRACT.md (v3.0)
- Updated: BUTTON_ACTION_IDS.md
- Updated: CHANGE_MANAGEMENT.md (this file)

---

**Last Updated:** 2024-12-24
**Version:** 1.1
