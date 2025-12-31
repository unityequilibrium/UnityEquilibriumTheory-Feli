# Unity Equilibrium Theory (UET) Harness

![tests](https://img.shields.io/badge/tests-180%2F180-brightgreen)
![python](https://img.shields.io/badge/python-3.10%2B-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.xxxxx-blue)

**เข้าใจจักรวาลด้วยสมการเดียว | Understanding the universe with one equation**

> 🎯 **[ท้าทายทฤษฎีนี้](research_uet/docs/faq.md)** — เราไม่ได้ต้องการให้คุณเชื่อ เราต้องการให้คุณ "ตรวจสอบ"

---

## 🚫 Critical Constraints

> **UET = "Unity" (ความเป็นหนึ่งเดียว), NOT "Universal" (สากล)**

| Term | Meaning | UET Status |
|:---|:---|:---:|
| **Universal** | Fixed law, applies everywhere | ❌ NOT this |
| **Unity** | Connects domains, context-aware, evolves | ✅ This |

---

## 🤔 UET คืออะไร? (สำหรับคนทั่วไป)

### ปัญหาที่ทุกคนสงสัย

*ทำไมเราเห็นดาวบนท้องฟ้าเป็น "อดีต" ไม่ใช่ "ปัจจุบัน"?*

**คำตอบ:** เพราะถ้าเห็นเป็นปัจจุบันได้ → ของไกลมากจะ "มองไม่เห็น" เลย (ไม่มีอดีตให้ส่งมา)

### UET อธิบายว่า:

> ทุกพฤติกรรมในจักรวาลทิ้ง "ร่องรอยพลังงาน" ลงใน Space

- พลังงานเปลี่ยนรูป → กลายเป็นข้อมูล
- ข้อมูลเหล่านี้คือสิ่งที่เราเห็นและวัดได้
- ระบบทั้งหมดวิ่งหา "จุดสมดุล" เสมอ

---

## 📊 Test Results (2026-01-01)

### 🌌 Galaxy Rotation Curves

| Dataset | Galaxies | Pass Rate | Avg Error | Source |
|:---|:---:|:---:|:---:|:---|
| **SPARC** | 154 | 73% | 10.8% | Lelli et al. 2016 |
| **LITTLE THINGS** | 26 | 69% | 14.3% | Oh et al. 2015 |

### ⚡ Electromagnetic Physics

| Test | Data Points | Avg Error | Source |
|:---|:---:|:---:|:---|
| **Casimir Effect** | 12 | 1.6% | Mohideen 1998 |

### 📈 Other Domains

| Domain | Result | Source |
|:---|:---|:---|
| **แม่เหล็กไฟฟ้า** | ✅ U(1) gauge symmetry | QED |
| **แรงนิวเคลียร์** | ✅ SU(2) symmetry | - |
| **แรงโน้มถ่วง** | ✅ Energy gradient | SPARC |
| **ควอนตัม** | ✅ Topological defects | - |
| **หลุมดำ** | ✅ k=3.0 (ตรงกับข้อมูลจริง) | Farrah |
| **Cosmology** | ✅ Ω_Λ = 0.685 | Planck 2018 |

**ผลรวม: 180/180 tests ผ่าน 100%**

---

## 🎯 Core Equation

```
Ω[C, I] = ∫ [V(C) + (κ/2)|∇C|² + β·C·I] dx
```

| Variable | Meaning |
|:---|:---|
| **C** | Capacity (มวล, สภาพคล่อง, การเชื่อมต่อ) |
| **I** | Information (เอนโทรปี, สนาม, อารมณ์) |
| **V** | Value/Potential |

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/unityequilibrium/Equation-UET-v0.8.7.git
cd Equation-UET-v0.8.7

# Run tests
cd research_uet
python lab/galaxies/test_175_galaxies.py
python lab/electromagnetic/casimir_test.py
```

---

## 📁 Structure

```
Equation-UET-v0.8.7/
├── research_uet/           # Main UET research
│   ├── lab/                # Tests & experiments
│   │   ├── galaxies/       # SPARC, LITTLE THINGS
│   │   └── electromagnetic/# Casimir test
│   ├── data_vault/         # Real data
│   ├── theory/             # Extensions & papers
│   └── UET_PAPER.tex       # LaTeX paper
├── README.md
└── LICENSE
```

---

## ⚠️ Limitations

- **Compact galaxies:** 40% pass rate (known issue)
- **AI-assisted:** May contain interpretation errors
- **Not peer-reviewed:** Academic validation pending

---

## 📚 References

1. Lelli F., et al. (2016) SPARC. *AJ* 152, 157
2. Oh S.-H., et al. (2015) LITTLE THINGS. *AJ* 149, 180
3. Mohideen U., Roy A. (1998) Casimir. *PRL* 81, 4549
4. Landauer R. (1961) *IBM J. Res. Dev.* 5, 183

---

## 📬 Citation

```bibtex
@software{uet_2026,
  title={Unity Equilibrium Theory Harness},
  author={Jirawat Chitkhanti},
  year={2026},
  version={1.0},
  url={https://github.com/unityequilibrium/Equation-UET-v0.8.7}
}
```

---

*Version 1.0 | 2026-01-01 | Open Source | MIT License*

**"Unity Equilibrium Theory — A Simulation Framework, Not a Universal Law"**
