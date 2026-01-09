# 📝 How to Write a Topic README

> **Template มาตรฐานสำหรับเขียน README ทุก topic ใน UET**

---

## 📋 โครงสร้างมาตรฐาน

README ทุก topic ต้องมี 9 ส่วนหลัก:

### 1. Badges + Quote

```markdown
# 🔬 0.XX Topic Name

![Status](https://img.shields.io/badge/Status-100%25_PASS-brightgreen)
![Data](https://img.shields.io/badge/Data-SOURCE_NAME-blue)
![Tests](https://img.shields.io/badge/Tests-N/N-green)
![DOI](https://img.shields.io/badge/DOI-Multiple_See_Below-orange)

> **Quote ที่อธิบาย core insight ของ topic นี้**
```

---

### 2. Table of Contents (สารบัญ)

```markdown
## 📋 Table of Contents

1. [Overview](#-overview)
2. [Theory Connection](#-theory-connection)
3. [The Problem](#-the-problem)
4. [UET Solution](#-uet-solution)
5. [Results](#-test-results)
6. [Data Sources](#-data-sources--references)
7. [Quick Start](#-quick-start)
8. [Files](#-files-in-this-module)
```

---

### 3. Mermaid Diagram (Theory Connection)

```markdown
## 🔗 Theory Connection

\`\`\`mermaid
graph TB
    subgraph Standard["🔬 Standard Physics"]
        Old["Standard approach"]
        Limit["Its limitations"]
    end
    
    subgraph Problem["❌ The Problem"]
        Issue["Specific issue"]
    end
    
    subgraph UET["✅ UET Approach"]
        Solution["UET solution"]
        Result["What it predicts"]
    end
    
    Old --> Limit
    Limit -->|"Leads to"| Issue
    Issue -->|"UET explains"| Solution
    Solution --> Result
    
    style UET fill:#d4edda,stroke:#28a745
\`\`\`
```

---

### 4. Problem Section (ปัญหาเดิม)

```markdown
## 🎯 The Problem

### The Classical View

ทฤษฎีเดิมทำได้แค่ไหน และติดตรงไหน

| Issue | Description |
|:------|:------------|
| **ปัญหา 1** | อธิบาย |
| **ปัญหา 2** | อธิบาย |

### The Key Question

> **คำถามหลักที่ยังตอบไม่ได้**
```

---

### 5. UET Solution (ทางแก้)

```markdown
## ✅ UET Solution

### Core Insight

อธิบาย UET แก้ปัญหาอย่างไร

### Formula/Equation

$$สูตร UET ที่ใช้$$

### Why It Works

| Concept | Standard | UET |
|:--------|:---------|:----|
| **X** | ทำไม | ทำได้ |
```

---

### 6. Results Table + DOIs

```markdown
## 📊 Test Results

### Summary

| Test | Data Source | Result | Status |
|:-----|:------------|:------:|:------:|
| Test 1 | Source | Value | ✅ PASS |
| Test 2 | Source | Value | ✅ PASS |

### Detailed Results

*(ใส่ตารางละเอียดพร้อมค่า error)*

## 📚 Data Sources & References

| Source | Description | DOI |
|:-------|:------------|:----|
| **Name** | What it is | [`10.xxxx/yyyy`](https://doi.org/) |
```

---

### 7. Quick Start + Expected Output

```markdown
## 🚀 Quick Start

### Run Tests

\`\`\`bash
cd research_uet/topics/0.XX_Topic_Name

# Download data
python Data/download_data.py

# Run test
python Code/section/test_xxx.py
\`\`\`

### Expected Output

\`\`\`
======================================================================
TEST NAME
======================================================================

[1] SECTION 1
--------------------------------------------------
  Result: Value
  Status: ✅ PASS

======================================================================
RESULT: [CONCLUSION]
======================================================================
\`\`\`
```

---

### 8. Files Table

```markdown
## 📁 Files in This Module

### Code

| File | Purpose |
|:-----|:--------|
| [`Code/xxx/test_xxx.py`](./Code/xxx/test_xxx.py) | ⭐ Main test |

### Data

| File | Source | Content |
|:-----|:-------|:--------|
| [`Data/xxx.json`](./Data/xxx.json) | Source | Description |

### Documentation

| Path | Content |
|:-----|:--------|
| [`Doc/section_1/before/`](./Doc/section_1/before/) | Problem |
| [`Doc/section_1/after/`](./Doc/section_1/after/) | Solution |
| [`Ref/REFERENCES.py`](./Ref/REFERENCES.py) | DOIs |
```

---

### 9. Navigation Links

```markdown
---

[← Previous Topic](../0.XX_Previous/README.md) | [← Back to Topics Index](../README.md) | [→ Next Topic](../0.XX_Next/README.md)
```

---

## 📌 Tips

1. **Badges สี**
   - `brightgreen` = 100% PASS
   - `green` = 90%+ PASS  
   - `yellow` = 80%+ PASS
   - `red` = FAIL

2. **Table ต้องมี DOI** ทุกครั้งที่อ้าง data จริง

3. **Mermaid diagram** ควรแสดง flow: Standard → Problem → UET Solution

4. **Expected Output** ควร copy จากการรันจริง

5. **ใช้ emoji อย่างสม่ำเสมอ**
   - 📋 = Contents
   - 🔗 = Connection
   - 🎯 = Problem
   - ✅ = Solution
   - 📊 = Results
   - 📚 = References
   - 🚀 = Quick Start
   - 📁 = Files

---

## 🎯 Example: ดู 0.3_Cosmology_Hubble_Tension

ไฟล์นี้เป็น gold standard:
[`0.3_Cosmology_Hubble_Tension/README.md`](./0.3_Cosmology_Hubble_Tension/README.md)
