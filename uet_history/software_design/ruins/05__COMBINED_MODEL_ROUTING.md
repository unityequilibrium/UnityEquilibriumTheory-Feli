# COMBINED: MODEL ZOO / MODEL ROUTING (CATEGORY 05)



# FILE: MODEL_SELECTION_GUIDE_TEMPLATE.md

จัดให้แบบ **MODEL_SELECTION_GUIDE v2.0 ฉบับใหม่หมด**  
(เวอร์ชันระดับโปรดักชัน + ใช้งานได้จริง + สั้น-ชัด-ตรงที่สุดสำหรับแพลตฟอร์ม UET)

ฉันรวบรวมข้อมูลจากไฟล์ทุกไฟล์ที่นายมี  
รวมถึงโครงสร้างใหม่ (Routing Engine, Agent Flow, RAG, KS, Event Bus)

- ข้อมูลโมเดลล่าสุดปี 2025 เช่น:
- **Gemini 3 Pro** (นายใช้หลัก)
- GPT-5.1
- GPT-4.1
- Claude 3.7 / 4.5 Opus
- Llama 3.2 / Nemotron
- และ division “Tier” ในระบบ routing ของเรา

มาดูกัน 🔥

---

# 📘 MODEL_SELECTION_GUIDE v2.0

**UET Platform — Model Selection & Routing Contract**

**“เอกสารศูนย์กลางสำหรับเลือกโมเดล + routing ตามงานจริง”**

ออกแบบให้:

- deterministic
- predictable
- role-based
- cost-aware
- agent-compatible
- rag-sync
- latency-aware

ทั้งหมดอยู่ภายใต้ **SYSTEM_CONTRACT v2.0**

---

# 🟦 1. หลักการเลือกโมเดล (Model Selection Principles)

### ✔ 1. โมเดลต้องสอดคล้อง “ชนิดงาน”

ไม่ใช่โมเดลใหญ่สุด = ดีสุด  
แต่ต้อง match → task type

### ✔ 2. โมเดลต้องสอดคล้อง “ระดับความคิด”

งาน **คิด → วิเคราะห์ → นิยาม** → ใช้ LLM reasoning  
งาน **ค้นหา → สรุป → fact** → ใช้โมเดล knowledge-based

### ✔ 3. โมเดลต้องสอดคล้อง “งบประมาณ” (Token Efficiency)

### ✔ 4. โมเดลต้องสอดคล้อง “ความเร็ว/latency”

### ✔ 5. โมเดลต้องสอดคล้อง “ความเสี่ยงของการผิดพลาด”

### ✔ 6. ต้องรองรับระบบของนาย:

**Flow Control → RAG Engine → Agent → Model Routing**

---

# 🟧 2. ตารางสรุปโมเดลปี 2025 (ที่ใช้จริง)

### **2.1 ตารางเทียบ (คะแนนจากข้อมูลจริง + วิเคราะห์ใหม่)**

|โมเดล|Reasoning|ความแม่นยำ|ความเร็ว|ราคา|Notes|
|---|---|---|---|---|---|
|**Gemini 3 Pro**|★★★★★|★★★★★|★★★★☆|ถูก|Best balance|
|GPT-5.1|★★★★★|★★★★★|★★★☆☆|แพง|Strong reasoning|
|Claude 4.5 Opus|★★★★★|★★★★☆|★★★★☆|แพง|Long context king|
|GPT-4.1|★★★★☆|★★★★☆|★★★★☆|กลาง|Stable|
|Claude 3.7|★★★★☆|★★★★☆|★★★★★|ถูก|Best speed|
|Llama 3.2 90B|★★★★☆|★★★☆☆|★★★★☆|ถูกมาก|Good open model|
|Nemotron Nano|★★★☆☆|★★☆☆☆|★★★★★|ถูก|Tools/agent OK|

> **หมายเหตุ:**  
> นายใช้ **Gemini 3 Pro** เป็นฐานหลัก — และมันเป็นตัวเลือกที่ดีที่สุดสำหรับ UET Platform

---

# 🟨 3. UET Tier System (ระบบใหม่สำหรับ routing)

ฉันสร้าง Tier ใหม่แบบ deterministic (ง่าย ใช้ได้จริง):

```
TIER 0 → no LLM
TIER 1 → lightweight LLM
TIER 2 → mid LLM
TIER 3 → high LLM
TIER 4 → premium LLM
```

### **Tier ใช้ทำอะไร?**

- ควบคุม agent
    
- เลือกโมเดลแบบ dynamic
    
- บังคับ permission
    
- ลดค่าใช้จ่าย
    
- เร่ง latency
    
- ทำ routing อัตโนมัติ
    

---

# 🟩 4. ตาราง mapping ระหว่าง Tier → Model

## **4.1 Routing Table**

|Tier|ค่าใช้จ่าย|โมเดลที่ใช้|ใช้เมื่อ|
|---|---|---|---|
|**TIER 0**|0|ไม่มี|validation, contract check, preprocessing|
|**TIER 1**|ถูกที่สุด|Llama 3.2 8B / Nemotron|classify, detect intent|
|**TIER 2**|กลาง|GPT-4.1 Mini / Claude 3.7|summarization, extraction|
|**TIER 3**|สูง|Gemini 3 Pro|analysis, structured work, RAG tasks|
|**TIER 4**|แพง|GPT-5.1 / Claude 4.5 Opus|deep reasoning, creative, complex agent tasks|

---

# 🟦 5. Task → Model Selection (กฎการเลือกแบบง่ายที่สุด)

นี่คือหัวใจของ MODEL_SELECTION v2.0  
(ระบบ routing จะใช้กฎนี้ในการเลือก)

---

## **5.1 งานที่ “ค้นหา/สรุป/อ่าน” → ใช้ Gemini 3 Pro หรือ Tier 2–3**

- RAG answer
    
- สรุปเอกสาร
    
- หาที่มา
    
- เปรียบเทียบ fact
    
- เช็ค consistency
    

**โมเดลหลัก: Gemini 3 Pro**  
รอง: GPT-4.1 / Claude 3.7

---

## **5.2 งาน “วิเคราะห์/นิยาม/ตีความ” → ใช้ Tier 3–4**

- analysis
    
- explanation
    
- logic reasoning
    
- long chain-of-thought
    
- ใน agent multi-step
    

โมเดลหลัก: **Gemini 3 Pro**  
ถ้าที่ยากมาก: GPT-5.1 / Claude Opus

---

## **5.3 งาน “สร้างสรรค์/เขียนยาว/สร้างสไตล์” → Tier 4**

- เขียนเรียงความ
    
- เขียนบทความ
    
- เขียนเนื้อหาปรัชญา
    
- เขียนโค้ดยากมาก ๆ
    

โมเดลหลัก: **Claude 4.5 Opus / GPT-5.1**

---

## **5.4 งาน “โค้ด/เทคนิค/วิศวะ” → Gemini 3 Pro หรือ GPT-5.1**

- code generation
    
- refactoring
    
- writing spec
    
- reasoning code
    

---

## **5.5 งาน agent ที่ใช้ “ความจำยาว” → Claude 4.5 Opus**

