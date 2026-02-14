มาแล้ว Santa — **COMPONENT_MAP.md (ฉบับเต็ม + กระชับ + อ่าน 10 วินาทีรู้เรื่อง)**  
อันนี้คือเวอร์ชันที่ “ถูกต้องทางสถาปัตยกรรม” + “เหมาะกับแพลตฟอร์ม UET” มากที่สุดแล้ว  
และเขียนให้เหมาะกับการเอาไปยื่นให้ AI-Dev / Agent / หรือใช้สร้างโปรเจกต์จริง

---

# 📦 **COMPONENT_MAP.md (UET Platform)**

> **ไฟล์นี้คือ “แผนที่ใหญ่ของทุกคอมโพเนนต์ในระบบ”**  
> เอาไว้ใช้เพื่อควบคุม React structure, Panel system, และลดงานซ้ำ

---

# 🟩 1) GLOBAL COMPONENTS

ใช้ได้ทุกหน้า (Page) และทุกระบบ

|Component|หน้าที่|อยู่ใน Pages ไหน|
|---|---|---|
|**NavBar**|เมนูบนสุด (Home / Theory / Projects / Community / Donate / Login)|ทุกหน้า|
|**SideNav**|แถบซ้าย toggle ได้ รวม History / Profile / Settings|ทุกหน้าแบบ Workspace|
|**PageShell**|กรอบมาตรฐานของทุกเพจ (padding / max-width / theme)|ทุกหน้า|
|**PanelShell**|กรอบของแต่ละ Panel (Source / Chat / Studio)|เฉพาะ Chat Page|
|**Modal**|Popup กลางจอ เช่น Login / Settings|ทุกหน้า|
|**Drawer**|แถบเลื่อนจากขอบ เช่น Member list, Info|Theory / Project / Community|
|**Toast**|แจ้งเตือน|ทุกหน้า|
|**ThemeProvider**|จัดการ Dark/Light|ทุกหน้า|

---

# 🟦 2) WORKSPACE COMPONENTS

ใช้เฉพาะหน้าแชท หรือหน้าที่มี 3-panel layout

|Component|หน้าที่|Panel|
|---|---|---|
|**SourceExplorer**|รายชื่อไฟล์, KB, อัปโหลด|Source Panel|
|**FileGraphView**|กราฟความสัมพันธ์เหมือน Obsidian|Source Panel|
|**ChatBox**|กล่องแชทแบบ GPT|Chat Panel|
|**ChatMessage**|bubble แชท|Chat Panel|
|**FunctionToolbar**|ปุ่ม + (Deep research / Upload / Canvas / Agent)|Chat Panel|
|**StudioEditor**|Markdown + AI AutoPrompt|Studio Panel|
|**StudioOutputTabs**|สลับ Notebook / AutoPrompt / Python / Summary|Studio Panel|
|**VersionTimeline**|ดูประวัติเวอร์ชันไฟล์|Source Panel|

---

# 🟨 3) PROJECT COMPONENTS

ใช้เฉพาะหน้า `/projects/[id]`

|Component|หน้าที่|
|---|---|
|**ProjectHeader**|ชื่อโปรเจกต์ + owner + tag|
|**ProjectTabs**|Overview / Notes / Tasks / KPI / Files|
|**ProjectNoteList**|รายโน้ตทั้งหมดของโปรเจกต์|
|**ProjectTaskTable**|ตารางงาน (task board / kanban)|
|**ProjectKPIWidget**|KPI จาก Balanced Scorecard|
|**ProjectFilePanel**|ไฟล์ทั้งหมดของโปรเจกต์|
|**ProjectMemberDrawer**|สมาชิกโปรเจกต์|

> หมายเหตุ: “Notes / Tasks / KPI / Files” ใช้ **StudioEditor**, **Table**, **ListView** แค่เปลี่ยน data source

---

# 🟧 4) THEORY COMPONENTS

ใช้เฉพาะหน้า `/theory`

