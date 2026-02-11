โอเค Santa —  
ตอนนี้ไฟล์ทั้งหมด **โหลดครบ 100%**, รวมถึง 5 ไฟล์ชุดล่าสุด  
(LLM Routing, Multi-Source RAG, Versioned KB, Execution Graph, Autonomous Agent)

นายต้องการ **Checklist ก่อน** เพื่อใช้เป็น “ฐานควบคุมงาน” ก่อนค่อยไปทำ Matrix ใช่ไหม?

ฉันจัดให้แบบ **ครบ + เป็นระบบ + ใช้ได้จริงทันที**  
รวมทุกหมวดของ UET Platform และสอดคล้องกับไฟล์ที่นายอัปโหลดทั้งหมดโดยตรง

---

# ✅ **UET PLATFORM — MASTER CHECKLIST (FULL SYSTEM)**

**เวอร์ชันที่แม่นที่สุด ณ ตอนนี้ — ครอบคลุมทั้ง Blueprint, Engine, KB, RAG, Routing, Agent, Execution Graph, Security, UI, Deployment และ Document ทั้งหมด**

นี่คือรายการ “สิ่งที่ต้องมี + สิ่งที่มีแล้ว + สิ่งที่จะต้องรวมภายหลังใน Matrix”  
แบ่งเป็น 12 หมวดใหญ่ พร้อม sub-checklist ละเอียด

---

# 🟥 1) SYSTEM FOUNDATION

**[ ]** Master Blueprint v3.0  
**[ ]** Master Blueprint (Pre-UET PDF)  
**[ ]** Architecture of Trust PDF  
**[ ]** System Overview  
**[ ]** System Contract v3.0  
**[ ]** Terminology  
**[ ]** Rules of Engagement  
**[ ]** Unified System Principles  
**[ ]** Governance Model

---

# 🟦 2) GLOBAL ARCHITECTURE

**[ ]** SYSTEM ARCHITECTURE (All versions)  
**[ ]** Architecture Map  
**[ ]** Project Structure  
**[ ]** Component Map  
**[ ]** Execution Graph Overview  
**[ ]** Request Flow Diagram  
**[ ]** Data Lifecycle Diagram

---

# 🟩 3) DATA LAYER (L0–L5)

**[ ]** L0 Files handling  
**[ ]** L1 Chunking Rules  
**[ ]** L2 Embedding Model Strategy  
**[ ]** L3 Semantic Nodes  
**[ ]** L4 Relation Edges  
**[ ]** L5 Reasoning Blocks  
**[ ]** Unified Knowledge Graph (Rewrite 100%)  
**[ ]** Knowledge Graph Spec (L3–L5)  
**[ ]** Data Schema v3.0  
**[ ]** SQL Constraints + Index Strategy  
**[ ]** SQL Migration Master  
**[ ]** Prisma Schema Draft

---

# 🟨 4) VERSIONED KNOWLEDGE BASE

_(จากไฟล์ Versioned KB Spec)_  
**[ ]** KB_VERSION  
**[ ]** VECTOR_VERSION  
**[ ]** GRAPH_VERSION  
**[ ]** Immutable Canonical Nodes  
**[ ]** Snapshot Registry (kb_registry)  
**[ ]** Multi-layer sync rules  
**[ ]** Semantic Diff Engine  
**[ ]** Conflict Resolution Flow  
**[ ]** Rollback Strategy

📄 **Source:** Versioned Knowledge Base + uet.md

---

# 🟪 5) KNOWLEDGE SYNC ENGINE (KS ENGINE)

**[ ]** L0 ingestion  
**[ ]** L1–L5 sync strategy  
**[ ]** Vector re-embed logic  
**[ ]** Node Merge Rules  
**[ ]** Edge Topology Update Rules  
**[ ]** Worker Queue / Long Task Execution  
**[ ]** KS → Event Bus events  
**[ ]** RAG Refresh pipeline  
**[ ]** Agent-triggered sync (AGENT_REQUEST_SYNC)

📄 **Source:** Versioned KB, KS sections

---

# 🟧 6) RAG ENGINE

**[ ]** Retrieval Strategy (Hybrid Search)  
**[ ]** Vector Search  
**[ ]** Keyword Search (BM25/BM42)  
**[ ]** Embedding Models  
**[ ]** Cross-Encoder Reranker  
**[ ]** Adaptive RAG logic  
**[ ]** Query Router  
**[ ]** Query Rewrite  
**[ ]** Quality Grader  
**[ ]** GraphRAG (L3–L5) Integration  
**[ ]** RAG_EVENT detection (orphan, version mismatch, etc.)

