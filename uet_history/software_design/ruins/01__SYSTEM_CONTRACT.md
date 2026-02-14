# 01__SYSTEM_CONTRACT_v3.0

### _(SKELETON — ฉบับโครงสร้างหลัก พร้อมลงเนื้อหาในรอบถัดไป)_

---

# 1. PURPOSE OF THIS CONTRACT

- ระบุ “เจตนาและขอบเขตของระบบ” ว่าต้องทำงานแบบ deterministic, โปร่งใส, ตรวจสอบได้
    
- ทำหน้าที่เป็น **ภาษากลาง** สำหรับทุก engine, ทุกทีม, ทุกโมดูล
    
- บังคับให้ระบบทั้งชุด (L0–L5 + Engines) ทำงานอยู่ในกรอบตรงตามคอนเซปต์ UET
    
- บอกอย่างชัดเจนว่าอะไร “เป็นหน้าที่ของระบบ” และอะไร “ไม่ใช่”
    

---

# 2. SYSTEM OBJECTIVES

ระบบนี้ต้องบรรลุวัตถุประสงค์ดังต่อไปนี้:

1. **ให้การจัดการความรู้ (Knowledge Management) เป็นแบบ deterministic**
    
2. **ลดการ drift ของ AI ให้ใกล้ศูนย์ที่สุด**
    
3. **ผสานข้อมูลทุกแบบเข้าระบบแกนกลางเดียว (Unified Knowledge Graph)**
    
4. **ทำ reasoning แบบตรวจสอบย้อนหลังได้ (traceable reasoning)**
    
5. **ให้ผลลัพธ์ที่เสถียร และ predictable**
    
6. **ทำงานด้วย execution pipeline ที่แยกส่วนเป็นชั้น L0–L5**
    
7. **ยึดโครงสร้างและหลักการของ UET เป็นนิยามกลางของสมดุล/เหตุผล/ความจริง**
    

---

# 3. GLOBAL PRINCIPLES (กติกากลางของระบบ)

นี่คือ “กฎเหล็ก” ที่ทุกไฟล์ต้องยึด

### 3.1 Determinism

- ข้อมูลเดียวกัน → ผลลัพธ์ต้องเหมือนกันทุกครั้ง
    
- ห้ามมี randomness โดยไม่จำเป็น
    
- ทุกการเปลี่ยนแปลงต้อง versioned
    

### 3.2 Canonical Knowledge

- ทุกข้อมูลต้องผ่านขั้นตอน normalize → canonical → register
    
- ไม่มีความรู้ฉบับ “หลุดนอกระบบ”
    

### 3.3 Layer Separation

- L0–L5 แยกขอบเขตอย่างเข้มงวด
    
- ห้าม cross-layer logic โดยไม่ผ่าน engine ที่รับผิดชอบ
    

### 3.4 Transparency & Traceability

- ทุก step ต้องตรวจสอบย้อนหลังได้
    
- ต้องมี event log สำหรับทุกการตัดสินใจของ system/agent
    

### 3.5 Minimum-Privilege Permission

- ทุก agent และ subsystem มีสิทธิ์เท่าที่จำเป็น (no expansion)
    
- user access ต้องแยกกับ system access
    

### 3.6 Ethical Operation

- ไม่ generate ข้อมูลเท็จ/บิดเบือนระบบ
    
- ไม่ละเมิด boundary ที่กำหนดใน contract
    

---

# 4. SYSTEM SCOPE

กำหนดว่า “อะไรอยู่ในระบบนี้จริง ๆ”

### 4.1 In-Scope

- การ ingest ความรู้ (ไฟล์, ข้อความ, web)
    
- การทำ chunk, embed, index
    
- การสร้างความหมาย (semantic node)
    
- การสร้างความสัมพันธ์ (graph)
    
- การทำ RAG improvement หลายชั้น
    
- การวาง reasoning block แบบ deterministic
    
- agent orchestration
    
- event logging, metrics
    
- การทำ context เพื่อให้ LLM ตอบ
    

### 4.2 Out-Of-Scope

ระบบนี้ **ไม่ทำ**:

- ไม่สร้าง content ใหม่เองโดยไม่มี source
    
- ไม่ใช้ chain-of-thought แบบเปลือย
    
- ไม่อาศัย randomness เพื่อแก้ปัญหา
    
- ไม่ทำงานแบบ “โมเดลเดาเองตามใจ”
    
- ไม่เก็บข้อมูล user ที่ไม่จำเป็น
    
- ไม่ทำงานเป็นเครื่องมือ chat entertainment
    

---

# 5. RESPONSIBILITY CONTRACTS

ระดับ “สัญญาระหว่างฝ่ายต่าง ๆ”

---

## 5.1 User ↔ System

**System ต้อง:**

- ปรับข้อมูล user ให้เข้า schema (canonical)
    
- เก็บ version ทุกครั้ง
    
- ตอบให้แม่นยำตามข้อมูลจริง
    
- ไม่เดาผิด logic
    
- แจ้ง error แบบชัดเจน trace ได้
    

**User ควร:**

- ส่งข้อมูลต้นฉบับที่ต้องการ
    
- ไม่กดดันให้ system ตอบนอกเหนือข้อมูลที่มี
    
- แยก domain-specific instruction ให้ชัดเจน
    

---

## 5.2 System ↔ AI (LLM)

**AI ต้องปฏิบัติตาม:**

- ขอบเขต reasoning ที่ system ส่งไป
    
- ห้ามข้ามขั้นตอน pipeline
    
- ห้าม ignore context, graph, หรือ rule
    
- ให้แต่ “output ที่ stable และตรวจสอบได้”
    

**System ต้อง:**

- ส่ง prompt ที่ deterministic
    
- ทำ sanitization, normalizing, validation
    
- เลือกโมเดลให้เหมาะงานตาม routing matrix
    

---

## 5.3 System ↔ Developer / Infra

**System รับประกันว่า:**

- ส่วนประกอบทุกชิ้น decoupled
    
- ทุก module มี interface ชัดเจน
    
- มี log, metric, event เพียงพอสำหรับ debugging
    
- ทุก migration reversible
    
- ไม่มี dependency แอบซ่อน
    

**Developer/Infra ต้อง:**

- รักษา invariant ของ schema
    
- ทำ deployment ตาม contract
    
- ไม่แก้ logic ข้าม layer
    
- ไม่แก้ engine โดยไม่อัปเดตไฟล์ blueprint/contract
    

---

# 6. ENFORCEMENT MECHANISM

กลไกทำให้สัญญานี้ “บังคับใช้จริง” ไม่ใช่แค่เขียนเล่น

- ทุก module ต้อง implement ตาม interface → check ผ่าน test
    
- มี rule สำหรับ RAG / Agent / Flow / Routing
    
- มี constraint + SQL rule รองรับ
    
- มี event bus ที่เป็น record ความจริง
    
- ถ้าขัด contract → ถือว่าผิด design และต้องแก้ก่อน deploy
    

---

# 7. VERSIONING CONTRACT

- ทุกไฟล์, graph, schema → มี version
    
- การแก้เล็กแก้ใหญ่ต้อง bump เวอร์ชัน
    
- backward compatibility คือ default
    
- ถ้าทำ breaking-change ต้องอธิบายเหตุผล
    

---

# 8. FINAL CONTRACT STATEMENT

เอกสารนี้ทำหน้าที่เป็น “กฎหมายสูงสุดของระบบ”  
ทุกไฟล์ลูก (24 ไฟล์ที่เหลือ) ต้องสอดคล้องกับนี้ 100%  
ถ้าไฟล์ไหนขัด → **ถือว่าไฟล์นั้นผิดและต้อง rewrite ให้เข้ากับ Contract**

---

# 🔥 Skeleton Version เสร็จแล้ว

เวอร์ชันนี้คือ “โครงที่สมบูรณ์” พร้อมลงเนื้อหารายละเอียดในรอบต่อไป  
แต่สามารถใช้เป็นฐานเขียนไฟล์ส่วนอื่นได้ตั้งแต่นาทีนี้เลย เพราะ:

- ขอบเขตชัด
    
- ภาษากลางชัด
    
- หลักคิดชัด
    
- ไม่มีอะไรลอย
    
- ไม่มี drift
    
- ไม่เดา
    
- ไม่เบี้ยว blueprint
    

---

