ได้เลย Santa —  
นี่คือ **STYLE_GUIDE.md (เวอร์ชันยกเครื่องใหม่สุด)**  
เขียนแบบ **กระชับ, ชัด, ใช้งานจริง**, และ **สอดคล้องกับ UET_DESIGN_PRINCIPLES + DESIGN_TOKENS + ระบบ 3-Panel ของ UET**

นี่จะเป็น “ไบเบิลของดีไซน์” ที่บอกว่า **ทุกหน้าบนแพลตฟอร์มต้องหน้าตายังไง, mood & tone แบบไหน, ใช้โทนสีแบบไหน, interaction แบบไหน**  
ง่ายต่อ dev / AI / นาย / community

ลุยเลย ❤️

---

# 📘 **STYLE_GUIDE.md**

> _“UET Style = ความเรียบง่าย, ลึก, สมดุล, สุภาพ, และทันสมัย — เหมือน Notion × Linear × Obsidian รวมกัน แต่มีลายเซ็นความเป็น UET ชัดเจน”_

---

# 🟦 1) BRAND IDENTITY (เอกลักษณ์ของ UET)

## **1.1 Tone & Mood**

- สงบ (Calm)
    
- สมดุล (Balanced)
    
- เทคโนโลยีแต่ละมุน (Soft Tech)
    
- เรียบลึก (Minimal Depth)
    
- ความคิดอ่านง่าย (Clarity-driven)
    

**สไตล์:**  
Notion (clean) + Linear (modern) + Obsidian (knowledge-driven)

---

## **1.2 Brand Personality**

- นิ่ง
    
- มั่นคง
    
- มีระเบียบ
    
- เป็นกลาง
    
- ฉลาด
    
- เสถียร
    
- ไม่โชว์พาว
    
- เรียบแต่ดูแพง
    

---

# 🟩 2) COLOR STYLE (การใช้สีแบบ UET)

### **Primary สีเขียว UET**

- Primary: `#4ADE80`
    
- Dark: `#16A34A`
    
- Light: `#BBF7D0`
    

> ใช้เน้น action สำคัญ เช่น ปุ่มหลัก, highlight ใน graph, active state

---

### **Neutral Palette**

สำหรับ UI ทั้งหมด:

- White → #FFFFFF
    
- Light gray → #F8FAFC / #F1F5F9
    
- Mid gray → #E2E8F0 / #DADADA
    
- Dark gray → #2E2E2E / #1A1A1A
    

> เป้าหมาย = UI ดูสะอาด, โปร, ไม่ล้าสายตา

---

### **Semantic Colors**

- Success → #22C55E
    
- Warning → #FACC15
    
- Danger → #EF4444
    
- Info → #3B82F6
    

> ใช้ทำให้ระบบ “พูดกับผู้ใช้” ได้เข้าใจง่าย

---

### **Dark Mode**

พื้นเข้มแบบ UET = เทาเข้ม + เขียวสว่าง  
(เหมือน Linear Dark Mode)

---

# 🟧 3) TYPOGRAPHY STYLE

### **ฟอนต์หลัก**

```
Inter / SF Pro / System UI
```

> เหตุผล: อ่านง่าย, รองรับหลายภาษา, ใช้ได้ทั้ง UI และ Content

---

### **Font Scale (ตาม design tokens)**

- Title: 22–24px
    
- H1: 20px
    
- H2: 18px
    
- Body: 16px
    
- Small: 14px
    
- Metadata: 12px
    

---

### **น้ำหนัก (Weight)**

- Title → 600
    
- H2 → 500
    
- Body → 400
    
- Metadata → 300
    

> ไม่ใช้ตัวหนาเยอะ เพราะทำให้ UI ดูหนัก

---

# 🟥 4) LAYOUT STYLE (การจัดวาง + ช่องไฟ)

## **4.1 UET = 3 PANEL SYSTEM**

เป็นฐานของทุกหน้า:

- **Sources (ซ้าย)** = กว้าง 260–360px
    
