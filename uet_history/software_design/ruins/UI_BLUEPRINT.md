# UET Lab - UI Blueprint v1.0 (Complete)

> **VISUAL CONTRACT**  
> นี่คือมาตรฐาน UI Layout ที่ต้องยึดตามอย่างเคร่งครัด (Rigid Spec) สำหรับทุกหน้าในระบบ

---

## 1. HOME PAGE (Landing)

หน้าแรกเน้นความ Modern, Clean และ Scientific. Background เป็น 3D Simulation วิ่งอยู่ข้างหลัง.

```text
SCREEN 100vw x 100vh
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ (BACKGROUND: WebGL Simulation - Slowly rotating galaxy or particles)                        │
│                                                                                            │
│ TOP NAV (Transparent)                                                                       │
│ [UET LOGO]                                              [About] [Docs] [GitHub] [Login]    │
│                                                                                            │
│                                                                                            │
│                  ┌──────────────────────────────────────────────────────┐                  │
│                  │  GLASS CARD (Centered, w: 600px)                     │                  │
│                  │                                                      │                  │
│                  │  UNIFIED EQUILIBRIUM THEORY                          │                  │
│                  │  LABORATORY v0.1                                     │                  │
│                  │                                                      │                  │
│                  │  Interactive Physics Simulation Platform             │                  │
│                  │  Bridging Classical mechanics and UET                │                  │
│                  │                                                      │                  │
│                  │  ┌────────────────────────────────────────────────┐  │                  │
│                  │  │ [ ▶ ENTER LABORATORY ]                         │  │                  │
│                  │  │ (Primary Glow Button, h: 56px)                 │  │                  │
│                  │  └────────────────────────────────────────────────┘  │                  │
│                  │                                                      │                  │
│                  │  [View Gallery]  [Run Diagnostics]                   │                  │
│                  │                                                      │                  │
│                  └──────────────────────────────────────────────────────┘                  │
│                                                                                            │
│                                                                                            │
│                                                                                            │
│ FOOTER (Fixed Bottom)                                                                       │
│ v0.1.0-alpha | Status: ● Online | User: Guest                                [Theme ☾]     │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. GALLERY PAGE (Projects)

หน้าเลือกห้องทดลอง (Presets) หรือโหลด Save เก่า. เน้น Grid ที่ดูง่าย.

```text
SCREEN 100vw x 100vh
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ TOP NAV (Solid/Glass 48px)                                                                  │
│ [UET] [Home] [Gallery] [Lab] [Diagnostics]                                     [User ▼]    │
├────────────────────────────────────────────────────────────────────────────────────────────┤
│ SUB-HEADER (Filters & Actions)                                                              │
│ ┌────────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ Search: [🔎 Find preset or run...    ]   Filter: [All▼] [My Saves] [Templates]         │ │
│ │ Sort: [Newest▼]                          Action: [＋ New Empty Project]                │ │
│ └────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                            │
│ CONTENT AREA (Scrollable Grid)                                                              │
│                                                                                            │
│  TEMPLATES (Section)                                                                        │
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐                    │
│  │ [ PREVIEW IMG ]    │  │ [ PREVIEW IMG ]    │  │ [ PREVIEW IMG ]    │                    │
│  │                    │  │                    │  │                    │                    │
│  │ Solar System       │  │ Kepler 2-Body      │  │ Galaxy Cluster     │                    │
│  │ 🏷️ Template        │  │ 🏷️ Template        │  │ 🏷️ Template        │                    │
│  │ [Load Preset]      │  │ [Load Preset]      │  │ [Load Preset]      │                    │
│  └────────────────────┘  └────────────────────┘  └────────────────────┘                    │
│                                                                                            │
│  MY SAVED RUNS (Section)                                                                    │
│  ┌────────────────────┐  ┌────────────────────┐                                            │
│  │ [ SNAPSHOT IMG ]   │  │ [ SNAPSHOT IMG ]   │                                            │
│  │                    │  │                    │                                            │
│  │ Run #2024-12-23    │  │ Stable Orbit Test  │                                            │
│  │ 🕒 2 mins ago      │  │ 🕒 1 day ago       │                                            │
│  │ [Open] [Del]       │  │ [Open] [Del]       │                                            │
│  └────────────────────┘  └────────────────────┘                                            │
│                                                                                            │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. LAB PAGE (The Core)

