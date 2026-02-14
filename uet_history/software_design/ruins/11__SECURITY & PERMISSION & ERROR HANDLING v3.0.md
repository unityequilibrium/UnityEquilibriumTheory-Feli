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