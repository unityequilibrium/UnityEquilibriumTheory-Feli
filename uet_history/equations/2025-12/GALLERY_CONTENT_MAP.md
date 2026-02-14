# Gallery Content Migration & Design

> **ANALYSIS OF EXISTING GALLERY**  
> Source: `runs_gallery/gallery.html`  
> Objective: Map existing static gallery content to the new UET Lab dynamic system.

---

## 1. CONTENT INVENTORY (สิ่งที่ต้องย้ายมา)

จากการตรวจสอบไฟล์เดิม เรามี Simulation Sets ทั้งหมด 4 กลุ่มใหญ่ (Total: 20+ Items)

### 1.1 Core Tests (6 Items)
Tests ระบบพื้นฐานและความเสถียร
- **test_coupling**: Weak/Strong coupling checks
- **test_delays**: Time delays $\tau_{CI}=1.0, \tau_{IC}=0.5$
- **test_memory**: Memory exponential with $\tau=10.0$
- **test_multifield**: Multi-field network (3 fields)
- **test_nonlocal**: Nonlocal gaussian kernel $\sigma=5.0$
- **test_stochastic**: Stochastic noise $\sigma_C=2.0$

### 1.2 Archetype Demos (5 Items)
รูปแบบพื้นฐานของสมการ (Behavior Archetypes)
- **BIAS_C**: Bias driven in C-field
- **BIAS_I**: Bias driven in I-field
- **Strong_Coupling**: High interaction strength
- **Weak_Coupling**: Low interaction strength
- **SYM**: Symmetric evolution

### 1.3 Einstein Connection (3 Items)
การเชื่อมโยงกับ General Relativity ($T_{\mu\nu} \to G_{\mu\nu}$)
- **einstein_binary**: Binary system mapping
- **einstein_collapse**: Gravitational collapse mapping
- **einstein_wave**: Gravitational wave mapping

### 1.4 Numerical Relativity (BSSN) (3 Items)
เปรียบเทียบกับ Standard BSSN Solver
- **nr_binary**: Binary Black Hole (Reference)
- **nr_collapse**: Collapse (Reference)
- **nr_wave**: GW (Reference)

### 1.5 Realistic GR (3 Items)
- **gr_realistic_binary**: Real-world parameter binary

---

## 2. NEW GALLERY UI DESIGN (The Update)

เราจะอัพเดทหน้า Gallery ใน `UI_BLUEPRINT` ให้รองรับ **Categorized Grids** เหมือนไฟล์ต้นฉบับ แต่สวยกว่าด้วย Glassmorphism.

### 2.1 UI Structure Mapping

```text
┌────────────────────────────────────────────────────────┐
│ FILTERS: [All] [Core Tests] [Archetypes] [Physics]     │
└────────────────────────────────────────────────────────┘

▼ CORE TESTS (Section Header with Count)
┌────────────────────┐  ┌────────────────────┐
│ [ GIF PREVIEW ]    │  │ [ GIF PREVIEW ]    │
│                    │  │                    │
│ Test Coupling      │  │ Test Delays        │
│ 🏷️ System          │  │ 🏷️ System          │
│ [Load Preset]      │  │ [Load Preset]      │
└────────────────────┘  └────────────────────┘

▼ EINSTEIN CONNECTION
┌────────────────────┐  ┌────────────────────┐
│ [ GIF PREVIEW ]    │  │ [ GIF PREVIEW ]    │
│                    │  │                    │
│ Einstein Binary    │  │ Einstein Collapse  │
│ 🏷️ Physics         │  │ 🏷️ Physics         │
│ [Load Preset]      │  │ [Load Preset]      │
└────────────────────┘  └────────────────────┘
```

---

## 3. MIGRATION PLAN (Action Items)

เพื่อให้หน้า Gallery ใหม่ทำงานได้จริงพร้อมข้อมูลชุดนี้:

### Step 1: Asset Migration
ย้ายไฟล์ GIF ทั้งหมดจาก `runs_gallery/` ไปยัง public folder:
- Source: `uet_harness/.../runs_gallery/{id}/CI_evolution.gif`
- Target: `frontend/public/assets/gallery/{id}.gif`

### Step 2: Database Seeding (Prisma)
สร้าง `Preset` records ลง database โดยใช้ข้อมูลจาก html:

```typescript
// prisma/seed.ts (Example)
const presets = [
  {
    id: 'test_coupling',
    name: 'Test Coupling',
    description: 'Weak/Strong coupling checks',
    category: 'CORE_TEST',
    tags: ['stability', 'coupling'],
    previewImage: '/assets/gallery/test_coupling.gif'
  },
  // ... others
]
```

### Step 3: Frontend Component
อัพเดท `features/gallery/ProjectGrid.tsx` ให้รองรับการ Grouping ตาม Category:
- Group By: `category` (Core, Archetype, Einstein, NR)
- Collapsible Sections (Accordions) แบบเดียวกับไฟล์ HTML เดิม

---

## 4. DATABASE SCHEMA IMPACT

ต้องตรวจสอบ `DATABASE_SCHEMA.md` ว่ารองรับ structure นี้ไหม?
- **Current**: `Template` -> `Preset`
- **Update**: เพิ่ม field `category` และ `preview_url` ในตาราง `presets` (หรือ `projects`) เพื่อรองรับการแยกหมวดหมู่และการแสดงผลภาพ GIF

---

**สรุป:** เราจะนำ content เดิม 20+ รายการนี้ เข้าสู่ระบบผ่าน **Seeding** และแสดงผลใน **Categorized Grid** ที่สวยงามตาม Blueprint ใหม่ครับ
