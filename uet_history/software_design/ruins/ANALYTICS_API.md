# 📘 **ANALYTICS_API.md**

**UET Platform — Analytics & Metrics API Specification**

ไฟล์นี้เป็น “แกนกลาง” ของระบบวิเคราะห์ข้อมูล (Analytics Layer)  
ใช้โดย:

- Agent ทุกตัว (autoprompt.research / autoprompt.finance / autoprompt.project)
- Studio (เวลาจะทำ dashboard, graph, KPI)
- Project Page (ดึงสถิติโดยตรง)
- Community Metrics
- Financial System (wallet KPI)

---

# 1. **เป้าหมายของ Analytics API**

API นี้ถูกออกแบบเพื่อ:

- ดึงตัวเลขแบบ real-time จาก database
- สร้างชุดข้อมูลที่ reproducible (มี source + query)
- รองรับงาน AI agent ที่ต้องการข้อมูล numerical
- ใช้แทนการ “เดา/วิเคราะห์เอง” ของ LLM
- รวมข้อมูลจากหลาย table แล้ว normalize ให้อยู่ในรูปแบบเดียวกัน

เป้าหมาย:  
**Agent คิดเรื่องคุณภาพ ส่วน API ส่งข้อมูลดิบให้**

---

# 2. **โครงสร้าง API หลัก**

Analytics API มี 4 กลุ่มใหญ่:

|กลุ่ม|หน้าที่|
|---|---|
|**Project Analytics API**|ตัวเลขสถานะแต่ละโปรเจกต์|
|**Engagement API**|ตัวเลข interaction|
|**KPI / Wallet API**|ตัวเลข KPI, scorecard|
|**Research Index API**|ค่า similarity, cluster index, citation count|

---
# 3. **รูปแบบ Response กลาง (Unified Response Contract)**

API ทุกตัวต้องตอบแบบนี้:

```json
{
  "success": true,
  " generated_at": "2025-12-04T14:32:00Z",
  "query_used": "SELECT ...",
  "source_table": ["project_stats"],
  "data": {
     ... numerical results ...
  }
}
```

เหตุผล:  
เพื่อให้ **Agent สามารถอ้างอิง แหล่งข้อมูล + query + timestamp**  
→ ทำงานวิชาการได้ → reproducible

---
# 4. **API รายตัว (แบบใช้งานจริง)**

## 4.1 **GET /api/analytics/project/:projectId**

ดึงสถานะโปรเจกต์ทั้งหมดแบบ one-shot  
เหมาะกับ Agent สรุปสถานะโปรเจกต์

### Response

```json
{
  "success": true,
  "data": {
    "note_count": 42,
    "task_open": 12,
    "progress_score": 0.72,
    "updated_at": "2025-12-04T13:20:10Z"
  }
}
```

---

## 4.2 **GET /api/analytics/project/growth/:projectId**

ดูว่าโปรเจกต์โตเร็วแค่ไหน

```json
{
  "growth_rate_per_day": 3.1
}
```

---

## 4.3 **GET /api/analytics/engagement/:projectId**

ค่าปฏิสัมพันธ์ (views/votes/comments)

```json
{
  "views": 188,
  "votes_up": 92,
  "votes_down": 3,
  "comments": 24
}
```

---

## 4.4 **GET /api/analytics/kpi/:walletId**

สถานะ KPI แบบเต็ม

```json
{
  "value": 87,
  "target": 100,
  "status": "warning",
  "percent": 0.87
}
```

---

## 4.5 **GET /api/analytics/research/similarity/:projectId**

ค่า similarity ระหว่างไฟล์ทั้งหมดในโปรเจกต์  
ใช้ทำ heatmap, cluster tree

```json
{
  "similarity_index": 0.82
}
```

(ดึงจาก vector DB)

---

## 4.6 **POST /api/analytics/research/statistics**

ส่ง dataset → API คำนวณสถิติให้