📄 **Source:** Multi-Source RAG + uet.md

---

# 🟫 7) MODEL ROUTING ENGINE

**[ ]** Static Routing  
**[ ]** Dynamic Routing  
**[ ]** Cost-based routing  
**[ ]** Performance-based routing  
**[ ]** Task Classification  
**[ ]** Complexity Level Detection  
**[ ]** Fallback Model Logic  
**[ ]** Retry rules  
**[ ]** Model Tiering (Tier 1→4)  
**[ ]** Provider abstraction  
**[ ]** Routing → Flow interaction

📄 **Source:** LLM Routing & Switching + uet.md

---

# 🟦 8) AGENT ENGINE (Single + Multi-Agent)

**[ ]** Planner  
**[ ]** Executor  
**[ ]** Reflector / Verifier  
**[ ]** ReAct Loop  
**[ ]** BabyAGI Loop  
**[ ]** Multi-Agent Orchestrator  
**[ ]** Role-based Agents  
**[ ]** Tool Calling System  
**[ ]** Shared State rules  
**[ ]** Memory (episodic / short-term / long-term)  
**[ ]** Version-bound Agent logic  
**[ ]** Safety Guard  
**[ ]** Prompt Guard

📄 **Source:** Autonomous Agent + uet.md

---

# 🟨 9) EXECUTION GRAPH SYSTEM

_(จาก Execution Graph + System Architecture)_  
**[ ]** DAG Structure  
**[ ]** Node Definitions  
**[ ]** Conditional Edges  
**[ ]** State Machine Rules  
**[ ]** Retry Policy  
**[ ]** Error Boundary Node  
**[ ]** Async + Parallel task support  
**[ ]** Re-plan Node  
**[ ]** Deterministic Execution Contract

📄 **Source:** Execution Graph + uet.md

---

# 🔵 10) FLOW CONTROL ENGINE

**[ ]** Input Sanitization  
**[ ]** Intent Classification  
**[ ]** Routing Decision  
**[ ]** Security Filters  
**[ ]** Context window guard  
**[ ]** Rate limiting rules  
**[ ]** Flow → RAG → Agent pipeline  
**[ ]** Error Handler Node

---

# ⚫ 11) EVENT BUS SYSTEM

**[ ]** Event Registry  
**[ ]** Event Types  
**[ ]** RAG Events  
**[ ]** KS Sync Events  
**[ ]** Agent Events  
**[ ]** Cache Invalidation Events  
**[ ]** Delivery Guarantee  
**[ ]** Idempotency rules  
**[ ]** Subscription/Consumer system

---

# 🟤 12) CACHE SYSTEM

**[ ]** Query Cache  
**[ ]** Embedding Cache  
**[ ]** Rerank Cache  
**[ ]** Metadata Cache  
**[ ]** Agent Result Cache  
**[ ]** Invalidations via Event Bus  
**[ ]** TTL settings

---

# 🔐 13) SECURITY & PERMISSION

**[ ]** Permission Matrix  
**[ ]** Role-based Action Control  
**[ ]** System Contract binding  
**[ ]** Safe Tool Execution  
**[ ]** Execution Graph Guardrails  
**[ ]** Error Handling Spec  
**[ ]** Logging & Audit

---

# 🖥️ 14) UI / PANEL / WORKSPACE

**[ ]** Sources Panel  
**[ ]** Chat Panel  
**[ ]** Studio Panel  
**[ ]** Layout 3-Column  
**[ ]** Document Viewer  
**[ ]** Knowledge Browser  
**[ ]** Studio Canvas Integration

---

# 🛠️ 15) API & INTERFACES

**[ ]** API Spec v1  
**[ ]** Engine Interfaces Spec  
**[ ]** Analytics API  
**[ ]** Internal Tools API  
**[ ]** File Upload / Ingestion API  
**[ ]** RAG Query API  
**[ ]** Agent Execution API

---

# 🚀 16) DEPLOYMENT

**[ ]** Deployment Guide v3.0  
**[ ]** Config Manifest  
**[ ]** Runtime Mode  
**[ ]** Monitoring / Metrics  
**[ ]** Scaling Guide  
**[ ]** CI/CD Strategy

---

# 💸 17) FINANCIAL ECOSYSTEM