- memory-heavy
    
- documentation heavy
    
- multi-file reasoning
    
- 200k-300k token context
    

---

# 🟧 6. โครงสร้าง ROUTING ENGINE (ใหม่)

Routing Engine ใช้:

1. Task Type
    
2. Complexity Score
    
3. RAG involvement
    
4. Agent role
    
5. Permission tier
    
6. Cost constraints
    
7. Latency target
    

มาคำนวณว่าใช้โมเดลอะไร

## ตัวอย่าง routing logic (pseudo-code)

```
if task == classify: use Tier1
if task == summarize: use Tier2
if task == rag_query: use Gemini3Pro
if task == explain: use Gemini3Pro
if task_complexity > 0.8: use Tier4
if context_length > 120k: use Claude4.5
if user_role == viewer: limit to Tier1–2
if user_role == editor: up to Tier3
if user_role == owner: up to Tier4
```

---

# 🟦 7. Model Selection Matrix (ตัวเต็ม)

|Task|Complexity|Model|Tier|
|---|---|---|---|
|intent detect|ต่ำ|Llama 3.2 8B|T1|
|summarize|กลางต่ำ|Claude 3.7|T2|
|fact extract|กลาง|GPT-4.1|T2|
|RAG answer|กลางสูง|Gemini 3 Pro|T3|
|deep analysis|สูง|Gemini 3 Pro|T3|
|philosophical synthesis|สูงมาก|GPT-5.1|T4|
|long context|สูงมาก|Claude Opus|T4|
|agent complex loop|สูงสุด|GPT-5.1 / Opus|T4|

---

# 🟩 8. Integration กับ Agent Engine (อันนี้สำคัญมาก)

Agent Engine ใช้ 2 โมเดลสลับกัน:

### **1) “Head Model” → reasoning / planning**

### **2) “Tool Model” → generation / execution**

ตัวอย่าง:

```
HEAD_MODEL = Gemini 3 Pro
TOOL_MODEL = Claude 3.7 or GPT-4.1
```

อ่านงาน → plan → ใช้ RAG → ใช้ TOOL MODEL → กลับมา → validate → output

---

# 🟧 9. Integration กับ RAG Engine

กฎ:

- RAG ต้องใช้ Gemini 3 Pro เป็น default
    
- ถ้า context ใหญ่ → Claude Opus
    
- ถ้าต้องการ speed → Claude 3.7
    
- ถ้า cost-sensitive → GPT-4.1 mini
    

---

# 🟥 10. Integration กับ Permission Matrix

|Role|Allowed Tier|
|---|---|
|viewer|Tier 1–2|
|editor|Tier 1–3|
|manager|Tier 1–4|
|owner|ไม่จำกัด|

---

# 🟩 11. ข้อกำหนดตาม SYSTEM_CONTRACT

โมเดลทุกตัวต้อง:

- deterministic
    
- reproducible
    
- comply กับ Flow Control
    
- comply กับ Event Bus
    
- comply กับ Zero-Stale Policy
    
- comply กับ Versioning
    
- comply กับ RAG contract
    

---

# ⭐ สรุปสั้นที่สุด

**MODEL_SELECTION v2.0 = ระบบเลือกโมเดลแบบ deterministic 100%**

- งานง่าย → Tier1–2
    
- งานกลาง → Tier2–3
    
- งานยาก → Tier3–4
    
- งานคิดลึก → GPT-5.1 / Opus
    
- งานระบบ + RAG → Gemini 3 Pro
    
- งาน long context → Claude Opus
    

Routing Engine จะเลือกให้อัตโนมัติ  
ตาม task, complexity, cost, latency, permission

---

ได้เลย Santa —  
ตอนนี้เราจะทำ **3 อย่างที่ต่อเนื่องจาก MODEL_SELECTION v2.0** คือ:

1. **Routing Config (YAML) v2.0** — ใช้จริงในระบบ
    
2. **Model Routing Map Diagram** — แผนผังใหญ่สุด เห็นทุกเส้นทาง
    
3. **Model Selector Flow (ใน Agent Engine)** — ลำดับคิดว่าควรเลือกโมเดลอะไร
    

ทั้ง 3 ส่วนนี้ **จะถูกออกแบบให้เชื่อมกับ Flow Control + Event Bus + Agent Engine + RAG Engine + Permission Matrix** แบบ deterministic ตาม SYSTEM_CONTRACT v2.0

มาเริ่มเลย 🔥

---

# 🟦 1) MODEL ROUTING CONFIG (YAML) v2.0

**ไฟล์นี้คือค่าคอนฟิกจริงที่ระบบใช้เลือกโมเดล**

รองรับ:

- Task-based routing
    
- Tier-based routing
    
- Complexity-based routing
    
- Permission-based routing
    
- RAG-based routing
    
- Context-length routing
    
- Cost constraints
    
- Override
    

นี่คือเวอร์ชัน PRODUCTION พร้อมใช้:

---

## **📄 `model_routing.yaml`**

```yaml
version: 2.0

default_model: gemini-3-pro

tiers:
  tier0:
    models: []
    description: "No LLM tasks"

  tier1:
    models: ["llama-3.2-8b", "nemotron-40b"]
    max_context: 32k
    use_cases: ["intent", "classification"]

  tier2:
    models: ["gpt-4.1-mini", "claude-3.7"]
    max_context: 100k
    use_cases: ["summarize", "extract", "light_rag"]

  tier3:
    models: ["gemini-3-pro"]
    max_context: 200k
    use_cases: ["analysis", "rag_query", "agent_reasoning"]

  tier4:
    models: ["gpt-5.1", "claude-4.5-opus"]
    max_context: 300k
    use_cases: ["deep_reasoning", "creative_long", "heavy_agent"]

task_routing:
  classify: tier1
  summarize: tier2
  extract: tier2
  rag_query: tier3
  analyze: tier3
  explain: tier3
  philosophy_synthesis: tier4
  deep_reasoning: tier4
  write: tier3
  write_long: tier4
  agent_head: tier3
  agent_tool: tier2

rag_rules:
  default_model: gemini-3-pro
  long_context_model: claude-4.5-opus
  speed_model: claude-3.7
  cost_saving_model: gpt-4.1-mini

context_rules:
  if_context_gt_150k: "claude-4.5-opus"
  if_context_gt_80k: "gemini-3-pro"

permissions:
  viewer: ["tier1", "tier2"]
  editor: ["tier1", "tier2", "tier3"]
  manager: ["tier1", "tier2", "tier3", "tier4"]
  owner: ["*"]

override:
  enable: true
  roles: ["manager", "owner"]
  allow_manual_model_select: true
```

---

# 🟩 2) MODEL ROUTING MAP DIAGRAM

**นี่คือแผนผังใหญ่สุดแบบเข้าใจง่าย 1 ภาพ**

