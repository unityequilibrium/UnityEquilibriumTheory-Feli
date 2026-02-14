# UPU v1 — DATA MODELING SPEC (03)

**Author:** ChatGPT (System Architect)  
**Version:** UPU-03 (Initial Draft)  
**Status:** ACTIVE — will be extended in 04, 05, 06

---

# 🔷 1. PURPOSE

เอกสารนี้นิยาม **Data Models ทั้งหมด** สำหรับ UPU Platform v1 โดยเป็นชุดโมเดลระดับองค์กร (Enterprise-grade) ที่รองรับทั้ง:

- Chat Workspace (ChatGPT + NotebookLM)
    
- Knowledge Base / Source Files
    
- Studio Workspace (Notebook + AutoPrompt Engine)
    
- Project System (Collaboration)
    
- User System (Profile, Preferences, Tiers)
    
- System Logs & Orchestration
    

โมเดลทั้งหมดถูกออกแบบให้ **รองรับสเกลสูง**, **รองรับ multi-agent**, **รองรับอนาคต**, และ **เชื่อมโยงเป็นกราฟเดียวกัน (Unified Data Graph)**

---

# 🔷 2. GLOBAL MODELING PRINCIPLES

เพื่อให้เป็นระบบบริษัทใหญ่ระดับ Google / OpenAI / Meta โมเดลทั้งหมดใช้หลักดังนี้:

## 2.1 Strict Separation of Concerns

- User data
    
- Chat data
    
- File data
    
- Knowledge data
    
- Studio data
    
- Project data  
    ต้องไม่ปนกัน แต่ต้องเชื่อมกันได้ผ่าน relations ชัดเจน
    

## 2.2 Immutable History + Mutable State

- Message = immutable
    
- Notebook = versioned
    
- Project = stateful
    
- KBChunks = immutable
    

## 2.3 Strong Typing

ทุก field ต้องมี type ที่ชัดเจน เช่น:

- ENUM
    
- JSON schema
    
- Vector type (pgvector)
    
- TEXT vs LONGTEXT
    

## 2.4 Global Indexing Rules

ทุกโมเดลต้องรองรับการ search:

- By user
    
- By project
    
- By recency
    
- By relevance
    

---

# 🔷 3. MASTER ENTITY LIST

นี่คือ **รายการ Entity ทั้งหมดแบบ Official** ของ UPU v1  
พร้อม state/relations ครบ

## 3.1 USER DOMAIN

### **User**

- id
    
- email
    
- passwordHash
    
- role (user / advanced / research / admin)
    
- createdAt
    
- updatedAt
    

### **UserProfile**

- id
    
- userId _(FK)_
    
- displayName
    
- bio
    
- avatar
    
- preferences (JSON)
    
- settings (JSON)
    

---

## 3.2 CHAT DOMAIN

### **ChatSession**

- id
    
- userId _(FK)_
    
- title
    
- createdAt
    
- updatedAt
    
- lastMessageAt
    
- sourcesState (JSON) — รายชื่อไฟล์ที่ถูกเลือกตอนคุย
    

### **ChatMessage**

- id
    
- sessionId _(FK)_
    
- sender ("user" | "assistant" | "system")
    
- content (TEXT)
    
- tokens
    
- model
    
- metadata (JSON)
    
- createdAt
    

---

## 3.3 SOURCE FILE DOMAIN (NotebookLM-style)

### **SourceFile**

- id
    
- userId _(FK)_
    
- projectId _(FK?) optional_
    
- name
    
- type (pdf / txt / markdown / docx / csv / audio)
    
- size
    
- storageUrl
    
- extractedText (LONGTEXT)
    
- metadata (JSON)
    
- createdAt / updatedAt
    

### **SourceFileVersion** _(immutable)_

- id
    
- sourceFileId _(FK)_
    
- extractedText
    
- diff
    
- updatedAt
    

---

# 3.4 KNOWLEDGE BASE DOMAIN (RAG)

### **KBDocument** _(เหมือน UETDocument)_

- id
    