|Component|หน้าที่|
|---|---|
|**TheoryFeed**|เลื่อนอ่านทฤษฎีเป็น feed (เหมือน Medium)|
|**TheoryGraph**|กราฟเชื่อมโยงหมวดต่าง ๆ|
|**TheoryIndex**|แผนที่ทฤษฎีย่อยทั้งหมด|
|**TheoryContentViewer**|ตัวอ่าน Markdown|
|**TheoryCommentDrawer**|คอมเมนต์แต่ละหมวด|

---

# 🟪 5) COMMUNITY COMPONENTS

เหมือน Social Feed + Group Chat

|Component|หน้าที่|
|---|---|
|**CommunityFeed**|โพสต์/สเตตัส/อัปเดต|
|**CommunityPost**|คอนเทนต์ 1 ชิ้น|
|**CommunityComment**|คอมเมนต์ใต้โพสต์|
|**CommunitySidebar**|Trending / Topic / Tag|
|**CommunityProfile**|โปรไฟล์ของผู้ใช้|

---

# 🟥 6) DONATE / WALLET / FINANCE COMPONENTS

ใช้ระบบเดียวกับ KPI (database)

|Component|หน้าที่|
|---|---|
|**WalletDashboard**|กระเป๋ารวม|
|**DonationTable**|รายการบริจาค + วันที่ + ref|
|**RevenueChart**|รายได้ทั้งหมด|
|**ExpenseChart**|ค่าใช้จ่าย|
|**WalletGoalWidget**|เป้าหมาย KPI|

---

# 🟫 7) AUTH / USER / PROFILE COMPONENTS

|Component|หน้าที่|
|---|---|
|**LoginModal**|Login ด่วน|
|**RegisterForm**|อัปโหลดข้อมูลเบื้องต้น|
|**ProfilePage**|ข้อมูลผู้ใช้|
|**ProfileStats**|ค่าใช้จ่าย / KPI ส่วนตัว|
|**SettingsPage**|API keys / plans|

---

# 🟩 8) UTILITIES / CORE LOGIC COMPONENTS (ไม่ใช่ UI แต่สำคัญมาก)

|Component|หน้าที่|
|---|---|
|**Fetcher**|wrapper ของ fetch API|
|**useChat**|hook จัดการแชท|
|**usePanelLayout**|hook จัด 3 panel|
|**useFileGraph**|hook คำนวณกราฟจาก metadata|
|**MarkdownRenderer**|ตัวแปลง markdown → HTML|
|**AIClient**|เรียก LLM|
|**VectorClient**|เรียก pgvector|
|**ProjectContext**|global state ของโปรเจกต์|
|**UserContext**|global state ของผู้ใช้|

---

# 🌐 9) DIAGRAM — COMPONENT MAP (ภาพรวมรวมทุก category)

```
GLOBAL COMPONENTS
    ├── NavBar
    ├── SideNav
    ├── PageShell
    ├── PanelShell
    ├── Modal
    └── Drawer

WORKSPACE (Chat Page)
    ├── SourceExplorer
    ├── FileGraphView
    ├── ChatBox
    ├── FunctionToolbar
    ├── StudioEditor
    └── StudioOutputTabs

PROJECT PAGE
    ├── ProjectHeader
    ├── ProjectTabs
    ├── ProjectNoteList
    ├── ProjectTaskTable
    ├── ProjectKPIWidget
    └── ProjectFilePanel

THEORY
    ├── TheoryFeed
    ├── TheoryGraph
    ├── TheoryIndex
    └── TheoryContentViewer

COMMUNITY
    ├── CommunityFeed
    ├── CommunityPost
    ├── CommunitySidebar
    └── CommunityProfile

DONATE / FINANCE
    ├── WalletDashboard
    ├── DonationTable
    ├── RevenueChart
    └── WalletGoalWidget

UTIL / CORE LOGIC
    ├── MarkdownRenderer
    ├── AIClient
    └── VectorClient
```

---
