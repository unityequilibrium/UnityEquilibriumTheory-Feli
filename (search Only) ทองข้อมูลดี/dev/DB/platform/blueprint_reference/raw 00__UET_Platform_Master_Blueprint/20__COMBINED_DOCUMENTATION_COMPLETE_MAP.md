# COMBINED: DOCUMENTATION / COMPLETE MAP (CATEGORY 20)


# FILE: ARCHITECTURE_MAP.md

# 🔧 UET Platform — Architecture Rationale (Why This Tech Stack)

เอกสารนี้อธิบาย "เหตุผลเชิงสถาปัตยกรรม" ว่าทำไมแพลตฟอร์ม UET จึงเลือกใช้เทคโนโลยีชุดนี้ โดยเน้นความเสถียร, ความสามารถในการสเกล, และความง่ายในการดูแลระยะยาว

---

## 1) ทำไมต้องเลือก Next.js 15 LTS (และไม่ใช้ Next.js 16/17 ตอนนี้)
- Next.js 16 ขึ้นไปยังมีการเปลี่ยน API บ่อยและไม่เสถียรพอสำหรับระบบขนาดใหญ่
- เวอร์ชัน LTS (Long-Term Support) คือฐานที่ปลอดภัยที่สุดสำหรับการทำ production
- Library ecosystem ส่วนใหญ่รองรับ Next.js 15 มากที่สุดในตอนนี้
- ปัญหาที่เคยเกิด (AI เปลี่ยนเวอร์ชันอัตโนมัติ → โค้ดพัง) จะหมดไป เพราะเราจะล็อกเวอร์ชันแบบ Hard Lock

**Locked Version Example:**
"next": "15.0.3"

---

## 2) การเลือก Next.js 15 ไม่ได้จำกัดการขยายระบบ (Scaling-safe)
Scaling ของเราอยู่ที่ Backend Layer:
- RAG Engine
- pgvector
- PostgreSQL
- Worker / Background Jobs
- CDN / Edge Functions
- Storage Layer
- KB Management

ไม่เกี่ยวกับเวอร์ชันของ Next.js โดยตรง  
ดังนั้นการใช้เวอร์ชันที่เสถียรสุด → มีผลดีมากกว่าเสี่ยงอัปเดตตามเทรนด์

---

## 3) เหตุผลสถาปัตยกรรมหลัก: ต้อง "Stable, Predictable, Upgrade-Path Safe"
UET Platform เป็นระบบขนาดใหญ่:
- มี Global Knowledge Base
- มี Project Knowledge Base แยกเป็นหลายสมองย่อย
- มี RAG, Vector Search, Semantic Engine
- มี Studio/Chat/Source Panel ที่ต้องทำงานร่วมกัน
- มี Wallet/KPI/Database Template
- มี Community + Project Feed + Graph
- ต้องรองรับผู้ใช้จำนวนมากในอนาคต

**ดังนั้นสถาปัตยกรรมต้องนิ่ง**  
เปลี่ยนเวอร์ชันพร่ำเพรื่อ = เสี่ยงพังทั้งระบบ

---

## 4) แผนการอัปเกรดในอนาคต (Migration Plan)
- เวอร์ชันหลักของแพลตฟอร์มจะประเมินใหม่ทุก 6 เดือน
- หาก Next.js 16 หรือ 17 เข้าสู่สถานะ LTS → จะเพิ่มใน Roadmap
- ทุกการเปลี่ยนเวอร์ชันต้องบันทึกใน DECISIONS.md
- ต้องตรวจสอบ Compatibility ของ:
  - RSC
  - App Router
  - Server Actions
  - Caching Layer
  - Middleware

---

## 5) กฎหลักของ UET Platform: "เสถียรก่อน ฉลาดทีหลัง"
เป้าหมายของแพลตฟอร์มคือ:
- ขยายได้ตลอด
- ใช้งานได้จริงทุกวัน
- ทุกโปรเจกต์มี ‘สมองเล็ก’ ของตัวเองที่ต้องไม่พัง
- AI ทุกตัวที่เข้ามาอ่านไฟล์นี้ต้องเข้าใจ Tech Stack เดียวกัน
- เปลี่ยนอะไรมากไม่ได้ เพราะจะกระทบโครงสร้าง Project KB และ Global KB

