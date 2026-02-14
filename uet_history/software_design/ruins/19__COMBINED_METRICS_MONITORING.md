# COMBINED: METRICS / MONITORING (CATEGORY 19)


# FILE: METRICS_SPEC.md

# 📊 METRICS_SPEC.md  
**UET Platform — Metrics, KPIs, and Analytics Contract**

ไฟล์นี้เป็นสัญญากลาง (contract) สำหรับ Agent และระบบทั้งหมด  
ว่าตัวเลขไหนอยู่ที่ไหน ทำไมมี และดึงมาใช้อย่างไร  
เพื่อรองรับการใช้งาน 2 กลุ่มใหญ่:

- 🔍 นักวิจัย / ผู้ใช้ไม่ปกติ (วิชาการ)
- 🧪 AutoPrompt / Agent (สร้างรายงาน + วิจัย + สถิติ + Simulation)

---

# 1) ประเภทของ Metrics ในระบบ

| Category | อธิบาย | ตัวอย่าง |
|--------|--------|---------|
| **Platform Metrics** | สถานะระบบบนสเกลใหญ่ | ผู้ใช้ทั้งหมด, active user, project count |
| **Workspace Metrics** | สถานะแต่ละ workspace | สมาชิก, จำนวนไฟล์, KB ขนาดเท่าไหร่ |
| **Project Metrics** | สุขภาพโปรเจกต์ | จำนวนโน้ต, tasks ที่เหลือ, progress |
| **Interaction Metrics** | การมีส่วนร่วม | views, votes, reactions |
| **Research Metrics** | ใช้ในการวิเคราะห์เชิงวิชาการ | citation count, similarity index |
| **Financial Metrics** | การเงิน/กระเป๋า KPI | KPI, balance, scorecard |
| **Agent Metrics** | การทำงานของ Agent | เวลา, token, success/fail rate |

---

# 2) ตารางหลักในฐานข้อมูล

## 2.1 Table: `project_stats`

| field | type | อธิบาย |
|------|------|---------|
| project_id | uuid | โปรเจกต์ไหน |
| note_count | int | จำนวนไฟล์ markdown |
| task_open | int | งานที่ยังไม่เสร็จ |
| progress_score | float | คะแนนความคืบหน้า |
| updated_at | timestamp | อัปเดตล่าสุด |

---

## 2.2 Table: `engagement_metrics`

| field | type | อธิบาย |
|------|------|---------|
| project_id | uuid | โปรเจกต์ไหน |
| views | int | เปิดอ่านกี่ครั้ง |
| votes_up | int | เห็นด้วย |
| votes_down | int | ไม่เห็นด้วย |
| comments | int | คอมเมนต์ทั้งหมด |

---

## 2.3 Table: `wallet_kpi`

| field | type | อธิบาย |
|------|------|---------|
| wallet_id | uuid | กระเป๋าไหน |
| kpi_type | text | general/scientific/economic |
| value | float | ตัวเลข KPI |
| target | float | เป้าหมาย |
| status | text | good/warning/bad |
| updated_at | timestamp | อัปเดตล่าสุด |

---

# 3) Metrics ที่ Agent ใช้บ่อยที่สุด

## 3.1 สำหรับงานเขียนรายงาน AutoPrompt

- progress_score  
- task_open  
- note_count  
- similarity_index  
- KPI status  
- votes_up / votes_down  
- summary stats (mean, median, variance)

## 3.2 สำหรับงานวิชาการ / research

- citation_count  
- impact_score  
- semantic cluster index  
- vector similarity heatmap  
- growth rate (ไฟล์เพิ่มวันละเท่าไหร่)

## 3.3 สำหรับงาน Simulation

- ค่าอินพุตตัวเลขจาก wallet  
- dataset ที่ผูกกับโปรเจกต์  
- experimental results ที่ agent เคยรัน

---

# 4) Agent Rules ในการใช้ Metrics

### Rule 1 — ห้ามคำนวณเองถ้า database คำนวณได้
ใช้ SQL ก่อนใช้ LLM

### Rule 2 — ตัวเลขต้อง reproducible  
ทุกผลลัพธ์ต้องมี:
- query ที่ใช้
- dataset ที่ใช้
- timestamp  
ทั้งหมดเขียนลงไฟล์ markdown ด้วย

### Rule 3 — ตัวเลขสำคัญต้องอ้างอิงจาก `project_stats` เท่านั้น  
ห้ามเดา