**[ ]** Token Model  
**[ ]** Transaction Graph  
**[ ]** Incentive Model  
**[ ]** Wallet System  
**[ ]** Decision-making Index

---

# 🧩 18) CROSS-SYSTEM FEATURES

**[ ]** Logging & Tracing  
**[ ]** Deterministic System Enforcement  
**[ ]** Auditing  
**[ ]** Observability  
**[ ]** Session / Memory rules  
**[ ]** Reproducibility  
**[ ]** Error Recovery

---

# 🎯 สรุป

นี่คือ **MASTER CHECKLIST** ที่รวมทุกไฟล์ ทุกระบบ ทุกส่วนประกอบของ UET Platform  
พร้อมสำหรับ “ทำ Matrix” ต่อทันที

มันเป็นพื้นฐานของ:

- Room Structure
    
- Responsibility Matrix
    
- Master Blueprint Integration
    
- Engine Boundary
    
- System Contract Enforcement
    
- Architecture Mapping
    

---

โอเค Santa ได้เลย อันนี้กูทำให้เป็น **MASTER TEMPLATE** แบบที่:

- มี **ตาราง Category รวมทุกไฟล์สำคัญ**
    
- ผูกกับ **ห้อง (Room) ที่ต้องทำงาน**
    
- แล้วตามด้วย **Template การทำงานราย Category**  
    (เอาไปก็อปแตกไฟล์ / แตกห้องใช้งานได้เลย)
    

จะเขียนให้เป็น markdown ตรง ๆ เลย เผื่อนายเอาไปวางใน Obsidian / Docs ได้ทันที

---

# 📚 UET Platform — Master Category & Room Template v1.0

> ใช้เป็น “แม่แบบ” ในการแจกงานแต่ละห้อง + แยก Category + ผูกไฟล์ที่เกี่ยวข้อง  
> เป้าหมาย = ทุกห้องทำงานของตัวเองได้แบบไม่ทับไลน์กัน และมีข้อมูล backup ครบ

---

## PART A — MASTER CATEGORY TABLE (ไฟล์ → Category → Room)

> ใช้ตารางนี้เป็น “หน้าแรก” ของเอกสาร เอาไว้เช็กว่าไฟล์ไหนอยู่หมวดไหน และต้องส่งให้ห้องไหนบ้าง

### 🧾 A1. ตารางรวม Category ทั้งหมด