**MASTER LAYOUT DIAGRAM**

```text
SCREEN 100vw x 100vh
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ TOP NAV (48px)                                                                              │
│ [UET] [Home] [Gallery] [Lab] [Diagnostics]     LAB / {presetName}                           │
│                                    [UNIT MODE: Physical▼] [FPS] [⚙ Settings] [⎋ Back]      │
├────────────────────────────────────────────────────────────────────────────────────────────┤
│ MAIN WORKSPACE                                                                              │
│                                                                                            │
│ ┌───────────────────────────────┐     WORLD CANVAS (3D)     ┌────────────────────────────┐ │
│ │ LEFT PANEL (OUTPUT)           │  (always visible background)│ RIGHT PANEL (STUDIO)     │ │
│ │ [◀ HIDE]                      │                            │ [HIDE ▶]                   │ │
│ │                               │                            │                            │ │
│ │ (A) VIEW/MODE BAR             │                            │ (A) TAB BAR (fixed)        │ │
│ │  View: [PHY] [UET] [IND] [#]  │                            │  [Equations][Params]        │ │
│ │  UnitCat: [QNT] [QLT] [ALL]   │                            │  [Inspector][Notes(+)]      │ │
│ │                               │                            │                            │ │
│ │ (B) METRIC CARDS (1-1-1)      │                            │ (B) EQUATIONS TAB           │ │
│ │  [Search metric…]             │                            │  Newtonian  [ON]  Role[▼]   │ │
│ │  ┌─────────────────────────┐  │                            │  GR         [OFF]           │ │
│ │  │ [▢] Total Energy (E)    │  │                            │  UET        [OFF]           │ │
│ │  │ -2534.11  J  [QNT][PHY] │  │                            │  ───────────────────────     │ │
│ │  │ [Graph ▾]  (collapsed)  │  │                            │  Selected Module: Newtonian  │ │
│ │  └─────────────────────────┘  │                            │  [Docs]                      │ │
│ │  ┌─────────────────────────┐  │                            │                            │ │
│ │  │ [▢] Kinetic (K)          │  │                            │ (C) PARAMS TAB               │ │
│ │  │ 2484.47  J  [QNT][PHY]   │  │                            │  Run Name: [____________]    │ │
│ │  │ [Graph ▾]                │  │                            │  dt: [ 0.01 ] (slider+inp)   │ │
│ │  └─────────────────────────┘  │                            │  Steps/Frame: [ 1 ]          │ │
│ │  ┌─────────────────────────┐  │                            │  Integrator: [Leapfrog▼]     │ │
│ │  │ [▢] Potential (U)        │  │                            │  Substeps: [ 1 ]             │ │
│ │  │ -5018.58  J  [QNT][PHY]  │  │                            │  Softening ε: [ 0.00 ]        │ │
│ │  │ [Graph ▾]                │  │                            │  G: [ 1.00 ]                  │ │
│ │  └─────────────────────────┘  │                            │  (Module params auto-load)    │ │
│ │  ┌─────────────────────────┐  │                            │  [Reset Params] [Apply Params]│ │
│ │  │ [▢] Angular Mom |L|      │  │                            │                            │ │
│ │  │ 8.09e+4 kg·m²/s [QNT][PHY]│ │                            │ (D) INSPECTOR TAB             │ │
│ │  │ [Graph ▾]                │  │                            │  Solver state (read-only)     │ │
│ │  └─────────────────────────┘  │                            │                            │ │
│ │  (More cards scroll…)        │                            │ (E) NOTES TAB                 │ │
│ │                               │                            │  [＋ New Note]                 │ │
│ │ (C) VALIDATION STRIP          │                            │  Notes list (left) + editor    │ │
│ │  [✅PASS] [❌FAIL] [🟧EXP]     │                            │  (autosave chip)               │ │
│ │  Reason: {1-line} [Details]   │                            │                            │ │
│ │                               │                            │  (No Save/Export here)         │ │
│ │ (D) SELECTION INSPECTOR       │                            │                            │ │
│ │  Selected: {entityName}       │                            │                            │ │
│ │  id: {id}                      │                            │                            │ │
│ │  pos: (x,y,z) m [QNT][PHY]    │                            │                            │ │
│ │  vel: (vx,vy,vz) m/s[QNT][PHY]│                            │                            │ │
│ │  mass: {val} kg [QNT][PHY]    │                            │                            │ │
│ │                               │                            │                            │ │
│ │ (E) RESULTS ACTIONS (OUTPUT)  │                            │                            │ │
│ │  [💾 Save to Gallery/DB]       │                            │                            │ │
│ │  [⬇ Export…]                  │                            │                            │ │
│ │  [🧪 Validate this Lab]        │                            │                            │ │
│ └───────────────────────────────┘                            └────────────────────────────┘ │
│                                                                                            │
│ (When LEFT hidden)  [▶ SHOW OUTPUT]         (When RIGHT hidden) [SHOW STUDIO ◀]            │
│                                                                                            │
│ CENTER HUD (floating, top-center, offset 12px)                                              │
│ ┌────────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ [Preset▼] [⏵Play] [⏸Pause] [⏭Step]  Speed:[—●——]  t:{val}s [QNT]  steps:{val}# [COUNT] │ │
│ │ (NO Save/Export here)   [📊 Open Dock]   [📌 Pin Metric]   [⟲ Reset Run]                 │ │
│ └────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                            │
│ GRAPH DOCK (BOTTOM, collapsible)                                                           │
│ [▲] handle   Selected: [TotalE ✕] [Kinetic ✕] [Ω ✕]  [Clear]  View:[Time▼]  Range:[Auto▼] │
│ ┌────────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ PLOT AREA (Plotly)                                                                      │ │
│ │ - Auto-group overlay: same plot_group only                                               │ │
│ │ - Mixed groups → auto-split into stacked plots                                           │ │
│ └────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                            │
│ TOAST/ALERT ZONE (bottom-left)   [ {N} issues ] [dismiss ✕]                                │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. CONSTRAINT RULES (กฎเหล็ก)

### 2.1 Left Panel (Output Only)
- **หน้าที่:** Read-only / Monitoring / Analysis
- **ส่วนประกอบ:**
  - View/Mode Bar: เลือก filter การแสดงผล
  - Metric Cards: ดูค่าปัจจุบัน + กราฟย่อ
  - Validation Strip: ดูผลการตรวจสอบอัตโนมัติ
  - Selection Inspector: ดูข้อมูล entity ที่คลิกใน 3D
  - **Result Actions (สำคัญ):** ปุ่ม Save, Export, Validate **ต้องอยู่ที่นี่เท่านั้น**

### 2.2 Right Panel (Studio - Input Only)
- **หน้าที่:** Controls / Configuration / Knowledge
- **Tabs:**
  1. **Equations:** เปิด/ปิด module, เลือก role (driver/modifier)
  2. **Params:** ปรับค่า G, dt, softening, steps/frame
  3. **Inspector:** ดูสถานะภายใน Solver (internal state)
  4. **Notes:** เขียนบันทึก, สร้างโน้ตใหม่ **(ห้ามมีปุ่ม Save Run ตรงนี้)**

### 2.3 Center HUD (Operations)
- **หน้าที่:** Time Control / Navigation
- **ห้าม:** ห้ามมีปุ่ม Save หรือ Export เด็ดขาด (เพื่อลด text/complex UI กลางจอ)

### 2.4 Graph Dock (Visualization)
- **ตำแหน่ง:** อยู่ล่างสุด ซ้อนทับ Canvas ได้ หรือดันขึ้นมา
- **Selection:** ใช้ Checkbox บน Metric Card เพื่อเพิ่ม graph ลงใน Dock

---

**เอกสารนี้ใช้ยืนยันกับ Code Implementation ว่า "วางถูกที่" หรือไม่**