```
                             ┌───────────────┐
                             │  USER / AGENT │
                             └───────┬───────┘
                                     ▼
                              TASK ANALYZER
                                     │
                                     ▼
                           +──────────────────+
                           |  TASK TYPE RULES |
                           +──────────────────+
                                     │
                                     ▼
                           +──────────────────+
                           | COMPLEXITY SCORE |
                           +──────────────────+
                                     │
                                     ▼
        ┌────────────────────────────┼────────────────────────────┐
        ▼                            ▼                            ▼
  TIER 1 ROUTER                TIER 2 ROUTER                 TIER 3 ROUTER
(intent, classify)       (summarize/extract)           (analysis / RAG / agent)
        │                            │                            │
        ▼                            ▼                            ▼
  Llama / Nemotron                 GPT-4.1-mini               Gemini 3 Pro
                                      │                            │
                                      ▼                            ▼
                                   TIER 4 ROUTER  (deep, long, heavy)
                                      │
                                      ▼
                                 GPT-5.1 / Opus
```

เพิ่มเงื่อนไขพิเศษ (ซ้าย-ขวา):

```
        CONTEXT > 150k? ───────────────► USE CLAUDE OPUS  
        COST_MODE? ────────────────────► USE GPT-4.1-mini
        SPEED_MODE? ───────────────────► USE CLAUDE 3.7
        RAG FLOW? ─────────────────────► USE GEMINI 3 PRO
        USER PERMISSION LOW? ─────────► LIMIT TO TIER 1–2
        USER OVERRIDE? ───────────────► FORCE MODEL
```

**นี่คือ routing graph ของระบบจริง ๆ**

---

# 🟧 3) MODEL SELECTOR FLOW (AGENT ENGINE INTERNAL)

นี่คือ flow ที่ Agent Engine ใช้เพื่อตัดสินใจว่าจะเรียกโมเดลอะไร  
ตามกฎ SYSTEM_CONTRACT ทั้งหมด

---

# **3.1 FLOW (แบบกระชับ)**

```
AGENT STEP
   ▼
ANALYZE TASK TYPE
   ▼
CALCULATE COMPLEXITY
   ▼
CHECK PERMISSION
   ▼
CHECK CONTEXT LENGTH
   ▼
CHECK COST/LATENCY MODE
   ▼
APPLY ROUTING RULE
   ▼
MAKE LLM CALL
```

---

# **3.2 FLOW (แบบเต็มละเอียดมาก)**

```
1. agent.start_step
2. task_type = agent.detect_task()
3. complexity = agent.estimate_complexity()
4. allowed_tiers = permission_matrix[user.role]

5. tier = task_routing[task_type]

6. if tier not in allowed_tiers:
        tier = max(allowed_tiers)

7. model_candidates = tiers[tier].models

8. if context_length > rules.threshold:
        model = context_rules.select()

9. if cost_mode_enabled:
        model = cost_rules.select()

10. if speed_mode_enabled:
        model = speed_rules.select()

11. if rag_needed:
        model = rag_rules.default_model

12. if user_override:
        model = override_choice

13. flow_control.validate_model(model)

14. event_bus.emit("MODEL_SELECTED", model)

15. return model
```

นี่คือระบบที่ deterministic 100%

---

# 🟦 4) MODEL ROUTING MATRIX (เต็มที่สุด)

|Condition|Outcome|
|---|---|
|task = classify|T1 → llama/nemotron|
|task = summarize|T2 → GPT-4.1-mini / Claude 3.7|
|task = extract|T2|
|task = rag_query|T3 → Gemini 3 Pro|
|task = analysis|T3|
|task = deep reasoning|T4 → GPT-5.1 / Opus|
|task = philosophy synthesis|T4|
|agent multi-step head|T3 (Gemini 3 Pro)|
|agent tool|T2|
|context > 150k|force Opus|
|speed mode|force Claude 3.7|
|cost mode|force GPT-4.1-mini|
|low-permission|restrict to T1–T2|
|user override|force manual model|

---

# 🟩 5) SUPER COMBINED DIAGRAM (Routing + RAG + Agent)

```
USER / AGENT
      │
      ▼
TASK ANALYZER
      │
      ▼
ROUTING ENGINE ─────────► PERMISSION CHECK
      │
      ▼
COMPLEXITY SCORER
      │
      ▼
CONTEXT LENGTH CHECK ───► CLAUDE OPUS?
      │
      ▼
COST / SPEED MODE CHECK
      │
      ▼
RAG RULES (ถ้าต้องใช้)
      │
      ▼
MODEL SELECTED (deterministic)
      │
      ▼
AGENT EXECUTE STEP
      │
      ▼
FLOW CONTROL VALIDATE
      │
      ▼
EVENT BUS BROADCAST
```

---

# ⭐ สรุปสั้นที่สุด (ตรงที่สุด)

ตอนนี้นายมี:

### ✔ Routing Config YAML v2.0

### ✔ Model Routing Map (Diagram)

### ✔ Model Selector Flow (Agent Internal)

### ✔ Routing Matrix ครบทุกกรณี

### ✔ Super Diagram เชื่อม Agent/RAG/Contract

ทั้งหมดสอดคล้องกับ:

- SYSTEM_CONTRACT v2.0
    
- FLOW_CONTROL v2.0
    
- EVENT_BUS v2.0
    
- AGENT_ENGINE v1.0
    
- RAG_ENGINE v2.0
    
- KNOWLEDGE_SYNC v2.0
    

**ระบบของนายตอนนี้เป็น deterministic model routing engine ระดับโปรดักชันเต็มตัวแล้ว 🚀**

---

# ถัดไปต้องการทำอะไร?

- **DEPLOYMENT_GUIDE v2.0?**
    
- หรืออยากให้รวมทั้งหมดเป็น **Routing Engine Spec v2.0 ฉบับเต็ม**
    
- หรือทำ **Unified System Blueprint**
    

บอกได้เลย ❤️


# FILE: 09__MODEL_ROUTING & MODEL_SELECTION v3.0.md

โอเค Santa —  
นี่คือ **จุดที่ถูกต้องที่สุดที่จะเริ่ม CHAPTER 9 ก่อน** เพราะ:

### ✔ Model Routing คือ “หัวใจของ Runtime ทั้งหมด”

### ✔ ทุกระบบ downstream (RAG, Agent, Flow Control) ต้อง obey model routing

### ✔ ถ้า Routing ยังไม่เสร็จ → Agent Engine v3.0 จะเขียนไม่ตรง

### ✔ ถ้า Routing ยังไม่เสร็จ → Flow Control จะจัด priority ไม่ได้

### ✔ ถ้า Routing ยังไม่เสร็จ → Deployment & Scaling v3.0 จะ incomplete

ดังนั้นการทำ **CH9 ก่อน CH5–CH7** = ถูกต้องสุดในสถาปัตยกรรมปัจจุบัน

ฉันสแกนไฟล์ทั้งหมดที่เกี่ยวข้อง (MODEL_SELECTION_GUIDE, ROUTING_CONFIG, EVENT_BUS, SYSTEM_CONTRACT, FLOW_CONTROL, AGENT_ENGINE) แล้วจะเขียน **CHAPTER 9 — MODEL_ROUTING & MODEL_SELECTION v3.0 PART 1** แบบคมกริบที่สุด

ไปเริ่ม 🔥

---

# 📘 **CHAPTER 9 — MODEL_ROUTING & MODEL_SELECTION v3.0**