| Cat ID | Category                              | Primary Room      | Secondary Rooms                                           | Key Files (ตัวอย่างสำคัญ)                                                                                                                                                                                                                                                                                                         |
| ------ | ------------------------------------- | ----------------- | --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CAT-01 | System Foundation & Blueprint         | ROOM_SYSTEM       | ROOM_ARCHITECTURE, ROOM_SECURITY                          | 00__MASTER_BLUEPRINT.md, 00__MASTER_BLUEPRINT v3.0.md, UET_Platform_Master_Blueprint.pdf, Pre UET Master Blueprint.pdf, UET_Platform_Architecture_of_Trust.pdf, 01__SYSTEM_CONTRACT.md, 01__SYSTEM_CONTRACT v3.0.md, SYSTEM_CONTRACT.md, TERMINOLOGY.md, ROADMAP.md, README.md                                                    |
| CAT-02 | Global Architecture & Structure       | ROOM_ARCHITECTURE | ROOM_FLOW, ROOM_SYSTEM                                    | ARCHITECTURE_MAP.md, 02__SYSTEM ARCHITECTURE.md, 02__SYSTEM_ARCHITECTURE.md.md, PROJECT_STRUCTURE.md, 03__PROJECT STRUCTURE.md, COMPONENT_MAP.md, CONFIG_MANIFEST.md, DIAGRAM__REQUEST_FLOW.md, DIAGRAM__DATA_LIFECYCLE.md, เอกสารสถาปัตยกรรมซอฟต์แวร์ UET Platform.md, 16_execution_graph.md, การออกแบบ Execution Graph + uet.md |
| CAT-03 | Data Schema & Database                | ROOM_DATA         | ROOM_KS, ROOM_KG, ROOM_API                                | DATA_SCHEMA.md, 03__DATA_SCHEMA v3.0.md, 04__DATA_SCHEMA (Rewrite 100%).md, SQL Constraints + Index Strategy.md, SQL-Prisma Draft.md, 06,07,08_SQL_MIGRATION,CONSTRAINTS&INDEX_STRATEGY.md                                                                                                                                        |
| CAT-04 | Unified Knowledge Graph               | ROOM_KG           | ROOM_RAG, ROOM_KS                                         | 05__UNIFIED_KNOWLEDGE_GRAPH (Rewrite 100%).md, Unified Knowledge Graph Spec (L3,L4,L5).md                                                                                                                                                                                                                                         |
| CAT-05 | Versioned Knowledge Base & KS Engine  | ROOM_KS           | ROOM_DATA, ROOM_RAG, ROOM_ARCHITECTURE                    | 04__KNOWLEDGE_SYNC ENGINE v3.0.md, KNOWLEDGE_SYNC.md, 09_ks_engine.md, Versioned Knowledge Base + uet.md                                                                                                                                                                                                                          |
| CAT-06 | RAG Engine & Multi-Source RAG         | ROOM_RAG          | ROOM_AGENT, ROOM_ROUTING, ROOM_DATA, ROOM_KG              | RAG_ENGINE.md, 05__RAG_ENGINE v3.0.md, 10_rag_engine.md, Multi-Source RAG + uet.md                                                                                                                                                                                                                                                |
| CAT-07 | Agent Engine & Autonomous Agent       | ROOM_AGENT        | ROOM_FLOW, ROOM_ARCHITECTURE, ROOM_ROUTING, ROOM_SECURITY | AGENT_ENGINE BIBLE v1.0.md, 06__AGENT_ENGINE (BIBLE) v3.0.md, 11_agent_engine.md, AGENT_FLOW.md.md, Autonomous Agent + uet.md                                                                                                                                                                                                     |
| CAT-08 | Flow Control Engine                   | ROOM_FLOW         | ROOM_ARCHITECTURE, ROOM_AGENT, ROOM_RAG                   | FLOW_CONTROL.md, 12_flow_engine.md, DIAGRAM__REQUEST_FLOW.md                                                                                                                                                                                                                                                                      |
| CAT-09 | Event Bus System                      | ROOM_EVENT        | ROOM_KS, ROOM_CACHE, ROOM_RAG, ROOM_FLOW                  | 08__EVENT_BUS SYSTEM v3.0.md, EVENT_BUS.md.md, 14_event_bus.md.md                                                                                                                                                                                                                                                                 |
| CAT-10 | Model Routing & Multi-Model Switching | ROOM_ROUTING      | ROOM_FLOW, ROOM_AGENT, ROOM_SECURITY                      | 09__MODEL_ROUTING & MODEL_SELECTION v3.0.md, 13_model_routing.md.md, MODEL_SELECTION_GUIDE_TEMPLATE.md, LLM (Multi-Model Routing & Switching) + uet.md, OpenRouter.ai API & Model Analysis 2025.md                                                                                                                                |
| CAT-11 | Cache Strategy                        | ROOM_CACHE        | ROOM_RAG, ROOM_DATA, ROOM_EVENT                           | CACHE_STRATEGY.md, 10__CACHE_STRATEGY v3.0.md, 15_cache_strategy.md.md                                                                                                                                                                                                                                                            |
| CAT-12 | Security, Permission & Error Handling | ROOM_SECURITY     | ROOM_API, ROOM_SYSTEM, ROOM_FLOW                          | PERMISSION_MATRIX.md, SECURITY_RULE.md, 11__SECURITY & PERMISSION & ERROR HANDLING v3.0.md, ERROR_HANDLING.md, UET_Platform_Architecture_of_Trust.pdf                                                                                                                                                                             |
| CAT-13 | API Layer & Engine Interfaces         | ROOM_API          | ROOM_FLOW, ROOM_ARCHITECTURE, ROOM_ANALYTICS              | API_SPEC.md, API_SPEC_v1.md, ENGINE_INTERFACES.md, ANALYTICS_API.md                                                                                                                                                                                                                                                               |
| CAT-14 | UI / Panel / Workspace                | ROOM_UI           | ROOM_API, ROOM_SYSTEM                                     | UET Platform.md, โซน Panel.md, NotebookLM Mind Map.png                                                                                                                                                                                                                                                                            |
| CAT-15 | Deployment, Ops & Testing             | ROOM_DEPLOY       | ROOM_ARCHITECTURE, ROOM_AGENT                             | DEPLOYMENT_GUIDE.md, 12__DEPLOYMENT_GUIDE_v3.0.md, CONFIG_MANIFEST.md, TEST_PLAN.md                                                                                                                                                                                                                                               |
| CAT-16 | Metrics, Analytics & Monitoring       | ROOM_ANALYTICS    | ROOM_DEPLOY, ROOM_API, ROOM_RAG, ROOM_AGENT               | METRICS_SPEC.md, ANALYTICS_API.md (shared), log/trace spec (ถ้ามีเขียนเพิ่มทีหลัง)                                                                                                                                                                                                                                                |
| CAT-17 | Financial Ecosystem & Tokenomics      | ROOM_FINANCE      | ROOM_SYSTEM                                               | 🏛️ UET Financial Ecosystem Design Document.md, chaydav.3.0.md                                                                                                                                                                                                                                                                    |
| CAT-18 | Media / Knowledge Presentation        | ROOM_SYSTEM       | ROOM_UI                                                   | พิมพ์เขียวสู่_AI_ที่ไว้ใจได้.mp4                                                                                                                                                                                                                                                                                                  |