สรุป:
เราต้องการ **เสถียรภาพแบบสูงสุด** ก่อนจะนำฟีเจอร์ใหม่มาใช้

**สรุปแบบหยิบไปใช้ได้เลย**

```arduino
"dependencies": {
   "next": "15.0.3",   ← ล็อค
   "react": "18.x",
   "react-dom": "18.x"
}
```

จะใช้คำสั่ง:

```perl
npm install next@15.0.3
```

----
# **ARCHITECTURE_MAP.md (ฉบับเต็ม • Enterprise Blueprint)**

# 🏛 UET Platform — System Architecture Map (Full Version)
สถาปัตยกรรมหลักของแพลตฟอร์ม UET ถูกออกแบบให้รองรับการขยายในระดับโลก (Global-Scale) 
พร้อมรองรับ Project จำนวนมาก, AI Agents หลายตัว, Knowledge Base หลากระดับ และ Token Economy

ระบบทั้งหมดถูกแบ่งออกเป็น 5 เลเยอร์:

1) **App Layer (Frontend UI) — Next.js 15 LTS**
2) **API Layer (Backend Services) — Edge + Node Server**
3) **AI Layer (RAG / Vector / Agents)**
4) **Data Layer (DB / File / Versioning / Logs)**
5) **Infrastructure Layer (Deployment / Scaling)**

---

# 1) App Layer (Frontend UI)
ใช้ Next.js 15 LTS (App Router) เพื่อความเสถียรสูงสุด และรองรับการอัปเดตในอนาคตได้ง่าย

## หน้าที่ของ App Layer
- แสดงผล UI ทั้งหมด (Community, Theory, Home, Projects, Donate)
- Render 3-panel workspace (Source / Chat / Studio)
- โหลดและแสดง Markdown (โน้ต, ทฤษฎี, ไฟล์โปรเจกต์)
- Render Graph View จาก JSON graph data
- ส่งคำสั่งไปยัง Backend API + AI Engine

## โครงสร้างหน้า (Page Architecture)

```md
/app  
├── community/  
├── theory/  
├── home/  
├── projects/  
│ ├── [projectId]/  
│ │ └── workspace (3 panels)  
├── donate/  
├── api/ → proxy ไป backend services  
└── layout.tsx
```


---

# 2) API Layer (Backend Services)
Backend จะถูกแบ่งเป็น "Service Modules" แบบเดียวกับบริษัทใหญ่ใช้

## Service Modules
### 2.1 Authentication Service
- Login, JWT, refresh tokens
- Role system: Guest / Member / Power User / Admin

### 2.2 Project Service
- CRUD โปรเจกต์
- สมาชิกในโปรเจกต์
- การ sync ข้อมูลกับ Global Knowledge Base

### 2.3 Knowledge Base Service (Global KB)
- เก็บไฟล์, โน้ต, metadata, version
- ใช้ Git-style versioning

### 2.4 Project Knowledge Service (Local KB)
- แยกคลังความรู้รายโปรเจกต์
- อัปเดตได้ถี่กว่า Global KB
- มี vector embeddings แยกของแต่ละโปรเจกต์

### 2.5 Token & Finance Service
- ระบบ UET Credits (UC)
- ระบบ AI Tokens (AT)
- ระบบ Wallet / Top-Up / Burn Rate
- KPI Template + Balanced Scorecard

### 2.6 File Processor Service
- Extract text จาก PDF / Docx / Image
- Generate Markdown + Metadata
- แจ้ง AI ให้ Summarize / Clean / Index

### 2.7 Graph Engine Service
- เก็บโครงสร้าง Node/Edge
- Render Graph JSON ให้ frontend
- วิเคราะห์ความสัมพันธ์ของไฟล์/โน้ต

---

# 3) AI Layer (RAG / Vectors / Agents)
เลเยอร์นี้คือ "สมอง" ของแพลตฟอร์ม

## 3.1 Embedding Engine
- ใช้ pgvector (PostgreSQL)
- แยกเป็น 2 ระดับ:
  - Global Embeddings
  - Project Embeddings

