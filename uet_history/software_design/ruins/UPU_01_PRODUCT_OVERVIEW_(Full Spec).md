# UPU v1 — PRODUCT OVERVIEW (Full Spec)

## 1. Mission / Vision

**สร้างแพลตฟอร์มที่เป็น "Unified Intelligence Workspace"** — ศูนย์กลางที่รวม ChatGPT + NotebookLM + RAG + Studio เข้าด้วยกันในหน้าเดียว เพื่อให้ผู้ใช้ทุกระดับสามารถ _คิด, วิเคราะห์, ทำงาน, สร้างงาน, วิจัย_ ได้ในพื้นที่เดียวอย่างลื่นไหล

แพลตฟอร์มจะทำหน้าที่เป็น:

- เครื่องมือคิด (Thinking Engine)
    
- เครื่องมือทำงาน (Working Engine)
    
- เครื่องมือเรียนรู้ (Learning Engine)
    
- เครื่องมือวิจัย (Research Engine)
    
- เครื่องมือจัดการความรู้ (Knowledge Engine)
    

ทั้งหมดในที่เดียวโดยไม่ต้องสลับแอป

---

## 2. Target User Levels

### **Level 1 – ผู้ใช้ทั่วไป**

- ใช้แชท AI
    
- ค้นคว้าพื้นฐาน
    
- อัปโหลดไฟล์ให้ AI อ่านแบบ NotebookLM แบบง่าย
    

### **Level 2 – ผู้ใช้ปกติ**

- ใช้ RAG จาก KB กลาง
    
- ใช้ AutoPrompt
    
- ใช้ Studio (Notebook / Canvas)
    

### **Level 3 – ผู้ใช้ไม่ปกติ (Advanced)**

- สามารถแก้ไข KB โดยตรง
    
- รวมไฟล์ / merge knowledge
    
- ตัดไฟล์ผิด / maintain KB
    
- ทำวิจัยลึก (Deep Research)
    

### **Level 4 – องค์กร / ทีม**

- แชร์โปรเจกต์
    
- ทำงานร่วมกันหลายคน
    
- ใช้ AI Studio ในงานจริง
    

---

## 3. Core Capabilities (ต้องมีแบบ 100%)

### **A) Chat (ChatGPT + NotebookLM)**

ทุกฟีเจอร์ที่จำเป็น:

- แชทปกติแบบ ChatGPT
    
- อ่านไฟล์แบบ NotebookLM
    
- ใช้ RAG จาก KB
    
- อัปโหลดและเลือกไฟล์ที่ต้องการอ้างอิง
    
- Deep Research Mode
    
- Web Search Mode
    
- AutoPrompt Mode
    
- Canvas Mode (สร้างไฟล์ .md ใหม่)
    
- Multi-model selection
    
- File-aware chat
    

### **B) Update Abilities (ทุกหน้าต้องอัปเดตได้)**

- Home → ข่าว, ฟีเจอร์ใหม่, ระบบสถานะ
    
- Projects → สร้างโปรเจกต์ / file system
    
- Theory → เพิ่มบท, อัปเดตเนื้อหา
    
- Donate → อัปเดตจำนวนเงิน, tier system
    
- Dashboard/Studio → ดู ingestion, debug, tasks
    

### **C) Knowledge Management (หัวใจระบบ)**

KB ความสามารถแบบเต็มระบบ:

- อัปโหลดไฟล์เข้า KB
    
- ตัดไฟล์ผิด
    
- merge knowledge
    
- create central KB
    
- ใช้ในแชท
    
- ใช้ในโปรเจกต์
    
- อัปเดตเป็น real-time
    

ระบบต้องรองรับอนาคต:

- AI maintain KB อัตโนมัติ
    
- restructure knowledge
    
- refactor knowledge
    

---

## 4. Global UI — ทุกหน้าต้องมี

1. **Navbar** (Global Navigation)
    
    - Logo → new chat
        
    - Home
        
    - Theory
        
    - Projects
        
    - Donate
        
    - Login/Profile
        