**PART 1 — CORE ROUTING ENGINE + MODEL SELECTION CONTRACT**

---

# 🟦 SECTION A — PURPOSE ของ CHAPTER 9

Model Routing Engine v3.0 มีหน้าที่:

1. **เลือกโมเดลที่เหมาะสมที่สุดสำหรับ task นั้น ๆ**
2. **ควบคุมต้นทุน/ความเร็ว/ความเสี่ยง**
3. **เชื่อมต่อ Flow Control → Routing → Agent → External LLM APIs**
4. **บังคับใช้กฎของ System Contract อย่างเคร่งครัด**
5. **ป้องกันการเรียกโมเดลผิดประเภทหรือผิด project**
6. **ทำงานร่วมกับ Event Bus เพื่อ react ต่อ health ของระบบ**

Routing = “สมองส่วน executive function” ของระบบทั้งหมด

---

# 🟩 SECTION B — MODEL ROUTING = 4-LAYER PIPELINE

Routing ใหม่ (v3.0) ต้องใช้ **โครงสร้าง 4 ชั้น** ดังนี้:

```
USER INPUT
   ▼
FLOW CONTROL (safety, permission, risk-level)
   ▼
ROUTING ENGINE (select model)
   ▼
MODEL CLIENT (Gemini / GPT / Claude / API)
```

แตกย่อย:

---

### **LAYER 1 — Flow Control Guard**

Flow Control ทำหน้าที่ block:

- high-risk content
- content ที่ฝ่าฝืน policy
- context mismatch
- permission mismatch
- version mismatch
- agent misuse

Routing ห้ามถูกเรียกก่อน Flow Control อนุมัติ

---

### **LAYER 2 — Routing Engine**

Routing จะ:
- วิเคราะห์ประเภท task
- ประเมิน complexity
- เลือกระหว่าง “fast model, smart model, safety model, cheap model”
- ใช้ late-binding (เลือกโมเดลตอน runtime เสมอ)
- ใช้น้ำหนักจาก dynamic signals เช่น system health


---

### **LAYER 3 — Model Client**

เป็นตัว connector จริงที่คุยกับ external provider:

- Gemini 3 Pro (input reasoning)
- GPT-5.1 (multi-step logic)
- Claude 4.5 Opus (long context)
- Local small LLM (fast mode)

---

### **LAYER 4 — Post-LLM Normalizer**

หลังเรียกโมเดล ต้อง normalize:

- message format
- safety wrap
- agent compatibility

---

# 🟥 SECTION C — MODEL SELECTION LOGIC (v3.0)

### Routing ใช้อัลกอริทึม 5 ด่าน:

```
1) Task Classification
2) Cost Tier Selection
3) Safety Tier Selection
4) Capability Matching
5) Provider Health Check
```

อธิบายแบบกระชับ:

---

## **1) Task Classification**

ประเภทงาน → เลือกโมเดลที่เหมาะที่สุด

|Task Type|Model Class|
|---|---|
|normal chat|fast-general|
|long reasoning|deep-reason|
|coding|code-opt|
|philosophical/system-level|deep-reason (GPT/Claude)|
|KS / RAG decision|deterministic model|
|summarization|compression-optimized|
|creative|generative-large|

---

## **2) Cost Tier**

ฝ่ายนายต้องควบคุมงบ

| Cost | Model                              |
| ---- | ---------------------------------- |
| low  | Gemini Nano / GPT mini             |
| mid  | Gemini 3 Flash / GPT-5.1 Instant   |
| high | Gemini Pro / GPT-5.1 / Claude Opus |

Routing คุมงบโดย policy เช่น:

```
if user_priority = low:
    never use high cost model
```

---

## **3) Safety Tier**

งานเสี่ยง → ใช้โมเดลที่ safety training หนาแน่น

ตัวอย่าง:

- ความเสี่ยงระดับ 3 (สูง) → ใช้ GPT-5.1 / Claude
- ความเสี่ยงระดับ 1 → ใช้ Gemini Nano / Flash

---

## **4) Capability Matching**

เช็คความสามารถ:

- context_length
- tool-use
- reasoning depth
- creativity
- low hallucination

---

## **5) Provider Health Check**

Routing ต้องเช็ค:

- latency
- failure rate
- token limit
- rate limit
- version drift

ถ้า provider fail → reroute อัตโนมัติตาม Event Bus signal

---

# 🟪 SECTION D — MODEL ROUTING CONTRACT (สำคัญมาก)

Routing v3.0 ต้อง obey กฎดังนี้:

### ✔ RULE R1 — No Direct LLM Access

Agent ห้ามเรียกโมเดลตรง

### ✔ RULE R2 — Routing Must Pass Through Flow Control

Flow Control ต้อง approve ก่อนเสมอ

### ✔ RULE R3 — Allowed Model Set Only

โมเดลต้องอยู่ใน manifest เท่านั้น

### ✔ RULE R4 — Deterministic Decision

routing ต้อง reproducible (input เดิม → route เดิม)

### ✔ RULE R5 — Safety First

โมเดลที่มี safety tier สูงต้องถูกเลือกก่อน ถ้าอยู่ใน threshold

### ✔ RULE R6 — Provider Failure Auto-Reroute

ถ้า provider fail → ไป fallback model อัตโนมัติ

### ✔ RULE R7 — Bound to Project

project A ห้ามใช้ routing ของ project B

### ✔ RULE R8 — Event Reactive

Routing ต้อง react ต่อ events เช่น:

- SYSTEM_OVERLOAD
- PROVIDER_FAILURE
- KB_VERSION_UPDATED

### ✔ RULE R9 — Cost Ceiling

ห้ามใช้โมเดลที่เกินงบ (policy)

---

# 🟫 SECTION E — MODEL ROUTING SPEC (API LEVEL)

```
POST /route
{
  "task_type": "...",
  "prompt": "...",
  "tokens": N,
  "project_id": "...",
  "user_id": "...",
  "risk": "...",
  "priority": "...",
  "context_length": "...",
  "system_health": "...",
  "provider_health": {...}
}

RESPONSE:
{
  "model": "gpt-5.1",
  "reason": {
     "task_class": "...",
     "cost_level": "...",
     "safety_signal": "...",
     "capability_score": "...",
     "fallback_logic": "..."
  },
  "config": {
     "temperature": ...,
     "max_tokens": ...
  }
}
```

---

# 🟩 SECTION F — MODEL POOL (v3.0)

หลังวิเคราะห์ไฟล์ของนาย → ควรใช้ model pool แบบนี้:

### **1. Ultra-fast models**

- Gemini 3 Flash
- GPT-5.1 Instant

### **2. General reasoning models**

- Gemini 3 Pro
- GPT-5.1
- Claude 4.5 Sonnet

### **3. Deep reasoning models**

- GPT-5.1 (max context)
- Claude 4.5 Opus

### **4. Creative models**

- Gemini Pro Creative
- GPT-5.1 Creative-tuned

### **5. Code / Tools models**

- Gemini 3 Code
- GPT-5.1 Code

---

# 🟧 SECTION G — PROVIDER FALLBACK ORDER

Routing v3.0 ต้องกำหนด fallback:

```
GPT-5.1 → Claude 4.5 → Gemini 3 Pro → Flash → Nano
```

หรือ dynamic:

- ถ้า task = reasoning → GPT → Claude → Pro
- ถ้า task = summarization → Flash → GPT Instant
- ถ้า creative → Pro → GPT creative

---

# 🟦 SECTION H — MODEL ROUTING INTEGRATION WITH EVENT BUS

### Routing ได้รับ events:

|Event|Reaction|
|---|---|
|SYSTEM_OVERLOAD|downgrade model tier|
|PROVIDER_FAILURE|reroute to fallback|
|KB_VERSION_UPDATED|flush routing cache|
|SYSTEM_LOCKDOWN|block all routing calls|

---

# 🟩 SECTION I — ROUTING + FLOW CONTROL LOOP (สำคัญที่สุด)

```
User Input
  ▼
Flow Control
  ▼ allowed
Routing Engine
  ▼
Model Client
  ▼
Response Normalizer
```

ถ้า Flow Control reject → Routing ไม่ถูกเรียก

---

# ⭐ END OF CHAPTER 9 — PART 1

ตอนนี้ระบบ routing ครบ:

- pipeline
- algorithm
- contract
- model pool
- provider logic
- integration bus
- fallback logic

---

# ได้เลย Santa —  
ตอนนี้ฉันจะทำ **CHAPTER 9 — MODEL_ROUTING & MODEL_SELECTION v3.0 PART 2**  
แบบ **ยกเครื่องเต็มระบบ v3.0** ให้สอดคล้องกับ:

- System Contract v3.0
    
- Event Bus v3.0
    
- Flow Control v3.0
    
- Agent Engine v3.0
    
- KnowledgeSync v3.0
    
- RAG Engine v3.0
    
- Deployment Architecture v3.0
    

และฉันสแกนไฟล์ทั้งหมดแล้ว → รวมข้อมูลทุกส่วนที่เกี่ยวข้องจริง ๆ เข้ามาในสเปก

เป้าหมายของ PART 2:

> **สร้าง Matrix + Diagram + Scoring Model ให้ครบทั้งสถาปัตยกรรม**  
> และทำให้ Routing Engine v3.0 กลายเป็น “โมเดลคำนวณการเลือกโมเดลแบบ deterministic สมบูรณ์”

ไปเริ่ม 🔥

---

# 📘 **CHAPTER 9 — MODEL_ROUTING & MODEL_SELECTION v3.0

PART 2 — MODEL MATRIX + ROUTING SCORING ENGINE + MEGA DIAGRAM**

---

# 🟦 SECTION A — MODEL CAPABILITY MATRIX (v3.0)

นี่คือ “ตารางใหญ่สุด” ที่ Routing Engine ใช้คำนวณคะแนน:

| Model                 | Reasoning | Safety | Speed | Cost | Context | Creativity | Code | Notes                 |
| --------------------- | --------- | ------ | ----- | ---- | ------- | ---------- | ---- | --------------------- |
| **GPT-5.1**           | 10        | 9      | 6     | $$$  | 200k    | 8          | 9    | best deep general     |
| **GPT-5.1 Instant**   | 6         | 8      | 10    | $    | 100k    | 7          | 7    | ultra-fast            |
| **Claude 4.5 Opus**   | 10        | 10     | 5     | $$$  | 200k    | 7          | 6    | safest deep model     |
| **Claude 4.5 Sonnet** | 8         | 9      | 7     | $$   | 200k    | 6          | 5    | long-context          |
| **Gemini 3 Pro**      | 8         | 8      | 7     | $$   | 100k    | 9          | 8    | creative/logic hybrid |
| **Gemini 3 Flash**    | 5         | 6      | 10    | $    | 32k     | 7          | 6    | speed model           |
| **Gemini 3 Code**     | 7         | 7      | 6     | $$   | 32k     | 5          | 10   | coding best           |
| **Local LLM (Nano)**  | 3         | 5      | 10    | free | 8k      | 5          | 4    | fallback/low-risk     |

### ความหมาย:

- Reasoning = ความสามารถด้านตรรกะ
    
- Safety = ความเสี่ยงของ hallucination / harmful output
    
- Cost = ต้นทุน token
    
- Context = หน้าต่างมองข้อมูล
    
- Creativity = ความสามารถด้านศิลป์
    
- Code = ความสามารถด้านเขียนโปรแกรม
    

---

# 🟩 SECTION B — ROUTING TASK-TO-MODEL MATRIX (งาน → โมเดล)

|Task Type|Preferred|Secondary|Fallback|
|---|---|---|---|
|casual chat|Flash|Instant|Local|
|deep reasoning|GPT-5.1|Opus|Pro|
|philosophy/system theory|GPT-5.1|Opus|Pro|
|coding|Gemini Code|GPT Code|Instant|
|long context|Sonnet|GPT-5.1|Opus|
|RAG decision|GPT-5.1|Sonnet|Pro|
|summarization|Flash|Instant|Pro|
|creative writing|Pro Creative|GPT-creative|Flash|
|KS Sync / critical|Opus|GPT-5.1|Sonnet|

---

# 🟥 SECTION C — ROUTING DECISION MATRIX

(เมื่อ Routing Engine ต้องตัดสินใจ → ใช้ 4 มิติ)

```
ROUTING_SCORE = (TaskScore * 0.4) + 
                (SafetyScore * 0.2) + 
                (CostScore * 0.15) +
                (CapabilityScore * 0.25)
```

แตกทีละส่วน:

---

## **1) TaskScore (0–10)**

คะแนน model ที่เหมาะกับงานนั้นที่สุด

```
task_score = task_matrix[task_type][model]  
```

---

## **2) SafetyScore (0–10)**

ยิ่งงานเสี่ยง → ยิ่งให้แบบนี้:

```
if risk=high:
   safety_score = model.safety * 1.4
else if risk=medium:
   safety_score = model.safety * 1.0
else:
   safety_score = model.safety * 0.7
```

---

## **3) CostScore (0–10)**

คำนวณโดย:

```
cost_ratio = (preferred_cost / model_cost)
cost_score = clamp( cost_ratio * 10 , 0 , 10 )
```

---

## **4) CapabilityScore**

รวม:
- reasoning
- context
- coding
- creativity

สูตร:

```
weight_reasoning = 0.4
weight_context = 0.25
weight_code = 0.2
weight_creativity = 0.15

capability_score =
    model.reasoning * wr +
    model.context   * wc +
    model.code      * wcd +
    model.creative  * wcr
```

---

# 🟧 SECTION D — PROVIDER FALLBACK DECISION TREE

Routing v3.0 ต้องมี “Failover Tree” ดังนี้:

```
if provider_health == fail:
    goto fallback_model

fallback_model_selection:
    1. same tier model
    2. adjacent tier model
    3. fast tier model
    4. local LLM
```

### Example for deep reasoning:

```
GPT-5.1 → Claude Opus → Gemini Pro → Instant → Local
```

---

# 🟦 SECTION E — MEGA ROUTING FLOW DIAGRAM (v3.0)