- **Chat (กลาง)** = adaptive
    
- **Studio (ขวา)** = กว้าง 400–520px (ขึ้นกับเนื้อหา)
    

---

## **4.2 Layout Grid**

ใช้ 8px spacing system:

- Small gap → 8px
    
- Medium → 16px
    
- Large → 24px
    
- Section → 32px
    

นี่ทำให้ UI ดูสมดุล, ละมุน, เหมือน work app ระดับ enterprise

---

## **4.3 White Space Philosophy**

- เน้นความโปร่งเหมือน Notion/Linear
    
- ใช้พื้นที่ว่างเป็นตัวแยก section
    
- ไม่ยัดของ
    

---

# 🟪 5) COMPONENT STYLE (หน้าตามาตรฐาน)

## **Button**

- Radius: 8px
    
- Height: 40px
    
- Font: 14–16px
    
- Primary = เขียว UET
    
- Secondary = เทาอ่อน
    
- Ghost = ขอบจางมาก
    

### ปุ่มต้องมี state:

- idle
    
- hover
    
- press
    
- focus
    
- loading
    
- disabled
    

> ปุ่มต้องนิ่งและมั่นคง ไม่วิ่ง ไม่กระโดด

---

## **Input**

- Radius 6px
    
- Border: #E2E8F0
    
- Focus: เส้นเขียว UET 1–2px
    
- Placeholder → สีจางมาก (ไม่แย่งตา)
    

---

## **Panel**

- BG: #F8FAFC
    
- Shadow: 0 1px 2px rgba(0,0,0,0.05)
    
- ใช้เส้นแบ่งบาง ๆ สี #E2E8F0
    

---

## **Chat Bubble**

- ของผู้ใช้ = จาง
    
- ของ AI = ขาว/ดำตามโหมด
    
- Reasoning = block พิเศษ (เหมือน Code Block)
    

---

## **Canvas / Editor**

- เน้น clean
    
- ใช้ spacing เยอะ
    
- ฟอนต์ใหญ่ (16–17px)
    
- เน้นมองอ่านง่าย
    

---

# 🟫 6) INTERACTION STYLE (ความรู้สึกตอนใช้งาน)

## **Motion**

- Fast = 120ms
    
- Normal = 240ms
    
- Slow = 360ms
    

ใช้ sparingly:  
→ เปิด/ปิด panel  
→ loading  
→ sync

ไม่ใช้ motion เพื่อความสวย  
แต่เพื่อสื่อสถานะ เช่น  
“กำลัง sync”  
“agent กำลังคิด”

---

## **Hover Behavior**

- เบามาก
    
- ไม่ใช้สีแรง
    
- ขยับขึ้น 1px ได้ (แบบ Linear)
    

---

## **Click Behavior**

- ไม่มี ripple
    
- เปลี่ยนสีเฉย ๆ
    
- Feedback ชัด แต่ไม่ aggressive
    

---

## **Drag & Drop**

- ใช้ shadow-lg เบา ๆ
    
- ยกขึ้น 4px
    
- highlight บริเวณ drop
    

---

## **Error / Warning**

- ใช้ semantic สีเท่านั้น
    
- message ชัดเจน
    
- ไม่ใช้ popup เด้งรบกวน
    

---

# 🟨 7) ICON STYLE

- เส้น 1.5–2px
    
- โทนกลาง ๆ
    
- มีความ modern
    
- ไม่มนเกิน ไม่แข็งเกิน
    
- แบบ Lucide / Feather / Remix Icon จะเหมาะสุด
    

---

# 🟩 8) BRAND SIGNATURE (เอกลักษณ์ของ UET)

สิ่งที่ทำให้ UI ของ UET แตกต่างจากแพลตฟอร์มอื่น:

- 3 Panel ที่นิ่ง
    
- เขียว UET โลว์คีย์
    
- ความเงาน้อย (anti-gloss)
    
- เส้นแบ่งบางแบบโปร
    
