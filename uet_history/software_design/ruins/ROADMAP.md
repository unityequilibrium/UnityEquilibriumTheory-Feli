# 🚀 **UET PLATFORM – PERSONAL ROADMAP (Founder Version)**

**ระยะเวลา: 20 วัน (5 – 10 – 5)**  
**เวอร์ชัน: 1.0 (ร่างแรก)**

---

# 🌟 **PHASE 0 – เตรียมความพร้อม**

_(ทำวันนี้เลย / ก่อนเริ่มนับ 20 วัน)_

### ✔ 0.1 เคลียร์วัตถุประสงค์โปรเจกต์

- เป้าหมาย: V1 ของแพลตฟอร์มที่ “เสถียร” และ “สเกลได้”
- ไม่ต้องสวย ให้ถูกต้องก่อน

### ✔ 0.2 เตรียม workspace

- Obsidian หรือ VS Code เปิด Project Folder ที่ใช้จริง
    
- ตั้งไฟล์ 3 ตัว:
    
    - `/ROADMAP.md` ← อันที่กำลังเขียนนี่
    - `/BLUEPRINT/` ← ทุก spec
    - `/INSPIRATION/` ← ตัวอย่างเว็บ / รูปอ้างอิง

### ✔ 0.3 ปักหมุดสิ่งสำคัญ

- เราจะไม่เขียนโค้ดก่อน blueprint เสร็จ
- ทุกอย่างจะต้อง normalize ก่อน
- ใช้ภาษา Page/Layout/Panel/Drawer/Modal เป็นมาตรฐาน

---

# ⭐ PHASE 1 (Day 1–5) — **MASTER BLUEPRINTING**

เป้าหมาย: ได้ภาพใหญ่ 100%, ยังไม่ลงลึกเกินไป

### ✔ 1.1 Finalize SYSTEM CORE (0.1)

- Role & permission
- Global KB vs Local KB
- AI Scope: global / project / private
- Data model overview

### ✔ 1.2 Draft 0.2 (Full Layout System)

- ทำชื่อ Page ทั้งหมดในระบบ
- ทำชื่อ Panel ทั้งหมดในระบบ
- ทำ Drawer / Modal ทั้งหมด
- ทำ relation ว่าอะไรเชื่อมอะไร
- ตีกรอบ: **แต่ละ page จะมี panel อะไรบ้าง**
- แยกตามหน้าหลัก: Home, Projects, Theory, Community, Chat, Donate

### ✔ 1.3 จัด category ให้ครบ

- Chat panels (3)
- Database panels (wallet / KPI / scorecard)
- Studio markdown system
- Source graph system
- Navigation system (global + local)

### ✔ 1.4 สร้าง Blueprint Folder tree

เช่น:
/BLUEPRINT/
    0.1 Core
    0.2 Layout System
    0.3 Page Map
    0.4 Panel Definitions
    0.5 Data Flow
    0.6 AI Flow
    0.7 Interaction Rules

### ✔ 1.5 ทำ DIAGRAM รอบแรก

- Page Map diagram
- Panel Map diagram
- AI Map diagram
- Data Map diagram  
    (เวอร์ชันง่าย ใช้แค่ text box → จะวาดสวยทีหลังได้)

**ผลลัพธ์ท้าย Phase 1:**  
นายเห็นภาพรวมทั้งหมดแบบ “ระบบบริษัทต่างประเทศ”

---
# ⭐ PHASE 2 (Day 6–15) — **DETAILED SYSTEM DESIGN**

เป้าหมาย: ลงลึกทีละระบบ จนเป็น spec จริง

### ✔ 2.1 ออกแบบ Chat System (3 แบบ)

- private
- friend
- community/project  
    → รวมกติกา / data flow / ai-binding

### ✔ 2.2 ออกแบบ Studio System (Markdown)

- new-file rules
- sync rules
- versioning
- AI autoprompt บน editor

### ✔ 2.3 ออกแบบ Source System (File + Graph)

- file structure
- graph generation
- sidebar behavior
- metadata template

### ✔ 2.4 ออกแบบ Project System

- project sections
- project chat
- project files
- project dashboard
- roles inside project
- auto-KPI connection

### ✔ 2.5 ออกแบบ Database System (Wallet + KPI)

- template type
- table rules
- api connection
- auto-update from tasks
- multi-level KPI logic

### ✔ 2.6 ออกแบบ Navigation

- top nav
- side nav
- breadcrumbs
- active state
- quick actions

### ✔ 2.7 ออกแบบ AI Behavior

- global AI
- project AI
- private AI
- switch-context
- memory rules
- fallback rules

### ✔ 2.8 ออกแบบ Permission System

- per-page
- per-panel
- per-project
- admin-only rules
- share rules

### ✔ 2.9 ทำ DIAGRAM เวอร์ชัน 2 (ละเอียด)

- state flow
- page flow
- panel communication
- AI inference flow
- backend call flow

### ✔ 2.10 เตรียม Spec สำหรับ Dev

- component list
- page list
- endpoint draft
- data model v1

**ผลลัพธ์ท้าย Phase 2:**  
นายจะได้ spec ที่ “ผลิตได้จริง” แบบบริษัททำ

---

# ⭐ PHASE 3 (Day 16–20) — **INTEGRATION & FINALIZATION**

### ✔ 3.1 รวม Blueprint เป็นเอกสารใหญ่ (v1)

- รวมทุกหมวด
- ทำสารบัญ
- ทำหัวข้อเชื่อมกัน

### ✔ 3.2 ตรวจ consistency

- ชื่อ page ต้องตรง
- ชื่อ panel ต้องตรง
- data map ตรง UI ทั้งหมด
- AI rules ไม่ขัดกัน

### ✔ 3.3 เตรียมไฟล์สำหรับ Figma (optional)

- page list
- layout mockup
- color/style guideline

### ✔ 3.4 เตรียมไฟล์สำหรับ Dev

- component spec
- api spec
- data spec
- state spec

### ✔ 3.5 ทำ LAUNCH PLAN

- เตรียม API
- เตรียม RAG
- เตรียม vector
- เตรียม database tables

**ผลลัพธ์ท้าย Phase 3:**  
นายได้สมุดสีน้ำเงินของระบบทั้งหมด  
พร้อมผลิต / พร้อมโยนให้ Dev หรือ AI สร้างทั้งระบบได้ทันที

---

# 🎯 สรุปแบบสุดท้าย (ใช้เป็น checklist ได้เลย)

## **PHASE 1 (Day 1–5) — Blueprint Overview**

- [ ]  SYSTEM CORE 0.1 เสร็จ
- [ ]  รายการ Page ทั้งหมด
- [ ]  รายการ Panel ทั้งหมด
- [ ]  รายการ Drawer + Modal
- [ ]  Page Map Diagram
- [ ]  Panel Map Diagram

## **PHASE 2 (Day 6–15) — Detailed Design**

- [ ]  Chat System Spec
- [ ]  Studio Spec
- [ ]  Source Spec
- [ ]  Project System Spec
- [ ]  KPI/Wallet Database Spec
- [ ]  Navigation Spec
- [ ]  AI Behavior Spec
- [ ]  Permission Spec
- [ ]  Diagram Round 2
- [ ]  Dev-ready spec

## **PHASE 3 (Day 16–20) — Integration**

- [ ]  รวมทุก blueprint → v1.0
- [ ]  ตรวจ consistency
- [ ]  เตรียม Figma (optional)
- [ ]  เตรียม Dev Spec
- [ ]  Launch Plan