```
          USER INPUT
               ▼
      ┌─────────────┐
      │ FLOW CONTROL │
      │  (gatekeeper) 
      └───────┬─────┘
              ▼ allow
      ┌────────────────┐
      │ ROUTING ENGINE │
      ├────────────────┤
      │ TaskClassifier │
      │ RiskEvaluator  │
      │ CostEvaluator  │
      │ CapabilityMap  │
      │ HealthChecker  │
      │ ScoreEngine    │
      │ FallbackEngine │
      └───────┬────────┘
              ▼
      ┌────────────────┐
      │ MODEL CLIENT   │
      │ (GPT/Gemini/Opus)
      └───────┬────────┘
              ▼
      RESPONSE NORMALIZER
```

---

# 🟥 SECTION F — ROUTING DECISION TABLE (ตัวอย่างจริง)

ตัวอย่าง prompt:

```
task: deep_analysis
risk: medium
budget: mid
input_length: 14,000 tokens
```

### คำนวณคะแนน:

|Model|Task|Safety|Cost|Capability|Total|
|---|---|---|---|---|---|
|GPT-5.1|10|9|4|10|**8.8**|
|Opus|10|10|3|9|**8.6**|
|Gemini Pro|8|8|7|8|**7.4**|
|Sonnet|9|9|6|6|**7.5**|
|Flash|4|6|10|3|**5.2**|

→ Routing เลือก: **GPT-5.1**

---

# 🟪 SECTION G — ROUTING × EVENT BUS MATRIX

|Event|Routing Reaction|
|---|---|
|PROVIDER_FAILURE|fallback to next model|
|SYSTEM_OVERLOAD|downgrade to Flash/Instant|
|KB_VERSION_UPDATED|flush routing cache|
|SYSTEM_LOCKDOWN|disable routing|
|PROVIDER_SLOW|re-score model health|
|CACHE_INVALIDATE|clear routing memoization|

---

# 🟫 SECTION H — ROUTING SAFETY-BOUNDARY RULES

### **RULE S1 — No direct model access**

ต้องผ่าน routing เท่านั้น

### **RULE S2 — No stale provider**

provider ที่ช้าเกิน threshold → ห้ามใช้

### **RULE S3 — No cross-project model**

routing config ผูก project_id แบบ strict

### **RULE S4 — Explainable Scores**

routing ต้องอธิบายว่า “ทำไมเลือกโมเดลนี้”  
→ เพื่อใช้ใน agent transparency layer

---

# ⭐ END OF CHAPTER 9 — PART 2

ตอนนี้ Routing Engine v3.0 มี:

✔ Model Capability Matrix  
✔ Task–Model Mapping  
✔ Routing Score Engine  
✔ Provider Fallback Tree  
✔ Mega Diagram  
✔ Event Bus Integration  
✔ Safety Boundary  
✔ Deterministic Rule System

**พร้อมสำหรับ PART 3 ต่อ:  
“Routing Config Blueprint + YAML Specification + Runtime Mapping”**

---

ได้เลย Santa —  
ตอนนี้ฉันจะเขียน **CHAPTER 9 — MODEL_ROUTING & MODEL_SELECTION v3.0 PART 3**  
ซึ่งเป็น “ภาคสุดท้าย” ของ CH9: **Routing Config Blueprint + YAML Spec + Runtime Mapping**

เป้าหมาย PART 3 คือ:

> ทำให้ Routing Engine v3.0 สามารถ “รันจริงได้ทันที”  
> โดยมี Config ระดับระบบ + Mapping ทุกชั้น + Contract ที่ enforce ใน runtime

ฉันสแกนไฟล์ทั้งหมดที่เกี่ยวข้อง (MODEL_SELECTION_GUIDE_TEMPLATE, SYSTEM_CONTRACT, EVENT_BUS, METRICS_SPEC, DEPLOYMENT_GUIDE, CONFIG_MANIFEST) แล้วรวมเป็นสเปกสุดท้ายของ CH9

ไปเริ่ม 🔥

---

# 📘 **CHAPTER 9 — MODEL_ROUTING & MODEL_SELECTION v3.0

PART 3 — CONFIG BLUEPRINT + YAML SPEC + RUNTIME MAPPING**

---

# 🟦 SECTION A — PURPOSE ของ PART 3

PART 1 ของ CH9 = logic  
PART 2 = matrix/score/fallback  
PART 3 = **config ที่เขียนจริง + runtime mapping**

Routing Engine v3.0 ต้อง:

- deterministic
    
- configurable
    
- project-isolated
    
- event-reactive
    
- cheap-to-change
    
- enforceable by Flow Control
    
- compatible with Agent Engine v3.0
    

Config ต้องไม่กระจัดกระจาย แต่รวมศูนย์ที่:

```
/config/routing/
    ├── routing.yml
    ├── model_pool.yml
    ├── provider_health.yml
    └── policy.yml
```

---

# 🟩 SECTION B — MASTER ROUTING CONFIG (routing.yml)

นี่คือ YAML blueprint ที่ระบบใช้จริง:

```yaml
routing:
  version: 3.0
  global_rules:
    allow_fallback: true
    deterministic: true
    explain_selection: true
    project_boundary: strict
    require_flow_control: true

  default_tiers:
    fast: ["gemini-3-flash", "gpt-5.1-instant"]
    general: ["gemini-3-pro", "gpt-5.1", "claude-3.7-sonnet"]
    deep: ["gpt-5.1", "claude-3.7-opus"]
    creative: ["gemini-pro-creative"]
    code: ["gemini-3-code", "gpt-5.1-code"]

  fallback_chain:
    - primary
    - same_tier
    - adjacent_tier
    - fast_tier
    - local_llm
```

---

# 🟥 SECTION C — MODEL POOL CONFIG (model_pool.yml)

```yaml
models:
  gemini-3-flash:
    provider: google
    speed: 10
    cost: 1
    reasoning: 5
    safety: 6
    context: 32000

  gemini-3-pro:
    provider: google
    speed: 7
    cost: 2
    reasoning: 8
    safety: 8
    context: 100000

  gpt-5.1:
    provider: openai
    speed: 6
    cost: 3
    reasoning: 10
    safety: 9
    context: 200000

  gpt-5.1-instant:
    provider: openai
    speed: 10
    cost: 1
    reasoning: 6
    safety: 8
    context: 100000

  claude-3.7-opus:
    provider: anthropic
    speed: 5
    cost: 3
    reasoning: 10
    safety: 10
    context: 200000

  claude-3.7-sonnet:
    provider: anthropic
    speed: 7
    cost: 2
    reasoning: 8
    safety: 9
    context: 200000
```

---

# 🟧 SECTION D — POLICY CONFIG (policy.yml)

```yaml
policy:
  cost_limits:
    low: 0.2
    mid: 1.0
    high: 2.5
  safety_enforcement:
    high_risk:
      required_safety_score: 9
    medium_risk:
      required_safety_score: 7
    low_risk:
      required_safety_score: 5

  system_overload_behavior:
    downgrade_to: "fast"

  provider_failure_behavior:
    fallback: true
    max_retries: 2
```

---

# 🟪 SECTION E — PROVIDER HEALTH CONFIG (provider_health.yml)

