# 🔥 **INTERACTION_RULES — Core Concept (แกนกลาง)**

> **งานนี้คือ “กฎการสื่อสารของจักรวาล UET”**  
> ทำให้ทุก Panel คุยกับกันแบบไม่มั่ว ไม่ตีกัน และ deterministic 100%

---

# ⭐ A. PRINCIPLE 1 — “Context Selection Rule”

เวลาคุยกับ AI ต้องเลือกว่าใช้สมองไหน

## 1) Default Rule

```css
ถ้าอยู่หน้า Project → ใช้ P-KB เป็นหลัก + G-KB เป็นรอง  
ถ้าอยู่หน้า Chat หลัก → ใช้ G-KB 100%  
ถ้าอยู่หน้า Community → ใช้ NONE (ไม่ใช้ KB)
```

## 2) AI ห้ามสลับ KB เองเด็ดขาด

ต้องเลือก KB ผ่านระบบ → ไม่ใช่ AI เดาเอง

---

# ⭐ B. PRINCIPLE 2 — “Panel Priority Rule”

ทุก interaction ต้องมาจาก panel ใด panel หนึ่งเท่านั้น

|Panel|Priority|ใช้เพื่อ|
|---|---|---|
|Studio|1|สร้าง/แก้ Markdown, commit|
|Source|2|อ่านไฟล์, filter, เลือก KB|
|Chat|3|โต้ตอบ, ขอ retrieve, summarize|

**ห้ามสลับ Panel โดยไม่ผ่าน event**  
เพื่อกัน context shift ที่มั่ว

---
# ⭐ C. PRINCIPLE 3 — “Write vs Influence Rule”

```java
Chat Panel = ทำได้แค่ “เสนอแนะ”
Studio Panel = ทำได้แค่ “เขียนจริง”
```


AI ห้ามเขียนลง KB โดยตรง  
ต้องมา Studio เสมอ

---
# ⭐ D. PRINCIPLE 4 — “Vector Contract”

```ini
Vector = ดัชนี → ค้นหา  
Markdown = ความจริง → อ้างอิง
```

→ เวลาจะ update vector ต้องผ่าน Source Panel เท่านั้น

---

# ⭐ E. PRINCIPLE 5 — “Project Isolation”

โปรเจกต์ห้ามปนกัน

```css
P-KB A ≠ P-KB B  
P-KB ต่างโปรเจกต์ห้ามคุยกัน  
```

ถ้าต้องการย้าย ต้องใช้ flow `PROMOTE → REVIEW → ACCEPT`

---
# ⭐ F. PRINCIPLE 6 — “User Level Influence”

สิทธิ์ต่างกัน ต้องส่งผลต่อการสื่อสาร:

|User Level|ทำอะไรได้|Chat Behavior|
|---|---|---|
|Guest|ask only|no KB|
|Member|ask + upload|P-KB only|
|Power User|manage project|P-KB + limited G-KB|
|Admin|merge KB|full access|

---

# ⭐ G. PRINCIPLE 7 — “State Lock Rule”

ตอน Studio Panel เปิดแก้ไฟล์ → AI ต้อง “นิ่ง”

```lua
State: EDITING  
→ AI ห้าม push output, ห้ามสรุป, ห้ามสร้างไฟล์ใหม่  
```

```vbnet
Studio Editing Rules:
- Editing file A does NOT block autoprompt from generating file B.
- Only block if AI attempts to overwrite file A directly.
- AI always writes new files to /output or /autoprompt.
```


---

# ⭐ H. PRINCIPLE 8 — “Autoprompt Step Rule”

Autoprompt = flow 3 ขั้นตอนตายตัว

```vbnet
STEP 1: Retrieve
STEP 2: Reason
STEP 3: Output (Markdown only)
```

---
# ⭐ I. PRINCIPLE 9 — “Error Handling Rule”

ผิดพลาด = ต้อง revert state  
ไม่ใช่เดาใหม่
```pgsql
ถ้า vector error → revert index  
ถ้า merge error → rollback commit  
ถ้า file conflict → create patch version
```

---
# ⭐ J. PRINCIPLE 10 — “Deterministic Response Rule”

AI ต้องตอบแบบ **อ่านซ้ำได้ 100%**  
ไม่มี random, ไม่มีข้าม KB, ไม่มีคิดเอง

```css
Prompt in → Flow → Output  
ต้องเหมือนเดิมทุกครั้ง
```

---

# 📌 “INTERACTION MAP” (ไดอะแกรมเข้าใจง่ายมาก)

```sql
USER → PANEL → API → CONTEXT ENGINE → AI MODEL → PANEL
```
### รายละเอียดในหนึ่งภาพ

```pgsql
                     ┌───────────────────────────┐
                     │     GLOBAL KB (G-KB)      │
                     └─────────────┬─────────────┘
                                   │
                 promote / review  │
                                   ▼
╔═══════════════════ PROJECT WORKSPACE ═══════════════════╗
║                                                         ║
║     ┌──────────────┐      ┌────────────────┐            ║
║     │ SOURCE PANEL │─────→│ CONTEXT ENGINE │───→ AI     ║
║     └──────────────┘      └────────────────┘            ║
║             ▲                       ▲                    ║
║             │                       │                    ║
║     ┌──────────────┐      ┌────────────────┐            ║
║     │ CHAT PANEL   │─────→│  VECTOR INDEX  │            ║
║     └──────────────┘      └────────────────┘            ║
║             ▲                                               
║             │                                               
║     ┌──────────────┐                                       
║     │ STUDIO PANEL │ → write markdown → versioning → edges 
║     └──────────────┘                                       
║                                                         ║
╚═════════════════════════════════════════════════════════╝
```


---

# 🎁 ถ้าต้องการ ฉันจะร่าง INTERACTION_RULES.md ฉบับ “สมบูรณ์ที่สุด” ให้เลย

โครงจะเป็นแบบนี้:

```pgsql
# INTERACTION_RULES.md
1. Summary
2. Global Rules
3. Communication Protocol
4. Panel Interaction
5. KB Logic (G-KB / P-KB)
6. Vector Flow
7. Autoprompt Behavior
8. User Policy
9. Error Rules
10. Examples (10 scenarios)
```