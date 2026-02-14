โอเค Santa —  
ฉันจะทำ **API_SPEC v2.0 (ยกเครื่องใหม่ทั้งฉบับ)** ให้แบบ _โคตรชัด, ครอบคลุมทั้งระบบ, กระชับสุด แต่ระดับ Production_

ฉันรวบรวมข้อมูลจากทุกไฟล์ของนาย (API_SPEC เก่า, SYSTEM_CONTRACT, AGENT_FLOW, DATA_SCHEMA, MODEL_ROUTING, KNOWLEDGE_SYNC, CACHE_STRATEGY, PERMISSION, EVENT_BUS ฯลฯ) แล้วออกแบบเป็น **Unified API Spec** ที่ใช้ได้จริงทันที.

---

# 📘 **API_SPEC.md (v2.0)**

**UET Platform — Unified API Specification**

---

# ⭐ 0. หลักการออกแบบ API เวอร์ชัน 2.0

- ใช้มาตรฐาน **RESTful + Event-driven**
    
- ทุก endpoint ต้อง:
    
    - เช็คสิทธิ์ตาม Permission Matrix
        
    - ส่ง error ตาม ERROR_SCHEMA v2.0
        
    - ส่งผลลัพธ์ตาม Response Schema
        
    - ไม่รั่วข้อมูลต่างโปรเจกต์
        
- รองรับระบบใหม่: Agent, Routing, KB Sync, RAG, Cache, Versioning
    

---

# ⭐ 1. API Structure (หมวดหมู่ API)

```
/auth
/projects
/files
/versions
/kb
/rag
/agent
/routing
/cache
/events
/metrics
/system
```

แต่ละหมวดจะมี endpoint ย่อย

---

# ⭐ 2. AUTH API

**เพื่อ login / token / role**

### **POST /auth/login**

```
body:
  email: string
  password: string
```

### **GET /auth/me**

→ คืนข้อมูล user, role

---

# ⭐ 3. PROJECT API

สำหรับจัดการโปรเจกต์

### **GET /projects**

→ รายการโปรเจกต์ที่ user เข้าถึงได้

### **POST /projects**

```
body:
  name: string
  description?: string
```

### **GET /projects/:id**

→ รายละเอียดโปรเจกต์

### **DELETE /projects/:id**

→ soft delete

---

# ⭐ 4. FILE API

สำหรับอัปโหลดไฟล์, ลบไฟล์, รายการไฟล์

### **GET /projects/:id/files**

→ รายการไฟล์ในโปรเจกต์

### **POST /projects/:id/files/upload**

```
form-data:
  file: binary
```

→ Trigger:

- parse
    
- version create
    
- chunk
    
- embed
    
- update KB registry
    

### **DELETE /files/:fileId**

→ soft delete + emit FILE_DELETED event

---

# ⭐ 5. FILE VERSION API

### **GET /files/:fileId/versions**

→ list เวอร์ชันไฟล์

### **GET /versions/:versionId**

→ เนื้อหาเวอร์ชันนั้น

### **POST /versions/:versionId/rollback**

→ revert file → create new version automatically

---

# ⭐ 6. KNOWLEDGE BASE (KB) API

สำหรับดู KB registry, sync, merge

### **GET /projects/:id/kb**

→ list files + version + chunks summary

### **POST /kb/sync**

```
body:
  fileId: string
  versionId: string
```

→ sync ไฟล์เข้าระบบ KB  
→ update registry  
→ trigger: KB_VERSION_UPDATED

### **GET /kb/:fileId/version/:versionId**

→ รายละเอียด KB entry

---

# ⭐ 7. RAG API

รองรับการค้นหาข้อมูลจาก vector DB

### **POST /rag/query**

```
body:
  projectId: string
  query: string
  topK?: number
```

response:

```
{
  chunks: [
    {
      id,
      text,
      score,
      metadata
    }
  ]
}
```

---

# ⭐ 8. AGENT API

หัวใจใหม่ของระบบ

### **POST /agent/run**

```
body:
  projectId: string
  input: string
  mode: "chat" | "studio" | "system"
  model?: string     // optional override
```

ทำงาน:

1. Load context
    
2. Model Routing
    
3. Execute
    
4. Validate
    
5. Save logs
    
6. Emit events
    

response:

```
{
  runId,
  output,
  model,
  tokens_in,
  tokens_out
}
```

### **GET /agent/run/:runId**

→ ดู history + step trace

---

# ⭐ 9. MODEL ROUTING API

### **POST /routing/choose**

```
body:
  taskType: string
  input: string
  userRole: string
```

response:

```
{
  model: "gemini-3-pro",
  tier: 3,
  reasoning: "chosen because..."
}
```

### **POST /routing/override**

```
body:
  runId?: string
  model: string
```

→ เฉพาะ Manager/Admin

---

# ⭐ 10. CACHE API

### **GET /cache/status**

→ cache hit/miss rate

### **POST /cache/clear**

```
body:
  type?: "rag" | "prompt" | "api" | "all"
```

---

# ⭐ 11. EVENT API

### **GET /events/project/:id**

→ list events (file updated, routing, model fail, cache invalidate, agent step)

### **GET /events/stream (SSE)**

→ real-time event stream (UI ใช้)

---

# ⭐ 12. METRICS API

### **GET /metrics/project/:id**

→ latency, rag_precision, cache_hit_rate

### **POST /metrics/report**

→ agent หรือระบบรายงานตัวเลขภายใน

---

# ⭐ 13. SYSTEM API

### **GET /system/health**

→ ตรวจสถานะ service ทั้งหมด

### **GET /system/config**

→ config manifest (read-only)

---

# ⭐ 14. Response Schema (สำคัญสุดใน API v2.0)

ทุก response ต้องอยู่ในรูปแบบนี้:

```
{
  success: boolean,
  data?: {},
  error?: {
    id: string,
    type: string,
    message: string,
    detail?: any,
    timestamp: datetime
  }
}
```

---

# ⭐ 15. Error Schema (ตาม ERROR_HANDLING v2.0)

```
MODEL_TIMEOUT
MODEL_OVERLOAD
RAG_FAIL
ROUTING_FAIL
PERMISSION_DENIED
CONTRACT_VIOLATION
VALIDATION_FAIL
```

---

# ⭐ 16. Permission Enforcement

API ต้อง enforce ตามตารางนี้:

|API|Viewer|Editor|Manager|Admin|
|---|---|---|---|---|
|Upload File|❌|✔|✔|✔|
|Delete File|❌|✔|✔|✔|
|KB Sync|❌|auto|✔|✔|
|Agent Run|✔ limited|✔ full|✔ override|✔ all|
|Routing Override|❌|❌|✔|✔|
|Metrics|read public|read project|read project|all|
|Event Log|self|project|project|all|

---

# ⭐ 17. API Flow Diagram (เข้าใจเร็วสุด)

```
[UI] → [API Layer] → [Flow Control Engine]
        │                  │
        ▼                  ▼
    Permission Check → Agent / RAG / KB / File Handler
        │                  │
        ▼                  ▼
   Error Engine ←── Event Bus
        │
        ▼
     Response
```

---

# ⭐ 18. API Lifecycle (ทุก Request ต้องผ่าน 7 ขั้นตอน)

```
1. Receive Request
2. Validate Schema
3. Authenticate User
4. Permission Check
5. Execute Module (File / RAG / Agent / KB / Routing)
6. Emit Event
7. Format Response + Log
```

---

# ⭐ 19. API Summary Table

_แบบอ่านเร็ว 10 วินาที_

|Module|Endpoint|Purpose|
|---|---|---|
|Auth|/auth/login|login|
|Project|/projects|manage project|
|File|/files/upload|upload, parse|
|FileVersion|/versions|version view, rollback|
|KB|/kb/sync|sync & registry|
|RAG|/rag/query|vector search|
|Agent|/agent/run|process prompt|
|Routing|/routing/choose|model routing|
|Cache|/cache/clear|invalidate|
|Event|/events/stream|real-time|
|Metrics|/metrics/report|performance tracking|
|System|/system/health|health check|

---

# 🎯 สรุปแบบเข้าใจง่ายที่สุด

API v2.0 คือ:

> “ระบบที่รองรับทุกฟีเจอร์ใหญ่: Agent, Routing, KB Sync, RAG, Cache, Permission, Event-Driven ทั้งหมดในสเปกเดียว”

มัน:

- ครอบคลุมของเก่า 100%
    
- แก้ข้อผิดของเดิม
    
- เพิ่มสิ่งสำคัญที่ระบบใหม่ต้องมี
    
- ทำให้ developer พัฒนาได้จริงทันที
    
- ไม่มีส่วนซ้ำ ไม่มีส่วนขาด
    

---

# ต้องการให้ฉันทำอะไรต่อ?

- EVENT_BUS v2.0
    
- FLOW_CONTROL v2.0
    
- AGENT_FLOW v2.0
    
- CACHE_STRATEGY v3.0
    
- KNOWLEDGE_SYNC v2.0
    
- หรือแปลง API ให้เป็น **OpenAPI (Swagger)**?
    

เลือกได้เลย ❤️