## 3.2 RAG Engine
ประกอบด้วย:
- Retriever (dense + sparse)
- Ranker (semantic + metadata-based)
- Context Builder (สรุปให้เหลือ token ต่ำสุด)
- Answer Composer (ใช้ LLM)

## 3.3 AI Agent Framework
Agents มี 4 โหมด:
1. **Chat Agent** → ใช้ใน Panel Chat
2. **AutoPrompt Agent** → รัน pipeline งานยาว
3. **Studio Agent** → สร้าง/แก้ Markdown ภายในโปรเจกต์
4. **Finance Agent** → วิเคราะห์ธุรกรรมและ KPI

---

# 4) Data Layer
## 4.1 PostgreSQL (Core DB)
ตารางหลัก:
- users
- projects
- project_members
- notes
- note_versions
- vectors_global
- vectors_project
- finance_wallet
- finance_transactions
- kpi_scores
- audit_logs

## 4.2 Object Storage (ไฟล์)
- Markdown
- PDF / DOCX
- Images
- Graph JSON
- Snapshots

## 4.3 Version Control Layer
- ทุกไฟล์ Markdown เก็บเป็น Git-style versions
- สามารถ roll-back

---

# 5) Infrastructure Layer
## 5.1 Deployment
- Frontend → Vercel (Next.js optimized)
- Backend → Node server / Docker / Cloud Run
- DB → Managed PostgreSQL
- Storage → Cloud Storage (S3-compatible)

## 5.2 Scaling Strategy
- Scale out ด้วย horizontal autoscaling
- Cache embedding และ metadata
- ใช้ background workers กับ Agent Runners

---

# 🚀 **DIAGRAM SET ใหม่ ใช้งานได้จริง (Plain Text)**

(แค่ copy → paste ไปไฟล์ไหนก็ได้ ไม่แตกแน่นอน)

---

## **1) HIGH-LEVEL ARCHITECTURE DIAGRAM (Plain Text)**

UET Platform – System Architecture (v1)

```
──────────────────────────────────────────────────────────  
				FRONTEND (Next.js 15)  
──────────────────────────────────────────────────────────
                    [ Next.js UI ]
                         │
                         │  HTTP / Websocket
                         ▼
──────────────────────────────────────────────────────────  
					API GATEWAY  
──────────────────────────────────────────────────────────  
			    │ 			 		│  			 			│  
				▼ 			 		▼  			 			▼  
		[ Project Service ], [ Knowledge Service ] ,[ Finance Service ]  
			    │ 			 		│  			 			│  
				▼ 			 		▼  			 			▼  
──────────────────────────────────────────────────────────  
			DATA SUBSYSTEMS (Multi-Layer KB)  
──────────────────────────────────────────────────────────
                    [ Next.js UI ]
                         │
                         │  HTTP / Websocket
                         ▼
──────────────────────────────────────────────────────────  
					AI ENGINE  
──────────────────────────────────────────────────────────  
				[ RAG / Vectors / Agents ]  
						│  
						▼
──────────────────────────────────────────────────────────  
					STORAGE  
──────────────────────────────────────────────────────────  
				[ PostgreSQL + pgvector ]  
					[ S3 Storage ]  
──────────────────────────────────────────────────────────
```

---
## **2) PANEL LAYOUT DIAGRAM (Workspace UI)**

UET Workspace (3-panel Architecture)

```UET Workspace (3-panel Architecture)
──────────────────────────────────────────────────────────  
│                       WORKSPACE                          │  
├───────────────────┬───────────────────┬──────────────────┤  
│ SOURCE            │ CHAT              │ STUDIO           │  
│ - Files           │ - AI Conversation │ - Markdown       │  
│ - Graph View      │ - Retrieve KB     │ - Editor         │  
│ - Metadata        │ - Local KB First  │ - Auto Assist    │  
└───────────────────┴───────────────────┴──────────────────┘
```

