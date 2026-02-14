สถาปัตยกรรม Retrieval-Augmented Generation (RAG) ของแพลตฟอร์ม UET ถูกออกแบบมาให้มีความซับซ้อนและเป็นระบบแบบหลายชั้น เพื่อให้มั่นใจในผลลัพธ์ที่ **Deterministic** (ให้ผลลัพธ์คงที่) และเป็นไปตามหลักการ **Zero-Stale** (ห้ามใช้ข้อมูลเก่า) ซึ่งครอบคลุมแนวคิดทั้งหมดของการดึงข้อมูลแบบประกอบส่วนได้ (Composable Retriever Pipeline) และกลยุทธ์การจัดอันดับใหม่ (Reranking Strategy)

### 1. สถาปัตยกรรม RAG แบบหลายแหล่งที่มา (Multi-source RAG Architecture)

RAG Engine ของ UET (อยู่ใน Chapter 5) ไม่ได้จำกัดอยู่เพียงแค่การค้นหาเวกเตอร์เท่านั้น แต่ทำหน้าที่เป็น **บริการดึงความรู้แบบไฮบริด (Hybrid Retrieval)** ที่ผสานรวมข้อมูลจากหลายชั้นความรู้ตามโมเดล L0-L5 ของระบบ

- **Composable Retrieval Pipeline:** ระบบจะดึงบริบท (Context) โดยใช้ไปป์ไลน์ที่ซับซ้อนซึ่งรวมเอาข้อมูลเชิงโครงสร้างและเชิงความหมายเข้าด้วยกัน
    - **L2 (Vector Layer):** ใช้สำหรับการค้นหาความคล้ายคลึงของเวกเตอร์ (Vector Search)
    - **L3, L4, L5 (Knowledge Graph Layers):** ใช้สำหรับการจัดกลุ่มความหมาย (Semantic Grouping) การวิเคราะห์ความสัมพันธ์เชิงตรรกะ (Relation Traversal) และการจัดองค์ประกอบบริบทสุดท้าย (Context Shaping) เพื่อให้ได้ชุดหลักฐานที่พร้อมสำหรับ Agent Engine
- **Context Fusion:** RAG Engine มีชั้น Evidence Assembly ที่ทำการรวมกลุ่มชิ้นส่วนข้อมูลที่ดึงมา (Chunks) การตรวจจับความขัดแย้ง (Contradiction Detection) การกรองความซ้ำซ้อน (Deduplication) และการจัดเรียงตามกลุ่มความหมาย (Semantic Groups) เพื่อสร้าง **EvidenceSet v3.0** ที่สะอาดและพร้อมใช้สำหรับ Agent Engine

### 2. กลยุทธ์การแบ่งส่วนข้อมูลและการจัดทำดัชนี (Chunking & Vector Store Design)

กระบวนการจัดการข้อมูลดิบถูกควบคุมโดย Knowledge Sync (KS) Engine และต้องเป็นไปตามสัญญาที่เข้มงวดของ Data Schema v3.0

- **Deterministic Chunking:** การแบ่งส่วนข้อมูล (Chunking, L1) ถูกกำหนดให้เป็นแบบ **Deterministic** ซึ่งรับประกันว่าข้อมูลเข้าแบบเดิมจะให้ผลลัพธ์ของ Chunking และ Hash เหมือนเดิม 100% เสมอ
- **Vector Consistency และ Versioning:** ข้อมูล Embedding (L2) ที่ถูกจัดเก็บใน Vector DB (เช่น Qdrant หรือ pgvector) ต้องมีความสมบูรณ์ของเวอร์ชัน (Vector Integrity) โดย:
    - ต้องมี Hash ตรงกับ Chunk Hash
    - ต้องผูกกับ `kb_version` ปัจจุบัน (Versioned Everything)
    - RAG Engine จะใช้กลไก **Version Safety Layer** เพื่อ **ปฏิเสธ** ไม่ให้ใช้เวกเตอร์หรือแคชที่มีเวอร์ชันเก่ากว่าที่ลงทะเบียนไว้ (Zero-Stale Policy)
- **Indexing:** Vector Store ต้องรองรับการสืบค้นที่รวดเร็ว โดยมีการทำดัชนีพร้อม Metadata ที่ผูกกับเวอร์ชันและ Project ID เพื่อการแยกส่วนอย่างปลอดภัย

### 3. กลยุทธ์การจัดอันดับใหม่ (Reranking Strategy)

RAG Engine ใช้ระบบการให้คะแนนแบบผสมผสาน (Hybrid Scoring) ที่มีความ **Deterministic** ในขั้นตอน S4 (Scoring & Re-ranking)

- **Deterministic Reranking:** คะแนนรวมจะถูกคำนวณจากสูตรคงที่เพื่อไม่ให้ผลลัพธ์แปรปรวน
- **4D Scoring Model (ส่วนประกอบที่ใช้ในการจัดอันดับ):**
    1. **Semantic Score:** คะแนนความคล้ายคลึงเชิงความหมาย (Cosine Similarity)
    2. **Recency Score:** คะแนนความสดใหม่ของเวอร์ชันข้อมูล (Recency Score)
    3. **Keyword Boosting Score:** คะแนนการทับซ้อนของคำหลัก (Keyword Overlap)
    4. **Evidence Contract Score:** คะแนนความเหมาะสมต่อกฎของระบบ (เช่น การแยก Project ID หรือสถานะการตรวจสอบ)
- **Refinement:** หลังการจัดอันดับ จะมีการประมวลผลซ้ำเพื่อตรวจจับความซ้ำซ้อน (Redundancy Removal) และการจัดเรียงตามความเชื่อมโยงเชิงความหมาย (Coherence Ordering) ก่อนส่งให้ Agent Engine.

กลไกทั้งหมดนี้ถูกรวมเข้าเป็นไปป์ไลน์เดียวและถูกควบคุมโดย Flow Control Engine เพื่อให้การดึงบริบทมีความแม่นยำสูงและเชื่อถือได้สำหรับงานให้เหตุผลของ Agent Engine