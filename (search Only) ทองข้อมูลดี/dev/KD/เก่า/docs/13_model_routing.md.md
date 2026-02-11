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