| Panel      | Description                            | Key Functions                                                                                         |
| ---------- | -------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **SOURCE** | ที่รวมข้อมูลทั้งหมดของโปรเจกต์         | - File list<br>- Graph view (Relationship Map)<br>- Metadata viewer<br>- Source search                |
| **CHAT**   | สมองกลางของโปรเจกต์ ใช้คุยกับ AI       | - AI Conversation<br>- Retrieve Local KB<br>- Retrieve Global KB (fallback)<br>- Contextual answering |
| **STUDIO** | พื้นที่สร้างงาน / เขียนโน้ต / Markdown | - Markdown Editor<br>- Auto Assist by AI<br>- Create notes<br>- Generate new files- Draft → Publish   |

---
## **3) RAG DATA FLOW DIAGRAM (Plain Text)**

```RAG DATA FLOW
Semantic Query Flow

User Query  
│  
▼  
Chat Panel  
│  
▼  
AI Agent Engine  
│  
▼  
Retriever  
│  
├── Check Local KB (per project)  
│  
└── If not found → Use Global KB  
▼  
Ranker  
▼  
Context Builder  
▼  
LLM Composer  
▼  
Final Answer to User
```

---

## **4) PROJECT KNOWLEDGE ARCHITECTURE (Plain Text)**

```ProjectFlow
Project A  
│  
├── notes/  
│ ├ note1.md  
│ ├ note2.md  
│ └ ...  
│  
├── vectors/  
│ ├ embeddings.vec  
│ └ metadata.json  
│  
├── graph/  
│ └ graph.json  
│  
├── studio/  
│ └ editor-temp.md  
│  
└── history/  
└ git-style snapshots

Global Knowledge Base  
│  
└── global_md/  
├ concept1.md  
├ theory_core.md  
└ ...
```

---
## **5) BACKEND SERVICE MAPPING (Plain Text)**

SERVICES OVERVIEW

Authentication Service  
- Login, Token, Role, Permission

Project Service  
- Create Project  
- Manage members  
- Project-level vector KB

Knowledge Service  
- Global KB  
- Markdown storage  
- Graph update engine

Finance Service  
- Wallet  
- UC (Credits)  
- AT (AI Tokens)  
- KPI Engine

File Processor Service  
- PDF → Text  
- DOCX → Text  
- Image OCR  
- Convert → Markdown

AI Engine  
- Embeddings  
- RAG  
- Agents  
- AutoPrompt

---
## **6) INFRASTRUCTURE DIAGRAM (Plain Text)**

Deployment

```Deployment
            ┌───────────┐
            │  Vercel   │  → Frontend
            └─────┬─────┘
                  │
        ┌─────────▼─────────┐
        │  API Gateway       │
        └───────┬───────────┘
                │
┌───────────────┼────────────────┐  
▼               ▼                ▼  
Backend (Cloud Run) Backend Workers Agent Runners  
                │  
                ▼  
		PostgreSQL (Managed)  
		pgvector extension  
                │  
                ▼  
S3 Storage (Files/Markdown/Graph)
```

---
# ⭐ **UET Platform — Master Panel & System Table (Full Version)**

_(อันนี้คือโครงสร้าง “ใหญ่สุด” ที่รวมทุกโซนของระบบ)_

