# 📝 How to Write a Topic README

> **Template มาตรฐานสำหรับเขียน README ทุก topic ใน UET (Triple-Green Standard)**

---

## 📋 โครงสร้างมาตรฐาน (The 5x4 Grid)

README ทุก topic ต้องแสดงความเชื่อมโยงระหว่าง **ทฤษฎี (Doc), หลักฐาน (Code/Ref), และ ข้อมูลจริง (Data)** ในรูปแบบของ 5 Root Pillars.

### 1. Badges + Core Quote

```markdown
# 🔬 0.XX Topic Name

![Status](https://img.shields.io/badge/Status-100%25_PASS-brightgreen)
![Standard](https://img.shields.io/badge/Standard-Extreme_Simplicity-blueviolet)
![Architecture](https://img.shields.io/badge/Architecture-5x4_Scientific_Grid-blue)
![Scientific_Rigor](https://img.shields.io/badge/Rigor-Zero_Curve_Fitting-orange)

> **Quote ที่อธิบาย "หัวใจ" ของการค้นพบใน Topic นี้ (เน้นว่า UET แก้สิ่งที่ของเดิมทำไม่ได้อย่างไร)**
```

---

### 2. Scientific Architecture (5 Pillars)

แสดงตารางที่บอกว่า Topic นี้แบ่งโครงสร้างอย่างไร:

| Pillar | Purpose |
| :--- | :--- |
| **Doc/** | ก่อน/หลัง (Before/After) และ Narrative ของการวิจัย. |
| **Ref/** | แหล่งอ้างอิงและ DOIs ของข้อมูลและทฤษฎี. |
| **Data/** | ข้อมูลจริงที่ใช้รัน (ต้องเป็น Real Data เท่านั้น). |
| **Code/** | Logic ทั้ง 4 ระดับ (Engine, Proof, Research, Competitor). |
| **Result/** | ผลลัพธ์ที่ Verify แล้ว (Plots, logs) - ต้อง Mirror Code. |

---

### 3. Mermaid Diagram (Theory Connection)

เน้นการข้ามผ่าน "ทางตัน" ของฟิสิกส์มาตรฐาน:

```markdown
## 🔗 Theory Connection

\`\`\`mermaid
graph TB
    subgraph Standard["🔬 Standard Physics"]
        Old["Standard Approach"]
        Limit["The specific limitation/blow-up"]
    end
    
    subgraph UET["✅ UET Solution"]
        Reformulation["UET Logic/Formula"]
        Result["Natural Smoothness/Speed/Accuracy"]
    end
    
    Old --> Limit
    Limit -->|"UET bridges via"| Reformulation
    Reformulation --> Result
    
    style UET fill:#d4edda,stroke:#28a745
\`\`\`
```

---

### 4. Problem & Solution (The Narrative)

- **The Problem:** อธิบายกำแพงที่ของเดิมติดขัด.
- **The Solution:** อธิบายว่า UET ใช้ "ความจำเป็น" (Necessity) ตัวไหนมาแก้.
- **Zero Curve Fitting Law:** ยืนยันว่าค่าที่ใช้นั้นคำนวณมาจากความจริง ไม่ใช่การเดาเพื่อให้กราฟสวย.

---

### 5. Results Table (Triple-Green Status)

```markdown
## 📊 Test Results

| Category | Test | Result | Status |
| :--- | :--- | :--- | :--- |
| **01_Engine** | Core Solver | Energy Conservation | ✅ PASS |
| **02_Proof** | Key Benchmark | Accuracy vs Analytical | ✅ PASS |
| **03_Research** | Real-world Sync | Match with Nobel/NASA data | ✅ PASS |
| **04_Competitor** | Standard Baseline | Speed/Stability Win | ✅ PASS |
```

---

### 6. Quick Start & Files

- **Quick Start:** ใส่คำสั่งที่รันแล้วเห็น "PASS" ทันที.
- **Files Table:** ลิงก์ไปยังไฟล์หลักใน `Code/` และ `Data/`.

---

## 📌 Tips

1. **Emoji Consistency:**
   - 🏛️ = Architecture
   - 🔗 = Connection
   - 🎯 = Problem
   - ✅ = Solution
   - 📊 = Results
   - 📚 = References
   - 🚀 = Quick Start
   - 📁 = Files

2. **No Placeholders:** อย่าใส่ "Coming Soon" หรือ "TBD" ใน README ของ Topic ที่เสร็จแล้ว.
3. **Traceability:** ข้อมูลใน `Result/` ต้องบอกที่มาได้ว่ามาจาก `Data/` ตัวไหน.

---

## 🎯 Gold Standard Example: 0.10_Fluid_Dynamics_Chaos

ใช้ไฟล์นี้เป็นแม่แบบเสมอ:
[`0.10_Fluid_Dynamics_Chaos/README.md`](./0.10_Fluid_Dynamics_Chaos/README.md)
