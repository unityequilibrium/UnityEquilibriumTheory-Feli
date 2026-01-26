# 🌐 UET Domain Mapping Guide

> **คู่มือการเชื่อมโยง UET กับศาสตร์อื่น — ไม่ตีความผิด**  
> **Version**: 0.8.7 | Merged from v0.8.6  
> **Purpose**: อธิบายว่า C/I หมายถึงอะไรในแต่ละ domain

---

## 🎯 TL;DR

ถ้าจะ "ลิงก์ไปศาสตร์อื่นแบบไม่เลอะ" ให้ยึด:

- **𝒱** (Value = ผลลัพธ์ที่วัดได้)
- **Ω** (ค่าความไม่สมดุล)

เป็นหลัก — เพราะทุกศาสตร์วัด "ผลสุทธิ" ได้

> **⚠️ สำคัญ**: C/I ไม่ได้หมายถึง "จิตสำนึก/สัญชาตญาณ" — มันหมายถึง **ระบบเปิด/ระบบปิด (openness/closure)**

---

## 📊 ความสัมพันธ์หลัก

```
𝒱 ↑  ⇒  Ω ↓
```

| การเปลี่ยนแปลง | ความหมาย |
|:--------------|:---------|
| **𝒱 เพิ่ม** | ระบบดีขึ้น (ได้ผลลัพธ์สุทธิเพิ่ม) |
| **Ω ลด** | สมดุล/ระเบียบดีขึ้น |

**สูตร**: $\mathcal{V} \approx -\Delta\Omega$ ต่อหนึ่งสเต็ป

---

## 🗺️ Mapping ตามโดเมน

### (A) Physics / Cosmology

| Symbol | Mapping | Description |
|:------:|:--------|:------------|
| **C** | Visible matter | สสารที่สังเกตได้ |
| **I** | Dark matter/sectors | สถานะที่ซ่อน |
| **β** | Gravitational coupling | ความแรงปฏิสัมพันธ์ |
| **κ** | Speed of propagation | อัตราการแพร่กระจาย |
| **Ω** | Energy functional | พลังงานระบบ |

---

### (B) Thermodynamics / Open Systems

| Symbol | Mapping | Description |
|:------:|:--------|:------------|
| **C** | Flux / Exchange capacity | ความสามารถแลกเปลี่ยนกับภายนอก |
| **I** | Dissipation | ความสูญเสีย/แรงต้าน |
| **𝒱** | Useful improvement | งานที่ใช้ได้ |
| **Ω** | Free-energy-like | ความไม่สมดุลของระบบ |

---

### (C) Neuroscience / Brain Dynamics

| Symbol | Mapping | Description |
|:------:|:--------|:------------|
| **C** | Excitatory neural activity | กิจกรรมกระตุ้น |
| **I** | Inhibitory neural state | กิจกรรมยับยั้ง |
| **β** | E-I balance | สมดุลกระตุ้น-ยับยั้ง |
| **κ** | Axonal connectivity | การเชื่อมต่อ |
| **Ω** | Neural energy | พลังงานระบบประสาท |

---

### (D) Economics / Markets

| Symbol | Mapping | Description |
|:------:|:--------|:------------|
| **C** | Market price | ราคาตลาด |
| **I** | Intrinsic value | มูลค่าแท้จริง |
| **β** | Market efficiency | ประสิทธิภาพตลาด |
| **κ** | Information spreading | การแพร่กระจายข่าวสาร |
| **s** | External shocks | ข่าว/นโยบาย |
| **Ω** | Market inefficiency | ความไม่มีประสิทธิภาพ |

---

### (E) Biology / Ecology

| Symbol | Mapping | Description |
|:------:|:--------|:------------|
| **C** | Activator (morphogen A) | สารกระตุ้น |
| **I** | Inhibitor (morphogen B) | สารยับยั้ง |
| **β** | Reaction rate | อัตราปฏิกิริยา |
| **κ** | Diffusion coefficient | สัมประสิทธิ์การแพร่ |
| **Ω** | Systemic stress | ความเครียดระบบ |

---

### (F) Machine Learning / AI