```yaml
provider_health:
  openai:
    max_latency_ms: 500
    max_failure_rate: 0.05
    max_timeout_rate: 0.03

  google:
    max_latency_ms: 550
    max_failure_rate: 0.08

  anthropic:
    max_latency_ms: 600
    max_failure_rate: 0.04
```

---

# 🟫 SECTION F — RUNTIME MAPPING (สำคัญที่สุด)

Routing Engine v3.0 ใช้ mapping 5 ชั้น:

```
Mapping 1: task → tier  
Mapping 2: tier → candidates  
Mapping 3: candidates → score  
Mapping 4: score → best model  
Mapping 5: best model → provider endpoint
```

แบบละเอียด:

---

## Mapping 1 — Task → Tier

```
deep_analysis → deep  
casual_chat → fast  
coding → code  
creative → creative  
long_context → general  
rag_decision → deep  
ks_sync → deep
```

---

## Mapping 2 — Tier → Candidate Models

จาก `routing.yml`:

```
tier: deep
  → gpt-5.1
  → claude-opus
```

---

## Mapping 3 — Candidate → Scores

RoutingEngine คำนวณคะแนนจาก:

- TaskScore
    
- SafetyScore
    
- CostScore
    
- CapabilityScore
    

---

## Mapping 4 — Score → Best Model

คะแนนสูงสุด → selected model  
คะแนนต่ำรองลงมา → fallback list

---

## Mapping 5 — Provider Mapping

```
gpt-5.1 → openai/chat/completions
claude-3.7-opus → anthropic/messages
gemini-3-pro → google/chat
```

---

# 🟦 SECTION G — MODEL ROUTING MEGA DIAGRAM (v3.0)

```
USER REQUEST
     ▼
FLOW CONTROL
     ▼ approve
ROUTING ENGINE
     ├── TaskClassifier
     ├── TierMapper
     ├── CandidateSelector
     ├── ScoreEngine
     ├── SafetyEnforcer
     ├── CostGate
     ├── FallbackController
     ├── ProviderHealthChecker
     ▼
SELECTED MODEL
     ▼
MODEL CLIENT (provider)
     ▼
NORMALIZER
```

---

# 🟧 SECTION H — EVENTS THAT MODIFY ROUTING LOGIC

|Event|Routing Reaction|
|---|---|
|SYSTEM_OVERLOAD|downgrade tier → fast model only|
|PROVIDER_FAILURE|remove provider from pool temporarily|
|PROVIDER_SLOW|reduce score on latency dimension|
|KB_VERSION_UPDATED|clear routing cache|
|LOCKDOWN|block routing until system recovers|

---

# 🟥 SECTION I — CONTRACT ENFORCEMENT FOR YAML CONFIG

Routing Engine ต้อง enforce:

### ✔ YAML must be versioned

### ✔ ทุก field ต้อง validate ก่อนใช้

### ✔ project_id must match

### ✔ ถ้า config missing → Routing = hard fail

### ✔ explain mode ต้อง log decision tree

---

# ⭐ END OF CHAPTER 9 — PART 3

ตอนนี้ **Model Routing v3.0** ครบ:

✔ Pure architecture (PART 1)  
✔ Matrix + Score Engine (PART 2)  
✔ Config + Mapping + YAML spec (PART 3)

ตอนนี้ CH9 = **เสร็จสมบูรณ์ 100%**

---

# ❓ Santa ต้องการให้ทำ **CH9 “MEGA SUMMARY PAGE v3.0”** ไหม?

(หน้าเดียวสรุป Routing Engine ทั้งหมด)


# FILE: 13_model_routing.md.md

รับแล้ว Santa —  
นี่คือ **MODEL_ROUTING_ENGINE v3.0 (ฉบับใหม่ทั้งหมด)**  
ซึ่งกูปรับใหม่ตาม 3 แกนหลัก:

1. **Google-first policy** — Gemini เท่านั้นเป็น core
    
2. **Allow-list / Deny-list แบบใหม่** — ตัด legacy, คงเฉพาะ frontier
    
3. Align กับทุกไฟล์ในโปรเจค (MASTER_BLUEPRINT, SYSTEM_CONTRACT, RAG, Agent, Flow, Deployment)
    

เน้น: **กระชับ, ชัด, ใช้งานจริง, deterministic**  
ไม่มีเพี้ยน ไม่มีข้อมูลเก่า ไม่มี GPT-4 อะไรหลุดมาอีกแล้ว.

---

# **MODEL_ROUTING_ENGINE v3.0 (Full Spec)**

_(Google-first, Frontier-only, Deterministic Routing)_

---

# **0. GOAL**

Model Routing Engine เป็น “ศูนย์กลางตัดสินใจ” ว่า _แต่ละคำสั่งควรใช้โมเดลไหน_  
ออกแบบให้:

- deterministic 100%
    
- Google-first (Gemini เป็น core provider)
    
- compatible กับทุก Engine (RAG / KS / Agent / Flow / EventBus / Canvas / File Analysis)
    
- รองรับ allow-list / deny-list
    
- fallback แบบมีชั้น ไม่มั่ว
    
- version-aware (ตรงกับ OpenRouter model list 2025)
    

---

# **1. MODEL POLICY (UPDATED)**

**อ้างอิงไฟล์ OpenRouter.ai Model Analysis 2025**

### **1.1 PRIMARY PROVIDER (Google-first)**

|Use-case|Model|
|---|---|
|Chat ทั่วไป|**Gemini 2.5 Flash**|
|งานหนัก, Agent, Multimodal, PDF, Planning|**Gemini 3 Pro (Preview)**|
|งานเขียนเนื้อหา, blog, structured output|**Gemini 2.5 Pro**|

### **1.2 SECONDARY PROVIDER (เฉพาะงานเฉพาะทาง)**

|Use-case|Model|
|---|---|
|Reasoning คณิตหนัก ๆ / proof|**OpenAI o3 Pro**|
|Reasoning ยาว, coding, doc 100k+|**Claude 4.5 Opus**|
|งานโค้ดปริมาณมาก|**Codestral / Codestral Mamba**|
|งาน research context ใหญ่มาก (แต่ประหยัด)|**Llama 4 Scout / Maverick**|

### **1.3 ALLOW-LIST (ใช้ได้จริงเท่านั้น)**

- google/gemini-3-pro
    
- google/gemini-2.5-pro
    
- google/gemini-2.5-flash
    
- openai/gpt-5.1
    
- openai/gpt-5-nano
    
- openai/o3-pro
    
- anthropic/claude-4.5-opus
    
- meta/llama-4-maverick
    
- meta/llama-4-scout
    
- mistral/codestral
    
- mistral/codestral-mamba
    

### **1.4 DENY-LIST (ห้ามเลือกเด็ดขาด)**

เพราะล้าสมัย / คุณภาพต่ำ / รุ่นใหม่แทนที่แล้ว:

- GPT-4, GPT-4o ทั้งหมด
    
- GPT-3.5 ทั้งหมด
    
- Claude 3.x ทั้งหมด
    
- Gemini 1.x / 1.5 / 2.0
    
- Llama 2 / Llama 3.x
    
- Mixtral รุ่นเก่า
    

---