### Input

```json
{
  "dataset": [1,2,2,3,5,8,13,21]
}
```

### Output

```json
{
  "mean": 6.8,
  "median": 4,
  "variance": 43.96,
  "std": 6.63
}
```

ใช้ใน:
- งานวิจัย
- AutoPrompt (สรุปผลทดลอง)
- Simulation

---
## 4.7 **POST /api/analytics/experimental/run**

ส่งชุด parameter → ระบบจำลอง (simulation)

### Input

```json
{
  "model": "simple_growth",
  "params": { "r": 1.2, "t": 30 }
}
```

### Output

```json
{
  "result": [1.2, 2.4, 4.8, 9.6, ... ]
}
```

ใช้โดย:
- นักวิจัย
- ฟังก์ชัน AutoPrompt: Full Research Paper
- ฟังก์ชันพิสูจน์ทางคณิต

---

# 5. **Matrix รวมทุก API แบบเข้าใจง่าย**

|API|Input|Output|Agent ใช้ทำอะไร|
|---|---|---|---|
|`/project/:id`|project id|health summary|สรุปโปรเจกต์|
|`/project/growth/:id`|project id|growth rate|รายงานคืบหน้า|
|`/engagement/:id`|project id|votes/views/comments|วิเคราะห์สังคม|
|`/kpi/:wallet`|wallet id|KPI status|การเงิน / scorecard|
|`/research/similarity/:id`|project id|sim index|วิเคราะห์ทฤษฎี|
|`/statistics`|dataset|mean/variance|งานวิจัย|
|`/experimental/run`|params|simulation|ทดลอง/พิสูจน์|

---
# 6. **API Hierarchy Diagram**

```
Analytics API
├── Project Analytics
│     ├── /project/:id
│     └── /project/growth/:id
│
├── Engagement Analytics
│     └── /engagement/:id
│
├── KPI / Wallet Analytics
│     └── /kpi/:walletId
│
└── Research Analytics
      ├── /research/similarity/:id
      ├── /statistics
      └── /experimental/run
```

---
# 7. **Agent Integration Flow**

```
Agent → Analytics API → SQL / Vector DB
       → Numeric Data → Analyzer → Markdown Report
```

ตัวอย่าง:  
AutoPrompt สร้างวิจัย =

1. ขอข้อมูล → `/project/:id`
2. ขอ similarity → `/research/similarity/:id`
3. ขอสถิติ dataset → `/statistics`
4. สร้างสรุป → Markdown
5. เขียนลง Studio

---
# 8. **Security / Permission**

|Role|ดึง metrics แบบไหน|
|---|---|
|Guest|เฉพาะ public project|
|Member|โปรเจกต์ที่ตัวเองอยู่|
|Power User|ทุกโปรเจกต์ที่ join|
|Admin|Full access|

---
# 9. **ข้อควรรู้สำหรับนักพัฒนา AI / Agent**

- ห้ามเดาตัวเลข
- ข้อมูลตัวเลขมาจาก API เท่านั้น
- ถ้า dataset เป็นความรู้ (text) → ใช้ RAG
- ถ้าต้องการตีความทฤษฎี → ส่งผ่าน LLM analyzer
- ถ้าเป็นการทดลอง → `/experimental/run`
- ถ้าเป็น KPI → `/kpi/:wallet`

---

# 🎉 สรุปให้สั้นมาก

Analytics API =  
**สมองตัวเลขของแพลตฟอร์ม**

Agent จะฉลาดแค่ไหน =  
ขึ้นอยู่กับ API นี้โดยตรง

มันทำให้:

- ทำรายงาน
- ทำ Dashboard
- วัด KPI
- ทำงานวิจัย
- ทำ simulation
- วิเคราะห์โปรเจกต์
- วิเคราะห์ interaction

ทั้งหมดอยู่ในไฟล์เดียวนี้!

---