| Symbol | Mapping | Description |
|:------:|:--------|:------------|
| **C** | Observable features | คุณลักษณะที่สังเกตได้ |
| **I** | Latent representation | ตัวแทนที่ซ่อน |
| **β** | Learning rate | อัตราการเรียนรู้ |
| **κ** | Weight sharing | การแชร์น้ำหนัก |
| **Ω** | Loss function | ฟังก์ชันสูญเสีย |
| **𝒱** | Learning progress | ความก้าวหน้าการเรียนรู้ |

---

## ⚠️ กติกาห้ามตีความผิด (5 Rules)

1. ❌ **ห้าม** ตีความ C/I เป็น "จิตสำนึก/สัญชาตญาณ/อารมณ์"
2. ✅ ถ้าโดเมนไหนนิยาม C/I ยาก ให้ **นิยามผ่าน 𝒱 ก่อนเสมอ**
3. ✅ 𝒱 ต้องเป็น "ตัวชี้วัดที่ observable/คำนวณได้" ในโดเมนนั้น
4. ✅ Ω ต้องเป็น "scalar" ที่บอกความไม่สมดุล และลดลงเมื่อ 𝒱 เพิ่ม
5. ✅ ทุก mapping ต้องบอก "หน่วย/สเกล" อย่างน้อยว่าเป็น rate หรือดัชนีไร้หน่วย

---

## 🔄 Flow Diagram: How to Map

```
┌──────────────────────────────────────────────────────────┐
│  1. DEFINE 𝒱 FIRST                                       │
│     "ผลลัพธ์สุทธิที่วัดได้ในโดเมนนี้คืออะไร?"               │
│     (Observable, Quantifiable)                           │
└────────────────────────┬─────────────────────────────────┘
                         ▼
┌──────────────────────────────────────────────────────────┐
│  2. DEFINE Ω                                             │
│     "ความไม่สมดุล/ความตึงของระบบวัดยังไง?"                 │
│     Ω must decrease when 𝒱 increases                     │
└────────────────────────┬─────────────────────────────────┘
                         ▼
┌──────────────────────────────────────────────────────────┐
│  3. THEN DEFINE C/I                                      │
│     C = สิ่งที่ทำให้ 𝒱 เพิ่ม (openness)                   │
│     I = สิ่งที่ทำให้ 𝒱 ลด (friction)                     │
└────────────────────────┬─────────────────────────────────┘
                         ▼
┌──────────────────────────────────────────────────────────┐
│  4. VALIDATE                                             │
│     ✓ 𝒱 ↑ ⇒ Ω ↓ ?                                        │
│     ✓ 𝒱 ≈ −ΔΩ ?                                          │
│     ✓ มีหน่วย/สเกลชัดเจน?                                 │
└──────────────────────────────────────────────────────────┘
```

---

## 📝 Prompt มาตรฐานสำหรับสั่ง AI อื่น

```
ใน UET: 
- C = openness/communication capacity
- I = closure/friction/dissipation
- ห้ามตีความเป็น consciousness/instinct

ให้ define ผ่าน 𝒱 (observable outcome) ก่อนเสมอ:
- 𝒱 = net value/ordering gain after costs
- Ω = disequilibrium potential
- 𝒱↑ ⇒ Ω↓ 
- ใช้ 𝒱 ≈ −ΔΩ ต่อสเต็ป

กรุณาเสนอ mapping ของโดเมน [X] โดยระบุ:
1. proxy ที่วัดได้สำหรับ 𝒱
2. นิยาม Ω ให้เป็น scalar objective ที่ลดลงเมื่อระบบดีขึ้น
```

---

## 🔗 Related Files

- [KEY_CONCEPTS.md](./KEY_CONCEPTS.md) — Entity/Field/Force/Equilibrium
- [VALUE_EQUATION.md](./VALUE_EQUATION.md) — 𝒱 = -ΔΩ
- [../core/SYMBOL_GLOSSARY.md](../core/SYMBOL_GLOSSARY.md) — Symbol definitions

---

*"C/I มีความหมายต่างกันในแต่ละ domain — แต่สมการเดียวกัน"*
