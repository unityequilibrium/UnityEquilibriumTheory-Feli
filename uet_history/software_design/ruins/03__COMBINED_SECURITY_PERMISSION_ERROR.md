# COMBINED: SECURITY / PERMISSION / ERROR



# FILE: PERMISSION_MATRIX.md

โอเค Santa —  
ต่อไปนี้คือ **PERMISSION_MATRIX.md** เวอร์ชัน “กระชับ ชัดเจน ครอบคลุมทั้งระบบ”  
ใช้ร่วมกับ SECURITY_RULES.md, SYSTEM_CONTRACT.md, KNOWLEDGE_SYNC.md และ AGENT_FLOW.md ได้ทันที

รูปแบบ = ตารางเดียวจบ + กฎประกอบสั้นๆ  
อ่านแล้วเข้าใจสิทธิ์ทั้งหมดภายใน 30 วินาที

---

# 📘 **PERMISSION_MATRIX.md**

**UET Platform — Permission & Access Control Matrix**  
**เวอร์ชัน 1.0 (แบบกระชับใช้จริงได้ทันที)**

---

# **0. เป้าหมายของไฟล์นี้**

กำหนดว่า “ผู้ใช้แต่ละประเภททำอะไรได้บ้าง” ในทุกส่วนของระบบ:

- Workspace
    
- Project
    
- Knowledge Base
    
- Studio
    
- Agent
    
- API
    
- Admin Ops
    

และกำหนด boundary ชัดเจนไม่ให้ก้าวล้ำสิทธิ์กัน  
เพื่อให้ระบบปลอดภัยและ deterministic

---

# **1. User Roles**

|Role|คำอธิบาย|
|---|---|
|**Guest**|ผู้ใช้ทั่วไป ไม่ล็อกอิน|
|**Member**|ผู้ใช้ทั่วไปที่ล็อกอิน + มีโปรเจกต์ส่วนตัว|
|**Power User**|ผู้ใช้ขั้นสูง + เข้าโหมด advanced / agent engine ได้|
|**Admin**|ผู้ดูแลระบบ มีสิทธิ์เต็ม|

---

# **2. Permission Matrix (ตารางสิทธิ์หลัก)**

## 🔥 ตารางสำคัญที่สุดในระบบ (ดูง่ายที่สุด)

```
Legend:
✔ = ทำได้
✖ = ทำไม่ได้
△ = ทำได้แต่จำกัด (มีเงื่อนไข)
A = ต้องได้รับอนุญาตเฉพาะจาก Admin
```

---

## **2.1 Project-Level Permissions**

|Action / Role|Guest|Member|Power User|Admin|
|---|:-:|:-:|:-:|:-:|
|ดูโปรเจกต์ Public|✔|✔|✔|✔|
|สร้างโปรเจกต์ใหม่|✖|✔|✔|✔|
|แก้โปรเจกต์ของตัวเอง|✖|✔|✔|✔|
|แก้โปรเจกต์ของผู้อื่น|✖|✖|✖|✔|
|ลบโปรเจกต์|✖|✖|△ (เฉพาะของตัวเอง)|✔|
|เข้าดูไฟล์ในโปรเจกต์คนอื่น|✖|✖|✖|✔|

---

## **2.2 Knowledge Base Permissions (P-KB / G-KB)**

|Action / Role|Guest|Member|Power User|Admin|
|---|:-:|:-:|:-:|:-:|
|อ่าน Global KB|✖|✔ (บางส่วน)|✔|✔|
|อัปโหลดไฟล์เข้า Project KB|✖|✔|✔|✔|
|แก้ไฟล์ใน Project KB|✖|✔|✔|✔|
|แก้ Global KB|✖|✖|✖|✔ (A)|
|ลบไฟล์|✖|△ (ไฟล์ตัวเอง)|△|✔|
|Merge P-KB → G-KB|✖|✖|✖|✔ (ผ่าน governance)|

> **หมายเหตุ:**  
> **Admin ต้องยืนยันทุกครั้งสำหรับการแก้ Global KB**

---

## **2.3 Studio Permissions (พื้นที่เขียนงาน)**

|Action / Role|Guest|Member|Power User|Admin|
|---|:-:|:-:|:-:|:-:|
|เปิด Studio|✖|✔|✔|✔|
|บันทึกไฟล์ลงโปรเจกต์|✖|✔|✔|✔|
|บันทึกไฟล์ลง Global|✖|✖|✖|✔|
|สร้าง canvas/report ผ่าน Agent|✖|✔|✔ (Advanced)|✔|

---

## **2.4 Agent Permissions**

|Action / Role|Guest|Member|Power User|Admin|
|---|:-:|:-:|:-:|:-:|
|ใช้ Agent (พื้นฐาน)|✖|✔|✔|✔|
|ใช้ Agent ขั้นสูง (analysis, simulation)|✖|✖|✔|✔|
|ให้ Agent เขียนไฟล์|✖|✔ (เฉพาะโปรเจกต์ตัวเอง)|✔|✔|
|ให้ Agent แก้ Global KB|✖|✖|✖|✖ (Admin ต้องทำเอง)|
|เรียก Data API ผ่าน Agent|✖|✔|✔|✔|

---

## **2.5 API Permissions**

|API / Role|Guest|Member|Power User|Admin|
|---|:-:|:-:|:-:|:-:|
|GET (public data)|✔|✔|✔|✔|
|GET private/project data|✖|✔|✔|✔|
|POST/PUT/PATCH project files|✖|✔|✔|✔|
|DELETE project files|✖|✖|△|✔|
|POST knowledge upload|✖|✔|✔|✔|
|Admin API|✖|✖|✖|✔|

---

## **2.6 System & Config Permissions**

|Action / Role|Guest|Member|Power User|Admin|
|---|:-:|:-:|:-:|:-:|
|อ่าน Config Manifest|✖|✖|△ (บางส่วน)|✔|
|แก้ Config Manifest|✖|✖|✖|✔|
|แก้ตั้งค่าระบบ (deployment / env)|✖|✖|✖|✔|
|เข้าถึง event logs|✖|✖|△|✔|

---

# **3. Boundary Rules (กฎเขตแดนการเข้าถึง)**

### **Rule 1 — ผู้ใช้ไม่สามารถเห็นโปรเจกต์ที่ไม่ใช่ของตัวเอง**

ยกเว้น:

- โปรเจกต์ public
    
- Admin
    

### **Rule 2 — Agent ถูกจำกัดตามสิทธิ์ของผู้ใช้**

Agent = extension ของผู้ใช้  
→ ทำอะไรเกินสิทธิ์ผู้ใช้ไม่ได้

### **Rule 3 — KB แบ่งชัดเจนเป็น 3 ระดับ**

- Personal
    
- Project
    
- Global
    

ไม่มีการข้ามระดับโดยอัตโนมัติ

### **Rule 4 — Global KB แตะได้เฉพาะ Admin**

ตาม SYSTEM_CONTRACT

### **Rule 5 — Merge, Delete, Promote ต้อง log เสมอ**

เพื่อ audit ย้อนหลัง

---

# **4. Permission Logic (เข้าใจภายใน 10 วิ)**

```
Guest        = อ่าน public ได้อย่างเดียว  
Member       = เขียนได้เฉพาะของตัวเอง  
Power User   = ทำงานหนัก + agent ขั้นสูง  
Admin        = คุมระบบทั้งหมด  
```

---

# **5. Permission Formula (กฎคำนวณแบบสั้น)**

เมื่อผู้ใช้ทำ action ใด ๆ:

```
is_allowed = ROLE.permit(action) 
             AND CONTEXT.match(project/user) 
             AND SYSTEM_CONTRACT.allow(action)
```

ถ้าผิดอย่างใดอย่างหนึ่ง → reject

---

# **6. Relationship กับ Security Rules**

PERMISSION_MATRIX ทำงานคู่กับ:

- SECURITY_RULES → ป้องกัน misuse
    
- SYSTEM_CONTRACT → กำหนด boundary
    
- KNOWLEDGE_SYNC → ควบคุมการแก้ไข KB
    
- AGENT_FLOW → จำกัด agent
    

**ทั้งหมดรวมกัน = ระบบปลอดภัยและ deterministic**

---

# **7. สรุปสั้นที่สุด (จำจริงได้ใน 5 วินาที)**

### ✔ Guest: ดูได้อย่างเดียว

### ✔ Member: แก้ของตัวเองได้

### ✔ Power User: ใช้ Agent ขั้นสูงได้

### ✔ Admin: ทำทุกอย่าง แต่ทุก action ต้องมี log

---

# ⚡ ถ้าต้องการส่วนเสริม:

ฉันสามารถเขียนให้ต่อได้ทันที:

- **MODEL_SELECTION_GUIDE.md** (กฎเลือกโมเดล AI)
    
- **CACHE_STRATEGY.md**
    
- **DEPLOYMENT_GUIDE.md**
    
- **TEST_PLAN.md**
    

เลือกอันถัดไปได้เลย ❤️


# FILE: SECURITY_RULE.md

โอเค Santa —  
ต่อไปนี้คือ **SECURITY_RULES.md** เวอร์ชันที่ “กระชับที่สุด แต่คุมระบบทั้งหมดแบบมืออาชีพ”  
เขียนโดยอิงทุกไฟล์ระบบที่นายมี: SYSTEM_CONTRACT, FLOW_CONTROL, AGENT_FLOW, API_SPEC, DATA_SCHEMA, PERMISSION_MATRIX, KNOWLEDGE_SYNC ฯลฯ

เป้าหมายคือให้:
- **เข้าใจง่าย**
- **ไม่เยิ่น**
- **ชัดเจนว่าอะไรทำได้/ทำไม่ได้**
- **เป็นกฎหมายความปลอดภัยกลางของแพลตฟอร์ม UET**

พร้อมใช้งานทันทีแบบระดับองค์กร

---

# 📘 **SECURITY_RULES.md**

**UET Platform — Security & Access Control Specification**  
**เวอร์ชัน 1.0 (กระชับ แต่คุมครบ)**

---

# **0. วัตถุประสงค์**

ไฟล์นี้กำหนดกฎด้านความปลอดภัยทั้งหมดของแพลตฟอร์ม UET เพื่อให้:

- ข้อมูลปลอดภัย
- Agent และ API ทำงานอย่างถูกต้อง
- KB และโปรเจ็กต์ไม่พัง
- สิทธิ์ผู้ใช้ควบคุมได้
- ป้องกันการแก้ไขข้อมูลผิดระบบ
- บังคับตาม SYSTEM_CONTRACT

**ทั้งหมดนี้สรุปเป็นกฎง่าย ๆ ที่ระบบต้อง enforce เสมอ**

---
# **1. Security Layers (ชั้นความปลอดภัย)**

UET ใช้ความปลอดภัย 4 ชั้น:

|ชั้น|หน้าที่|
|---|---|
|**1. Authentication**|ยืนยันตัวผู้ใช้|
|**2. Authorization (สิทธิ์)**|คุมว่าใครทำอะไรได้|
|**3. Data Protection**|ป้องกันไฟล์/KB/DB|
|**4. Execution Safety**|ป้องกัน Agent หรือ API ทำงานผิด|

ทั้งหมดต้องเชื่อมกับ PERMISSION_MATRIX + SYSTEM_CONTRACT

---
# **2. User Roles & Privileges (สิทธิ์ตามระดับผู้ใช้)**

|Role|สิทธิ์|ข้อจำกัด|
|---|---|---|
|**Guest**|ดูเนื้อหา public|ห้ามใช้ KB / Agent|
|**Member**|ใช้ chat + studio + โปรเจกต์ส่วนตัว|เห็นเฉพาะข้อมูลตัวเอง|
|**Power User**|สร้างโปรเจกต์ + ใช้ Agent ขั้นสูง|แก้ได้เฉพาะพื้นที่ตนเอง|
|**Admin**|ดูทุกโปรเจกต์ + ปรับระบบได้|ต้อง log ทุก action|

---
# **3. Global Security Rules (กฎกลางทั้งระบบ)**

### **3.1 ห้าม Agent แก้ไข G-KB โดยตรง**

ต้องผ่านผู้ใช้ → Studio → Save → Versioning เท่านั้น

### **3.2 ห้าม API รับข้อมูลที่ไม่ผ่าน schema validation**

อิง DATA_SCHEMA.md

### **3.3 ทุกไฟล์ต้องอยู่ในพื้นที่ของโปรเจกต์ / ผู้ใช้ที่เป็นเจ้าของ**

ห้ามสร้าง orphan file

### **3.4 ทุก action สำคัญต้องมี Logging**

เช่น:
- ลบไฟล์
- แก้สิทธิ์
- merge knowledge

### **3.5 ห้าม bypass Flow**

ห้ามเขียนไฟล์โดยไม่ผ่าน Studio Panel  
ห้ามเรียก API โดยไม่ผ่าน Auth

### **3.6 ต้องปฏิบัติตาม STATE_MACHINE + STATE_TRANSITION**

ป้องกัน error พังระบบ

---
# **4. API Security Rules**

จาก API_SPEC.md:

### ✔ Rule 1 — ทุก Endpoint ต้องมี `auth token`

ยกเว้น route ที่เป็น public

### ✔ Rule 2 — ห้ามส่งข้อมูลเกินสิทธิ์ของผู้ใช้

เช่น Member ห้ามเห็นโปรเจกต์ของคนอื่น

### ✔ Rule 3 — Rate Limit

กัน spam / abuse  
เช่น Chat = 30 req/min

### ✔ Rule 4 — Input Sanitization

กัน script / HTML injection

### ✔ Rule 5 — Zero Trust Architecture

API ต้อง “ไม่เชื่อ” การ input ใด ๆ จนกว่าจะ validate

---
# **5. Knowledge Base (KB) Security**

RAG / KB / Sync ต้องปฏิบัติตามกฎ:

### ✔ Rule 1 — KB แยกตามระดับ (Global / Project / Personal)

Agent ต้องเลือก source ตามสิทธิ์ผู้ใช้

### ✔ Rule 2 — ห้าม merge ข้ามโปรเจกต์โดยอัตโนมัติ

ป้องกันเนื้อหาหลุดโปรเจกต์

### ✔ Rule 3 — ทุกไฟล์ต้องผ่าน Versioning

กันความรู้พัง

### ✔ Rule 4 — ห้ามลบไฟล์ถาวร (ยกเว้น Admin)

ใช้ soft delete ตาม KNOWLEDGE_SYNC.md

### ✔ Rule 5 — Validation ก่อน vectorize

กันข้อมูลขยะเข้า vector DB

---
# **6. Agent Security Rules**

อิงจาก AGENT_FLOW.md:

### ✔ Rule 1 — Agent อ่านข้อมูลได้เฉพาะตามสิทธิ์ผู้ใช้

ไม่สามารถดึงข้อมูลโปรเจกต์ที่ผู้ใช้ไม่ได้อยู่

### ✔ Rule 2 — Agent แก้ได้เฉพาะใน Studio / โปรเจกต์ปัจจุบัน

ห้ามแตะไฟล์นอก context

### ✔ Rule 3 — Agent ต้องคืน output แบบ markdown เท่านั้น

กัน execute code ที่อันตราย

### ✔ Rule 4 — Agent ต้องยิง event AGENT_ERROR หากพบสิ่งผิดปกติ

ระบบแจ้งผู้ใช้ทันที

### ✔ Rule 5 — ไม่อนุญาต Agent เขียนโค้ดที่รันบน server

เพื่อกัน remote code execution (RCE)

---
# **7. Data Access Rules**

### ✔ Rule 1 — ผู้ใช้เข้าถึงข้อมูลของตัวเองเท่านั้น

Power User / Member ห้ามอ่านโปรเจกต์ของคนอื่นโดยไม่ได้รับเชิญ

### ✔ Rule 2 — Admin เห็นทั้งหมด แต่ต้องมี log

“superuser actions” ต้อง trace ได้เสมอ

### ✔ Rule 3 — ทุก query ต้องผ่าน Data API

Agent ห้าม query DB ตรง

### ✔ Rule 4 — Encryption at Rest

ไฟล์สำคัญ เช่น:
- access token
- user data

ต้องเข้ารหัส (database).

---
# **8. File Security Rules**

### ✔ Rule 1 — ชนิดไฟล์ที่อนุญาต

`.md`, `.pdf`, `.docx`, `.txt`

ห้าม:
- `.exe`
- `.js`
- `.html`
- `.sh`

### ✔ Rule 2 — Scan before process

ระบบต้อง scan ไฟล์ก่อน parse  
กันมัลแวร์ / script แฝง

### ✔ Rule 3 — Path Isolation

ทุกไฟล์ต้องอยู่ในโปรเจกต์ของตัวเอง  
กัน “path traversal attacks”

---
# **9. UI Security Rules**

### ✔ Rule 1 — ปิด script execution

Studio ห้ามรัน JS/HTML ฝั่ง client

### ✔ Rule 2 — Panel Isolation

Panel หนึ่งไม่สามารถอ่านข้อมูลภายในอีก panel โดยตรง  
ต้องผ่าน API layer