|Zone / Panel|Input|Output|Uses KB / DB|User Actions|AI Actions|
|---|---|---|---|---|---|
|**HOME — Feed Panel**|Posts, Theory updates, Project summaries|Feed items (scroll), notifications|Global KB (read-only), Public Posts DB|Scroll feed, open post, share, navigate|Summaries, highlight important items|
|**HOME — Featured Panel**|Manual curated list|Highlights section|Config DB|Admin sets featured content|Auto-generate featured suggestions|
|**COMMUNITY — Timeline**|Text, images, links|Public post|Community DB|Post, comment, vote|Auto-tag, NSFW detection, summarization|
|**COMMUNITY — Comments Drawer**|Comments, replies|Thread view|Community DB|Comment, reply, collapse threads|Thread summarization|
|**COMMUNITY — Profile Panel**|Profile info|Profile page|User DB|Edit profile|Suggest tags, auto-fill|
|**CHAT — Private AI Chat**|User message, files|AI response, generated content|Local KB, User KB|Ask questions, upload files|Process files, generate drafts, RAG reasoning|
|**CHAT — Friend Chat**|Direct messages|Conversation log|Messaging DB|Send DM|Auto-reply suggestion|
|**CHAT — Project/Community Chat**|Multi-user text|Chat thread|Project DB, Community DB|Send message, attach files|Thread summary, citations|
|**SOURCE — File List Panel**|Upload (pdf/doc/md/zip)|File item|Source DB, File Storage|Upload, rename, tag|Parse file, extract metadata|
|**SOURCE — Graph View**|KB nodes & relations|Interactive graph|Source KB graph|Explore relations|Auto-generate connections|
|**SOURCE — Metadata Panel**|File metadata|Structured metadata|Index DB|View/edit metadata|Extract topics, generate tags|
|**STUDIO — Markdown Editor**|Text, images, AI commands|Markdown file|Notes DB, Project DB|Write, save, publish|Auto-fix, generate sections|
|**STUDIO — Published Panel**|Drafts|Published content|Project DB, Theory DB|Publish/unpublish|Re-write, validate|
|**PROJECTS — Project Feed Panel**|Project list|List view|Project DB|Browse, open project|Suggest related projects|
|**PROJECTS — Project Dashboard**|Project metadata|Status, tasks, files|Project DB|Create/edit project|Auto-generate project structure|
|**PROJECTS — Task Panel (B-S/KPI)**|KPIs, tasks, metrics|Scoreboard|KPI DB|Add task/KPI|Track progress, auto-calc|
|**PROJECTS — Files Panel**|File list|File browser|Project File DB|Add/remove files|Suggest file structure|
|**THEORY — Theory Feed**|Published theory content|Scroll feed|Theory DB|Read content|Suggest related concepts|
|**THEORY — Theory Section Panel**|Section files|Rendered content|Theory DB|Navigate sections|Summaries, deep links|
|**THEORY — Studio Integration**|Draft text|New theory sections|Theory DB, Notes DB|Create theory content|Auto-format, citations|
|**DONATE — Donation Form**|Bank slip/transaction|Transaction log|Donation DB, Wallet DB|Donate|Parse slip, log record|
|**DONATE — Transparency Panel**|Donation logs|Public report|Donation Ledger|View all donations|Summaries, anomaly detect|
|**SETTINGS — User Settings**|User config|Config file|User DB|Edit preferences|AI-mode select, autoset|
|**SETTINGS — System Settings**|Admin config|System config|Config DB|Admin edits|Validate config|

---
# 💎 ทำไมตารางนี้ “เข้ากลุ่มที่สุด”

### ✓ 1. รวมทุกโซนของ Platform → ไม่หลุดหัวข้อ

ตารางนี้รวม **Workspace + Community + Projects + Theory + Donate + Settings**

### ✓ 2. มีตัวชี้วัดสำคัญของงานสถาปัตยกรรมทุกจุด

- Input
- Output
- Database/KB ที่ใช้
- User actions
- AI actions

ครบหมด → เหมาะกับ Blueprint / API / System Design

### ✓ 3. ใช้ภาษาที่อ่านง่าย → เอาไปใช้กับทุก AI ได้

จะเอาไปให้รุ่นไหน หรือให้หลายตัวช่วยทำงานต่อก็เข้าใจเหมือนกัน

### ✓ 4. ใช้แทน “System Overview + Panel Overview” ได้เลย

ควบทั้งสองระดับในไฟล์เดียว

---


# FILE: COMPONENT_MAP.md

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


# FILE: Flie.md

โอเค Santa —  
**ฉันเข้าใจปัญหาที่นายพูดแบบ “ชัดเจน 100%” แล้ว**  
และเราจะ “แก้ทั้งระบบ” แบบไม่ให้เละเทะอีกต่อไป  
ไม่มีไฟล์ซ้ำ ไม่มีไฟล์มั่ว ไม่มีชื่อแปรผันไปเรื่อย ไม่มีไฟล์งอกมั่วจนต้องเขียนใหม่

จากนี้ไป:

# 🔥 **เราจะรีเซ็ตระบบไฟล์ UET ใหม่ทั้งหมดแบบมืออาชีพ**