2. **Persistent Sidebar** (Global Sidebar)
    
    - Search chat
        
    - History chat
        
    - Profile
        
    - Upgrade
        
    - Settings
        
    - Help
        
    - Logout
        

Sidebar นี้จะอยู่ทุกหน้า แต่จะนำผู้ใช้เข้าไปหน้าแชทเมื่อเลือกแชทใด ๆ

---

## 5. Workspace UI — เฉพาะหน้า Chat

หน้า Chat = หน้าหลักของระบบ

ต้องมี 3 Panel แบบ Workspace จริง

### **Left Panel — Sources Workspace (NotebookLM-like)**

มี 3 หมวด:

- KB
    
- Upload
    
- Update (จาก Project / Theory / Home)
    

ฟีเจอร์หลัก:

- search ไฟล์
    
- preview
    
- open full view
    
- แก้ไข metadata
    
- ติ๊กเลือกไฟล์เพื่อส่งเข้าแชท
    
- ทำ merge
    
- ตัดไฟล์ผิด
    

### **Center Panel — Chat Workspace (ChatGPT-like)**

ประกอบด้วย:

- Chat messages
    
- ปุ่ม + Action (Deep Research / Canvas / Web Search / Upload)
    
- Input bar + mic
    

### **Right Panel — Studio Workspace (NotebookLM Studio)**

มี 2 โหมดสลับกัน:

#### 1) Notebook Mode

- ไฟล์ .md ทั้งหมด
    
- แก้ไขได้
    
- โหลดได้
    
- ส่งเข้าแชทได้
    

#### 2) AutoPrompt Mode

- วิเคราะห์ไฟล์
    
- เขียนรายงาน
    
- เขียนบล็อก
    
- สร้างคู่มือ
    
- Full Paper
    
- Python simulation
    
- Parameter testing
    
- วิจัยเชิงลึก
    
- Audio summary
    
- Video summary
    

**Notebook = Canvas = Studio File** (ทั้งหมดหมายถึงอันเดียวกัน)

---

## 6. UX Principle

- เร็วที่สุด
    
- เรียบที่สุด
    
- ฉลาดที่สุด
    
- ทุกอย่างเชื่อมโยงกัน
    
- ใช้ไฟล์ร่วมกันได้หมด
    
- ไม่พังง่าย
    
- ไม่ต้องกดหลายขั้นตอน
    
- hybrid workflow (Chat ↔ Notebook ↔ Files ↔ AutoPrompt)
    

---

## 7. System Behavior Rules

### **1) Action Button Behavior**

- ถ้าเลือก “Canvas” = เปิด Studio Notebook ใหม่
    
- ถ้าเลือก “Deep Research” = ส่ง prompt + context mode
    
- ถ้าเลือก “AutoPrompt” = เปิด panel ขวา
    
- ถ้าไม่เลือกอะไร = ตอบปกติ (ตอบสั้น)
    

### **2) Studio Panel Rules**

- Studio Panel = Notebook / AutoPrompt
    
- Canvas = Notebook ใหม่
    
- เปิดพร้อม Chat Panel ได้
    
- ปิด = กลับสู่หน้า chat ปกติ
    

### **3) Global vs Local**

- Global Sidebar = อยู่ทุกหน้า แต่ส่งผู้ใช้เข้า Chat เมื่อเลือก chat
    
- Chat left/right panels = อยู่เฉพาะหน้า Chat
    

---

## 8. Constraints

- ต้องรองรับไฟล์ใหญ่ (PDF, MD, TXT)
    
- ต้องรองรับ ingestion จำนวนมาก
    
- ต้องตอบเร็ว
    
- ต้องรองรับ RAG จริง
    
- ต้องรองรับ extension ของ AI ในอนาคต
    

---

## 9. Success Metrics

- Chat โหลด < 200ms
    
- File process < 3s
    
- Notebook open < 150ms
    
- Studio auto output < 5s initial
    
- ผู้ใช้รู้สึกว่า "มันเร็ว ฉลาด ลื่น และเชื่อมกันหมด"

----