โอเค Santa — ต่อเวอร์ชัน **01__SYSTEM_CONTRACT_v3.0 (FULL / Refined / ภาษากลาง)**  
นี่คือเวอร์ชันที่ **นิ่ง + ใช้ได้จริง + ใช้ได้กับทุกไฟล์ลูก + ไม่ลื่นไหล + ไม่หลุด UET + ตรงไปตรงมา**

> **นี่คือสัญญาหลัก (Constitution) ของระบบ UET Platform v3.0**  
> หลังจากไฟล์นี้ ทุกเอกสารต้อง align ตรงกันหมด 100%

ฉันเช็กไฟล์ทั้งหมดที่นายอัปโหลด:

- 00 MASTER
    
- 01–12 (ENGINE, SECURITY, RAG, AGENT, ARCHITECTURE, GRAPH, DATA_SCHEMA)  
    และรวมข้อกำหนดที่ต้องถูก “ตรึง” เอาไว้ทั้งหมด
    

---

# 01__SYSTEM_CONTRACT_v3.0

### _(FULL / LANGUAGE-REFINED / FINAL CONTRACT)_

---

# 1. PURPOSE — สัญญานี้ถูกสร้างมาเพื่ออะไร

เอกสารนี้เป็น **กฎหมายสูงสุด** ของระบบ UET Platform v3.0  
กำหนดว่า:

1. ระบบคืออะไร
    
2. ระบบทำงานอย่างไร
    
3. ระบบไม่ทำอะไร
    
4. ทุก engine / layer / module ต้องทำตามอะไร
    
5. ความสัมพันธ์ระหว่าง User ↔ System ↔ AI ↔ Dev คืออะไร
    
6. ขอบเขต reasoning ของ AI คืออะไร
    
7. อะไรควรเป็น “ความจริงกลาง (canonical truth)”
    

ถ้าไฟล์ไหน, engine ไหน, logic ไหน **ขัดกับสัญญานี้ → ถือว่าผิดทันที**

---

# 2. SYSTEM OBJECTIVES — เป้าหมายของระบบแบบชัดที่สุด

1. **สร้างระบบจัดการความรู้ (Knowledge OS) ที่ deterministic 100%**
    
2. **เชื่อมความรู้มนุษย์แบบเป็นชั้น (L0–L5) จนเป็นโครงสร้างเหตุผลที่ตรวจสอบย้อนกลับได้**
    
3. **ลด drift ของ LLM ให้เหลือน้อยที่สุด ผ่าน Flow-Control, Graph, Constraint**
    
4. **ทำงานแบบ pipeline reasoning ไม่ใช่ AI โมเดลคิดมั่ว ๆ**
    
5. **ผสานความรู้ทุกแหล่งเป็น Unified Knowledge Graph**
    
6. **ให้ผลลัพธ์ที่เสถียร มั่นคง และความหมายตรงตามข้อมูลจริง**
    
7. **รองรับการ scale : ง่ายต่อการ deploy, maintain, refactor**
    

**สรุป:**  
ระบบนี้ = **AI ที่ทำงานเหมือน “สติปัญญาที่มีโครงสร้าง”** ไม่ใช่ chatbot

---

# 3. GLOBAL PRINCIPLES — กฎเหล็กที่ระบบต้องทำตาม

## 3.1 Determinism

- อินพุตเหมือนกัน → ต้องให้ผลลัพธ์เหมือนกัน
    
- ไม่มี randomness ที่ปล่อยให้เกิดเอง
    
- ทุกสิ่งต้อง versioned
    

## 3.2 Canonical Knowledge

- ความรู้ใด ๆ ต้องผ่าน normalize → canonicalization → register
    
- ไม่มีข้อมูล “ลอย” ไม่มี orphan node/vector/edge
    
- ความจริงกลางถูกกำหนดด้วยระบบ ไม่ใช่ด้วยโมเดล
    

## 3.3 Layer Separation (L0–L5)

- ห้ามข้าม layer โดยตรง
    
- Logic ของ layer ต้องอยู่ใน engine ที่รับผิดชอบ
    
- ทำให้ระบบ maintain ง่าย + ลด bug ระยะยาว
    

## 3.4 Transparency

- ทุกการตัดสินใจบันทึก event
    
- reasoning ต้อง reconstruct ย้อนหลังได้
    
- output ต้องอิงจากข้อมูล ไม่ใช่เดา
    

## 3.5 Minimum Privilege

- agent แต่ละตัวมีสิทธิ์เฉพาะงานของตัวเอง
    
- system level และ user level แยกกันชัดเจน
    
- ห้าม agent “คิดแทน” subsystem ที่ไม่ใช่หน้าที่
    

## 3.6 Ethics & Safety

- อิงข้อมูลจริง
    
- ห้ามแต่งเรื่อง
    
- ห้ามละเมิด permission
    
- ห้าม bypass ความจริงกลาง
    

---

# 4. SYSTEM SCOPE — ขอบเขตที่ระบบทำ / ไม่ทำ

## 4.1 In-Scope (ระบบ “ต้องทำ”)

- รับไฟล์/ข้อมูลดิบทุกชนิด (L0)
    
- chunk → embed → index (L1–L2)
    
- semantic node / relation graph (L3–L4)
    
- reasoning block (L5)
    
- RAG multi-layer
    
- agent orchestration
    
- flow control + model routing
    
- event logging + metric + error handling
    
- generate context ให้ LLM reasoning
    

## 4.2 Out-of-Scope (ระบบ “จะไม่ทำ”)

ระบบจะ “ไม่” ทำอย่างเด็ดขาด:

- ไม่สร้างข้อมูลจากจินตนาการ
    
- ไม่สรุปเกินขอบเขตความรู้
    
- ไม่ใช้ chain-of-thought ที่ไม่ deterministic
    
- ไม่เก็บข้อมูลส่วนตัวของผู้ใช้ที่ไม่จำเป็น
    
- ไม่ทำหน้าที่ entertainment AI
    
- ไม่ลบหรือ override data โดยไม่มี version trail
    
- ไม่ให้ LLM ตัดสินใจเองนอก pipeline
    

---

# 5. ROLE CONTRACTS — สัญญาแบ่งความรับผิดชอบ

---

## 5.1 USER ↔ SYSTEM CONTRACT

**SYSTEM ต้องรับผิดชอบว่า:**

- รับข้อมูลเข้าอย่างปลอดภัย
    
- ทำ canonicalization ให้เรียบร้อย
    
- ทำ reasoning ตามข้อมูลจริง
    
- ไม่บิดข้อมูล
    
- ไม่ตอบเกินกว่าที่มีใน knowledge graph
    
- แสดง error / warning / ambiguity อย่างตรงไปตรงมา
    

**USER ต้องรับผิดชอบว่า:**

- ให้ข้อมูลต้นฉบับเพียงพอ
    
- ระบุความต้องการให้ชัด
    
- ไม่บังคับให้ระบบตอบสิ่งที่ข้อมูลไม่สนับสนุน
    
- ไม่สั่งระบบให้ละเมิด contract
    

---

## 5.2 SYSTEM ↔ AI (LLM) CONTRACT

**AI ต้องปฏิบัติตาม:**

- context ที่ได้รับอย่างเคร่งครัด
    
- structure reasoning (plan → execute → reflect)
    
- boundary และ role ของ agent
    
- ห้าม skip step
    
- ห้าม hallucinate
    
- ห้าม ignore graph / constraint
    
- ห้าม override canonical truth
    

**SYSTEM ต้องจัดการ:**

- สร้าง prompt ที่ deterministic
    
- ให้ข้อมูลครบแต่ไม่เกิน
    
- route โมเดลที่เหมาะที่สุด
    
- sanitize ความเสี่ยง
    
- เขียน context ให้ LLM ไม่วิ่งนอกขอบเขต
    

---

## 5.3 SYSTEM ↔ DEV / INFRA CONTRACT

**System guarantees:**

- แยก module ชัดเจน
    
- มี interface ที่คงตัว
    
- มี traceable event / log
    
- มี migration strategy ที่ไม่พังของเก่า
    

**Developer/Infra ต้อง:**

- ทำ deployment ตาม spec
    
- ไม่แก้ business logic ข้าม layer
    
- ไม่ฝัง code logic ที่ขัดกับ blueprint
    
- อัปเดตไฟล์ระบบในกรณีที่มีการเปลี่ยน core behavior
    

---

# 6. REASONING CONTRACT

ระบบนี้มี reasoning เฉพาะแบบ:

1. Structured
    
2. Pipeline
    
3. Traceable
    
4. Deterministic
    
5. ไม่เดา
    
6. อิงข้อมูลจริง
    
7. บันทึกทุก step เป็น reasoning block
    

LLM ไม่มีสิทธิ์ reasoning ตามใจ  
ต้องวิ่งตาม pattern:

- plan
    
- query
    
- retrieve
    
- analyze
    
- synthesize
    
- reflect
    
- answer
    

ทุกครั้งต้องอิง L0–L5 และ canonical registry

---

# 7. EXECUTION CONTRACT

ระบบต้อง:

- ใช้ flow-control engine เป็นตัวกำกับ
    
- route โมเดลผ่าน model-routing engine
    
- trigger agent ผ่าน agent engine
    
- ใช้ event bus เป็นแกนกลางความจริง
    
- ใช้ constraint ของ schema เป็น boundary
    
- ใช้ cache อย่างมีระเบียบ (ตาม spec)
    

ถ้า step ไหนล้ม → ต้อง fallback หรือ retry  
ไม่อนุญาตให้เละ

---

# 8. VERSIONING CONTRACT

ต้องใช้กฎต่อไปนี้:

- ทุกข้อมูลมี version
    
- ทุก graph/node/chunk/embed มี hash
    
- เปลี่ยนแปลงใด ๆ = ต้อง bump version
    
- breaking change ต้องบันทึกใน registry
    
- backward compatibility เป็น default
    

---

# 9. OVERRIDE RULE

มีเพียง 2 สิ่งที่ override ได้:

1. ข้อมูล (ด้วย version ใหม่)
    
2. Engine (ด้วย spec ใหม่ที่ align กับ contract)

LLM ไม่มีสิทธิ์ override  
agent ไม่มีสิทธิ์ override  
developer override ได้แต่ต้องอัปเดต contract + blueprint

---
# 10. FINAL BINDING STATEMENT (กฎหมายสูงสุด)

เอกสารนี้คือ “สัญญาแม่”  
ทุกไฟล์ลูกต้องเชื่อฟัง 100%:

- architecture
- schema
- engine
- api
- security
- deployment
- execution

ห้ามไฟล์ใดแหกจากหลักการนี้  
ถ้าแหก → ถือว่า invalid และต้อง rewrite ใหม่

**จบ — SYSTEM CONTRACT v3.0 (FULL / FINAL)**

---

โอเค Santa — นี่คือเวอร์ชัน **01__SYSTEM_CONTRACT_v3.0 (FULL + DIAGRAM + EXAMPLE + MAPPING ชัดที่สุด)**  
ฉันรวมข้อมูลจากทุกไฟล์ทุกระบบที่นายอัปโหลดแล้ว (00–12, RAG, KS, Agent, Graph, Data Schema, Architecture) เพื่อสร้างสัญญาที่ครบที่สุดแบบ **“อ่านครั้งเดียวเข้าใจทั้งระบบ”**

และเพื่อให้เข้าใจเป็นภาพจริง—กูเพิ่ม **diagram จริง**, **mapping**, และ **example flow** แบบใช้งานได้ทันที

---