**และจัดโครงเป็น “25 ไฟล์คงที่” เท่านั้น**  
แต่ละไฟล์มีชื่อ, หมายเลข, เวอร์ชัน, โครงสร้างตายตัว  
และรวมทุกเนื้อหาที่เคยคุยกันให้อยู่ในไฟล์ที่ถูกต้อง

---

# 🟥 PART 1 — ทำไมไฟล์มันเละตอนนี้? (วิเคราะห์ตรงปัญหา)

ปัญหาตอนนี้คือ:

### 1) ไฟล์ถูกสร้างแยก เพื่อไม่ให้แชทตัน

→ ผลลัพธ์: ชื่อไฟล์เปลี่ยนไปตาม session → มั่ว

### 2) ไม่มีระบบ versioning

→ ไฟล์เก่าไม่ถูกลบ → กองเป็นขยะ

### 3) นายต้องการไฟล์แบบ “รวมทุกอย่างในหมวดเดียว”

→ แต่ตอนนี้มันแยก 30–40 ไฟล์

### 4) ไม่มี “กฎกลาง” ว่าไฟล์ไหนอยู่หมวดไหน

→ ทำให้งานซ้อน งานซ้ำ เนื้อหาตกหล่น

### 5) ชื่อไฟล์ไม่คงที่

เช่น  
API_SPEC part 1 → API Spec → API Work System → API Layer (งงคนทำ, งงคนอ่าน)

---

# 🟦 PART 2 — แผนใหม่: ระบบไฟล์แบบ “25 ไฟล์ FIXED”

ไฟล์ใหม่จะถูกจัดตามหมวดใหญ่ 6 หมวด  
และ **ใช้รหัสคงที่ ไม่เปลี่ยนชื่ออีก**  
ทุกไฟล์มีรูปแบบ:

```
XX__FILE_NAME_v3.0.md
```

ทั้งหมดไม่เกิน 25 ไฟล์

---

# 🟩 PART 3 — โครงสร้างไฟล์ใหม่ (25 ไฟล์ FINAL)

นี่คือโครงสร้างที่ “ตรงกับโปรเจกต์จริง” + “ไม่เกิน 25 ไฟล์”  
และครอบคลุมเนื้อหา **100% จากทั้งหมดที่เราคุยมา**

---

## 🟦 A. SYSTEM FOUNDATION (5 ไฟล์)

### **01__SYSTEM_CONTRACT_v3.0.md**

รวมกฎทั้งหมดของระบบ  
(เดิมหลายไฟล์ → รวมเป็นไฟล์เดียว)

### **02__SYSTEM_ARCHITECTURE_v3.0.md**

แผนภาพ + แบบจำลอง Eng/Module/Flow

### **03__PROJECT_STRUCTURE_v3.0.md**

Mapping + Directory + Dependencies

### **04__ENGINE_INTERFACES_v3.0.md**

รวม API/Interface ระหว่าง engines  
(รวมทุก part)

### **05__DEPLOYMENT_GUIDE_v3.0.md**

---

## 🟧 B. CORE ENGINES (7 ไฟล์)

### **06__FLOW_CONTROL_ENGINE_v3.0.md**

### **07__MODEL_ROUTING_ENGINE_v3.0.md**

### **08__RAG_ENGINE_v3.0.md**

### **09__KNOWLEDGE_SYNC_ENGINE_v3.0.md**

### **10__AGENT_ENGINE_v3.0.md**

(รวม Bible + Behavior + Test spec → 1 ไฟล์)

### **11__CACHE_STRATEGY_v3.0.md**

### **12__EVENT_BUS_SYSTEM_v3.0.md**

---

## 🟨 C. DATA LAYER (5 ไฟล์)

### **13__DATA_SCHEMA_v3.0.md**

รวม schema ทั้งหมด

### **14__SQL_MIGRATION_v3.0.md**

### **15__SQL_CONSTRAINTS_v3.0.md**

(PART 1–4 รวมแบบสุดสมบูรณ์)

### **16__SQL_INDEX_STRATEGY_v3.0.md**

(PART 1–4 รวม + optimization)

### **17__DATA_INTEGRITY_TESTS_v3.0.md**

---

## 🟩 D. KNOWLEDGE GRAPH LAYER (3 ไฟล์)

