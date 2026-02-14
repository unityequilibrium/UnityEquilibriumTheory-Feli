สถาปัตยกรรมของแพลตฟอร์ม UET ได้รับการออกแบบมาเพื่อรองรับการดำเนินการเวิร์กโฟลว์ LLM ที่มีความซับซ้อน (LLM workflow orchestrator) โดยใช้แนวคิดหลักของ **Execution Graph (กราฟการดำเนินการ)** ซึ่งคล้ายคลึงกับสถาปัตยกรรมแบบ DAG (Directed Acyclic Graph) และการจัดการโหนดแบบมีเงื่อนไข (conditional routing) ที่พบในเครื่องมือเช่น LangGraph

นี่คือภาพรวมของกลไกการจัดการเวิร์กโฟลว์แบบกราฟในระบบ UET:

### 1. โครงสร้าง Execution Graph และ DAG-based Execution

**Execution Graph (EG)** ของระบบ UET คือหัวใจของการให้เหตุผล (Reasoning) ของ Agent Engine กราฟนี้ถูกกำหนดให้เป็นไปตามหลัก **Deterministic** (ให้ผลลัพธ์ที่คงที่) และ **Reproducible** (สามารถทำซ้ำได้)

- **โครงสร้าง 3 ชั้นของ EG:** Execution Graph ประกอบด้วย 3 ชั้นหลักคือ **Nodes (โหนด)**, **Edges (เส้นเชื่อม)**, และ **Execution Rules (กฎการดำเนินการ)**
- **Nodes (โหนด):** โหนดแต่ละตัวแทน **งานชนิดหนึ่ง** หรือโมดูลย่อยที่ต้องดำเนินการ โหนดเหล่านี้ไม่ได้จำกัดอยู่เพียงแค่การเรียกใช้ LLM เท่านั้น แต่รวมถึงขั้นตอนอื่น ๆ ในไปป์ไลน์ทั้งหมด เช่น:
    - **การจัดการความรู้:** INGEST_FILE (รับไฟล์ L0), CHUNK_PROCESS (L1), EMBEDDING_PROCESS (L2), SEMANTIC_EXTRACT (L3), RELATION_BUILD (L4), CANONICALIZE (L5), และ **KS_SYNC** (อัปเดต Knowledge Graph)
    - **การดึงข้อมูล:** RAG_VECTOR_SEARCH, RAG_RERANK_WITH_L5, RAG_RESULT_FORMAT
    - **การให้เหตุผล:** AGENT_REASON_BASE, AGENT_PLAN, AGENT_EXECUTE
    - **การควบคุมระบบ:** FLOW_START, FLOW_DECISION, ROUTER_SELECT_MODEL, EVENT_PUBLISH

### 2. LLM Workflow Orchestrator และ Flow Control

**Flow Control Engine (FCE)** ทำหน้าที่เป็น **Master Orchestrator** ของ Execution Graph และระบบทั้งหมด FCE ควบคุมลำดับการดำเนินการ (execution order) และเป็นผู้ตรวจสอบกฎสูงสุดของระบบ (System Contract)

- **การควบคุมการไหล:** FCE กำหนดให้ทุก request ต้องผ่านขั้นตอนการตรวจสอบที่เข้มงวดก่อนเข้าสู่การดำเนินการ
- **การจัดลำดับงาน:** Flow Control มีหน้าที่ **schedule tasks (กำหนดการทำงาน)**, **run agents (รัน Agent)**, **handle dependencies (จัดการความสัมพันธ์ระหว่างงาน)**, **manage concurrency (จัดการการทำงานพร้อมกัน)**, และ **handle retries (จัดการการลองใหม่)**
- **การส่งต่อการทำงาน:** FCE จะส่งต่อ Execution Context ที่ผ่านการตรวจสอบแล้วไปยัง **Executor Engine** ซึ่งทำหน้าที่รันโหนดเฉพาะทาง เช่น Agent Executor, RAG Executor, และ KS Executor

### 3. Conditional Routing และ Modular Reasoning Graph