- Reading-focused
    
- ระบบ reasoning แบบ block
    
- Event-driven status indicator
    
- Minimal depth (shadow น้อย)
    
- Canvas/editor ที่ clean มาก
    
- Graph สีเขียวอ่อน/ฟ้าอ่อน signature
    

---

# 🟦 9) ACCESSIBILITY

- Contrast ข้อความต้องเกิน 4.5:1
    
- ขนาดตัวอักษรขั้นต่ำ 14px
    
- รองรับ Light/Dark Mode
    
- รองรับ blind mode (high contrast)
    

---

# 🟥 10) DON’Ts (กฎห้าม)

- ห้ามใช้สีสดแรง
    
- ห้ามใช้ฟอนต์แฟนซี
    
- ห้ามใช้เงาหนัก ๆ
    
- ห้ามใส่องค์ประกอบเยอะเกิน
    
- ห้ามเปลี่ยนตำแหน่ง 3 panel
    
- ห้ามสร้าง component ใหม่เองโดยไม่ใช้ component library
    
- ห้ามเปลี่ยน layout โดยไม่ผ่าน principles
    

---

# 🟪 11) SUMMARY (สรุปแบบสั้นที่สุด)

> **UET = Minimal, Modern, Balanced, Calm, Stable, AI-first, 3-panel-first**
> 
> ใช้เขียว signature, เทา clean, interaction เบา, spacing 8px, ฟอนต์ Inter, motion 120–240ms
> 
> เป็นสไตล์ที่อ่านง่าย, ทำงานง่าย, และเข้ากับ nature ของระบบ AI+Knowledge อย่างมาก

---

โอเค Santa มานี่ เดี๋ยวฉันเคลียร์ให้แบบ **สั้นที่สุด ชัดที่สุด** — เข้าใจประเด็นของนายแล้วว่า

> **นายอยากเห็น "สีจริงแบบภาพ" เหมือนใน Figma / Photoshop เพื่อใช้ทำ STYLE_GUIDE.md**

พร้อมทั้งกำลังคิดว่า  
**สีต้องผูกกับ Dark/Light Mode ยังไง**  
และ  
**ต้องมีระบบ Theme/Template แบบที่ผู้ใช้ปรับเองได้ไหม**

ฉันสรุปให้ตรงใจนายแบบนี้ก่อน แล้วเราค่อยไปสร้าง STYLE_GUIDE.md ฉบับจริงพร้อมภาพสี:

---

# ✅ 1) เรื่อง “สีต้องผูกกับ Dark/Light Mode” — ใช่ 100%

มาตรฐานสากลของ UI/UX (Figma, Material Design, Apple HIG, Tailwind, Radix) บอกตรงกันว่า:

### **สีของระบบต้องมีสองชั้น:**

1. **Mode tokens** → สีพื้นฐานที่เปลี่ยนตาม Light / Dark
    
2. **Brand tokens** → สีประจำแบรนด์ (primary/accent/success/error)
    

### ❗แปลว่าโครงสร้างการกำหนดสีต้องหน้าตาแบบนี้:

```
light {
  --bg: #FFFFFF;
  --text: #111111;
  --panel: #F7F7F7;
  --border: #EAEAEA;
}

dark {
  --bg: #0D0D0D;
  --text: #FFFFFF;
  --panel: #1A1A1A;
  --border: #333333;
}

brand {
  --primary: #4ADE80;
  --accent: #34D399;
  --success: #22C55E;
  --warning: #FACC15;
  --danger: #EF4444;
}
```

👉 **นี่คือมาตรฐานสากล 100%**  
(Figma, Radix UI, Tailwind Colors, Material Design ทุกอย่างเป็นแบบนี้หมด)

---

# ✅ 2) ทำไมต้องทำแบบนี้? (เหตุผลที่สำคัญจริง ๆ)

เพราะ:

### **- Dark/Light Mode** ต้องสลับได้แบบ Smooth

### **- Brand สีต้องอยู่เฉย ไม่เปลี่ยน**

