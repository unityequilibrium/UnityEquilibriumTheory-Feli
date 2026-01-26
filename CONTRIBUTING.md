# 🤝 Contributing to Unity Equilibrium Theory

![Status](https://img.shields.io/badge/Tests-127_Scripts-brightgreen)
![Topics](https://img.shields.io/badge/Topics-21_Domains-blue)
![Pass](https://img.shields.io/badge/Pass_Rate-98.4%25-success)

> **"Zero fitted parameters. 23 DOI-verified sources. All results reproducible."**

---

## 📋 Table of Contents

1. [Mission](#-mission)
2. [Core Equation](#-core-equation)
3. [Contribution Standards](#-contribution-standards-strict)
4. [Platinum Standard Checklist](#-platinum-standard-checklist)
5. [Topic Structure](#-topic-structure)
6. [Development Workflow](#-development-workflow)
7. [Code Quality](#-code-quality)
8. [Bug Reports](#-bug-reports)
9. [License](#-license)

---

## 🌟 Mission

### The Problem

Physics is fragmented: General Relativity for stars, Quantum Mechanics for atoms, Standard Model for particles. They don't naturally connect. Dark matter remains undetected after 50+ years.

### The Solution

**Unity Equilibrium Theory (UET)** unifies 21 physics phenomena with one equation:

$$\Omega[C,I] = \int \left[ V(C) + \frac{\kappa}{2}|\nabla C|^2 + \beta C I \right] dx$$

The key insight: **Information has physical cost** (Landauer principle).

---

## 🧮 Core Equation

### Terms Explained

| Term | Symbol | Meaning | Source |
|:-----|:------:|:--------|:-------|
| Equilibrium | V(C) | Cost of deviation | Thermodynamics |
| Gradient | κ|∇C|² | Cost of non-uniformity | Boundary stability |
| **Info-Mass** | βCI | Information = Mass | Landauer (DOI: 10.1147/rd.53.0183) |

### Derived Parameters (NOT FITTED)

| Parameter | Value | Derivation |
|:----------|:------|:-----------|
| κ | 0.1 | Ω minimization |
| β | k_B T ln 2 | Landauer limit |
| Σ_crit | 1.37×10⁹ M☉/kpc² | Holographic Bound |

> ⚠️ **CRITICAL:** All UET parameters are **derived from physics**, never curve-fitted.

---

## 📋 Contribution Standards (STRICT)

### ✅ Accepted

| Type | Requirements |
|:-----|:-------------|
| **New Topic** | Real data + DOI + Test script + Before/After docs |
| **Bug Fix** | Clear description + Test that reproduces bug |
| **Enhancement** | Maintains or improves pass rate |

### ❌ Prohibited

| Type | Reason |
|:-----|:-------|
| ❌ Pure theory | No data validation |
| ❌ Parameter fitting | Breaks derivation principle |
| ❌ Made-up data | Must use external DOI sources |
| ❌ Circular logic | Can't validate against own predictions |

---

## 🏆 Platinum Standard Checklist

### Required for New Topics

- [ ] **README.md** with badges, theory table, results
- [ ] **Code/** with at least one `test_*.py` (PASS outcome)
- [ ] **Real data source/** with `download_*.py` and `DOI_Reference.txt`
- [ ] **Doc/** with `before.md` (problem) and `after.md` (solution)
- [ ] **Result/** with generated plots (PNG)

### Before/After Documentation

Every new topic must document:

**before.md:**
- What is the problem?
- What do existing methods predict?
- Where do they fail?

**after.md:**
- What is the UET solution?
- What are the verified test results?
- What are the limitations?

---

## 📁 Topic Structure

```
topics/0.XX_Topic_Name/
├── README.md                    # Summary with badges
├── Code/
│   ├── test_*.py                # Verification scripts
│   └── __init__.py
├── Real data source/
│   ├── DOI_Reference.txt        # Data citations
│   ├── download_*.py            # Data download script
│   └── data_file.csv/json
├── Doc/
│   ├── before.md                # Problem statement
│   └── after.md                 # UET solution
├── Ref/
│   └── REFERENCES.py            # DOI constants
└── Result/
    └── *.png                    # Generated figures
```

---

## 🛠️ Development Workflow

### 1. Setup

```bash
git clone https://github.com/unityequilibrium/Equation-UET-v0.8.7.git
cd Equation-UET-v0.8.7
pip install -r requirements.txt
```

### 2. Verify Current Tests Pass

```bash
python research_uet/topics/run_all_tests.py
# Expected: 127 tests, 98.4% pass
```

### 3. Create New Topic

```bash
# Create structure
mkdir -p "research_uet/topics/0.XX_New_Topic/{Code,Doc,Real data source,Ref,Result}"

# Create required files
touch "research_uet/topics/0.XX_New_Topic/README.md"
touch "research_uet/topics/0.XX_New_Topic/Code/test_new_topic.py"
touch "research_uet/topics/0.XX_New_Topic/Doc/before.md"
touch "research_uet/topics/0.XX_New_Topic/Doc/after.md"
touch "research_uet/topics/0.XX_New_Topic/Real data source/DOI_Reference.txt"
```

### 4. Implement Test

```python
"""
Test for Topic 0.XX: New Topic
Data: [Source Name]
DOI: [DOI Number]
"""

import numpy as np

def test_new_topic():
    # 1. Load REAL data (with DOI)
    observed = load_real_data()  # Must have DOI reference
    
    # 2. Calculate UET prediction (NO FITTED PARAMETERS)
    predicted = uet_calculation()
    
    # 3. Compare
    error = np.mean(np.abs(predicted - observed) / observed)
    
    # 4. Assert
    assert error < 0.15, f"Error {error:.1%} exceeds 15% threshold"
    print(f"✅ PASS: Error = {error:.2%}")

if __name__ == "__main__":
    test_new_topic()
```

### 5. Update Documentation

After tests pass, update:
- `research_uet/topics/README.md` — Add to topic index
- `research_uet/SINGLE_SOURCE_OF_TRUTH.md` — Add metrics
- `research_uet/DATA_SOURCE_MAP.md` — Add DOI reference

---

## 🔍 Code Quality

### Test Naming

```
test_*.py              # Standard test file
test_4way_comparison.py # Comparison test
test_validation.py     # Validation test
```

### Docstrings Required

```python
"""
Topic X.XX: [Topic Name]
========================
Data Source: [Source]
DOI: [DOI Number]
Expected: [Expected outcome]
"""
```

### Assert Pattern

```python
# Good ✅
assert error < 0.15, f"Error {error:.1%} exceeds threshold"

# Bad ❌
if error < 0.15:
    print("PASS")
```

---

## 🐛 Bug Reports

### Required Information

1. **Script Name:** Which test failed?
2. **Python Version:** `python --version`
3. **Error Log:** Full traceback
4. **Data Context:** Which dataset?

### Issue Template

```markdown
## Bug Report

**Script:** `topics/0.XX.../test_*.py`
**Python:** 3.10.x
**Error:**
```
[Paste full traceback]
```
**Expected:** Test should pass
**Actual:** Test fails with [error]
```

---

## 🤖 AI-Assisted Development

This codebase is developed with AI assistance.

### Transparency Policy

| Aspect | Policy |
|:-------|:-------|
| Code Generation | AI-assisted |
| Scientific Claims | Must be verified by data |
| Review Standard | Data accuracy, not authorship |

### The Final Arbiter

> **The data is the final arbiter of truth, not the author.**

---

## 📜 License

By contributing, you agree your code will be licensed under **MIT License**.

---

## 📚 Essential Reading

| Document | Purpose |
|:---------|:--------|
| [README.md](README.md) | Project overview |
| [research_uet/topics/how to README.md](research_uet/topics/how%20to%20README.md) | README template |
| [research_uet/topics/how to topics and section-test.md](research_uet/topics/how%20to%20topics%20and%20section-test.md) | Topic structure guide |
| [research_uet/CALIBRATION_DECLARATION.md](research_uet/CALIBRATION_DECLARATION.md) | No fitted parameters |

---

*Unity Equilibrium Theory — Testable, Falsifiable, Open*

*[GitHub](https://github.com/unityequilibrium/Equation-UET-v0.8.7)*