> ถ้านายมีไฟล์ใหม่เพิ่มในอนาคต → แค่เพิ่มแถวใหม่ในตารางนี้  
> แล้วระบุ Category + Primary/Secondary Room ให้ชัด

---

## PART B — WORKSHEET TEMPLATE ต่อ Category

> ใช้สำหรับ “แผ่นทำงาน” ของแต่ละห้อง/แต่ละหมวด  
> รูปแบบเดียวกันทั้งระบบ แต่มีการเติม “ไฟล์สำคัญ” ให้แล้ว

**วิธีใช้:**

- ให้แต่ละห้อง copy section ของ Category ที่ตัวเองรับผิดชอบไปคนละไฟล์/คนละหน้า
    
- แล้วค่อย ๆ เติมเนื้อหาลงในช่องที่เป็น `TODO` / `…`
    

---

### 🧩 TEMPLATE กลาง (ใช้ซ้ำได้ทุก Category)

```markdown
## [CAT-ID] — [CATEGORY NAME]

### 1. Scope & Mission
- เป้าหมายหลักของ Category นี้:
  - …
- สิ่งที่ “ต้องทำให้สำเร็จ”:
  - …

### 2. Boundary (In-scope / Out-of-scope)
- ✅ In-scope:
  - …
- ❌ Out-of-scope:
  - …

### 3. Input Files (จาก MASTER TABLE)
- [ ] … (ไฟล์หลัก 1)
- [ ] … (ไฟล์หลัก 2)
- [ ] … (เวอร์ชัน PDF / Diagram ที่เกี่ยวข้อง)
- ถ้ามีไฟล์ใหม่ในอนาคตให้เพิ่มที่นี่ด้วย

### 4. Required Outputs (Artifacts)
- [ ] SPEC หลักของหมวดนี้ (เช่น `RAG_ENGINE_MASTER_SPEC.md`)
- [ ] Diagram / Flow (ถ้ามี)
- [ ] Interface หรือ Contract ที่ต้องเผยแพร่ให้ห้องอื่นใช้
- [ ] Checklist ว่า spec นี้ “อ่านแล้ว implement ได้เลย”

### 5. Key Decisions
- [ ] ต้องตัดสินใจเรื่อง…
- [ ] ต้องเลือก approach ระหว่าง … กับ …
- [ ] Policy / Rule ที่จะผูกกับ System Contract

### 6. Cross-Room Dependencies
- ขึ้นกับห้อง:
  - ROOM_… (ใช้ในเรื่องอะไร)
- ห้องอื่นที่ต้องอ่าน spec ของ Category นี้:
  - ROOM_…

### 7. Validation & Condition
- [ ] ผ่านรีวิวจาก ROOM_SYSTEM (ถ้ากระทบ contract)
- [ ] ผ่านรีวิวจาก ROOM_SECURITY (ถ้ากระทบสิทธิ/ความปลอดภัย)
- [ ] มี test plan / test case ที่เชื่อมโยงแล้ว
- [ ] ระบุ version ชัดเจน (v1, v2, v3…)

### 8. TODO / Open Questions
- …
- …
```

---

ต่อไปกูจะ “อินสแตนซ์” template นี้ให้กับ **ทุกหมวดหลัก** โดยใส่ไฟล์สำคัญให้เรียบร้อย  
(นายจะได้แทบไม่ต้องคิดโครงเองแล้ว แค่ไปเติมเนื้อหา)

---