### **18__UNIFIED_KNOWLEDGE_GRAPH_v3.0.md**

รวม L3 + L4 + L5 ทั้งหมด

### **19__KNOWLEDGE_BLUEPRINT_v3.0.md**

### **20__TYPE_SYSTEM_v3.0.md**

สำหรับ L3/L4/L5 + engines

---

## 🟧 E. API LAYER (3 ไฟล์)

### **21__API_SPEC_v1.0.md**

รวมทุก endpoint + auth + validation

### **22__API_PAYLOAD_EXAMPLES_v1.0.md**

ตัวอย่าง request/response ครบ 100%

### **23__ERROR_RESPONSE_SPEC_v1.0.md**

---

## 🟫 F. RUNTIME & WORKER (2 ไฟล์)

### **24__WORKER_AND_TASK_SYSTEM_v3.0.md**

รวม scheduler, queue, retry

### **25__EXECUTION_GRAPH_v3.0.md**

Agent flow + system behavior

---

# ✔ รวมทั้งหมด = **25 ไฟล์ถ้วน**

ไฟล์จะไม่เกินจากนี้  
และแต่ละไฟล์มีเวอร์ชัน v3.0 (หรือ v1.0 สำหรับ API)

---

# 🟥 PART 4 — ขั้นตอนรีเซ็ต (ทำให้เนี้ยบแบบมือโปร)

1. ฉันจะ:
    

- รวมไฟล์ทั้งหมดที่นายมี
    
- จัดหมวดใหม่ตาม 6 หมวด
    
- ย้ายเนื้อหาที่กระจัดกระจายให้ถูกหมวด
    
- ลบเนื้อหาซ้ำ
    
- ปรับชื่อไฟล์ให้คงที่ตาม 25 ไฟล์นี้
    

2. จากนั้น:
    

- แจ้งไฟล์ไหนถูก merge
    
- แจ้งไฟล์ไหนถูกลบ
    
- แจ้งไฟล์ไหนถูก rewrite แบบเต็ม
    
- แจ้งไฟล์ใหม่ให้ครบ 25 ไฟล์
    
- แจ้ง version ของทุกไฟล์
    

3. จากนั้นค่อยเริ่ม rewrite ตามลำดับ:  
    1 → 25  
    หรือเลือกหัวข้อที่ต้องการก่อน
    

---

# 🟦 PART 5 — ตอบตรง ๆ:

**ต้องใช้กี่บทสนทนาเพื่อจัดไฟล์ทั้งหมดให้ 100% ครอบคลุม??**

นี่คือคำตอบแบบมืออาชีพ:

### 🔥 ถ้าทำแบบ “ละเอียด + ครบทุกไฟล์”:

**ต้องใช้ 15–18 บทสนทนา**

### 🔥 ถ้าทำแบบ “เร็วแต่ครบทุกหัวข้อ”:

**ประมาณ 10–12 บทสนทนา**

### 🔥 ถ้าทำแบบ “ความสมบูรณ์ระดับโปรดักชัน 100%”

**20 บทสนทนา = พอดีที่สุด**

นายเลือกระดับได้เลย  
ฉันไม่กลัวคุยยาว  
เพราะมันดีกว่าทำแล้วเนื้อหาขาด

---

# 🟩 PART 6 — สิ่งที่ต้องการจากนายตอนนี้

ให้เลือก 1:

### A) **เริ่มรีเซ็ตไฟล์ทั้งหมดตอนนี้ (แนะนำที่สุด)**

→ ฉันจะสร้างไฟล์ **01__SYSTEM_CONTRACT_v3.0.md** ก่อน

### B) ให้ฉัน

**สแกนไฟล์จริงที่นายอัปโหลด + จัด map ว่าไฟล์ไหนควรไปอยู่ใน 25 ไฟล์ไหน**

### C) หรือให้เริ่ม

**สร้างไฟล์ใหม่ v3.0 ทีละไฟล์ตามหมวด (1–25)**

---

# 🔥 Santa ต้องการแบบไหน?

เลือก A / B / C แล้วฉันจะเริ่มทันทีแบบ 100% ระบบ ระเบียบ เรียบร้อย ชัดเจน ❤️