### ✔ Rule 3 — Sensitive data masking

เช่น token, internal ID

---
# **10. Security Threat Prevention (ป้องกันภัยทั่วไป)**

|ภัยคุกคาม|วิธีแก้|
|---|---|
|Unauthorized Access|Auth + Permission Matrix|
|Prompt Injection|Sanitize input + restrict agent functions|
|Data Leakage|KB isolation + Project boundary|
|DDOS / Spam|Rate limit + Bot detection|
|Corrupted Knowledge|Versioning + Conflict Resolver|
|Agent Misbehavior|Flow Control + State Machine|

---

# **11. Security Enforcement Rules (กฎบังคับใช้)**

ระบบต้อง enforce:

1. **reject request หากสิทธิ์ไม่ตรง**
2. **ออก error ที่เหมาะสม (ตาม ERROR_HANDLING.md)**
3. **log ทุกเหตุการณ์ที่เกี่ยวกับความปลอดภัย**
4. **block agent หากผิดกฎ security**
5. **ไม่อนุญาตการ access ตรงโดยไม่ผ่าน API**
6. **validate KB / API / Agent ทุกครั้งตาม SYSTEM_CONTRACT**

---
# **12. สรุปสั้นที่สุด**

**SECURITY_RULES.md** ทำหน้าที่:

- กันข้อมูลหลุด
- กัน agent ทำเกินสิทธิ์
- กันโปรเจกต์ชนกัน
- กัน API misuse
- กัน error ที่พังระบบ
- รักษา boundary ของโปรเจกต์ / user
- enforce SYSTEM_CONTRACT ทุกประตู

**ทุกระบบต้องผ่านกฎนี้ก่อนอนุญาตให้ทำงาน**

---

# ✨ ถ้าต้องการ ฉันสามารถทำไฟล์ต่อไป:

- **PERMISSION_MATRIX.md (แบบตารางละเอียด)**
    
- **MODEL_SELECTION_GUIDE.md**
    
- **CACHE_STRATEGY.md**
    
- **DEPLOYMENT_GUIDE.md**
    
- **TEST_PLAN.md**
    

บอกได้เลยอยากให้เขียนอันไหนถัดไป ❤️


# FILE: ERROR_HANDLING.md

โอเค Santa —  
ฉันจะเขียน **ERROR_HANDLING.md** ให้ “ดีที่สุด – กระชับ – คุมกฎระบบทั้งหมดในหน้าเดียว”  
และให้สอดคล้องกับไฟล์อื่นในโปรเจกต์ของนายทั้งหมด เช่น:

- SYSTEM_CONTRACT.md
- FLOW_CONTROL.md
- API_SPEC.md
- AGENT_FLOW.md
- EVENT_BUS.md
- KNOWLEDGE_SYNC.md
- DATA_SCHEMA.md

นี่คือเวอร์ชัน **ระดับแพลตฟอร์มองค์กร**, ใช้งานได้ทันที, ไม่ซับซ้อน, ไม่เยิ่นเย้อ  
มีกฎหลัก + โครงสร้าง error + lifecycle + event ที่ UI ต้องรับ

---

# 📘 **ERROR_HANDLING.md**

**UET Platform — Global Error Handling Specification**  
**เวอร์ชัน 1.0 (กระชับที่สุด + คุมทั้งระบบ)**

---
# **0. เป้าหมายของระบบ Error Handling**

ทำให้ทุก error ในระบบ:

1. **สม่ำเสมอ (consistent)**
2. **เข้าใจง่าย (human readable)**
3. **ตรวจสอบย้อนกลับได้ (traceable)**
4. **ไม่พัง flow หลักของระบบ (safe fail)**
5. **ให้ Agent / UI / API รับรู้เหมือนกัน**

และสิ่งสำคัญที่สุด:

> **Error ต้องทำให้ระบบ “บอกเราว่ามันผิดอะไร – ไม่ใช่เงียบตาย”**

---
# **1. Error Types (ประเภทของ Error)**

ทุก error ถูกจัดเป็น 5 กลุ่มชัดเจน:

|ประเภท|ความหมาย|ตัวอย่าง|
|---|---|---|
|**1. USER_ERROR**|ผู้ใช้ทำผิด input / action|ส่งไฟล์ผิดประเภท, พิมพ์ prompt ผิด format|
|**2. SYSTEM_ERROR**|ระบบผิด เช่น logic / module พัง|flow control พัง, state transition ผิด|
|**3. API_ERROR**|การคุยกับ API fail|500, 403, timeout|
|**4. AGENT_ERROR**|Agent ทำงานผิด step|step fail, context load ไม่เจอไฟล์|
|**5. DATA_ERROR**|ปัญหาข้อมูล / KB / vector / DB|ไฟล์ไม่พบ, chunking fail, DB conflict|

---
# **2. Error Format (มาตรฐาน ERROR JSON เดียวทั้งระบบ)**

ทุก error ต้องมีรูปแบบเดียว:

```json
{
  "error_id": "ERR_XXXX",
  "type": "USER_ERROR | SYSTEM_ERROR | API_ERROR | AGENT_ERROR | DATA_ERROR",
  "message": "ข้อความสั้น เข้าใจง่าย",
  "details": "รายละเอียดที่ใช้ debug (optional)",
  "source": "module/file",
  "timestamp": "2025-01-01T12:00:00Z",
  "state": "current_state_if_any"
}
```

### ✔ เหตุผล

- ช่วย debug ได้เร็ว
- Agent / UI handle ได้เหมือนกัน
- Log เก็บในระบบเดียว
- ทุกไฟล์ในระบบเชื่อมผ่าน schema เดียว

---
# **3. Error Lifecycle (แบบกระชับที่สุด)**

```
[เกิด Error]
     ↓
[Normalize → ให้เป็น ERROR JSON มาตรฐาน]
     ↓
[Flow Control: ตัดสินว่าต้อง retry, cancel, หรือ escalate]
     ↓
[Event Bus ยิง AGENT_ERROR / SYSTEM_ERROR]
     ↓
[UI แสดงผลแบบ human readable]
     ↓
[เขียนลง Log Center]
```

**สั้น ๆ:** ทุก error ต้องถูกแปลง → ส่ง event → แสดงให้คน → เก็บ log

---
# **4. Error Sources (แหล่งที่ error จะเกิด)**

มาจาก 4 Layer:

### **4.1 UI Layer**

- รับ event ผิด format
- panel load ล้มเหลว
- user input ผิดประเภท

→ classify เป็น `USER_ERROR`

---
### **4.2 API Layer**

- auth fail
- endpoint ตอบ 500
- network timeout

→ classify เป็น `API_ERROR`

---
### **4.3 Application Logic Layer**

รวมถึง:

- AGENT_FLOW
- FLOW_CONTROL
- KNOWLEDGE_SYNC

เช่น
- step agent หาย
- knowledge merge conflict
- flow เดินผิด state

→ classify เป็น `SYSTEM_ERROR` หรือ `AGENT_ERROR`

---
### **4.4 Data Layer**

- vector missing
- DB constraint fail
- version conflict
- sync ไม่ผ่านกฎ SYSTEM_CONTRACT

→ classify เป็น `DATA_ERROR`

---
# **5. Error Mapping Table (จำง่ายสุด)**

|แหล่ง|เป็น error ประเภท|ตัวอย่าง|
|---|---|---|
|User|USER_ERROR|อัปโหลดไฟล์เสีย|
|API|API_ERROR|API timeout|
|Agent|AGENT_ERROR|step 3 ไม่เจอ context|
|System|SYSTEM_ERROR|flow ค้างใน state ไม่ถูกต้อง|
|Data|DATA_ERROR|chunk ไม่ match schema|

---
# **6. Error Severity (ระดับความร้ายแรง)**

```
INFO        (แจ้งเฉยๆ)
WARNING     (แก้ได้ด้วยตัว user)
ERROR       (ระบบทำงานต่อได้แต่ต้องแจ้ง)
CRITICAL    (agent/system ต้องหยุด)
FATAL       (ต้อง restart module)
```

ในระบบ UET:
- UI ใช้แค่ INFO / WARNING / ERROR
- Agent ใช้ ERROR / CRITICAL
- Backend ใช้ CRITICAL / FATAL

---
# **7. System Behavior (ระบบต้องทำอะไรเมื่อเกิด Error)**

|ระดับ|ระบบต้องทำ|
|---|---|
|WARNING|แจ้งเตือน + ให้ user แก้เอง|
|ERROR|หยุดงานปัจจุบัน + rollback state|
|CRITICAL|หยุด agent + แจ้งระบบกลาง|
|FATAL|ปิด module + แจ้งทีม dev|