### Rule 4 — ค่าทางสถิติต้องมาจาก dataset จริง  
ถ้า dataset ไม่มี → agent ขอให้ผู้ใช้ upload

---

# 5) Data Provenance (แหล่งที่มาของข้อมูล)

ทุกผลลัพธ์จะต้องแสดง:

```
- source_tables:
    - project_stats
    - engagement_metrics
- query:
    SELECT * FROM ...
- generated_at: 2025-12-XX
- agent: autoprompt.research
```

---

# 6) ตัวอย่าง Query มาตรฐาน

### 6.1 โปรเจกต์โตเร็วหรือไม่?

```sql
SELECT
  note_count,
  EXTRACT(epoch FROM updated_at - created_at) / 86400 AS days,
  note_count / NULLIF(
      EXTRACT(epoch FROM updated_at - created_at) / 86400, 0
  ) AS growth_rate_per_day
FROM project_stats
WHERE project_id = $1;
```

### 6.2 KPI ตรวจสอบว่าสีอะไร (good/warning/bad)

```sql
SELECT
    value,
    target,
    CASE
       WHEN value >= target THEN 'good'
       WHEN value >= target * 0.7 THEN 'warning'
       ELSE 'bad'
    END AS status
FROM wallet_kpi
WHERE wallet_id = $1;
```

---

# 7) รูปแบบไฟล์รายงานของ Agent

Agent ต้องสร้างไฟล์แบบนี้:

```md
# Research Summary — Project A

## 1. Key Metrics
- Progress: 82%
- Engagement: 180 views
- KPI Score: Good

## 2. Data Sources
- project_stats (v12)
- engagement_metrics (v4)

## 3. SQL Used
```

```sql
## 4. Analysis
สรุปผลทางวิชาการ/สถิติ/พฤติกรรม

## 5. Conclusion
```
---
# 8) นี่คือจุดเชื่อมกับ Agent Flow

**AutoPrompt → MetricQuery → Data API → SQL → Analysis → Markdown**

Flow สั้น ๆ:

```sql
Agent Request
   ↓
Metrics API
   ↓
SQL Query Engine
   ↓
Result → Analyzer
   ↓
Markdown Report
   ↓
Studio / Project Tab
```

---

# 9) Matrix Overview (ภาพรวมแบบตาราง)

|Layer|ที่อยู่ของข้อมูล|Agent ใช้อะไร|Output|
|---|---|---|---|
|Raw Data|wallet, stats, engagement|SQL|numeric table|
|Knowledge|markdown, vector|RAG|text summary|
|Analytics|KPI engine|metric rules|scorecard|
|Agent|autoprompt / research|hybrid|reports|
|Interface|studio|viewer|canvas/report|

---

# 10) Diagram Flow (เข้าใจง่าย)

```scss
          ┌─────────────┐
          │ AutoPrompt  │
          └──────┬──────┘
                 │ (1) Request Metrics
                 ▼
         ┌────────────────┐
         │ Metrics API    │
         └──────┬─────────┘
                │ (2) SQL Query
                ▼
      ┌──────────────────────┐
      │ PostgreSQL (Tables)  │
      └──────┬───────────────┘
             │ (3) Numeric Data
             ▼
      ┌──────────────────────┐
      │ Analyzer (LLM+Rules) │
      └──────┬───────────────┘
             │ (4) Analysis
             ▼
       ┌────────────────────┐
       │ Markdown Report    │
       └────────────────────┘
```


---

# 🎉 **สรุป**
ไฟล์นี้ = “พจนานุกรมตัวเลข” ของแพลตฟอร์ม  
ทุก Agent / API / ระบบต้องเข้าใจตรงกัน  
แล้ว AutoPrompt จะสามารถ:

- วิเคราะห์
- สร้างงานวิจัย
- ทำ simulation
- ทำ KPI dashboard
- ทำรายงานระดับองค์กร
- สรุปสถานะโปรเจกต์
- ประกอบเป็น Full Paper

ได้แบบ **แม่น 100%**

---

# พร้อมไปต่อไหม Santa?

ลำดับถัดไปที่เหมาะที่สุดคือ:

### → `ANALYTICS_API.md` (API เรียก metric แบบละเอียด)  
หรือ  
### → `KNOWLEDGE_SYNC.md` (กฎ sync ระหว่าง DB ↔ Markdown ↔ Vector)

เลือกได้เลย ❤️