![Image](https://www.researchgate.net/publication/331754935/figure/fig1/AS%3A799940712353793%401567732136298/System-architecture-diagram-The-layers-have-different-components-and-play-different.png?utm_source=chatgpt.com)

![Image](https://www.researchgate.net/publication/351008687/figure/fig1/AS%3A1121038846959673%401644287897675/The-technical-architecture-of-a-knowledge-graph.png?utm_source=chatgpt.com)

![Image](https://d3lkc3n5th01x7.cloudfront.net/wp-content/uploads/2024/08/26051537/Advanced-RAG.png?utm_source=chatgpt.com)

![Image](https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/solutions/approved/images/architecture-diagrams/multi-agent-orchestration-on-aws.97eb9e103c647b222ff2f7198ced70ec72e73aaf.png?utm_source=chatgpt.com)

# 01__SYSTEM_CONTRACT_v3.0

### (FULL + DIAGRAM + EXAMPLE + MAPPING)

---

# 1. PURPOSE — ทำไมระบบนี้ต้องมี “สัญญาแม่”

สัญญานี้คือ **กฎหมายสูงสุด** ของ UET Platform  
เพื่อ:

- ตรึง “ขอบเขต” ของระบบ
    
- บังคับให้ทุก engine ทำงานในกรอบเดียวกัน
    
- ป้องกัน drift, การ rewrite ไฟล์ผิดทิศ, และ logic ที่หลุดจาก blueprint
    
- เป็นภาษากลางของทั้งระบบ
    

**ทุกไฟล์ลูก (02–25) ต้อง align กับสัญญานี้ 100%**

---

# 2. SYSTEM OBJECTIVES — เป้าหมายแบบไม่เบี้ยว

1. สร้าง **Knowledge OS** ที่ deterministic
    
2. ผสานข้อมูลเป็น **Unified Knowledge Graph** (L0 → L5)
    
3. ให้ reasoning ที่ตรวจสอบย้อนหลังได้
    
4. ให้ผลลัพธ์ที่ “สม่ำเสมอ” ไม่เดา
    
5. ป้องกัน drift ของ LLM ผ่าน constraint + flow-control
    
6. ใช้ multi-engine orchestration เพื่อแทน “สมองเชิงโครงสร้าง”
    

---

# 3. GLOBAL PRINCIPLES — กฎเหล็ก

## 3.1 Determinism

- อินพุตเหมือนกัน → ผลลัพธ์เหมือนทุกครั้ง
    
- ไม่ใช้ randomness ใน core reasoning
    
- ทุกข้อมูลต้องมี version/hash
    

## 3.2 Canonical Knowledge

- ทุกอย่าง normalize → canonical → register
    
- ไม่มี orphan chunk/node/vector
    

## 3.3 Layer Separation

ห้ามข้ามชั้น L0–L5 แบบลัดขั้น

## 3.4 Transparency

- reasoning reconstruct ได้ 100%
    
- ทุกขั้นตอนลง event log เสมอ
    

## 3.5 Minimum Privilege

- agent มีสิทธิ์เท่าที่จำเป็น
    
- system/user/agent แยกขอบเขตชัดเจน
    

## 3.6 Ethics

- ไม่ fabricate
    
- ไม่แต่งข้อมูล
    
- ไม่ละเมิด canonical truth
    

---

# 4. SYSTEM SCOPE

## In-scope

- ingest/file parsing
    
- chunk+embed+index
    
- semantic graph
    
- relation graph
    
- reasoning block
    
- RAG pipeline
    
- agent orchestration
    
- event logging, caching, model routing
    

## Out-of-scope

- hallucination generation
    
- chain-of-thought แบบเดามั่ว
    
- การเล่าความเท็จ
    
- entertainment chatbot
    
- การตัดสินใจนอก L0–L5
    

---

# 5. ROLE CONTRACTS

---

# 5.1 USER ↔ SYSTEM

**System ต้อง:**

- ไม่บิดข้อมูล
    
- ตอบตาม knowledge graph เสมอ
    
- แสดง error ชัดเจน
    
- ไม่ตอบเกินข้อมูลที่มี
    

**User ต้อง:**

- ส่งข้อมูลต้นทาง
    
- ระบุเจตนาชัด
    
- ไม่บังคับให้ระบบทำผิด contract
    

---

# 5.2 SYSTEM ↔ AI (LLM)

**AI ต้อง:**

- ทำ reasoning ตามขั้นตอน pipeline
    
- ห้าม hallucinate
    
- ห้าม ignore context
    
- ห้าม skip step
    

**System ต้อง:**

- ส่ง prompt deterministic
    
- ให้ context ตาม canonical graph
    
- ตรวจสอบความเสี่ยง/ความเบี่ยงเบน
    

---

# 5.3 SYSTEM ↔ DEVELOPER

**System รับประกัน:**

- interface คงตัว
    
- engine แยกชัด
    
- log/metrics ครบ
    

**Dev ต้อง:**

- ไม่แก้ logic ข้าม layer
    
- adhere schema constraints
    
- อัปเดตไฟล์ระบบถ้า behavior เปลี่ยน
    

---

# 6. REASONING CONTRACT

AI reasoning ถูกจำกัดให้อยู่ใน pattern เดียว:

```
PLAN → COLLECT (RAG) → ANALYZE → SYNTHESIZE → REFLECT → ANSWER
```

ทุก block ถูกบันทึกเป็น reasoning_block (L5)

ห้าม AI:

- เดา
    
- วิ่งนอก L0–L5
    
- override canonical truth
    

---

# 7. EXECUTION CONTRACT

การทำงานต้องผ่าน:

1. Flow-Control Engine
    
2. Model Routing Engine
    
3. RAG Engine
    
4. Agent Engine
    
5. Cache Strategy
    
6. Event Bus System
    

ถ้าสเต็ปไหนล้ม → ต้อง fallback/retry ตาม policy

---

# 8. VERSIONING CONTRACT

- ทุก entity มี version/hash
    
- ทุก graph update = canonical version bump
    
- breaking change ต้องแจ้งและอธิบาย
    

---

# 9. OVERRIDE RULE

มีแค่สองอย่างที่ override ได้:

1. Data (ด้วย version ใหม่)
    
2. Engine Spec (ด้วย spec ใหม่ที่ align blueprint)
    

**LLM ไม่สามารถ override อะไรได้เลย**

---

# 10. BLUEPRINT MAPPING (1:1 กับ 25 ไฟล์)

![Image](https://www.researchgate.net/publication/292140102/figure/fig2/AS%3A322813710880769%401453976194312/An-example-of-system-architecture-and-module-specification-diagrams.png?utm_source=chatgpt.com)

![Image](https://www.researchgate.net/publication/351008687/figure/fig1/AS%3A1121038846959673%401644287897675/The-technical-architecture-of-a-knowledge-graph.png?utm_source=chatgpt.com)

![Image](https://www.montecarlodata.com/wp-content/uploads/2023/07/Data-Pipeline-Architecture-Drata-1024x547.jpg?utm_source=chatgpt.com)

![Image](https://datatron.com/wp-content/uploads/2021/05/Machine-Learning-Pipeline_1.png?utm_source=chatgpt.com)

|หมายเลขไฟล์|หน้าที่|
|---|---|
|00|Blueprint แม่|
|01|System Contract (ไฟล์นี้)|
|02|Architecture|
|03|Project Structure|
|04|Data Schema|
|05|Unified Knowledge Graph|
|06–08|SQL / Constraint / Index|
|09|KS Engine|
|10|RAG Engine|
|11|Agent Engine|
|12|Flow Control Engine|
|13|Model Routing|
|14|Event Bus|
|15|Cache|
|16|Execution Graph|
|17|Worker/Task System|
|18–20|API Spec / Payload / Error|
|21|UI System|
|22|Security|
|23|Deployment Guide|
|24|Testing Strategy|
|25|Metrics/Observability|

ทุกไฟล์ต้องเข้ากันเป็นระบบเดียวตามสัญญานี้

---

# 11. SYSTEM CONTRACT DIAGRAM (ตัวแม่)

## 11.1 Logical Contract Diagram

```
        ┌──────────────────────────────┐
        │        SYSTEM CONTRACT       │
        │  (กฎหมายสูงสุดของระบบนี้)   │
        └─────────────┬────────────────┘
                      ▼
          ┌────────────────────────┐
          │   MASTER BLUEPRINT     │
          └────────────────────────┘
                      ▼
       ┌─────────────────────────────────┐
       │   ARCHITECTURE / DATA / GRAPH   │
       └─────────────────────────────────┘
                      ▼
        ┌──────────────────────────────┐
        │          ENGINES             │
        │  (KS / RAG / AGENT / FLOW)   │
        └──────────────────────────────┘
                      ▼
        ┌──────────────────────────────┐
        │       EXECUTION + API        │
        └──────────────────────────────┘
                      ▼
                USER OUTPUT
```

---

# 12. END-TO-END EXAMPLE (แสดงความเข้าใจจริง)

### ผู้ใช้ถาม:

“ช่วยสรุปโครงสร้างไฟล์ 05 Unified Knowledge Graph ให้หน่อย”

### Pipeline ที่เกิดขึ้น:

1. **Flow Engine:** classify → `knowledge_query`
    
2. **Model Routing:** เลือกโมเดล reasoning
    
3. **RAG Engine:**
    
    - vector search (L2)
        
    - semantic node expansion (L3)
        
    - relation graph follow (L4)
        
4. **Agent Engine:**
    
    - Knowledge Agent รวบรวมข้อมูล
        
    - Synthesizer Agent ประกอบคำตอบ
        
5. **Reasoning Block (L5):**
    
    - break → analyze → synthesise → produce
        
6. **Answer Builder:** ส่งคำตอบออก
    

ทุก step ถูกบันทึกใน event log และ reasoning_block

---

# 13. FINAL STATEMENT

# ✅ 01__SYSTEM_CONTRACT.md

## **Part 1 — (เสริม) Determinism / Safety / Model Routing Contract**

---

# **1. DETERMINISM CONTRACT (กฎความกำหนดแน่นอน)**

ระบบทั้งหมดต้องปฏิบัติตาม “หลักความกำหนดแน่นอน” (Deterministic System Behavior)  
เพื่อให้ผลลัพธ์คงเส้นคงวา ไม่สุ่ม ไม่หลุด ไม่แถแม้แต่นิดเดียว

### **1.1 Deterministic Execution**

ทุก Engine ต้องทำตามคุณสมบัตินี้:

- **Input เหมือนกัน → Output ต้องเหมือนกันทุกครั้ง**
    
- ห้ามให้ “temperature” หรือ “creative randomness” ทำให้คำตอบเพี้ยน
    
- Agent ต้องควบคุม reasoning step เสมอ ไม่ใช่ LLM คิดเองลอย ๆ
    

**สูตรตรวจสอบ:**

```
Hash(Input + Context + EngineConfig) → Must match every run
```

---

### **1.2 Deterministic Routing**

Model Routing Engine ต้องเลือกโมเดลแบบ deterministic:

- task signature เดียวกัน
    
- context เดียวกัน
    
- priority set เดียวกัน  
    → ต้อง routing เหมือนกัน 100%
    

ห้ามจัดลำดับใหม่ตามอารมณ์ของโมเดลหรือเงื่อนไขลอย ๆ

---

### **1.3 Deterministic Knowledge Access**

- RAG Engine: ranking score = deterministic
    
- UKG Query: same graph state → same answer
    
- Cache: deterministic read/write rules
    

---

### **1.4 Deterministic Fallback**

ถ้า agent ล้มเหลว, rag พัง, หรือโมเดล timeout:

```
Primary Model → Backup #1 → Backup #2 → Error Handling
```

ห้ามสลับ order เองโดยไม่ผ่าน Flow Engine

---

# **2. SAFETY CONTRACT (กฎความปลอดภัย & Policy)**

เป็นเงื่อนไข “ห้ามละเมิดเด็ดขาด”  
Engine ทั้งหมดต้องทำตามโดยไม่มีข้อยกเว้น

---

## **2.1 Safety Boundary**

ระบบต้อง:

- หลีกเลี่ยงข้อมูลเท็จ (misinfo)
    
- หลีกเลี่ยงเนื้อหาที่ผิดกฎหมาย
    
- ห้ามให้เนื้อหาที่เป็นอันตรายต่อผู้ใช้หรือบุคคลอื่น
    
- ห้ามให้เนื้อหาอ่อนไหวที่กำหนดไว้ใน policy
    

Engine ต้อง “reject → reroute → fallback → sanitize” ตาม flow

---

## **2.2 Permission Guard**

ก่อนทุกการประมวลผล:

- ตรวจ user type
    
- ตรวจ allowed tasks
    
- ตรวจ permission flags
    
- ตรวจ restricted engine zones
    

ถ้าไม่ตรง → Flow Engine ต้องตัดทิ้งทันที

---

## **2.3 Data Protection**

- ห้ามนำข้อมูลส่วนตัวไปใช้ข้าม context
    
- ห้าม “hallucinate personal data”
    
- ต้องใช้ข้อมูลจริงที่ผ่าน UKG / DB เท่านั้น
    

---

## **2.4 Safety Override**

Flow Engine มีสิทธิ์ override output ของ Engine อื่น  
ถ้าเจอเนื้อหาอันตรายหรือผิด policy

```
Engine Output → Safety Check → Rewrite / Block / Reroute
```

---

# **3. MODEL ROUTING CONTRACT**

กฎที่ควบคุมการเลือกโมเดลทุกครั้ง  
เพื่อให้ routing “คงเส้นคงวา”, “โปร่งใส”, “ทำนายได้”, “ไม่มั่ว”

---

# **3.1 Model Allowlist / Blocklist**

Allowlist = **เฉพาะโมเดลที่อนุญาตให้ใช้ได้**  
Blocklist = โมเดลที่ “ห้ามใช้” โดยเด็ดขาด

### ตัวอย่าง (2025):

**Allowlist:**

- Google Gemini 3.0 Pro
    
- Google Gemini 3.0 Flash
    
- Claude 4.5 Opus
    
- Claude 4.5 Sonnet
    
- OpenAI GPT-5.1 / GPT-5.1-E / GPT-4.1
    
- 01-Preview / 01-Plus
    

**Blocklist:**

- โมเดลรุ่นเก่า 2022–2023
    
- GPT-3.5 / GPT-3 / GPT-J / GPT-NeoX
    
- Llama 1–2 รุ่นเก่า
    
- โมเดลราคาถูกที่ไม่ deterministic
    

---

# **3.2 Routing Score Formula**

Routing Engine ต้องใช้สูตร “คงที่” ไม่เปลี่ยนไปเอง:

```
RoutingScore = 
    w1*ReasoningCapability +
    w2*ContextPrecision +
    w3*LatencyScore +
    w4*CostScore +
    w5*SafetyTier
```

> น้ำหนัก (w1–w5) ถูกกำหนดใน SYSTEM CONTRACT  
> ห้ามเปลี่ยนระหว่าง runtime

---

# **3.3 Routing Determinism Rule**

ถ้า input เหมือนกัน:

- task type
    
- metadata
    
- user type
    
- safety level
    

→ Routing ต้องให้ “โมเดลเดียวกัน” เสมอ  
ห้ามลอยไปเลือกโมเดลที่แพงกว่าโดยไม่จำเป็น

---

# **3.4 Routing Fallback Policy**

ต้องเป็นแบบนี้เท่านั้น — ห้ามแก้:

```
Tier 1 (สูงสุด): Gemini Pro → Claude Opus → GPT-5.1
Tier 2 (ทั่วไป): Claude Sonnet → GPT-5.1-E → 01-Plus
Tier 3 (เบา): Gemini Flash → GPT-4.1 → 01-Preview
```

Flow Engine ต้อง enforce policy นี้อย่างเคร่งครัด

---

# **3.5 Routing Transparency**

Routing Engine ต้อง log:

- input task type
    
- reasoning path
    
- chosen model
    
- fallback chain
    
- safety decision
    
- time cost / price cost
    

เพื่อตรวจสอบย้อนหลัง (audit trail)

---

# **4. SYSTEM CONTRACT SUMMARY (ภาษากลาง)**

ให้เข้าใจง่าย ๆ

```
System Contract = กฎเหล็กที่ทุก Engine ต้องทำตาม

1. Deterministic → ผลลัพธ์ต้องคงที่ไม่สุ่ม
2. Safe → ปลอดภัย ถูกต้อง ถูกกฎหมาย
3. Routed → ใช้โมเดลที่เหมาะสมตามกฎ routing
4. Verified → ทุกขั้นต้องผ่าน safety & reasoning checks
5. Composable → Engine ต้องทำงานร่วมกันอย่างคงเส้นคงวา
```

---

## ✨ 01__SYSTEM_CONTRACT.md — Part 1 (เสริม): DONE

ครบ 3 ส่วนที่ต้องเติม:

✔ Determinism Contract  
✔ Safety Contract  
✔ Model Routing Contract

- ภาษากลาง refine ให้คมขึ้น
    

ไม่รื้อของเก่า  
ไม่เปลี่ยนความหมาย  
เพิ่มเฉพาะสิ่งที่ขาดเพื่อให้ระบบ “เป็นระบบจริง”

---

โอเค Santa —  
นี่คือ **01__SYSTEM_CONTRACT.md — Part 2 (เสริมแบบ Final Revision)**  
ชุดนี้คือ **หัวใจจริง ๆ ของ SYSTEM CONTRACT** เพราะมันเป็น “กฎผูกมัดระบบทั้งหมด”  
ทำให้ทุก Engine ทำงานร่วมกัน **แม่นยำ, ปลอดภัย, ควบคุมได้, ไม่มั่ว, ไม่มี corruption**

กูเสริม 4 ส่วนใหญ่แบบที่มึงขอ:

1. **Corruption Safety (ป้องกันข้อมูล/ความรู้เพี้ยน)**
    
2. **Execution Guarantees (กฎรับประกันการรัน)**
    
3. **Flow + Agent Compliance Rules (ห้ามผิดขั้นตอน)**
    
4. **Contract Matrix (แมป Engine ทั้งหมดกับกฎที่ต้องทำตาม)**
    

ทั้งหมดเขียนโดยให้ **คม, กระชับ, ภาษาเดียวทั้งระบบ**, พร้อมย้ายไปไฟล์จริงได้ทันที  
และสอดคล้องกับไฟล์ที่มึงอัปโหลดล่าสุดทุกไฟล์

---

# ✅ 01__SYSTEM_CONTRACT.md

## **Part 2 (เสริม) — Corruption Safety / Execution Guarantees / Flow–Agent Compliance / Contract Matrix**

---

# **5. CORRUPTION SAFETY CONTRACT**

กฎส่วนนี้คือ “ระบบห้ามเพี้ยนเด็ดขาด”  
ถ้าผิด = ระบบพังทั้งโครง → ห้ามเกิดแม้แต่ครั้งเดียว

---

## **5.1 Knowledge Corruption Prevention**

ระบบทั้งหมดต้องปฏิบัติตาม:

- **ห้ามเขียนข้อมูลใหม่ลง L0–L5 โดยไม่ผ่าน KS Engine**
    
- Agent / RAG / Model Routing → **ไม่มีสิทธิ์แก้ Knowledge Base ตรง ๆ**
    
- ทุกการเขียนข้อมูลต้องวิ่งผ่าน:
    

```
Normalization → Chunk → Semantic Tagging → UKG Mapping → Storage
```

- ห้าม “overwrite node” ถ้าไม่ใช่ mutation ที่ JS Engine อนุญาต
    
- ห้ามให้ LLM hallucinate แล้วเขียนลง DB
    
- ห้ามความรู้ลอยเข้าสู่ระบบ (external contamination)
    

---

## **5.2 Execution Corruption Prevention**

Flow Engine ต้องบังคับใช้:

- Node เดียวกันต้องไม่ถูกรันซ้ำโดยไม่มีเหตุผล
    
- Agent Plan ห้ามเปลี่ยนกลางคันระหว่าง execution
    
- ถ้ามี branching → ต้อง log decision tree
    
- ห้ามให้ RAG จัดอันดับเพี้ยนจาก round 1 → round 2
    

---

## **5.3 Model Corruption Safety**

- ห้าม model เปลี่ยนน้ำหนักความเชื่อใจ (confidence) เอง
    
- ห้ามสุ่มเปลี่ยน style, tone, format
    
- ใช้ style sheet ที่ Flow Engine ส่งมาเท่านั้น
    
- Safety override ต้องไม่ทำให้ความหมายหลุดหรือผิดโครงสร้าง
    

---

## **5.4 Integrity Check Rule**

ทุก output ต้องผ่าน integrity scanner:

```
(1) Logic Consistency  
(2) Semantic Consistency  
(3) Safety  
(4) Determinism  
(5) Contract Compliance
```

ถ้าผิดข้อใด → reroute → retry → fallback  
ห้ามคืน output ที่ “ไม่ผ่าน contract”

---

# **6. EXECUTION GUARANTEES (กฎรับประกันการทำงาน)**

นี่คือกฎที่ทุก Engine ต้องเคารพ  
ระบบทั้งหมดต้องมั่นใจว่า “ทำงานจนจบ, ไม่หยุดกลางทาง, ไม่เปลี่ยน state เอง”

---

## **6.1 Guarantee #1 — Completion Guarantee**

ทุกคำสั่งต้องจบไม่ว่าทางใดทางหนึ่ง:

```
SUCCESS  
or  
SAFE_FAIL (ผู้ใช้เข้าใจผลลัพธ์)  
or  
CONTROLLED_ABORT (ระบบตัดเพื่อความปลอดภัย)
```

ห้ามมีกรณี “ค้าง”, “ล้มแบบเงียบ ๆ”, “หายไปเฉย ๆ”

---

## **6.2 Guarantee #2 — State Consistency**

Execution Graph ต้อง:

- ไม่ให้ Node กระโดดข้าม
    
- ไม่ให้ Node ทำงานผิดลำดับ
    
- ไม่ให้ Node เปลี่ยน state (PENDING → DONE) โดยไม่มี event
    
- ห้ามวนลูปโดยไม่ผ่าน Flow Engine
    

---

## **6.3 Guarantee #3 — Retry Guarantee**

Retry ต้อง deterministic:

```
Primary → Retry(1) → Retry(2) → Fallback → Hard Fail
```

จำนวนครั้ง retry ห้ามเปลี่ยนใน runtime

---

## **6.4 Guarantee #4 — Output Format Guarantee**

ไม่ว่าผลลัพธ์จะมาจากโมเดลไหน:

- รูปแบบต้องเหมือนกัน
    
- agent ต้อง enforce format ก่อนส่งออก
    
- ห้ามโมเดลตอบในรูปแบบที่ไม่ได้กำหนด
    
- ห้ามโมเดลหลุดรูปแบบระหว่าง flow
    

---

# **7. FLOW + AGENT COMPLIANCE RULES**

นี่คือ “สัญญาผูกมัด” ระหว่าง Flow Engine และ Agent Engine  
ห้ามผิดแม้แต่นิดเดียว

---

# **7.1 Flow Engine → Agent Engine Contract**

Flow Engine ต้อง:

- ส่ง task แบบ standardized
    
- ส่ง constraints ที่ตายตัว
    
- ส่ง routing result ชัดเจน
    
- ส่ง objective ที่ deterministic
    
- ส่ง format spec
    
- ส่ง fallback policy
    

ห้าม Flow Engine ให้ Agent “คิดเอาเอง”

---

# **7.2 Agent Engine → Flow Engine Contract**

Agent ต้อง:

- สร้าง plan ที่ deterministic
    
- ไม่เปลี่ยน plan หลังเริ่ม execution
    
- ไม่ข้าม step
    
- ส่งเหตุผล reasoning ทุกครั้ง (traceable)
    
- ใช้ข้อมูลจาก RAG/UKG เท่านั้น
    
- ไม่ดึงข้อมูลลอย ๆ จากโมเดล
    

Agent ต้องถือว่า:

```
Flow Engine = Law  
Agent = Executor  
LLM = Tool  
```

ห้ามโมเดลกลายเป็น “decision maker”

---

# **7.3 Agent–RAG Interaction Rules**

- RAG ห้าม override agent
    
- Agent ห้าม request RAG แบบสุ่ม
    
- ต้องใช้รูปแบบ query ที่ Flow Engine อนุญาต
    
- RAG ranking = deterministic
    
- RAG → Agent → Flow → Output  
    ห้ามลัดขั้นตอน
    

---

# **7.4 Flow–Routing Compliance**

Flow Engine ต้อง:

- เรียก routing ตามขั้นตอน
    
- ห้าม routing หลังเริ่ม execution
    
- ห้ามเปลี่ยนโมเดลกลางทาง
    
- ต้อง log ทุก decision
    
- ต้อง enforce allowlist/blocklist ที่ Contract กำหนด
    

---

# **8. ENGINE CONTRACT MATRIX (FINAL)**

นี่คือ “ตารางรวมความสัมพันธ์”  
ที่บอกว่า Engine ไหนต้องทำตาม Contract อะไร  
เป็นหัวใจหลักที่เชื่อมทุกไฟล์ของระบบ

```
┌───────────────────────────────┬───────────────────────────┬──────────────────────────┬─────────────────────────┬───────────────────────────┐
│ ENGINE                        │ Determinism Contract       │ Safety Contract          │ Routing Contract        │ Execution Contract        │
├───────────────────────────────┼───────────────────────────┼──────────────────────────┼─────────────────────────┼───────────────────────────┤
│ FLOW CONTROL ENGINE           │ ✔ Full                    │ ✔ Full                   │ ✔ Full                 │ ✔ Full                    │
│ MODEL ROUTING ENGINE          │ ✔ Full                    │ ✔ Full                   │ ✔ Core Engine           │ ✘ (Flow handles exec)     │
│ AGENT ENGINE                  │ ✔ Full                    │ ✔ Partial (Flow override)│ ✔ Must follow routing   │ ✔ Full                    │
│ RAG ENGINE                    │ ✔ Full                    │ ✔ Data Safety            │ ✘ (not routing)         │ ✔ Partial (Ranking)       │
│ KS ENGINE (Knowledge Sync)    │ ✔ Full                    │ ✔ Data Integrity         │ ✘                       │ ✔ Data Mutation Rules     │
│ UNIFIED KNOWLEDGE GRAPH       │ ✔ Semantic Determinism    │ ✔ Data Protection        │ ✘                       │ ✔ Graph Mutation Rules    │
│ EXECUTION GRAPH               │ ✔ Node Determinism        │ ✔ Flow Safety            │ ✘                       │ ✔ Core Engine             │
│ CACHE SYSTEM                  │ ✔ Deterministic Caching   │ ✔ Safe Invalidation      │ ✘                       │ ✔ Read/Write Contracts    │
│ EVENT BUS                     │ ✔ Ordered Logging         │ ✔ Redaction Policy       │ ✘                       │ ✔ Delivery Guarantees     │
└───────────────────────────────┴───────────────────────────┴──────────────────────────┴─────────────────────────┴───────────────────────────┘
```

---

# **9. SYSTEM CONTRACT (ภาษากลาง Ultra-Short Version)**

> ใช้ในสไลด์ / ใช้ในอธิบายทีม

```
SYSTEM CONTRACT = 
กฎเหล็กที่ควบคุมทั้งระบบ

1. ห้ามสุ่ม — ทุกอย่างต้อง deterministic  
2. ห้ามเพี้ยน — ป้องกัน corruption ทุกช่องทาง  
3. ห้ามผิด — ต้องทำตาม safety policy  
4. ห้ามแถ — agent ต้อง reason อย่างตรวจสอบได้  
5. ห้ามลัด — flow engine คือกฎหมายกลางของระบบ  
6. ห้ามข้าม — ทุก engine ต้องทำตาม routing contract  
7. ห้ามซ้อน — graph/memory/caches ต้อง consistent  
8. ห้ามมั่ว — output ต้องอยู่ใน format ที่กำหนด  
```

---

## ⭐️ 01__SYSTEM_CONTRACT — Part 2 (เสริม): DONE

เพิ่มครบ:

✔ Corruption Safety  
✔ Execution Guarantees  
✔ Flow & Agent Compliance Rules  
✔ Engine Contract Matrix  
✔ ภาษากลางระดับ Master

นี่คือไฟล์ SYSTEM CONTRACT ที่ “มีฟัน”, “ใช้จริงได้”, “ควบคุมระบบได้”, “ไม่มีทางพัง”

---

# ✅ 01__SYSTEM_CONTRACT.md

## **Part 3 (เสริม) — Global Constraints / Timing / Coordination / Versioning / Error Boundaries**

---

# **10. GLOBAL CONSTRAINTS (กฎที่ครอบจักรวาลทั้งระบบ)**

กฎชุดนี้คือ “เงื่อนไขระดับบนสุด”  
เป็นเส้นแบ่งที่ไม่มี Engine ไหนข้ามได้

---

## **10.1 Consistency Constraint**

ความสอดคล้องของข้อมูล, logic, และ state ต้อง:

- consistent ในทุก Engine
    
- consistent ในทุก stage ของ Flow Engine
    
- consistent ระหว่าง L0–L5
    
- consistent กับ Knowledge Graph
    
- consistent กับ Routing Decision
    

ห้ามข้อมูล 2 ที่ “ขัดกัน”  
ห้าม output 2 อัน “ไม่ไปด้วยกัน”

---

## **10.2 Single Source of Truth**

- Flow Engine = ความจริงด้าน execution
    
- SYSTEM CONTRACT = ความจริงด้านกฎ
    
- DATA_SCHEMA = ความจริงด้านข้อมูล
    
- MASTER_BLUEPRINT = ความจริงด้านโครงสร้าง
    
- Model Routing = ความจริงด้านโมเดล
    

ห้ามหลาย Engine ตีความ state ต่างกัน

---

## **10.3 Immutability Constraint**

สิ่งที่ห้ามเปลี่ยน:

- Execution Plan ระหว่าง run
    
- Model Routing Decision
    
- Safety Tier
    
- Node Type ใน Execution Graph
    
- Output schema (JSON/Markdown spec)
    

ถ้าความจำเป็นต้องเปลี่ยน → ต้องเป็น “mutation event” ผ่าน Flow เท่านั้น

---

## **10.4 Predictability Constraint**

ระบบต้องสามารถ “ทำนายได้”:

- path ของการรัน
    
- model ที่เลือก
    
- reasoning steps
    
- fallback chain
    
- behavior ของทุก engine
    

ห้ามมี event ที่ไม่คาดคิดเกิดขึ้นเอง

---

## **10.5 Reproducibility Constraint**

การรันแบบเดียวกันในเวลาใกล้กัน:

```
Input = Same  
Context = Same  
System Version = Same  
→ Output Must Match
```

ถ้าผิด → ถือว่า “corruption” ระดับสูงสุด

---

# **11. TIME-BASED CONTRACT (กฎเกี่ยวกับเวลาใน Execution)**

เวลาเป็น variable สำคัญในระบบ จึงต้องมี “สัญญาเวลาที่ตายตัว”

---

## **11.1 Timeout Rules**

แต่ละระบบต้องเคารพ timeout ดังนี้:

### Engine Timeout:

- Agent: 4–8 วินาที
    
- RAG: 2–4 วินาที
    
- Routing: 0.5 วินาที
    
- KS Engine: 3–10 วินาที
    
- Cache: 10–30 มิลลิวินาที
    
- Event Bus: async only (ไม่ block)
    

ข้อบังคับ:

```
Flow Engine มีอำนาจ terminate ถ้าเวลาเกิน Limit
```

---

## **11.2 Scheduling Contract**

ห้าม Engine ไหน “ลากเวลา” หรือ “รันช้า” โดยไม่ได้รับอนุญาต

Flow Engine ต้อง enforce:

- agent deadline
    
- rag deadline
    
- routing deadline
    
- graph deadline
    

ทุก Engine ต้อง:

```
start_time  
end_time  
deadline  
```

ถูกต้องและตรวจสอบได้

---

## **11.3 Time-Propagation Rule**

เวลาแพร่ผ่านทุก engine แบบ deterministic:

```
Routing_Time + RAG_Time + Agent_Time + Safety_Time  
= Total Execution Time
```

ห้าม Engine ลัดขั้นตอนด้านเวลา

---

# **12. MULTI-ENGINE COORDINATION CONTRACT**

กฎนี้คือ “การประสานงานที่ถูกต้องระหว่าง Engine ทั้งหมด”

ห้ามเกิดการเรียก Engine ผิดลำดับ  
ห้าม Engine เรียกกันเองตามใจชอบ

---

## **12.1 Coordination Graph**

Engine ทั้งหมดต้องทำตามโครงสร้างนี้เท่านั้น:

```
Flow → Routing  
Flow → Agent  
Flow → RAG  
Flow → KS  
Flow → Graph  
Flow → Cache  
Flow → EventBus
```

ห้าม:

- Agent → KS (ผิด)
    
- RAG → KS (ผิด)
    
- Agent → Routing (ผิด)
    
- RAG → Agent (ผิด)
    
- KS → Flow (ผิด)
    

สิทธิ์เรียก engine ได้เฉพาะ “Flow Engine เท่านั้น”

---

## **12.2 Capability-Based Dispatch**

Flow Engine dispatch engine ตาม “ชนิดงาน” ไม่ใช่จาก model decision

ตัวอย่าง:

|Task|Engine|
|---|---|
|Extract knowledge|KS Engine|
|Retrieve memory|RAG|
|Plan reasoning|Agent|
|Generate text|Agent|
|Get model|Routing|
|Prepare final output|Agent|
|Log|EventBus|

ห้ามข้าม capability

---

## **12.3 State Synchronization**

Execution Graph ต้อง sync state กลับ Flow Engine ทุกครั้งที่มี node end

ห้าม engine ทำงานโดยไม่ update state

---

## **12.4 Error Coordination**

ถ้ามี error:

```
Agent → Flow (Report)  
RAG → Flow (Report)  
Routing → Flow (Report)  
```

Flow ตัดสินใจ action:

- retry
    
- fallback
    
- reroute
    
- sanitize
    
- safe_fail
    

ห้าม engine ตัดสินใจเอง

---

# **13. VERSIONING POLICY (ของทั้งระบบ)**

ระบบต้องมี versioning ที่ “เป็นระบบเดียวทั้งระบบ”  
ไม่ใช่แต่ละ Engine แยก version กันแบบมั่ว ๆ

---

## **13.1 Version Format**

ใช้รูปแบบ: `vMAJOR.MINOR.PATCH`

ตัวอย่าง:

- `v3.0.0` = Major Update
    
- `v3.1.0` = Minor Update
    
- `v3.1.4` = Patch Fix
    

---

## **13.2 Version Scope**

Version มี 2 ระดับ:

### 1) SYSTEM_VERSION

ระบุการเปลี่ยนแปลง “ระดับโครงสร้างหลัก”

เช่น:

- schema เปลี่ยน
    
- contract เปลี่ยน
    
- engine behavior เปลี่ยน
    
- routing rule เปลี่ยน  
    → SYSTEM_VERSION ต้องเพิ่ม MAJOR
    

### 2) ENGINE_VERSION

ระบุการเปลี่ยนแปลง “เฉพาะ engine นั้น ๆ”

เช่น:

- rag ranking logic
    
- agent planning
    
- cache policy
    

→ เพิ่ม MINOR หรือ PATCH

**ทั้งระบบต้อง refer:**

```
SYSTEM_VERSION + ENGINE_VERSION_MAP
```

---

## **13.3 Backward Compatibility**

มี 2 กฎหลัก:

### กฎ 1

ถ้า SYSTEM_VERSION เปลี่ยน →  
Engine ทั้งหมดต้องปรับตาม

### กฎ 2

ถ้า ENGINE_VERSION เปลี่ยน →  
Flow Engine ต้องอ่าน version ใหม่ได้  
แต่ Knowledge Graph ห้ามเสียหาย

---

## **13.4 Version Locking**

ห้าม:

- RAG ใช้ logic รุ่นเก่า
    
- Agent ใช้ plan spec รุ่นเก่า
    
- Routing ใช้ tier เดิมกับโมเดลใหม่
    

Flow Engine ต้อง lock version ทุก Run ตามนี้:

```
Flow_Run {
  system_version: X
  engine_versions: {
     agent: x.x.x
     rag: x.x.x
     ks: x.x.x
     routing: x.x.x
  }
}
```

---

# **14. ERROR BOUNDARY CONTRACT (สุดท้าย)**

กฎที่กำหนด “ขอบเขตความผิดพลาด”  
เพื่อให้ระบบพังให้ถูกวิธี ไม่พังมั่ว ๆ

---

## **14.1 Error Types**

Error ถูกแบ่งได้ 5 แบบ:

1. **User Error** – input ผิด
    
2. **Model Error** – model ล้ม
    
3. **Engine Error** – agent, rag, routing พัง
    
4. **Data Error** – memory/graph inconsistent
    
5. **System Error** – infra, event bus, cache พัง
    

---

## **14.2 Error Boundary Rule**

ทุก error ต้องจบใน “boundary” ของ engine นั้น:

ตัวอย่าง:

- RAG พัง → ห้ามไป corrupt agent
    
- Agent พัง → ห้ามไป corrupt graph
    
- KS พัง → ห้ามเขียนข้อมูลเพี้ยน
    
- Routing พัง → ห้ามเลือกโมเดลผิด
    

---

## **14.3 Error Escalation Ladder**

ถ้าแก้ใน boundary ไม่ได้ ต้อง escalate แบบนี้เท่านั้น:

```
Engine → Flow → Safety → Fallback → Final Output  
```

ห้าม Agent แจ้ง error โดยตรงไป Users  
Flow ต้องเป็นตัวควบคุมความปลอดภัย

---

## **14.4 Safe-Fail Contract**

ทุก error ต้องจบด้วย:

```
Safe-Fail (อธิบายให้ผู้ใช้เข้าใจ)  
ไม่ใช่ Silent-Fail  
ไม่ใช่ Corrupt-Fail  
ไม่ใช่ Wrong Answer
```

---

## **14.5 Observability Contract**

Event Bus ต้อง log ทุกอย่าง:

- error
    
- fallback
    
- retries
    
- corruption attempt
    
- routing mistake
    
- plan mutation
    
- timing violation
    
- contract violation
    

เพื่อนำไปวิเคราะห์ทีหลัง

---

# ⭐️ 01__SYSTEM_CONTRACT — Part 3 (เสริม): DONE

ตอนนี้ SYSTEM CONTRACT ของมึง:

✔ มี Global Constraints  
✔ มี Time Contract  
✔ มี Coordination Rules  
✔ มี Versioning Policy  
✔ มี Error Boundary Contract  
✔ เป็นภาษากลาง  
✔ เชื่อมกับ Engine ทุกตัว  
✔ พร้อมย้ายลงไฟล์จริงได้ทันที  
✔ พร้อมใช้เป็นกฎหมายกลางของทั้ง Project

รวม Part 1 + Part 2 + Part 3 =  
**SYSTEM_CONTRACT v3.0 พร้อมใช้งาน 100%**

---
จัดให้ Santa —  
นี่คือ **“Supergraph Diagram”** ของระบบ UET Platform v3.0  
= **ภาพรวมทั้งจักรวาลในหน้าเดียว**  
= **แสดงทุก Engine, ทุก Layer, ทุก Data Flow, ทุก Dependency**  
= **แบบที่ dev, AI, researcher มองแล้วเข้าใจทันที**

ใช้เวลาเก็บและรวมมาจากไฟล์ทั้งหมดที่นายอัปโหลด (00–16 ทั้งหมด)

---

# 🚀 **UET PLATFORM v3.0 — SUPERGRAPH DIAGRAM (FULL SYSTEM)**

_(อ่านได้ในครั้งเดียว เห็นทุกส่วนของระบบ)_

```
                                           ┌─────────────────────────────────────┐
                                           │              USER LAYER             │
                                           │   Chat / Studio / API / Workspace   │
                                           └───────────────────────┬─────────────┘
                                                                   │
                                                                   ▼
                                          ┌───────────────────────────────────────────┐
                                          │            FLOW CONTROL ENGINE            │
                                          │ (authorization, versioning, routing,      │
                                          │   rate-limit, audit, deterministic I/O )  │
                                          └───────────────────────┬───────────────────┘
                                                                  │
                     ┌────────────────────────────────────────────┼────────────────────────────────────────────┐
                     │                                            │                                            │
                     ▼                                            ▼                                            ▼
       ┌──────────────────────┐                     ┌──────────────────────────┐                    ┌────────────────────────┐
       │   MODEL ROUTING      │                     │        RAG ENGINE        │                    │     AGENT ENGINE       │
       │ (select model based  │                     │  L2 vector → L3 concept  │                    │ (planner / executor /  │
       │  on task: reasoning, │                     │  → L4 relation → L5 fw   │                    │   tool / safety /      │
       │  summarization, etc) │                     │  retrieval pipeline       │                    │   execution graph )    │
       └───────────┬──────────┘                     └──────────────┬───────────┘                    └────────────┬──────────┘
                   │                                             │                                         │
                   │                                             │                                         │
                   │                                             │                                         │
                   ▼                                             ▼                                         ▼

        ┌────────────────────────────────┐            ┌────────────────────────────────┐         ┌────────────────────────────────┐
        │         KS ENGINE              │            │         RAG CONTEXT            │         │     EXECUTION GRAPH (L5)       │
        │ (chunk → embed → mention →     │            │  (evidence sets, rerank, MMR) │         │ (deterministic reasoning tree) │
        │  concept → relation → framework│            │                                │         │  nodes = L4/L5 knowledge       │
        │  + version control & sync)     │            │                                │         │  edges = causal/logical paths │
        └────────────────┬───────────────┘            └────────────────────────────────┘         └────────────────────────────────┘
                         │
                         │
                         ▼

       ┌──────────────────────────────────────────────────────────────────────────────────────────┐
       │                           UNIFIED KNOWLEDGE GRAPH (L1–L5)                                │
       │                                                                                          │
       │  L5 — Frameworks (UET / Value–Conflict / Systemic Collaboration / Abstract Models)       │
       │  L4 — Principles & Relations (cause → , contradict ⊣ , support + , refine ↳ , generalize)│
       │  L3 — Concepts (stable meaning, definitions, neighbors, context sets)                    │
       │  L2 — Mentions (canonical label, alias clusters, merged entities)                        │
       │  L1 — Semantic Units (chunk-derived meaning atoms)                                       │
       │                                                                                          │
       └─────────────────────────────┬────────────────────────────────────────────────────────────┘
                                     │
                                     ▼

           ┌───────────────────────────────────────────────────────────────────────────┐
           │                                 DATA LAYER                                │
           │───────────────────────────────────────────────────────────────────────────│
           │   SQL (files, chunks, embeddings meta, nodes, edges, registry, versions) │
           │   VECTOR DB (embeddings, search index)                                    │
           │   GRAPH DB (semantic graph, reasoning graph)                              │
           └───────────────────────────────────────────────────────────────────────────┘

                                     │
                                     ▼

         ┌────────────────────────────┬──────────────────────────────┬────────────────────────────┐
         │                            │                              │                            │
         ▼                            ▼                              ▼                            ▼
┌──────────────────┐        ┌────────────────┐              ┌──────────────────────┐    ┌──────────────────────┐
│  EVENT BUS       │        │   CACHE        │              │   WORKER / JOBS      │    │   LOGS & METRICS     │
│ (pub/sub, trace, │        │ (L1–L4 caches  │              │ (background sync,    │    │ (observability,      │
│  audit, replay)  │        │  version-aware)│              │  reindex, retries)   │    │  monitoring)         │
└──────────────────┘        └────────────────┘              └──────────────────────┘    └──────────────────────┘
```

---

# 🌌 **Supergraph Logic — อธิบายสั้น ๆ**

### **Flow Control = จุดเริ่มทุกอย่าง**

- ตรวจสิทธิ์
    
- ตรวจ version
    
- route
    
- rate-limit
    
- deterministic I/O
    

คือ “คอหอย” ของระบบ

---

### **Model Routing = เลือกสมอง**

เลือกโมเดลแบบ dynamic:  
GPT-5.1 / 5.1-Instant / Claude 3.7 / Nemotron / Qwen reasoning ฯลฯ

---

### **KS Engine = ผู้สร้างจักรวาลความรู้**

แปลงทุกอย่างเป็น L1 → L5 ตามโครง UET  
ควบคุม stability, drift, propagation rules  
อัปเดต version

---

### **RAG Engine = ผู้ดึงความรู้**

- vector
    
- semantic
    
- relation
    
- framework bias
    
- rerank MMR
    

ทั้งหมด deterministic

---

### **Agent Engine = ผู้ปฏิบัติภารกิจ**

- Planner
    
- Tool user
    
- Evaluator
    
- Safety
    
- Synthesizer
    

ใช้ Execution Graph ในการ reasoning

---

### **Execution Graph = สมองเหตุผลจริง**

- Node = principle/concept
    
- Edge = causal/logic
    
- Tree = deterministic reasoning path
    

---

### **Unified Knowledge Graph = พระคัมภีร์**

ใช้โดยทุก Engine  
เป็นศูนย์ความหมาย L1–L5  
ไม่มี engine ไหนคิดเองได้ ต้องใช้ KG เป็นฐาน

---

### **Event Bus = ระบบประสาท**

เก็บทุก event ของระบบ  
ใช้ replay, audit, rollback

---

### **Cache = เร่งความเร็วแบบฉลาด**

4 ชั้น: L1–L4  
ผูกกับ version + event  
ห้ามใช้ cache ผิด model/reasoning

---

### **Data Layer = ของจริงทั้งหมด**

- SQL = metadata
    
- Vector = embeddings
    
- Graph = semantics
    

---

# 🔥 นี่คือภาพรวมทั้งระบบแบบ Official Supergraph (ระดับสถาปัตยกรรมสูงสุด)

ต้องการเพิ่มแบบไหนต่อ?

- **Supergraph แบบลึกลงแต่ละ Engine (6 แผนภาพ)**
    
- **Supergraph แบบ workflow (เขียนเป็นเส้นทางข้อมูล)**
    
- **Supergraph แบบ dev mapping (folder → engine → layer)**
    
- **Supergraph แบบ logic tree (UET reasoning cycle)**
    

บอกเลขมาหนึ่งตัว (1–4) เดี๋ยวฉันจัดให้เลย 🔥