---
# **8. Error Events (EVENT_BUS ที่ต้องยิงเมื่อมี error)**

จาก EVENT_BUS.md:

```
AGENT_ERROR
SYSTEM_ERROR
API_ERROR
DATA_ERROR
USER_ERROR
```

เพื่อให้:
- UI → แสดงบน Notification
- Studio → หยุดงาน
- Agent → เคลียร์ state
- Log → เก็บข้อมูล

---
# **9. Error Rendering (UI ต้องแสดงอะไร)**

UI ต้องแสดง:

```
ข้อความง่าย ๆ
สิ่งที่ควรทำต่อ
error_id (สำหรับนักพัฒนา)
timestamp
```

ตัวอย่าง:

```
❌ ไม่สามารถโหลดไฟล์ได้
ลองอัปโหลดใหม่อีกครั้ง

รหัสปัญหา: ERR_DATA_004
เวลา: 15:32
```

---
# **10. Error Prevention (กฎกันความพังตั้งแต่ต้น)**

ระบบต้องป้องกัน:
- state ไม่ตรงกัน → ใช้ STATE_MACHINE
- flow ข้ามขั้นตอน → FLOW_CONTROL
- agent เขียน KB ตรง → SYSTEM_CONTRACT
- schema mismatch → DATA_SCHEMA
- vector mismatch → DATA_LIFECYCLE

**ชุดกฎพวกนี้ = ป้องกัน error ตั้งแต่ยังไม่เกิด**

---

# **11. Error Examples (เข้าใจใน 10 วินาที)**

### Example 1 — User อัปโหลดไฟล์ที่ระบบอ่านไม่ได้

```
USER_ERROR: ไฟล์รูปไม่รองรับ กรุณาอัปโหลด PDF หรือ MD
```

### Example 2 — Agent หาไฟล์ไม่เจอ

```
AGENT_ERROR: missing context: file_12.md
```

### Example 3 — API ล่ม

```
API_ERROR: 500 internal server error
```

### Example 4 — KB conflict

```
DATA_ERROR: version conflict detected in knowledge registry
```

---
# 🎯 **สรุปสั้นที่สุด**

**ERROR_HANDLING.md = ระบบกลางจัดการ error ทั้งหมดของ UET**

มันทำ 5 อย่าง:

1. รวม error ทุกประเภทให้เป็นรูปเดียว
2. ส่ง event แบบเดียวให้ทุก panel
3. บอกมนุษย์ด้วยภาษาที่เข้าใจง่าย
4. ป้องกันไม่ให้ flow พัง
5. ทำงานร่วมกับ Agent / Sync / RAG แบบสมบูรณ์

---

# 💬 ต้องการเวอร์ชัน “ย่อกว่านี้” หรือให้ฉันสร้างโครงสร้างโค้ด mock API / mock UI error overlay ให้ไหม?

ฉันสามารถต่อให้ได้ทันที ❤️

---



# FILE: 11__SECURITY & PERMISSION & ERROR HANDLING v3.0.md

โอเค ไป CH11 แล้วนะ 🛡️

ฉันจะทำเป็น **CH11 — SECURITY / PERMISSION / ERROR HANDLING v3.0 — PART 1**  
โฟกัส 3 อย่างพร้อมกันเลย:

1. **Security Stack ภาพใหญ่**
2. **Permission Matrix ระดับระบบ (ต่อยอดจาก UET Platform.md)**
3. **Error Handling Flow กลาง (ผูกกับ EVENT_BUS + FLOW_CONTROL)**
4. พร้อม **ไดอะแกรม + Matrix + System Flow** ตามที่ขอ

---

## 🟥 SECTION 1 — SECURITY STACK OVERVIEW (v3.0)

ให้มอง CH11 เป็น “เลเยอร์กำกับระบบทั้งหมด” ที่อยู่ข้างๆ SYSTEM_CONTRACT / FLOW_CONTROL / EVENT_BUS เลย

### 1.1 Security Stack Diagram

```text
USER / CLIENT
   ▼
AUTH LAYER
   - Login / Token / Session
   - Device / Rate Limit
   ▼
PERMISSION LAYER
   - Role + State + Project Scope
   - Zone-based permissions (Chat / Sources / Studio / Projects / Community / Donate)
   ▼
SECURITY_RULES ENGINE
   - Global rules (system_contract binding)
   - Content policy / privacy policy
   - Data access rules (KB / Project / Global)
   ▼
FLOW_CONTROL ENGINE
   - Decide allowed flows
   - Throttle / block / redirect
   ▼
APPLICATION LOGIC
   - AGENT_ENGINE
   - RAG_ENGINE
   - KNOWLEDGE_SYNC
   - MODEL_ROUTING
   - EVENT_BUS
   ▼
ERROR_HANDLING ENGINE
   - Classify error
   - Map → event / log / user-facing message
   - Decide retry / fallback / safe-mode
```

> Concept: **“ทุก request ต้องผ่าน Auth → Permission → Security Rules → Flow Control ก่อนถึง Logic”**

---

## 🟦 SECTION 2 — PERMISSION MODEL v3.0 (Role + Zone + Scope)

เรามี “permission แบบ UI/Platform” อยู่แล้วใน `UET Platform.md` (Guest / Member / Power User / Admin per zone)  
CH11 v3.0 คือเอาแนวคิดนั้น ลงไปใน **Engine / API / KB / Project** ให้ครบ

### 2.1 Role & Zone Matrix (ENGINE VIEW)

**Roles**

- `guest`    
- `member`
- `power_user`
- `admin`
- `system` (internal, ใช้กับ background jobs / system agents)

**Zones (ENGINE)**

- `chat_engine` (Agent + Model)
- `kb_sources` (ไฟล์ / KB / Project)
- `studio` (notebook / canvas / theory drafts)
- `projects` (project config, member list)
- `community` (post, comment, report)
- `donate` (ledger, reports)

### 2.2 Core Permission Matrix (ย่อยลงมาแบบอ่านง่าย)

```text
Table: Role × Zone × Capability (สรุปสั้น)

Columns:
- read_self      (อ่านของตัวเอง)
- write_self     (แก้ของตัวเอง)
- read_project   (อ่านของทั้งโปรเจกต์)
- write_project  (แก้ของโปรเจกต์)
- manage_system  (เปลี่ยน config / global KB / ledger / ban)

guest:
  chat_engine:    read_self, write_self (rate limit, no agents)
  kb_sources:     none
  studio:         none
  projects:       read_project (demo only)
  community:      read_project
  donate:         create_donation (public/semi-private only)

member:
  chat_engine:    read_self, write_self (normal limit)
  kb_sources:     read_self, write_self (private files)
  studio:         read_self, write_self
  projects:       join_project, read_project (where member)
  community:      read/write own posts
  donate:         donate + view own donations

power_user:
  chat_engine:    + use_agents, multi-KB, deep research
  kb_sources:     read_project, write_project (when owner)
  studio:         publish → Theory / Project
  projects:       create_project, manage_members (own project)
  community:      create_topics, pin posts (in own project)
  donate:         view project-level report (own project)

admin:
  chat_engine:    debug, impersonate (with audit)
  kb_sources:     manage_system (global KB)
  studio:         force unpublish / lock
  projects:       archive / freeze / take_ownership
  community:      ban / moderation / delete content
  donate:         audit / export ledger

system:
  everything via internal tokens only (no UI), always audit logged
```

> ตรงนี้สุดท้ายจะไปเขียนลง `PERMISSION_MATRIX.md` เป็นตารางจริงๆ (v3.0)

---

## 🟩 SECTION 3 — PERMISSION MATRIX (ENGINE x ENTITY)

อันนี้คือ Matrix แบบ “ระดับ Entity” ไว้สำหรับ implement จริงใน API / Data layer

### 3.1 Entity × Action Matrix

```text
Entities:
- user_profile
- project
- project_member
- kb_file
- kb_index (vector / metadata)
- chat_session
- message
- donation_record
- ledger_export
- community_post
- community_comment

Actions (ตัวอย่าง):
- view
- create
- update
- delete
- publish
- moderate
- export
```

**ตัวอย่าง rule หลัก**

- `kb_file.delete`
    - allowed if: role ∈ {member, power_user} AND user is owner
    - OR role == admin AND scope includes project or global
        
- `kb_index.rebuild`
    - allowed if: role ∈ {power_user, admin} AND user is project_owner
    - OR background system job (role = system)
        
- `ledger_export`
    - allowed if: role == admin AND audit log required

ทั้งหมดนี้จะถูก mapping ลง `PERMISSION_MATRIX.md` แบบ:

```markdown
| Entity          | Action  | Guest | Member | Power User | Admin | System | Conditions |
|-----------------|---------|-------|--------|------------|-------|--------|-----------|
| kb_file         | delete  |  -    | owner  | owner      | yes   | yes    | logged    |
| kb_index        | rebuild |  -    |  -     | owner      | yes   | yes    |           |
| donation_record | view    | self  | self   | self+proj  | all   | all    |           |
```

---
## 🟨 SECTION 4 — ERROR HANDLING MODEL v3.0 (Overview)

CH11 รวม **ERROR_HANDLING.md** ให้ align กับ Event Bus + Flow Controlแล้วจัดระดับ error ให้ชัดว่า “ใครแก้ / แก้ยังไง”

### 4.1 Error Class Diagram (Concept)

```text
ERROR
 ├─ ClientError (4xx)
 │    ├─ ValidationError
 │    ├─ PermissionDenied
 │    ├─ NotFound
 │    └─ RateLimited
 │
 ├─ SystemError (5xx)
 │    ├─ ProviderError (LLM, API, payment)
 │    ├─ StorageError  (DB, file, cache)
 │    └─ InternalError (bug, panic, unknown)
 │
 └─ DomainError (Business Logic)
      ├─ QuotaExceeded
      ├─ ProjectLocked
      └─ ConflictError (version conflict / merge conflict)
```

### 4.2 Error → Handling Strategy Matrix

|Error Type|User-facing|Log Level|Event Bus|Auto Retry|Fallback|
|---|---|---|---|---|---|
|ValidationError|400 msg|info|no|no|none|
|PermissionDenied|403 msg|warning|yes|no|none|
|NotFound|404 msg|info|no|no|none|
|RateLimited|429 msg|warning|yes|maybe|suggest wait|
|ProviderError|502/503|error|yes|yes|fallback model|
|StorageError|500|error|yes|maybe|read-only mode|
|InternalError|500|critical|yes|no|safe mode|
|QuotaExceeded|402/429|warning|yes|no|upsell / limit|
|ProjectLocked|423|info|yes|no|explain lock|
|ConflictError|409|info|yes|maybe|show diff / fork|

---
## 🟦 SECTION 5 — SECURITY + PERMISSION + ERROR FLOW (SYSTEM FLOW)

### 5.1 Request Flow (Security-first Pipeline)

```text
1) Request เข้าระบบ
   ▼
2) AUTH CHECK
   - ตรวจ token / session / device / rate limit
   - ถ้าล้มเหลว → Error: Unauthorized / RateLimited

3) PERMISSION CHECK
   - ดึง role + state + project scope
   - เช็ค PERMISSION_MATRIX ตาม entity+action
   - ถ้าล้มเหลว → Error: PermissionDenied

4) SECURITY_RULES CHECK
   - global rule (privacy, content policy, etc.)
   - zone-specific rule (donate, community, KB)
   - ถ้าผิด → Error: DomainError / Block

5) FLOW_CONTROL
   - ตรวจ system load, feature flags, safe mode
   - อาจ redirect หรือ block บาง action

6) APPLICATION LOGIC
   - Agent / RAG / KS / Routing …

7) ERROR_HANDLING
   - ถ้าเกิด error ระหว่าง logic
     → classify (client/system/domain)
     → map to error response + event

8) EVENT_BUS
   - ส่ง event: ERROR_OCCURRED + context
   - อาจ trigger cache invalidation / safe-mode / alerts

9) RESPONSE
   - ส่ง msg ที่ human-friendly กลับ user
   - ไม่ leak internal stack trace
```

---
## 🟧 SECTION 6 — DIAGRAM: GLOBAL SECURITY FLOW

```text
                    ┌───────────────────────────────┐
                    │           USER / UI           │
                    └──────────────┬────────────────┘
                                   ▼
                        ┌──────────────────────┐
                        │      AUTH LAYER      │
                        └──────────┬───────────┘
                                   ▼
                        ┌──────────────────────┐
                        │   PERMISSION LAYER   │
                        │ (Role + Scope + Zone)│
                        └──────────┬───────────┘
                                   ▼
                        ┌──────────────────────┐
                        │   SECURITY_RULES     │
                        └──────────┬───────────┘
                                   ▼
                        ┌──────────────────────┐
                        │    FLOW_CONTROL      │
                        └──────────┬───────────┘
                                   ▼
                        ┌──────────────────────┐
                        │  APP LOGIC (ENGINES) │
                        └──────────┬───────────┘
                                   ▼
                        ┌──────────────────────┐
                        │   ERROR_HANDLING     │
                        └──────────┬───────────┘
                                   ▼
                        ┌──────────────────────┐
                        │      EVENT_BUS       │
                        └──────────────────────┘
```

---
## 🟫 SECTION 7 — CHECKLIST ว่า CH11 PART 1 ครอบคลุมอะไรแล้ว

**ตอนนี้ CH11 — PART 1 ครอบคลุม:**

- ✅ Security Stack ภาพรวม
- ✅ Role / Zone Permission Model (ต่อยอดจาก UET Platform)
- ✅ Entity × Action Permission Matrix (แบบเอาไปลง PERMISSION_MATRIX.md ได้)
- ✅ Error Class Model v3.0 (จัดหมวดชัดๆ)
- ✅ Error → Handling Strategy Matrix
- ✅ Global Request Flow (Security + Permission + Error)
- ✅ Diagram ใหญ่ของ Security Pipeline

---
# **SECURITY_RULES v3.0 (กฎละเอียด + example ruleset ต่อ module)**

# 🟦 SECTION A — SECURITY MODEL v3.0 (ภาพใหญ่)

Security v3.0 ทำงานแบบ **RULE → CHECK → FLOW → ERROR → EVENT**  
และทุก request ต้องผ่าน security pipeline ตามลำดับ:

```
AUTH → PERMISSION → SECURITY_RULES → FLOW_CONTROL → ENGINE LOGIC → EVENT BUS
```

---

# 🟥 SECTION B — CORE SECURITY RULES v3.0 (กฎกลางระดับระบบ)

## **RULE 1 — Version Consistency Rule**

ห้ามใช้ข้อมูล / model / vector / KS ที่เวอร์ชัน mismatch

```
if kb_version != cache.kb_version → deny
if vector_version != index.vector_version → deny
if routing_version != model.routing_version → deny
```

> เป็นกฎ **บังคับเด็ดขาด** ทุก engine ต้อง enforce

---

## **RULE 2 — Project Isolation Rule**

ข้อมูลต้องแยกตามโปรเจกต์ 100% (RAG, KS, Cache, Index)

```
resource.project_id == user.project_id OR role = admin
```

ห้ามข้ามโปรเจกต์เด็ดขาด — แม้แต่ metadata

---

## **RULE 3 — No Cross-User File Access**

ไฟล์ของผู้ใช้ X ห้ามให้ผู้ใช้ Y เข้าถึง  
ยกเว้น owner, project_owner หรือ admin

```
if file.owner != user.id and not admin → deny
```

---

## **RULE 4 — No Cross-Session Leakage**

ข้อมูลใน Chat session เดียว ไม่อนุญาตให้ใช้ใน session อื่น

→ Binding: `session_id`

---

## **RULE 5 — Determinism Requirement Rule**

งานที่ไม่ deterministic → ห้าม cache → ห้าม re-execute แบบ unsafe

```
if task.type in ["reasoning","planning","creative"]:
    cache = disabled
```

---

## **RULE 6 — LLM Safety Policy Binding**

ทุก model ต้องผ่าน guideline ต่อไปนี้:

- ห้าม output ที่ผิดกฎหมาย
- ห้าม output ที่เปิดเผยข้อมูลของผู้อื่น    
- ห้าม output ที่เปิดเผย internal system
- ห้ามยุยง/อันตราย

(ถ้ามี violation → EVENT: SAFETY_BREACH → Flow Control ใส่ Safe Mode)

---
## **RULE 7 — Audit Required Rule**

กิจกรรมสำคัญต้องบันทึกลง Audit Log:

- rebuild vector
- edit KB
- merge conflict resolved
- admin actions
- permission changes
- ledger export
- project archive

---

## **RULE 8 — Rate Limit + Abuse Detection Rule**

ระบบตรวจ pattern:

- high-frequency message
- repeated failed requests
- model spam
- vector rebuild spam
- community spam

→ auto slow-down (Flow Control)  
→ หรือ BAN (admin)

---

## **RULE 9 — Donation / Financial Security Rules**

เข้มงวดกว่า module อื่น:

- ทุก donation ต้องเข้า ledger
- ห้ามแก้ไขย้อนหลัง
- export ledger ต้องใช้ admin + audit log
- admin ห้ามลบ donation records

---

## **RULE 10 — Community Safety Rules**

คล้าย platform: ห้ามโพสต์

- hate speech
- sexual content กับ minor
- harassment
- private data leaks

Violation → EVENT_BUS: COMMUNITY_FLAG → moderation engine

---

# 🟩 SECTION C — RULESETS ต่อ MODULE (Production-Ready)

นี่คือหัวใจของ PART 2 — รวมเป็นกฎแยกตาม engine/module แบบ implement ได้จริง

---

# 🟧 MODULE 1 — **AGENT_ENGINE Rules**

### AGENT_RULE 1 — No agent may execute unsafe command

ห้าม:

- system command
- file write นอก project scope
- HTTP request นอก allowlist
- code-execution outside sandbox

---

### AGENT_RULE 2 — Session Isolation

Agent ห้ามเห็นข้อมูลจาก session อื่น

---

### AGENT_RULE 3 — Model-bound Access

Agent จะเลือก model ตาม routing rules และห้าม override model ที่ถูกบังคับ

---

### AGENT_RULE 4 — Safe-LLM Enforcement

ถ้า agent ขอ output แบบ reasoning chain → ให้ safe-mode reasoning (ไม่เปิดเผย chain-of-thought)

---

### AGENT_RULE 5 — Agent Memory Safety

ห้ามเก็บข้อมูลผู้ใช้งานแบบ sensitive ลงใน agent memory

---

# 🟥 MODULE 2 — **RAG_ENGINE Rules**

### RAG_RULE 1 — Vector-Version Binding

ห้ามใช้ vector index ที่เวอร์ชัน mismatch

---

### RAG_RULE 2 — Owner-bound Retrieval

การค้นต้องเป็นของ owner หรือ project member เท่านั้น

---

### RAG_RULE 3 — No Orphan Retrieval

ห้าม retrieve chunks ที่ orphan (ไม่มีไฟล์ต้นทาง)

---

### RAG_RULE 4 — Privacy Mode

ถ้าเป็น private chat → RAG ดึงเฉพาะไฟล์ส่วนตัว

---

### RAG_RULE 5 — Secure Reranking

LLM reranker ต้องไม่ leak content ทั้งเอกสาร

---

# 🟦 MODULE 3 — **KNOWLEDGE_SYNC (KS) Rules**

### KS_RULE 1 — Only diff-based merge

ห้าม overwrite ทั้งไฟล์แบบยกก้อน

---

### KS_RULE 2 — Merge Conflict Must Block

ถ้า detect conflict → ต้องหยุด sync และ require manual resolve

---

### KS_RULE 3 — Project Ownership Binding

เฉพาะ owner / admin เท่านั้นที่สามารถ:

- delete file
- rename file
- reindex project
- rebuild vector

---

### KS_RULE 4 — No “Cross-KB Sync”

ไฟล์ของโปรเจกต์ A ห้ามไป sync กับ B

---

# 🟫 MODULE 4 — **MODEL_ROUTING Rules**

### MR_RULE 1 — Provider Health Must Be Live

ถ้า provider unhealthy → ห้ามส่งงานไป

---

### MR_RULE 2 — Capability Verified

ห้ามส่งงานผิด model เช่น:

- GPT-5.1-Instant → deep reasoning
- Gemini → high-privacy task (ข้อจำกัดตาม provider)

---

### MR_RULE 3 — Cost Guard

ห้ามรัน model แพงเกิน limit ของโปรเจกต์

---

### MR_RULE 4 — Fallback Allowed

หาก provider fail → fallback model (ตาม config)

---

# 🟩 MODULE 5 — **EVENT_BUS Rules**

### EB_RULE 1 — All critical events must be logged

รวมถึง:
- KB_UPDATE
- VECTOR_REBUILD
- PERMISSION_CHANGE
- ERROR_OCCURRED
- SAFETY_BREACH
- MERGE_CONFLICT

---

### EB_RULE 2 — Cascade Safety

ถ้าเหตุการณ์อันตรายเกิด → flow control เข้าสู่ safe mode

---

### EB_RULE 3 — Event Integrity

ห้ามเปลี่ยนย้อนหลัง  
ห้ามลบ event logs

---

# 🟧 MODULE 6 — **FLOW_CONTROL Rules**

### FC_RULE 1 — Overload Protection

ถ้าโหลดสูง → slow-down chat / disable expensive models

---

### FC_RULE 2 — Safe Mode Activation

ถ้า EVENT_BUS แจ้งว่า:
- provider fail
- merging conflict
- orphan index
- system overload

→ disableบางฟีเจอร์อัตโนมัติ

---

### FC_RULE 3 — Action-Allowlist per Mode

ตัวอย่าง:

```
NORMAL_MODE:
  - allow all

SAFE_MODE:
  - disable model GPT-5.1 full
  - disable vector rebuild
  - allow RAG read-only

RECOVERY_MODE:
  - enable rebuild
  - disable chat

LOCKDOWN:
  - allow admin only
```

---

# 🟨 MODULE 7 — **API_SPEC Security Rules**

### API_RULE 1 — must include project_id

เพื่อ enforce project isolation

### API_RULE 2 — must include role binding

ผ่าน token decode

### API_RULE 3 — must return safe error

ไม่มี stack trace/ internal code

### API_RULE 4 — must run through rate limit

ทั้ง per-user และ per-project

---

# 🟦 SECTION D — DIAGRAM: SECURITY RULES PIPELINE

```
REQUEST
  ▼
AUTH (identity, token, device)
  ▼
PERMISSION (role + zone + entity)
  ▼
SECURITY_RULES (global + module rules)
  ▼
FLOW_CONTROL (decide safe/normal)
  ▼
ENGINE (Agent / RAG / KS / Routing)
  ▼
ERROR_HANDLER
  ▼
EVENT_BUS (log + broadcast)
  ▼
RESPONSE
```

---

# 🟥 SECTION E — CHECKLIST ว่า PART 2 ครอบคลุมอะไรแล้ว

**CH11 PART 2 Complete:**

✔ กฎกลางทั้งระบบ (10 ข้อ)  
✔ Ruleset แยกตามโมดูล (Agent, RAG, KS, Routing, EventBus, FlowControl)  
✔ API Security Rules  
✔ Diagram pipeline  
✔ เวอร์ชันใช้งานได้จริง (production-ready)

---
# **PERMISSION_MATRIX v3.0 (ตารางจริงเต็มๆ)**

ได้เลย Santa —  
ตอนนี้ฉันจะทำ **CH11 — PART 3: PERMISSION_MATRIX v3.0 (ตารางจริงเต็มที่สุดในระบบ)**  
นี่คือ version ที่สามารถนำไป implement ใน API, Engine, Database, UI ได้ทันที  
และ align ครบกับ CH11 PART 1–2 + SYSTEM_CONTRACT v3.0 + UET Platform rules + KS/RAG/Routing/Donation/Community ทั้งหมด

ฉันรวมข้อมูลจากไฟล์ทั้งหมดที่เคยให้:

- SECURITY_RULE.md
- PERMISSION_MATRIX.md เก่า
- SYSTEM_CONTRACT.md
- KS / RAG / Routing / Model rules
- Donation Ecosystem
- UET Platform.md (role-per-zone)
- EVENT_BUS rules
- FLOW_CONTROL rules

แล้วออกเป็น **Matrix เดียวที่รวมทุก layer**  
ไปแบบเต็ม สะอาด กระชับ 🔥

---

# 📘 **CH11 — PART 3

PERMISSION_MATRIX v3.0 (Full Table + Conditions)**

> โครงสร้าง permission v3.0 = **Role × Zone × Entity × Action × Conditions**

รองรับ roles:

- `guest`
- `member`
- `power_user`
- `admin`
- `system` _(background/internal)_

รองรับ zones:

- `chat_engine`
- `kb_sources`
- `studio`
- `projects`
- `community`
- `donate`

รองรับ entities:

- user_profile
- chat_session
- message
- project
- project_member 
- kb_file
- kb_index
- ks_merge
- vector_index    
- rag_query
- studio_document
- donation_record
- ledger
- community_post
- community_comment

---

# 🟥 SECTION A — MASTER PERMISSION TABLE (Role × Zone × Capability)

```
Capabilities:
- read_self
- write_self
- read_project
- write_project
- moderate
- manage_system
```