### **- ผู้ใช้สามารถสร้าง Theme ของตัวเองได้ (ถ้าต้องการ)**

### **- Code ง่ายขึ้นมาก เพราะ UI อ่านแค่ Tokens**

เวลา Dev เขียน UI เขาจะเขียนแค่:

```
color: var(--text);
background: var(--panel);
border-color: var(--border);
```

เพราะฉะนั้นโหมดเปลี่ยน = UI เปลี่ยนทั้งระบบโดยไม่ต้องแก้โค้ดหนึ่งบรรทัด

---

# ✅ 3) แล้ว “สีแบบภาพจริง” ต้องทำยังไง?

นายอยากเห็น **Swatch แบบเป็นภาพ** — เดี๋ยวฉันทำให้เป็นภาพแบบนี้:

- แถบสีขนาดใหญ่
    
- เขียน HEX ใต้แต่ละสี
    
- มีทั้ง Light Mode และ Dark Mode
    
- มีทั้ง Brand Colors และ Semantic Colors
    

ตัวอย่าง (ที่ฉันจะสร้างให้ในรูปจริง):

**LIGHT MODE PREVIEW**  
[██████████] #FFFFFF  
[██████████] #F7F7F7  
[██████████] #EAEAEA  
[██████████] #111111

**BRAND PALETTE**  
[██████████] #4ADE80  
[██████████] #16A34A  
[██████████] #34D399

**DARK MODE PREVIEW**  
[██████████] #0D0D0D  
[██████████] #1A1A1A  
[██████████] #333333  
[██████████] #FFFFFF

ถ้านายบอก  
**“โอเค ทำภาพเลย”**  
ฉันจะ generate เป็น image block ให้ดูครบทุกสีทันที (เหมือน Figma)

---

# ✅ 4) เรื่อง “Template/Theme ผู้ใช้ปรับเองได้” = ทำได้ 100%

นายพูดถูกเป๊ะเลยว่า:

- เรามี UI ของระบบ: Original Theme
    
- ผู้ใช้สามารถทำ Template เพิ่มได้
    
- แต่ Template ต้องเป็น “ชั้นบน” ที่ override Tokens เดิม
    
- Tokens พื้นฐานของระบบยังคงเดิมเพื่อไม่ให้พัง
    

เหมือน LINE / Discord / Obsidian:

- เปลี่ยนพื้นหลังได้
    
- เปลี่ยน Theme ได้
    
- แต่ระบบ UI ไม่พัง
    

---

# 🎯 สรุปสั้นแบบเข้าใจง่ายที่สุด

> **1) เราต้องมี Light/Dark Mode ก่อน**  
> เพราะมันเป็น “OS-level UI Spec” ของสากล

> **2) หลังจากนั้นค่อยมี Brand Colors ของ UET**  
> สีเขียวสมดุลที่นายเลือกถูกต้องอยู่แล้ว

> **3) แล้วค่อยมี Theme/Template ที่ผู้ใช้สร้างได้**  
> ผ่าน CSS Tokens (safe และไม่ทำให้ระบบพัง)

> **4) STYLE_GUIDE.md ต้องใส่ภาพสีจริง ๆ**  
> ฉันพร้อมสร้างภาพให้ทันที

---

# ❓ Santa ต้องการแบบไหนสำหรับขั้นตอนต่อไป?

เลือก 1 อัน:

### **A) ให้ฉันสร้างรูป Swatch สี Light/Dark ทั้งหมดให้เลย (แบบ Figma)**

หรือ

### **B) ให้ฉันสร้าง STYLE_GUIDE.md พร้อมภาพสีเลย**

หรือ

### **C) ให้ฉันออกแบบ Design Tokens v3.0 แบบสมบูรณ์ (พร้อมภาพ)**

แค่บอกว่า:  
**“เอาแบบ A”** หรือ **“เอาแบบ B”** หรือ **“เอาแบบ C”**

ฉันจัดให้ทันที 💚