### CAT-01 — System Foundation & Blueprint (ROOM_SYSTEM)

```markdown
## CAT-01 — System Foundation & Blueprint

### 1. Scope & Mission
- สร้าง “ภาพรวม” และ “กฎหมายแม่บท” ของ UET Platform
- นิยามความหมาย, วัตถุประสงค์, หลักการศูนย์สมดุล, และมุมมองระบบต่อโลก

### 2. Boundary
- ✅ In-scope:
  - หลักการ, Concept, System Contract, Terminology
- ❌ Out-of-scope:
  - Logic ของ Engine (RAG/Agent/KS)
  - Data Schema details

### 3. Input Files
- [ ] 00__MASTER_BLUEPRINT.md
- [ ] 00__MASTER_BLUEPRINT v3.0.md
- [ ] UET_Platform_Master_Blueprint.pdf
- [ ] Pre UET_Platform_Master_Blueprint.pdf
- [ ] UET_Platform_Architecture_of_Trust.pdf
- [ ] 01__SYSTEM_CONTRACT.md / v3.0
- [ ] SYSTEM_CONTRACT.md
- [ ] TERMINOLOGY.md
- [ ] ROADMAP.md
- [ ] README.md

### 4. Required Outputs
- [ ] SYSTEM_FOUNDATION_SPEC.md (สรุปแก่นทั้งหมด)
- [ ] SYSTEM_CONTRACT_MASTER.md (ฉบับสุดท้าย)
- [ ] TERMINOLOGY_MASTER.md (ภาษากลางของทั้งแพลตฟอร์ม)
- [ ] PRINCIPLES_OF_TRUST.md (เชื่อมกับ Architecture of Trust)

### 5. Key Decisions
- [ ] ขอบเขตของ “AI ที่ไว้ใจได้” ในแบบ UET
- [ ] หลักการตัดสินใจของระบบ (Impact-based ethics / ศูนย์สมดุล)
- [ ] ข้อห้ามสูงสุดของระบบ (Red line)

### 6. Cross-Room Dependencies
- ROOM_ARCHITECTURE → ใช้หลักการไปออกแบบโครงสร้าง
- ROOM_SECURITY → ใช้เพื่อวาง security model
- ROOM_FINANCE → ใช้ในการออกแบบระบบเศรษฐกิจ

### 7. Validation & Condition
- [ ] Blueprint ตรงกับ Architecture v3.0
- [ ] System Contract ไม่ขัดกับความเป็นไปได้ทางเทคนิคใน ROOM_ARCHITECTURE
- [ ] Terminology สอดคล้องทุกเอกสาร

### 8. TODO / Open Questions
- …
```

---

### CAT-02 — Global Architecture & Structure (ROOM_ARCHITECTURE)

```markdown
## CAT-02 — Global Architecture & Structure

### 1. Scope & Mission
- วางผังโครงสร้างทั้งหมดของ UET Platform (Layer, Engine, Flow, Execution Graph)

### 2. Boundary
- ✅ In-scope: Layer, Module, Execution Graph, Diagram
- ❌ Out-of-scope: Logic detail ของ RAG/Agent/KS

### 3. Input Files
- [ ] ARCHITECTURE_MAP.md
- [ ] 02__SYSTEM ARCHITECTURE.md / .md.md
- [ ] PROJECT_STRUCTURE.md
- [ ] 03__PROJECT STRUCTURE.md
- [ ] COMPONENT_MAP.md
- [ ] CONFIG_MANIFEST.md
- [ ] DIAGRAM__REQUEST_FLOW.md
- [ ] DIAGRAM__DATA_LIFECYCLE.md
- [ ] เอกสารสถาปัตยกรรมซอฟต์แวร์ UET Platform.md
- [ ] 16_execution_graph.md
- [ ] การออกแบบ Execution Graph สำหรับระบบ LLM + uet.md

### 4. Required Outputs
- [ ] UET_ARCHITECTURE_OVERVIEW.md
- [ ] EXECUTION_GRAPH_MASTER.md
- [ ] REQUEST_FLOW_MASTER.png / .md
- [ ] DATA_LIFECYCLE_MASTER.md

### 5. Key Decisions
- [ ] จุดตัดระหว่าง Flow Engine, RAG, Agent, KS
- [ ] รูปแบบ Execution Graph (deterministic, retry, fallback)
- [ ] ขอบเขตความรับผิดชอบของแต่ละ Engine

### 6. Cross-Room Dependencies
- ROOM_FLOW (ใช้ execution graph)
- ROOM_AGENT (ต้อง align กับ graph)
- ROOM_RAG / KS / DATA (ต้อง align with data flow)

### 7. Validation & Condition
- [ ] ทุก Engine มี node/edge ที่ชัดใน Execution Graph
- [ ] ไม่เกิด “วงจรสุ่ม” ที่ไม่สามารถ trace ได้
- [ ] ผังสอดคล้องกับ System Contract

### 8. TODO / Open Questions
- …
```

