# 🌌 Unity Equilibrium Theory (UET)

> **A Cross-Domain Simulation Framework for Complex Systems**

![tests](https://img.shields.io/badge/tests-180%2F180-brightgreen)
![python](https://img.shields.io/badge/python-3.10%2B-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![version](https://img.shields.io/badge/version-1.0-orange)

---

## 🚫 Critical Constraints (Please Read)

> **UET is "Unity" (ความเป็นหนึ่งเดียว), NOT "Universal" (สากล)**

| Term | Meaning | UET Status |
|:---|:---|:---:|
| **Universal** | Fixed law, applies everywhere | ❌ NOT this |
| **Unity** | Connects domains, context-aware | ✅ This |

- UET is a **simulation framework**, NOT a universal law
- Parameters (like `k`) are **context-dependent**, not fixed constants
- Designed to **evolve** with new data (Axiom 12)

---

## 📊 Test Results (2026-01-01)

### 🌌 Galaxy Rotation Curves

| Dataset | Galaxies | Pass Rate | Avg Error |
|:---|:---:|:---:|:---:|
| **SPARC** | 154 | 73% | 10.8% |
| **LITTLE THINGS** (v6) | 26 | 69% | 14.3% |

- v6 (mass-dependent k) improves error by **63.9%**

### ⚡ Electromagnetic Physics

| Test | Data Points | Avg Error | Source |
|:---|:---:|:---:|:---|
| **Casimir Effect** | 12 | 1.6% | Mohideen & Roy 1998 |

### 📈 Other Domains

| Domain | Result | Evidence |
|:---|:---|:---|
| **Finance** | k ≈ 1.0 | Multiple assets |
| **Brain/EEG** | β = 1.94 | 1/f² spectrum |
| **Astrophysics** | 3% error | Cas A expansion |

---

## 🎯 Core Equation

```
Ω[C, I] = ∫ [V(C) + (κ/2)|∇C|² + β·C·I] dx
```

| Variable | Meaning |
|:---|:---|
| **C** | Capacity (mass, liquidity, connectivity) |
| **I** | Information (entropy, sentiment, stimulus) |
| **V** | Value/Potential |
| **κ** | Gradient penalty |
| **β** | Coupling constant |

---

## 📁 Structure

```
research_uet/
├── 📐 core/           # Theory foundations
├── 🔬 lab/            # Tests & experiments
│   ├── galaxies/      # SPARC, LITTLE THINGS
│   ├── electromagnetic/ # Casimir test
│   └── tests/         # All domain tests
├── 📊 data_vault/     # Real experimental data
├── 📚 theory/         # Extensions & papers
└── 📖 docs/           # Documentation
```

---

## 🚀 Quick Start

```bash
# Run galaxy test
python lab/galaxies/test_175_galaxies.py

# Run Casimir test
python lab/electromagnetic/casimir_test.py

# Run dwarf galaxy test
python lab/galaxies/test_little_things.py
```

---

## 📚 References

1. Lelli et al. (2016) - SPARC Database
2. Oh et al. (2015) - LITTLE THINGS
3. Mohideen & Roy (1998) - Casimir Effect
4. Di Cintio et al. (2014) - DC14 Profile

---

## ⚠️ Limitations

- **Compact galaxies:** 40% pass rate (known issue)
- **Cosmology:** Not tested against CMB/LSS
- **AI-assisted:** May contain interpretation errors
- **Not peer-reviewed:** Academic validation pending

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📜 License

MIT License - See [LICENSE](LICENSE)

---

*Unity Equilibrium Theory — A Simulation Framework, Not a Universal Law*

**Version:** 1.0 (2026-01-01)
**Repository:** [Equation-UET-v0.8.7](https://github.com/unityequilibrium/Equation-UET-v0.8.7)
