# 🏛️ UET Platform
Unified Intelligence Workspace for Research, Theory-Building, and Collaboration

UET Platform คือแพลตฟอร์มที่ออกแบบมาเพื่อ **พัฒนา สังเคราะห์ และทดลองความรู้เชิงโครงสร้าง**  
โดยรวม AI, ระบบจัดการไฟล์, ชุมชน, โปรเจกต์, และ Studio สำหรับสร้างงานวิชาการไว้ในที่เดียว

เป้าหมายของระบบคือสร้าง “ศูนย์กลางความรู้ (Unified Knowledge Core)”  
ที่ให้ทุกคนสามารถสร้างทฤษฎี งานวิจัย และโปรเจกต์ร่วมกันได้อย่างโปร่งใส ขยายตัวได้ และตรวจสอบได้

---

## 🎯 Core Concept
UET Platform ขับเคลื่อนด้วย 3 แกนหลัก:

1. **Knowledge Workspace**  
   – Sources Panel (ไฟล์ + กราฟ)  
   – Chat Panel (AI/RAG)  
   – Studio Panel (เขียน/ตัดต่อความรู้)

2. **Unified Knowledge Base (KB)**  
   – เก็บไฟล์ → chunk → embed → search  
   – ใช้ร่วมกันทั้งระบบ (Theory / Project / Community)

3. **Collaboration Layer**  
   – Projects ให้คนทำงานร่วมกัน  
   – Community สำหรับพูดคุย/เสนอไอเดีย  
   – Theory สำหรับเผยแพร่เนื้อหาที่ผ่านการสังเคราะห์แล้ว

---

## 🧱 System Architecture
แพลตฟอร์มถูกออกแบบเป็น 3 ชั้นซ้อนกัน:

- **Frontend (UI/UX)**  
  Next.js + Tailwind + Panel System  
  ใช้โครงสร้าง Page → Layout → Panel เพื่อ reuse ได้ทุกหน้า

- **Application Layer**  
  ระบบ Chat, Studio, Projects, Community, RAG Engine, Voting, Metrics

- **Backend + Data Layer**  
  Auth, DB, Vector Search, Knowledge Base, Donation Ledger

อิงจากการออกแบบโซนและระบบ panels ตามเอกสารภายใน
(เช่น Sources/Chat/Studio)  
และสเปกของโซนต่าง ๆ จากไฟล์ UET Platform  
:contentReference[oaicite:2]{index=2}

---

## 🖼️ Core Panels (หัวใจแพลตฟอร์ม)
1. **Sources Panel** — คลังความรู้  
2. **Chat Panel** — โต้ตอบ AI + citation  
3. **Studio Panel** — พื้นที่สร้างโน้ต รายงาน ทฤษฎี บทวิเคราะห์  

โครงสร้างนี้ใช้เป็นแกนกลางของทุก Workspace  
:contentReference[oaicite:3]{index=3}

---

## 📦 Main Features
- **RAG Chat + Multi-KB**
- **Graph File Navigator (เหมือน Obsidian)**
- **Studio Editor + AutoPrompt**
- **Projects (เหมือน Discord + Notion workspace)**
- **Community (Feels + Feed + Social Chat)**
- **Theory Publishing (หมวด 1–12)**
- **Donation & Ledger (โปร่งใส ตรวจสอบได้)**

---

## 🔐 User Roles
- **Guest** – เข้าชมส่วนสาธารณะ  
- **Member** – แชท + ไฟล์ส่วนตัว + Studio  
- **Power User** – โปรเจกต์, multi-KB, auto research  
- **Admin** – ดูแลระบบ, audit, manage KB

---

## 📂 Repository Structure (แนะนำแบบมาตรฐาน)

/app  
/api # API endpoints  
/components # UI components (panels/layouts)  
/pages # Page routes  
/workspace # Sources + Chat + Studio  
/lib  
/rag # File processor + embeddings  
/db # Database models  
/utils  
/public  
/assets

---

## 🚧 Development Status
- [x] Architecture Defined  
- [x] Zone System & Panel System  
- [x] Knowledge Base Workflow  
- [ ] API Implementation  
- [ ] Frontend Integration  
- [ ] Project/Community Full Features  

Roadmap เต็มอยู่ในไฟล์ `ROADMAP.md`  
:contentReference[oaicite:4]{index=4}

---

## 📜 License
Proprietary — UET Research & Santa Initiative

---