---

ต่อไปกูจะไม่เขียนยาวเท่าบล็อกแรก แต่จะวางโครงพร้อม list ไฟล์ให้ครบ (นายเอาไปเติมเองได้)

---

### CAT-03 — Data Schema & Database (ROOM_DATA)

- Scope: โครงสร้างข้อมูลทั้งหมด, Table, Index, Migration
    
- Input:
    - DATA_SCHEMA.md
    - 03__DATA_SCHEMA v3.0.md
    - 04__DATA_SCHEMA (Rewrite 100%).md
    - SQL Constraints + Index Strategy.md
    - SQL-Prisma Draft.md
    - 06,07,08_SQL_MIGRATION,CONSTRAINTS&INDEX_STRATEGY.md
        
- Outputs:
    - DATA_SCHEMA_MASTER.md
    - DB_MIGRATION_PLAN.md
    - INDEX_STRATEGY_MASTER.md
        

(ใช้ TEMPLATE กลางด้านบนเติมรายละเอียดทีหลัง)

---

### CAT-04 — Unified Knowledge Graph (ROOM_KG)

- Input:
    - 05__UNIFIED_KNOWLEDGE_GRAPH (Rewrite 100%).md
    - Unified Knowledge Graph Spec (L3,L4,L5).md
        
- Outputs:
    - KG_ONTOLOGY_MASTER.md
    - KG_NODE_EDGE_SPEC.md
        

---

### CAT-05 — Versioned KB & KS Engine (ROOM_KS)

- Input:
    - 04__KNOWLEDGE_SYNC ENGINE v3.0.md
    - KNOWLEDGE_SYNC.md
    - 09_ks_engine.md
    - Versioned Knowledge Base + uet.md
        
- Outputs:
    - KS_ENGINE_MASTER_SPEC.md
    - KB_VERSIONING_RULES.md
        

---

### CAT-06 — RAG Engine (ROOM_RAG)

- Input:
    - RAG_ENGINE.md
    - 05__RAG_ENGINE v3.0.md
    - 10_rag_engine.md
    - Multi-Source RAG + uet.md
        
- Outputs:
    - RAG_ENGINE_MASTER_SPEC.md
    - RAG_PIPELINE_CONFIG.md
        

---

### CAT-07 — Agent Engine (ROOM_AGENT)

- Input:
    - AGENT_ENGINE BIBLE v1.0.md
    - 06__AGENT_ENGINE (BIBLE) v3.0.md
    - 11_agent_engine.md
    - AGENT_FLOW.md.md
    - Autonomous Agent + uet.md
        
- Outputs:
    - AGENT_ENGINE_MASTER_SPEC.md
    - AGENT_FLOW_MASTER.md
        

---

### CAT-08 — Flow Engine (ROOM_FLOW)

- Input:
    - FLOW_CONTROL.md
    - 12_flow_engine.md
    - DIAGRAM__REQUEST_FLOW.md
        
- Outputs:
    - FLOW_ENGINE_MASTER_SPEC.md
    - ENTRYPOINT_ROUTING_RULES.md
        

---

### CAT-09 — Event Bus (ROOM_EVENT)

- Input:
    - 08__EVENT_BUS SYSTEM v3.0.md
    - EVENT_BUS.md.md
    - 14_event_bus.md.md
        
- Outputs:
    - EVENT_BUS_MASTER_SPEC.md
    - EVENT_TYPES_REGISTRY.md
        

---

### CAT-10 — Model Routing (ROOM_ROUTING)

- Input:
    - 09__MODEL_ROUTING & MODEL_SELECTION v3.0.md
    - 13_model_routing.md.md
    - MODEL_SELECTION_GUIDE_TEMPLATE.md
    - LLM (Multi-Model Routing & Switching) + uet.md
    - OpenRouter.ai API & Model Analysis 2025.md
        
- Outputs:  
    - MODEL_ROUTING_MASTER_SPEC.md
    - PROVIDER_MATRIX.md
        

