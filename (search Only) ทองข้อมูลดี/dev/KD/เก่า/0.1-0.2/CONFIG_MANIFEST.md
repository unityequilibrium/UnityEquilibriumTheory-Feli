จัดให้ Santa — นี่คือ **CONFIG_MANIFEST.md** เวอร์ชันที่ “ถูกต้องที่สุด + ครอบคลุมที่สุด + ใช้งานได้จริงในโปรเจกต์ใหญ่”  
ไม่เยิ่นเย้อ แต่ครบทุกหมวดที่แพลตฟอร์มระดับ UET ต้องมี  
และทั้งหมดนี้ออกแบบให้เข้ากันกับสถาปัตยกรรม _Scale-first fixed architecture_ ที่เราวางไว้ก่อนหน้า

---

# 🧩 **CONFIG_MANIFEST.md**

### _UET Platform — Centralized Configuration Specification_

> **ไฟล์นี้คือ “พจนานุกรมกลางของค่าคอนฟิกทั้งหมดในระบบ”  
> ทุกโมดูลต้องอ้างอิงจากไฟล์นี้เท่านั้น ห้าม hardcode ค่าใด ๆ ในโค้ดจริงเด็ดขาด**

หมดปัญหา
- โค้ดคนละไฟล์ แต่ค่าคนละอัน
- Agent แก้ไฟล์ผิด
- Dev งงว่า config ไหนควรแก้ตรงไหน
- เปลี่ยน environment แล้วพังทั้งระบบ

---

# 🟩 1) GLOBAL CONFIG

ค่าระดับ "Platform-wide"

```yaml
global:
  appName: "UET Platform"
  version: "0.2.0"
  defaultLocale: "th-TH"
  supportedLocales: ["th-TH", "en-US"]
  theme:
    default: "dark"
    allowSystemTheme: true
```

---

# 🟦 2) ENVIRONMENT CONFIG

ใช้ `.env.local`, `.env.production`, `.env.dev`

```yaml
env:
  NEXT_PUBLIC_ENV: "development" | "production" | "staging"
  NEXT_PUBLIC_API_URL: "<api-url>"
  NEXT_PUBLIC_WS_URL: "<websocket-url>"

  DATABASE_URL: "<postgresql-connection>"
  VECTOR_DB_URL: "<pgvector-connection>"
  STORAGE_BUCKET_URL: "<s3-or-supa-or-firebase>"
```

**สิ่งสำคัญ**
- ทุกอย่างต้องอ่านผ่าน “Config Loader”
- ห้ามเรียก `process.env` ตรง ๆ ใน component

---

# 🟥 3) AI / MODEL CONFIG

กำหนดโมเดลหลักที่แพลตฟอร์มใช้

```yaml
ai:
  defaultModel: "gemini-3.5-pro"
  allowedModels:
    - "gpt-5.1"
    - "claude-3.5-Opus"
    - "gemini-3.5-pro-preview"
  maxTokens:
    input: 128000
    output: 32000
  embeddings:
    model: "text-embedding-3-large"
    dimension: 3072
```

---

# 🟪 4) WORKSPACE (UI Layout) CONFIG

```yaml
workspace:
  layout:
    leftPanelWidth: 280
    rightPanelWidth: 360
    minPanelWidth: 200
  animations:
    enableTransitions: true
    transitionSpeed: 180ms
```

---

# 🟨 5) PROJECT CONFIG

ใช้ทุกครั้งที่สร้าง Project ใหม่

```yaml
project:
  defaultStructure:
    - "README.md"
    - "notes/"
    - "files/"
    - "references/"
  permissions:
    roles:
      - owner
      - editor
      - viewer
    defaultRole: "owner"
```

---

# 🟧 6) DATA STORAGE CONFIG

แนวทางจัดเก็บข้อมูล

```yaml
storage:
  markdown:
    extension: ".md"
    encoding: "utf-8"
  uploads:
    maxFileSizeMB: 50
    allowedTypes: ["pdf", "docx", "md", "txt", "jpg", "png"]
```

---

# 🟫 7) RAG / KNOWLEDGE CONFIG

(สำคัญมากสำหรับระบบ AI ทั้งแพลตฟอร์ม)

```yaml
rag:
  chunking:
    size: 1000
    overlap: 150
  indexing:
    vectorStore: "pgvector"
    maxFilesPerProject: 5000
  query:
    topK: 8
    maxContextTokens: 50000
```

---

# ⚫ 8) WALLET / KPI / FINANCE CONFIG

```yaml
finance:
  wallet:
    defaultCurrency: "THB"
    allowMultiCurrency: false
  kpi:
    defaultScale: 0-100
    scoringMethod: "weighted"
```

---

# 🟦 9) SECURITY CONFIG

```yaml
security:
  rateLimit:
    enabled: true
    windowMs: 60000
    maxRequests: 120
  auth:
    sessionExpirationHours: 72
    require2FA: false
```

---

# 🟫 10) LOGGING CONFIG

```yaml
logging:
  level:
    development: "debug"
    production: "warn"
  output:
    file: true
    console: true
```

---

# 🟣 11) FEATURE FLAGS (สำคัญโคตร ๆ)

เอาไว้เปิด/ปิดฟีเจอร์ระหว่างพัฒนา  
ไม่ต้องแก้โค้ด ไม่ต้องลบไฟล์ ไม่ต้องสร้าง branch ใหม่

```yaml
features:
  enableVectorSearch: true
  enableGraphView: true
  enableStudioAI: true
  enableAgentMode: false
  enableRealtimeChat: true
```

---

# 🟩 12) VERSIONING CONFIG

```yaml
versioning:
  blueprintVersion: "0.2"
  apiVersion: "v1"
  migration:
    autoApply: false
```

---

# 🧭 DIAGRAM — CONFIG LAYER MAP

แบบอ่านง่ายมากที่สุด

```
CONFIG_MANIFEST
│
├── GLOBAL
├── ENV
├── AI
├── WORKSPACE
├── PROJECT
├── STORAGE
├── RAG
├── FINANCE
├── SECURITY
├── LOGGING
└── FEATURES
```

หรือแบบเมทริกซ์

|Category|Purpose|Used By|
|---|---|---|
|GLOBAL|ค่าหลักแพลตฟอร์ม|ทุกโมดูล|
|ENV|backend/api connection|server|
|AI|โมเดล + token|chat/agent|
|WORKSPACE|layout|FE UI|
|PROJECT|โครงสร้างโปรเจกต์|Projects page|
|STORAGE|ไฟล์|Source Panel|
|RAG|AI memory|chat, KB|
|FINANCE|wallet/KPI|finance engine|
|SECURITY|auth/rate-limit|all|
|LOGGING|debug|dev tools|
|FEATURES|เปิด/ปิดฟีเจอร์|rollout|

---
# 🔥 สรุป

**CONFIG_MANIFEST = หัวใจควบคุมพฤติกรรมทั้งหมดของแพลตฟอร์ม UET**

- เปลี่ยน config = เปลี่ยนระบบทั้งแพลตฟอร์ม
- ทุกฟีเจอร์ AI, Chat, Project, Graph, Wallet คุมจากที่เดียว
- ช่วยให้ AI agent เข้ามาอ่าน แล้ว “เข้าใจระบบทันที”
- ช่วยให้ dev ทีมอื่นทำงานได้ไม่หลงทาง

---