|Zone / Role|Guest|Member|Power User|Admin|System|
|---|---|---|---|---|---|
|**Chat Engine**|read_self, write_self (limited)|read/write self|read/write (agents allowed)|full + debug|full|
|**KB Sources**|none|read/write own|read/write project (owner only)|full|full|
|**Studio**|none|read/write own|publish + manage project docs|full|full|
|**Projects**|read public|join, read|create/manage own project|archive, force take-over|full|
|**Community**|read|read/post|pin/manage own topic|full mod|full|
|**Donate**|create donation|view own|project-level view|full ledger access|full|

---

# 🟦 SECTION B — ENTITY × ACTION MATRIX (ใช้งานจริงใน API/DB)

> ตารางนี้คือ “ตัวจริง” ที่ลงใน PERMISSION_MATRIX.md v3.0 ได้เลย  
> เขียนแบบ production-ready พร้อมเงื่อนไข

## 1) user_profile

|Action|Guest|Member|Power User|Admin|System|Conditions|
|---|---|---|---|---|---|---|
|view|self|self|self|all|all|-|
|update|self|self|self|all|all|-|
|delete|-|-|-|yes|yes|audit|

---

## 2) chat_session

|Action|Guest|Member|Power User|Admin|System|Conditions|
|---|---|---|---|---|---|---|
|create|yes|yes|yes|yes|yes|rate limit|
|view|self|self|self|all|all|-|
|delete|self|self|self|yes|yes|-|
|use_agents|limited|limited|yes|yes|system only for background||

---

## 3) message

|Action|Guest|Member|Power User|Admin|System|Conditions|
|---|---|---|---|---|---|---|
|create|yes|yes|yes|yes|yes|rate limit|
|view|self|self|self|all|all|no cross-user|
|delete|self|self|self|yes|yes|cannot delete system logs|

---

## 4) project

|Action|Guest|Member|Power User|Admin|System|Conditions|
|---|---|---|---|---|---|---|
|create|-|-|yes|yes|yes|-|
|read|public|member|owner|all|all|-|
|update|-|owner|owner|yes|yes|audit|
|delete|-|-|owner|yes|yes|archive only|

---

## 5) project_member

|Action|Guest|Member|Power User|Admin|System|Conditions|
|---|---|---|---|---|---|---|
|add_member|-|owner|owner|yes|yes|notify + audit|
|remove_member|-|owner|owner|yes|yes|cannot remove admin|

---

## 6) kb_file

|Action|Guest|Member|Power User|Admin|System|Conditions|
|---|---|---|---|---|---|---|
|read|-|owner|project|all|all|project isolation|
|write|-|owner|owner|yes|yes|version bump|
|delete|-|owner|owner|yes|yes|audit, KS sync|
|upload|-|owner|owner|yes|system|run KS diff|
|rename|-|owner|owner|yes|yes|KS sync|
|move|-|owner|owner|yes|yes|no cross-project|

---

## 7) kb_index (metadata)

|Action|Guest|Member|Power User|Admin|System|Conditions|
|---|---|---|---|---|---|---|
|read|-|owner|project|all|all|project isolation|
|write|-|-|owner|yes|system|KS sync required|
|rebuild|-|-|owner|yes|system|expensive op|

---

## 8) ks_merge (merge conflict resolve)

|Action|Guest|Member|Power User|Admin|System|Conditions|
|---|---|---|---|---|---|---|
|view_diff|-|owner|owner|yes|system|-|
|resolve|-|owner|owner|yes|system|must be diff-based|
|force_resolve|-|-|-|yes|system|heavy audit|

---

## 9) vector_index (embedding store)

|Action|Guest|Member|Power User|Admin|System|Conditions|
|---|---|---|---|---|---|---|
|read|-|owner|owner/project|yes|yes|version check|
|rebuild|-|-|owner|yes|system|EVENT: VECTOR_REBUILD|

---

## 10) rag_query

|Action|Guest|Member|Power User|Admin|System|Conditions|
|---|---|---|---|---|---|---|
|query|-|yes|yes|yes|system|file must belong to user/project|
|retrieve_chunks|-|yes|yes|yes|system|no orphan chunks|

---

## 11) studio_document

|Action|Guest|Member|Power User|Admin|System|Conditions|
|---|---|---|---|---|---|---|
|read|-|owner|project|yes|system|respect privacy flag|
|write|-|owner|owner|yes|system|read-only in safe mode|
|publish|-|-|owner|yes|system|must pass content rules|

---

## 12) donation_record

|Action|Guest|Member|Power User|Admin|System|Conditions|
|---|---|---|---|---|---|---|
|create|yes|yes|yes|yes|system|project-bound|
|view|self|self|project owner|admin|system|sensitive|
|export|-|-|-|yes|system|heavy audit|

---

## 13) ledger

|Action|Guest|Member|Power User|Admin|System|Conditions|
|---|---|---|---|---|---|---|
|view|-|self|project|admin|system|anonymized for project|
|export|-|-|-|yes|system|cannot modify|

---

## 14) community_post

|Action|Guest|Member|Power User|Admin|System|Conditions|
|---|---|---|---|---|---|---|
|read|yes|yes|yes|yes|system|-|
|create|-|yes|yes|yes|system|spam filter|
|delete|self|self|self/topic_owner|admin|system|mod_required|

---

## 15) community_comment

|Action|Guest|Member|Power User|Admin|System|Conditions|
|---|---|---|---|---|---|---|
|read|yes|yes|yes|yes|system|-|
|create|-|yes|yes|yes|system|-|
|delete|self|self|topic_owner|admin|system|-|

---

# 🟩 SECTION C — PERMISSION LOGIC (Pseudo-Code)

```python
def check_permission(user, entity, action, resource):
    role = user.role
    zone = entity.zone
    rule = PERMISSION_MATRIX[entity][action][role]

    # 1. rule deny?
    if rule is None or rule == "deny":
        raise PermissionDenied()

    # 2. ownership checks
    if rule == "owner" and resource.owner != user.id:
        raise PermissionDenied()

    # 3. project scope
    if rule == "project" and user not in resource.project.members:
        raise PermissionDenied()

    # 4. admin bypass
    if rule == "admin" and role != "admin":
        raise PermissionDenied()

    # 5. system allowed
    if role == "system":
        return True

    return True
```

---

# 🟧 SECTION D — DIAGRAM: PERMISSION FLOW

```
USER REQUEST
   ▼
Decode Token → resolve role / project / scope
   ▼
Lookup PERMISSION_MATRIX[entity][action][role]
   ▼ rule? 
      ▼ none → deny
      ▼ owner → check resource.owner == user
      ▼ project → check membership
      ▼ admin → require admin
   ▼ pass
SECURITY_RULES
   ▼
FLOW_CONTROL
   ▼
ENGINE LOGIC
```

---

# 🟨 SECTION E — CHECKLIST ว่า PART 3 ครอบคลุมอะไรแล้ว

**PERMISSION_MATRIX v3.0 (Completed):**

✔ Role × Zone Capability Table  
✔ Entity × Action × Conditions matrix พร้อมเงื่อนไขจริง  
✔ ครอบคลุมทุก module (KB, KS, RAG, Studio, Chat, Community, Donation, Project)  
✔ มี pseudo-code implementation  
✔ มี Security Flow Diagram  
✔ Align กับ SYSTEM_CONTRACT, FLOW_CONTROL, EVENT_BUS  
✔ พร้อม implement ใน API และ DB

----
# **ERROR_HANDLING v3.0 (spec ราย endpoint + code-style + event mapping)**

ได้เลย Santa —  
นี่คือ **CH11 — SECURITY / PERMISSION / ERROR HANDLING v3.0  
PART 4 → ERROR_HANDLING v3.0 (Spec ราย endpoint + code-style + event mapping + flow)**

ฉันทำให้เป็น “เวอร์ชัน Production-Grade” ที่ใช้ได้จริงกับ API, Agent Engine, RAG, KS, Routing, Event Bus และ Cache v3.0  
โดยรวบรวมข้อมูลทั้งหมดจากไฟล์ในระบบ และผูกให้สอดคล้องกับ:

- SYSTEM_CONTRACT v3.0
    
- FLOW_CONTROL v3.0
    
- EVENT_BUS v3.0
    
- CACHE_STRATEGY v3.0
    
- MODEL_ROUTING v3.0
    
- KNOWLEDGE_SYNC v3.0
    

ไปเริ่มแบบสมบูรณ์ที่สุด 🔥

---

# 📘 **CH11 PART 4 — ERROR_HANDLING v3.0**

(Endpoint Spec + Error Categories + Retry/Fallback + Event Mapping + Flow)

---

# 🟦 SECTION A — ERROR MODEL v3.0 (คลาสหลัก)

Error ในระบบแบ่งเป็น **3 Layer (Client / Domain / System)**