- title
    
- type (manual / theory / projectNote / autoExtract)
    
- createdBy _(FK User)_
    
- createdAt / updatedAt
    

### **KBChunk** _(เหมือน UETChunk)_

- id
    
- kbDocumentId _(FK)_
    
- content (TEXT)
    
- vector (vector)
    
- sourceFileId _(optional)_
    
- metadata (JSON)
    

### **KBMergeTask**

เพื่อรองรับฟีเจอร์ "ผสานข้อมูล" เหมือนใน NotebookLM

- id
    
- userId
    
- inputDocuments (JSON)
    
- outputDocumentId _(FK)_
    
- status
    
- createdAt
    
- updatedAt
    

---

## 3.5 STUDIO WORKSPACE DOMAIN (NotebookLM Studio)

### **StudioNotebook**

Notebook แบบ .md

- id
    
- userId
    
- title
    
- content (Markdown)
    
- createdAt
    
- updatedAt
    
- version
    

### **StudioTask**

เป็น AutoPrompt Engine

- id
    
- notebookId _(FK)_
    
- type ("analysis" | "rewrite" | "blog" | "canvas" | "deep_research")
    
- input (JSON)
    
- output (LONGTEXT or Markdown)
    
- modelUsed
    
- status
    
- createdAt
    
- updatedAt
    

---

## 3.6 PROJECT DOMAIN

### **Project**

- id
    
- name
    
- description
    
- ownerId _(FK)_
    
- visibility (public / private / link)
    
- createdAt
    
- updatedAt
    

### **ProjectMember**

- id
    
- projectId _(FK)_
    
- userId _(FK)_
    
- role (viewer / editor / admin)
    

### **ProjectMessage** _(เหมือน Chat แต่เป็นกลุ่ม)_

- id
    
- projectId _(FK)_
    
- senderId _(FK)_
    
- content
    
- model
    
- metadata
    
- createdAt
    

### **ProjectFile**

ไฟล์ที่อยู่ใน Project โดยไม่ปนกับ KB

- id
    
- projectId _(FK)_
    
- sourceFileId _(FK)_
    
- addedAt
    

---

## 3.7 SYSTEM + LOGGING DOMAIN

### **SystemEvent**

- id
    
- userId _(optional)_
    
- eventType
    
- payload (JSON)
    
- createdAt
    

### **RateLimitRecord**

- id
    
- userId
    
- tokensUsed
    
- windowStart
    

---

# 🔷 4. RELATION GRAPH (HIGH-LEVEL)

```
User ────┬──────── ChatSession ───── ChatMessage
         │
         ├──────── UserProfile
         │
         ├──────── SourceFile ───── SourceFileVersion
         │
         ├──────── StudioNotebook ─── StudioTask
         │
         └──────── Project ───── ProjectMember ───── ProjectMessage

SourceFile ───── KBChunk ───── KBDocument
```

---

# 🔷 5. DATA CONTRACT RULES (INTERFACE SPECS)

ทุก service ต้องใช้รูปแบบนี้:

```
interface DataResult<T> {
  success: boolean
  data?: T
  error?: {
    code: string
    message: string
  }
  meta?: {
    duration: number
    tokens?: number
  }
}
```

ใช้ร่วมกันทุก service endpoint → ทำให้ Agent เขียนโค้ดและดีบักง่าย

---

# 🔷 6. VERSIONING RULES

- ทุก Model ต้องมี: createdAt, updatedAt
    
- ทุกข้อมูลที่แก้ไขต้องใช้ _versioned copy_ หรือ _immutable log_
    

---

# 🔷 7. WHAT’S NEXT

ไฟล์ **UPU_04 — API Spec** จะนิยาม:

- REST/Route structure
    
- Request/Response schema
    
- Authorization model
    
- Error contracts
    
- RAG pipelines (retriever + ranker + orchestrator)
    

พิมพ์ต่อได้เลย:

# "เริ่มเลย 04"

เพื่อให้กูสร้าง **API SPEC** ระดับบริษัท Tech