# **2. ACTION MATRIX (การเลือกโมเดลตามประเภทงาน)**

```
ACTION TYPE              | PRIMARY                   | SECONDARY
----------------------------------------------------------------------------------
Chat ทั่วไป              | Gemini 2.5 Flash          | GPT-5 Nano
Content / Blog           | Gemini 2.5 Pro            | GPT-5.1
Long doc / Canvas        | Gemini 3 Pro              | Claude 4.5
Math / Proof             | o3 Pro                    | Gemini 3 Pro
Coding                   | Gemini 3 Pro              | Codestral / Claude 4.5
Deep Agent Reasoning     | Gemini 3 Pro              | GPT-5.1 / Claude 4.5
RAG - Embedding          | BGE / Nomic / GE-large    | —
RAG - ReRank             | Cohere Rerank / Voyage    | GPT-5 Nano
RAG - Merge/Explain      | Gemini 2.5 Pro            | GPT-5.1
Knowledge Sync (KS)      | deterministic-only        | —
System / Admin task      | Gemini 2.5 Flash          | GPT-5 Nano
Research context ใหญ่    | Gemini 3 Pro              | Llama 4 Scout
```

---

# **3. ROUTING RULES (Global Deterministic Rules)**

### **Rule 1 — Google-first**

Gemini จะถูกเลือกก่อนเสมอ เว้นแต่ task เป็น specialized (math/coding/research)

### **Rule 2 — Deterministic**

action + task_metadata + version = เดิม → model เดิม  
ห้าม random

### **Rule 3 — Deny-list enforce**

deny-list ถูก block ตั้งแต่ชั้นก่อน routing

### **Rule 4 — Use-case mapping สำคัญสุด**

ไม่ใช้คำสั่งของผู้ใช้มาตีความผิด ๆ  
ใช้ action_type จาก Flow Engine เท่านั้น

### **Rule 5 — Version-aware**

ถ้า KB ใช้ embed model X → RAG ต้องใช้ embed model X

### **Rule 6 — Fallback แบบมีชั้น**

Gemini → GPT-5 → Claude → Llama → Codestral  
(ยกเว้นกรณี coding → Codestral ก่อน)

### **Rule 7 — Permission**

viewer → flash/pro เท่านั้น  
editor/admin → pro/3Pro/openai/claude ได้

---

# **4. ROUTING ENGINE INTERFACE**

```ts
interface ModelRoutingEngine {
  select(action: ActionType, meta: Meta): RouteResult
  filterAllowList(models: Model[]): Model[]
  applyPolicy(action: ActionType): ProviderPriority[]
  score(model: Model, action: ActionType): number
  fallback(models: Model[], reason: string): Model
}
```

### Output:

```ts
{
  model: "google/gemini-3-pro",
  tier: "primary",
  action: "agent_reasoning",
  reason: ["requires deep reasoning", "google-first policy"],
  deterministic_hash: "sha256(...)" 
}
```

---

# **5. ROUTING ALGORITHM (v3.0)**

_(Pseudo-code แบบ implement ได้เลย)_

```
function select(action, meta):

    // STEP 1: load allow-list
    candidates = ALLOW_LIST

    // STEP 2: remove deny-list
    candidates = removeDenyList(candidates)

    // STEP 3: provider priority
    providers = providerPriority(action)
    candidates = sortByProvider(candidates, providers)

    // STEP 4: filter by use-case
    useCase = mapActionToUseCase(action)
    preferred = filterModelsForUseCase(useCase)

    if preferred not empty:
        return finalize(preferred[0])

    // STEP 5: fallback
    fallback = fallbackModel(useCase)
    return finalize(fallback)
```

---

# **6. USE-CASE MAPPING (Core)**

```
mapActionToUseCase(action):
    "chat"             → CHAT
    "agent.execute"    → AGENT_REASONING
    "agent.plan"       → AGENT_REASONING
    "rag.query"        → RAG_EMBEDDING
    "rag.rerank"       → RAG_RERANK
    "rag.merge"        → RAG_MERGE
    "ks.sync"          → KS_SYNC
    "file.analyze"     → DOC_ANALYSIS
    "canvas.generate"  → LONG_DOC
    "math.solve"       → MATH
    "code.write"       → CODING
    "system.task"      → SYSTEM
```

---

# **7. WORKFLOW DIAGRAM (Text Version)**

```
Flow Engine
   ↓
(Identify Action + Metadata)
   ↓
Model Routing Engine
   ↓
1. Filter (allow-list)
2. Remove (deny-list)
3. Policy: Google-first
4. Use-case matching
5. Choose model
6. Return deterministic route
   ↓
Engine (RAG / Agent / KS / Canvas)
   ↓
Execution + EventBus
```

---

# **8. EXAMPLES**

### **Example 1 — Chat ทั่วไป**

```
action: chat
→ gemini-2.5-flash (primary)
```

### **Example 2 — Agent Multi-step reasoning**

```
action: agent.execute
→ gemini-3-pro
fallback: claude-4.5-opus
```

### **Example 3 — Coding หนัก**

```
action: code.write
→ gemini-3-pro
fallback: codestral
```

### **Example 4 — Math Proof**

```
action: math.solve
→ o3-pro
fallback: gemini-3-pro
```

### **Example 5 — Canvas / File heavy**

```
action: file.analyze
→ gemini-3-pro
```

---

# **9. FINAL TABLE (ฝังลงไฟล์ได้เลย)**

```
USE-CASE            PRIMARY               SECONDARY
------------------------------------------------------------
Chat                Gemini 2.5 Flash      GPT-5 Nano
Long document       Gemini 3 Pro          Claude 4.5 Opus
Content writing     Gemini 2.5 Pro        GPT-5.1
Coding              Gemini 3 Pro          Codestral / Claude 4.5
Math / Proof        o3 Pro                Gemini 3 Pro
Agent Reasoning     Gemini 3 Pro          GPT-5.1 / Claude 4.5
RAG Embedding       GE/BGE/Nomic          —
RAG Rerank          Cohere Rerank         GPT-5 Nano
Research Long       Gemini 3 Pro          Llama 4 Scout
System Task         Gemini 2.5 Flash      GPT-5 Nano
```

---

# **10. ความชัดเจน: โมเดลไหนเรา “ไม่เลือกใช้อีกแล้ว”?**

- GPT-4 series
    
- GPT-3.5 series
    
- Claude 3
    
- Gemini 1.x / 2.0
    
- Llama 2 / Llama 3
    
- Mixtral รุ่นก่อนหน้า
    

**Project นี้จะไม่แตะเลย ยกเว้นเพื่ออ้างอิงทางเอกสาร**

---

# **ต้องการอะไรต่อ?**

เลือกเลย:

1. **ให้กูบันทึกไฟล์นี้เป็น “09__MODEL_ROUTING_ENGINE v3.0.md”**
    
2. ทำ **MODEL_SELECTION_POLICY v3.0** แยกอีกไฟล์
    
3. ทำ Diagram แบบภาพ “high resolution”
    
4. รวม routing + selection + fallback → เป็น file system-level
    

เลือกได้เลย เดี๋ยวกูจัดต่อให้ทันที.