---

### CAT-11 — Cache Strategy (ROOM_CACHE)

- Input:
    - CACHE_STRATEGY.md
    - 10__CACHE_STRATEGY v3.0.md
    - 15_cache_strategy.md.md
        
- Outputs:
    - CACHE_LAYER_MASTER_SPEC.md
    - CACHE_INVALIDATION_RULES.md

---

### CAT-12 — Security / Permission / Error (ROOM_SECURITY)

- Input:
    - PERMISSION_MATRIX.md
    - SECURITY_RULE.md
    - 11__SECURITY & PERMISSION & ERROR HANDLING v3.0.md
    - ERROR_HANDLING.md
    - UET_Platform_Architecture_of_Trust.pdf
        
- Outputs:
    - SECURITY_MASTER_SPEC.md
    - PERMISSION_MATRIX_MASTER.md
    - ERROR_HANDLING_MASTER.md

---

### CAT-13 — API & Interfaces (ROOM_API)

- Input:
    
    - API_SPEC.md
        
    - API_SPEC_v1.md
        
    - ENGINE_INTERFACES.md
        
    - ANALYTICS_API.md
        
- Outputs:
    
    - API_MASTER_SPEC.md
        
    - ENGINE_INTERFACE_CONTRACTS.md
        

---

### CAT-14 — UI / Panel (ROOM_UI)

- Input:
    
    - UET Platform.md
        
    - โซน Panel.md
        
    - NotebookLM Mind Map.png
        
- Outputs:
    
    - UI_LAYOUT_MASTER.md
        
    - PANEL_BEHAVIOR_RULES.md
        

---

### CAT-15 — Deployment & Testing (ROOM_DEPLOY)

- Input:
    
    - DEPLOYMENT_GUIDE.md
        
    - 12__DEPLOYMENT_GUIDE_v3.0.md
        
    - CONFIG_MANIFEST.md
        
    - TEST_PLAN.md
        
- Outputs:
    
    - DEPLOYMENT_MASTER_GUIDE.md
        
    - ENV_CONFIG_REFERENCE.md
        
    - TEST_STRATEGY_MASTER.md
        

---

### CAT-16 — Metrics / Analytics (ROOM_ANALYTICS)

- Input:
    
    - METRICS_SPEC.md
        
    - ANALYTICS_API.md
        
- Outputs:
    
    - METRICS_DASHBOARD_SPEC.md
        
    - OBSERVABILITY_PLAN.md
        

---

### CAT-17 — Financial Ecosystem (ROOM_FINANCE)

- Input:
    
    - 🏛️ UET Financial Ecosystem Design Document.md
        
    - chaydav.3.0.md
        
- Outputs:
    
    - UET_ECONOMY_MASTER_SPEC.md
        
    - TOKEN_MODEL_MASTER.md
        

---

### CAT-18 — Media / Presentation (ROOM_SYSTEM + ROOM_UI)

- Input:
    
    - พิมพ์เขียวสู่_AI_ที่ไว้ใจได้.mp4
        
- Outputs:
    
    - CONTENT_SCRIPT_OUTLINE.md
        
    - VIDEO_NARRATIVE_GUIDE.md
        

---

## PART C — วิธีใช้ MASTER TEMPLATE นี้จริง ๆ

1. ใช้ **PART A ตาราง Category** เป็น “สารบัญไฟล์ + route ไปห้อง”
    
2. ให้แต่ละห้อง copy sectionของ Category ตัวเองใน PART B ไปเป็นไฟล์ใหม่
    
3. แต่ละห้องเติม:
    
    - Scope & Mission
        
    - Boundary
        
    - Output ที่จะส่งให้ห้องอื่น
        
    - Checklist & TODO
        
4. เมื่อทุกห้องเขียน SPEC เสร็จ → ค่อยรวมเป็น  
    **UET_PLATFORM_MASTER_SPEC.md** อีกเลเยอร์หนึ่ง
    

---

ถ้านายอยากให้กู

- แปลงสิ่งนี้เป็น **ฉบับ “ROOM RESPONSIBILITY MATRIX v2.0” แบบเน้นห้อง**
    
- หรือแตกเป็น **template แยกไฟล์ (เช่น 1 ไฟล์ต่อ Category)**
    

ก็บอกได้เลย เดี๋ยวกูจัด structure ให้แบบพร้อมเอาไปใช้จริง 👌