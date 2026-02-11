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
