# UPU v1 — 02: Unified System Architecture (USA)

### _Master Specification for the UET Platform Core System_

---

## 🔰 **PURPOSE OF THIS DOCUMENT**

เอกสารนี้คือ **สถาปัตยกรรมระบบกลาง (Unified System Architecture)** สำหรับแพลตฟอร์ม UET ทั้งหมด

- เพื่อให้ **AI Agent อ่านแล้วเข้าใจระบบทั้งก้อน**
    
- เพื่อให้ Developer ในอนาคตสามารถ Build / Scale ได้
    
- เพื่อให้การแก้ปัญหาและขยายระบบเป็น Structure เดียวกันทั้ง Platform
    
- เพื่อเป็นแกนกลางของ Version 1.0
    

_**นี่คือกระดูกสันหลังของแพลตฟอร์ม → ทุกฟีเจอร์เชื่อมจากสถาปัตยกรรมนี้เท่านั้น**_

---

# 1) SYSTEM OVERVIEW

แพลตฟอร์มประกอบด้วย 3 Core Subsystems ที่ต้อง Sync กันเสมอแบบ Hybrid:

## **A. Chat System (ChatGPT + NotebookLM Fusion Engine)**

- Chat Session
    
- Message Routing
    
- Knowledge Retrieval (RAG)
    
- Studio AutoTask Engine
    
- UI Workspace (3-panel Fusion)
    

## **B. Knowledge System (KB Engine)**

- File Ingestion → Extraction → Chunking → Embeddings → Storage
    
- Knowledge Base (Global + Project-scoped + User private)
    
- KB Conflict Resolver
    
- KB Merging Engine
    

## **C. User & Project System**

- Auth & Profile
    
- Chat History + Session Manager
    
- Projects + Project Files
    
- Theory Documents
    
- Notebook / Canvas
    
- Donation Page / Analytics
    

ทั้ง 3 ส่วนนี้ต้องทำงานเป็น **Hybrid State Machine** ที่เกี่ยวข้องกันแบบ real-time

---

# 2) GLOBAL SYSTEM DIAGRAM

```
[Client UI]
   │
   ▼
[Next.js App Router Layer]
   │
   ├── Chat API → ChatService → Generation Engine → Model Router
   ├── KB API → KB Service → Chunker + Embedder + Vector Storage
   ├── Project API → CRUD + File Links + KB Sync
   ├── Theory API → CRUD
   └── User API → Auth + Profiles + Limits

[Database Cluster]
   ├── PostgreSQL (Primary)
   ├── pgVector Index
   └── File Storage (Local / S3)
```

---

# 3) UNIFIED DOMAIN MODEL (FINAL SPEC)

นี่คือ Domain Model ที่ใช้ทั้ง Platform ทั้งหมด (เชื่อมกับ UPU_01 Step 1–3)

## **A. User & Profile Layer**

- User
    
- UserProfile
    
- RateLimitRecord
    

## **B. Chat Layer**

- ChatSession
    
- ChatMessage
    

## **C. Knowledge Layer**

- SourceFile (Uploaded Files)
    
- KBChunk (Chunks)
    
- KnowledgeEntry (Merged KB node) — _optional v1.1_
    

## **D. Project Layer**

- Project
    
- ProjectFile
    

## **E. Theory Layer**

- TheoryDocument
    

## **F. Studio Layer (NotebookLM Engine)**

- StudioNotebook
    
- StudioTask
    

ทุก Model มีความสัมพันธ์ข้ามระบบ เช่น:

- ChatSession ใช้ KB
    
- StudioTask ใช้ ChatHistory
    
- Projects สามารถดึงไฟล์จาก KB
    

---

# 4) BACKEND ARCHITECTURE (SERVICE LAYER)

เพื่อให้ระบบ maintain ง่าย ต้องแยกเป็น 7 Services ชัดเจน

## **1. ChatService**

- รับข้อความจากผู้ใช้
    
- ตรวจ intent
    
- ส่งให้ Model Router
    
- รวม Sources (Knowledge + Uploaded Files)
    
- สร้าง StudioTask อัตโนมัติถ้าผู้ใช้กดฟังก์ชัน
    

## **2. RAG Retrieval Service**

- Hybrid Search (Vector + Keyword)
    
- Metadata Boosting
    
- Ranking / Reranking
    
- Context Window Optimizer
    

## **3. KB Ingestion Service**

- Text extraction
    
- Chunking
    
- Embeddings
    
- Ingest pipeline
    
- Logging / Monitoring
    

## **4. ProjectService**

- CRUD + File Management
    
- Project-level KB sync
    
- Multi-user collaboration foundation
    

## **5. TheoryService**

- CRUD
    
- Tagging + Search
    
- Knowledge linking
    

## **6. StudioService**

- Notebook Engine
    
- AutoPrompt Engine
    
- Deep Research
    
- Canvas / Markdown Processor
    

## **7. AuthService**

- Login / Register
    
- Session token
    
- User profile settings
    

---

# 5) FRONTEND ARCHITECTURE (NEXT.JS 14–16)

ใช้แผนแบบ **App Router + Server Actions + Client Islands**

### **GLOBAL LAYOUT**

- Navbar (global)
    
- PersistentChatSidebar (global)
    

### **CHAT WORKSPACE (3 panels)**

1. **Left Panel** = Sources Workspace
    
2. **Center Panel** = Chat GPT UI + Multi-Model Toolbar + MessageList
    
3. **Right Panel** = Studio Workspace (Notebook + AutoPrompt)
    

### **UI STATE MODEL**

```
GlobalState
│
├── UserState
├── ChatState
├── KBState
├── StudioState
└── UIState (panels open/close)
```

---

# 6) HYBRID STATE MACHINE (UPU v1 CORE)

มาตรฐานนี้สำคัญมากที่สุด เพราะเป็นตัวประสานทั้ง Platform

```
Input → Intent Engine → Mode Selector → (Chat | Studio | KB Ops)
```

### Modes

- **Chat Mode** → ตอบแบบสั้น
    
- **Studio Mode** → NotebookLM Generation
    
- **Deep Research Mode** → Multistep + Sources
    
- **Canvas Mode** → เปิดไฟล์ใหม่ใน Studio
    
- **Knowledge Mode** → แก้ไขไฟล์/เพิ่ม KB
    

ทุกคำสั่งในระบบต้องเข้า State Machine ตัวนี้

---

# 7) VERSIONING MODEL (UET Platform v1.0)

```
v0.1 – v
```