Execution Graph รองรับ **Conditional Routing (การกำหนดเส้นทางตามเงื่อนไข)** และ **Fallback Edge (เส้นทางสำรองเมื่อเกิดข้อผิดพลาด)** ซึ่งจำเป็นสำหรับการจัดการเวิร์กโฟลว์ของ AI ที่มีหลายขั้นตอน

- **Edges (เส้นเชื่อม):** เส้นเชื่อมแต่ละเส้นจะระบุ:
    - **ลำดับงาน (Order):** Node A → Node B
    - **เงื่อนไข (Condition):** ภายใต้เงื่อนไขอะไร (เช่น _if confidence > 0.8_ หรือ _if RAG_FAIL_)
    - **วิธีดำเนินการ (How):** (sync / async / parallel)
- **Modular Reasoning:** Execution Graph ถูกออกแบบให้รองรับรูปแบบการทำงานที่ซับซ้อน เช่น **Branch Execution Graph** (สำหรับตัดสินใจแบบมีเงื่อนไข) และ **Multi-branch Parallel Execution Graph** (สำหรับการประมวลผลพร้อมกัน เช่น งาน L0–L5 Sync)
- **การตัดสินใจเชิงตรรกะ:** Flow Control ใช้โหนด **FLOW_DECISION** เพื่อตัดสินใจว่าเส้นทางควรไปสู่ขั้นตอนใดต่อไป (เช่น ไป RAG หรือไป Agent โดยตรง) นอกจากนี้ยังใช้ **ROUTER_SELECT_MODEL** เพื่อทำการตัดสินใจเลือกโมเดล (Routing) ภายใต้เงื่อนไขของงานและบริบท

### 4. Multi-Node Agent Execution

สถาปัตยกรรมของ Agent Engine สนับสนุนรูปแบบ **Multi-Agent** หรือ **Hierarchical Agent Model** โดย Execution Graph ทำหน้าที่เป็นเครื่องมือหลักในการประสานงานระหว่าง Agent หลายตัว

- **การแยก Agent:** Agent Engine สามารถสร้าง Agent เฉพาะทาง (เช่น Analyst Agent, Research Agent, Synthesis Agent, Validation Agent) ที่แต่ละตัวถูกแมปเข้ากับโหนดที่แตกต่างกันในกราฟ
- **การควบคุมการวนซ้ำ:** FCE ควบคุมการวนซ้ำ (loop) ของ Agent โดยกำหนด **Step Limit** และใช้กลไกตรวจจับการวนซ้ำ หากพบการวนซ้ำที่ไม่ถูกต้อง Flow Control จะสั่งหยุด (abort) เพื่อป้องกันข้อผิดพลาด
- **การสื่อสาร:** การสื่อสารระหว่าง Agent และ Engine อื่น ๆ เกิดขึ้นผ่าน **Event Bus** โดยมี Flow Control เป็นผู้ควบคุมการไหลของ Event เพื่อรักษาลำดับ (ordering) และความถูกต้องของเวอร์ชัน (version safety)

สถาปัตยกรรมนี้ทำให้มั่นใจว่างาน LLM ที่ซับซ้อนจะไม่ทำงานแบบไร้ทิศทาง (random) แต่จะถูกควบคุมอย่างเข้มงวดตาม **Execution Graph** ที่ถูกออกแบบไว้ล่วงหน้า

### อุปมาอุปไมย:

Execution Graph เปรียบเสมือน **ผังวงจรไฟฟ้า** ที่กำหนดเส้นทางตายตัว **Flow Control Engine** คือ **ชิปประมวลผล (CPU)** ที่คอยสั่งการเปิดปิดสวิตช์ในวงจรตามเงื่อนไข (Conditional Routing) โหนดต่าง ๆ (Nodes) คือ **ส่วนประกอบอิเล็กทรอนิกส์** (เช่น ตัวต้านทาน, ตัวเก็บประจุ, LLM API) ที่มีหน้าที่เฉพาะตัว และทั้งหมดถูกประกอบเข้าด้วยกันอย่างเป็นระบบเพื่อรับประกันผลลัพธ์ที่ถูกต้องและเสถียร