## **1) Client Errors (4xx)**

เกิดจากผู้ใช้

- `ValidationError`
    
- `BadRequest`
    
- `Unauthorized`
    
- `PermissionDenied`
    
- `NotFound`
    
- `RateLimited`
    

## **2) Domain Errors (ธุรกิจ / ระบบภายใน)**

- `QuotaExceeded`
    
- `ProjectLocked`
    
- `MergeConflict`
    
- `VersionMismatch`
    
- `OrphanChunkDetected`
    

## **3) System Errors (5xx)**

เกิดจากระบบ / Provider / Infra

- `ProviderError`
    
- `RoutingError`
    
- `StorageError`
    
- `InternalError`
    
- `CacheError`
    
- `IndexCorruption`
    
- `VectorRebuildError`
    
- `SafeModeActivated`
    

👉 ทุกอัน map ไปที่ EVENT_BUS v3.0 ภายหลัง

---

# 🟥 SECTION B — ERROR SPEC ราย Endpoint (API-Level Spec)

นี่คือ pattern ทุกรูปแบบ API ของระบบต้องใช้  
(สั้น กระชับ หน้าเดียวอ่านเข้าใจ)

---

## **1) Format ของ Error Response (มาตรฐานกลาง)**

```json
{
  "error": {
    "type": "PermissionDenied",
    "message": "You do not have permission to modify this file.",
    "code": 403,
    "context": {
      "endpoint": "/api/kb/file/update",
      "resource_id": "file_abc",
      "required_role": "owner"
    },
    "retry": false,
    "fallback": null
  }
}
```

### กฎกลาง:

- ไม่แสดง stack trace
    
- ไม่แสดงข้อมูล internal
    
- context ชัดเจน
    
- retry / fallback บอกชัดว่าได้ไหม
    
- error.type ใช้ชื่อจากระบบ error model เท่านั้น
    

---

# 🟦 SECTION C — ERROR SPEC ต่อโมดูล (Production Style)

## **1) AGENT_ENGINE**

|Error Type|Trigger|Action|Fallback|
|---|---|---|---|
|AgentPlanError|agent วางแผนผิด|ส่งกลับ + log|ไม่มี|
|UnsafeOperation|agent ขอทำ unsafe|block|none|
|LoopDetected|agent loop ไม่จบ|abort|none|
|ModelFail|model ตอบไม่ได้|retry (flow control)|fallback model|

---

## **2) RAG_ENGINE**

|Error Type|Trigger|Handling|Fallback|
|---|---|---|---|
|VersionMismatch|vector_version mismatch|clear L3 + re-run query|none|
|OrphanChunkDetected|chunk ไม่มีไฟล์ต้นทาง|invalidate index|rebuild index|
|IndexCorruption|metadata แตก|fail → EVENT: VECTOR_REBUILD_REQUIRED|rebuild|

---

## **3) KNOWLEDGE_SYNC ENGINE**

|Error|Trigger|Handling|
|---|---|---|
|MergeConflict|diff ขัดแย้ง|block sync + require manual resolve|
|FileModifiedDuringSync|file ถูกแก้ระหว่าง sync|abort sync|
|KBVersionMismatch|เวอร์ชันไม่ตรง|force KS sync|

---

## **4) MODEL_ROUTING ENGINE**

|Error|Trigger|Handling|
|---|---|---|
|ProviderDown|model provider ล่ม|EVENT + fallback model|
|CapabilityMismatch|model ไม่รองรับงาน|reroute engine|
|RoutingLoop|routing ติดลูป|abort + EVENT|

---

## **5) CACHE_MANAGER**

|Error|Trigger|Handling|
|---|---|---|
|StaleCache|version mismatch|clear layer|
|CacheCorruption|ไฟล์ cache เสีย|clear all|
|NonDeterministicCache|พยายาม cache reasoning|block|

---

## **6) EVENT_BUS**

|Error|Trigger|Handling|
|---|---|---|
|EventOverflow|event เยอะเกิน|throttle|
|InvalidEvent|event ผิด format|drop + log|
|EventLoop|event ซ้ำ|dedupe|

---

# 🟥 SECTION D — RETRY MODEL v3.0 (เมื่อไหร่ retry / ไม่ retry)

```
ClientError → ไม่ retry  
DomainError → retry บางเคส  
SystemError → มี retry (ควบคุมโดย Flow Control)
```

### **Retry Allowed**

- ProviderError
    
- RoutingError
    
- StorageError
    
- CacheError (ไม่ใช่ corruption)
    
- VectorRebuildError (หลัง rebuild เสร็จ)
    

### **Retry Disallowed**

- PermissionDenied
    
- ValidationError
    
- MergeConflict
    
- ProjectLocked
    
- OrphanChunkDetected
    

---

# 🟩 SECTION E — FALLBACK MODEL (เมื่อ main model ล่ม)

System จะ fallback เสมอตาม MODEL_ROUTING v3.0:

1. fallback model (เช่น GPT-5.1 → 5.1-instant)
    
2. ถ้ายังล่ม → safe-mode deterministic model
    
3. ถ้ายังล่ม → error แบบ human-friendly
    

---

# 🟦 SECTION F — ERROR → EVENT MAPPING (หัวใจของ PART 4)

ทุก error → ถูกส่งเข้า EVENT BUS พร้อม context  
นี่คือ mapping เต็ม:

|Error Type|EVENT|
|---|---|
|PermissionDenied|SECURITY_EVENT.PERMISSION_DENIED|
|Unauthorized|SECURITY_EVENT.UNAUTHORIZED|
|ValidationError|REQUEST_EVENT.BAD_INPUT|
|RateLimited|SYSTEM_EVENT.RATE_LIMITED|
|MergeConflict|KS_EVENT.MERGE_CONFLICT|
|KBVersionMismatch|KS_EVENT.VERSION_MISMATCH|
|OrphanChunkDetected|RAG_EVENT.ORPHAN_DETECTED|
|IndexCorruption|RAG_EVENT.INDEX_CORRUPTED|
|ProviderError|ROUTING_EVENT.PROVIDER_FAIL|
|RoutingError|ROUTING_EVENT.ROUTING_FAIL|
|CacheError|CACHE_EVENT.INVALID|
|CacheCorruption|CACHE_EVENT.CORRUPTED|
|SystemError|SYSTEM_EVENT.CRITICAL|
|SafeModeActivated|SYSTEM_EVENT.SAFE_MODE_ON|

ทุก event ดังกล่าวสามารถ:

- invalidate cache
    
- trigger safe mode
    
- stop certain features
    
- trigger automatic recovery
    
- notify monitoring subsystem
    

---

# 🟨 SECTION G — ERROR FLOW (Master Diagram)

```
ENGINE ERROR
   ▼
ERROR_HANDLER classify(error)
   ▼
 map → error.type (client/domain/system)
   ▼
build response object
   ▼
emit EVENT_BUS(event_type, context)
   ▼
FLOW_CONTROL decides:
    - retry?
    - fallback?
    - safe mode?
    - lock project?
   ▼
return human-friendly response
```

---

# 🟧 SECTION H — CODE STYLE (Implementation Guide)

## **Error Base Class**

```ts
class UETError extends Error {
  constructor(message, type, code, context = {}, retry = false, fallback = null) {
    super(message)
    this.type = type
    this.code = code
    this.context = context
    this.retry = retry
    this.fallback = fallback
  }
}
```

## **Example: Permission Error**

```ts
throw new UETError(
  "You do not have permission to modify this project.",
  "PermissionDenied",
  403,
  { projectId },
  false,
  null
)
```

## **Example: Provider Fallback**

```ts
try {
  return await modelProvider.run(query)
} catch (err) {
  emitEvent("ROUTING_EVENT.PROVIDER_FAIL", { provider })
  return await fallbackProvider.run(query)
}
```

---

# 🟫 SECTION I — CHECKLIST ว่า PART 4 ครอบคลุมอะไรแล้ว

**ERROR_HANDLING v3.0 (PART 4) now complete:**

✔ Error Model (Client/Domain/System)  
✔ API-Level Error Spec  
✔ Module Error Spec (Agent/RAG/KS/Routing/Cache/EventBus)  
✔ Retry Model v3.0  
✔ Fallback Model v3.0  
✔ Error–Event Mapping  
✔ Error Handler Flow  
✔ Code-style สำหรับ implement  
✔ สอดคล้องครบทุก chapter ก่อนหน้า

---

# ❓ Santa ต้องการไป CHAPTER 12 ต่อเลยไหม?

**CH12 — LOGGING & OBSERVABILITY v3.0**  
หรืออยาก refine CH11 เพิ่มเติมอีก?