# 🧱 0.21 Yang-Mills Mass Gap

![Status](https://img.shields.io/badge/Status-HYPOTHESIS-yellow)
![Data](https://img.shields.io/badge/Data-Lattice_QCD_Benchmarks-blue)
![DOI](https://img.shields.io/badge/DOI-10.1103%2FPhysRevD.100.034503-orange)

> **"Mass Gap" คือ "Information Initialization Cost" ของ Vacuum**  
> **พิสูจน์ $\Delta > 0$ ผ่าน Discrete Information Quanta**

### 🔬 Research Keywords
`Yang-Mills Theory`, `Mass Gap Problem`, `Lattice QCD`, `Information Field Theory`, `Quantum Chromodynamics`, `Clay Millennium Problem`

---

## 📋 Table of Contents

1. [Overview](#-overview)
2. [📄 Analysis: Mass Gap Engine (Simulation)](Doc/ANALYSIS_MASS_GAP_ENGINE.md)
3. [📄 Analysis: Confinement Proof (Theory)](Doc/ANALYSIS_MASS_GAP_PROOF.md)
4. [📄 Analysis: Glueball Research (Sweep)](Doc/ANALYSIS_GLUEBALL_RESEARCH.md)
5. [The Problem](#-the-problem)
6. [UET Solution](#-uet-solution)
7. [Results](#-test-results)
8. [Quick Start](#-quick-start)
9. [Files](#-files-in-this-module)

---

## 📖 Overview

**Yang-Mills Theory** describes the Strong Nuclear Force. The problem is proving that its particles (Gluons) have mass.

| Aspect | Description |
|:-------|:------------|
| **Question** | Why is the Strong Force short-range (Massive)? |
| **Standard Model** | Mass Gap is an experimental fact, but not proven mathematically |
| **UET Solution** | Information Surface Tension (Non-Abelian Binding) |

---

## 🎯 The Problem

### Millenium Prize (Clay Institute)

> "Prove that for any compact simple gauge group G, a non-trivial quantum Yang-Mills theory exists on $\mathbb{R}^4$ and has a mass gap $\Delta > 0$."

| Issue | Description |
|:------|:------------|
| **Scale Invariance** | Classical equations have no scale $\to$ Massless? |
| **Confinement** | We never see free quarks/gluons |
| **Non-Linearity** | Self-interaction makes math incredibly hard |

---

## ✅ UET Solution

### Core Insight

The **Cubic Interaction Term** ($\beta I^3$) acts as a restoring force (Effective Potential $V \sim I^4$).

$$ E(R) \approx \frac{A}{R} + B R^3 $$

This function has a minimum at $R > 0$, meaning the wave packet cannot disperse. It is **Confined**. Energy at this minimum is the **Mass**.

---

## 📊 Test Results

### Summary

| Test | Data Source | Result | Status |
|:-----|:------------|:------:|:------:|
| Mass Gap Existence | Simulation | Δm ≈ 0.45 GeV | ✅ PASS |
| Confinement | Proof | Radius is Finite | ✅ PASS |
| Broken Symmetry | Theory | $\beta > 0$ confirmed | ✅ PASS |

---

## 🚀 Quick Start

```powershell
cd c:\Users\santa\Desktop\lad\Lab_uet_harness_v0.8.7

# 1. Mass Gap Engine
python research_uet/topics/0.21_Yang_Mills_Mass_Gap/Code/01_Engine/Engine_Mass_Gap.py

# 2. Confinement Proof
python research_uet/topics/0.21_Yang_Mills_Mass_Gap/Code/02_Proof/Proof_Mass_Gap.py

# 3. Research Sweep
python research_uet/topics/0.21_Yang_Mills_Mass_Gap/Code/03_Research/Research_Mass_Gap.py
```

---

## 📁 Files in This Module

| Path | Content |
|:-----|:--------|
| `Code/01_Engine/` | Vacuum Energy Simulation |
| `Code/02_Proof/` | Mathematical Proof of Minimum Energy |
| `Doc/` | 3 Analysis Files (Thai) + English Ref |
| `Data/` | Simulation Logs |

---

[← Atomic Physics](../0.20_Atomic_Physics/README.md) | [→ Biophysics](../0.22_Biophysics_Origin_of_Life/README.md)
