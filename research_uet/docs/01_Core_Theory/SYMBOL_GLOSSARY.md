# 📖 UET Symbol Glossary

> **นิยามสัญลักษณ์ทั้งหมดของ UET — Single Source of Truth**  
> **Version**: 0.8.7 | Merged from v0.8.6  
> **Last Updated**: 2026-01-13

---

## 🎯 Purpose

ไฟล์นี้นิยามสัญลักษณ์ทุกตัวที่ใช้ใน UET อย่างเป็นทางการ  
**ทุกเอกสารและ code ต้องอ้างอิงไฟล์นี้**

---

## 📐 Core Symbols

| Symbol | Name | Mathematical Meaning | Physical Interpretation |
|:------:|:-----|:---------------------|:------------------------|
| **C** | Capacity Field / Conscious Field | State Vector C(x,t) | Observable state, Mass, Density |
| **I** | Information Field / Instinctive Field | Entropy/Stimulus field | Hidden state, Structural complexity |
| **J** | Flux Field | J_in - J_out | Open system energy exchange |
| **Ω** | Omega (Equilibrium Functional) | ∫[...] dx | Total disequilibrium (minimize this) |
| **𝒱** | Value | -ΔΩ | Improvement per step |
| **V(C)** | Potential | (α/2)C² + (γ/4)C⁴ | Cost of existence (Higgs-like) |
| **κ** | Kappa (Gradient cost) | |∇C|² coefficient | Surface tension, Space memory |
| **β** | Beta (Coupling) | C·I coefficient | Landauer limit (kT ln 2) |
| **s** | Source/External Drive | External bias term | External force pushing the system |
| **W_N** | Natural Will | |∇Ω| coefficient | Existence persistence drive |

---

## 🔤 Symbol Disambiguation

### c (lowercase) vs C (uppercase)

| Symbol | Meaning | Value/Type |
|:------:|:--------|:-----------|
| **c** | Speed of light | 299,792,458 m/s (constant) |
| **C** | Capacity/Conscious Field | C(x,t) (variable field) |

### I (uppercase) vs i (lowercase)

| Symbol | Meaning | Context |
|:------:|:--------|:--------|
| **I** | Information/Instinctive Field | UET variable |
| **i** | Imaginary unit | Mathematics (√-1) |

---

## 🌐 Multi-Domain Interpretation

### The Key Rule

> **C และ I มีความหมายต่างกันในแต่ละ domain**  
> **แต่ความสัมพันธ์ 𝒱 = -ΔΩ ใช้ได้ทุกที่**

---

### Physics

| Symbol | Interpretation |
|:------:|:---------------|
| **C** | Visible matter, Observable fields |
| **I** | Dark matter, Hidden sectors |
| **β** | Gravitational coupling |
| **κ** | Speed of propagation |
| **Ω** | Energy functional |

---

### Neuroscience

| Symbol | Interpretation |
|:------:|:---------------|
| **C** | Excitatory neural activity |
| **I** | Inhibitory neural state |
| **β** | E-I balance |
| **κ** | Axonal connectivity |
| **Ω** | Neural energy (minimize for stability) |

---

### Economics

| Symbol | Interpretation |
|:------:|:---------------|
| **C** | Market price |
| **I** | Intrinsic/Fundamental value |
| **β** | Market efficiency |
| **κ** | Information spreading |
| **s** | External shocks (news, policy) |
| **Ω** | Market inefficiency |

---

### Biology

| Symbol | Interpretation |
|:------:|:---------------|
| **C** | Activator (morphogen A) |
| **I** | Inhibitor (morphogen B) |
| **β** | Reaction rate |
| **κ** | Diffusion coefficient |
| **Ω** | Systemic stress |

---

### Machine Learning

| Symbol | Interpretation |
|:------:|:---------------|
| **C** | Observable features |
| **I** | Latent representation |
| **β** | Learning rate |
| **κ** | Weight sharing/convolution |
| **Ω** | Loss function |
| **𝒱** | Learning progress |

---

## 📊 Key Relationships

### The Master Equation (v0.8.7)

$$\Omega[C,I,J] = \int d^3x \left[ V(C) + \frac{\kappa}{2}|\nabla C|^2 + \beta C \cdot I + \gamma_J (J_{in} - J_{out}) \cdot C + W_N |\nabla \Omega| + \beta_U V_{game} + \lambda \Sigma (C_i - C_j)^2 \right]$$

### The Value Equation

$$\mathcal{V} = -\Delta\Omega$$

**Meaning**: เมื่อ Ω ลด → ระบบได้ Value (𝒱) เพิ่ม

---

## ⚠️ Common Mistakes

| ❌ Wrong | ✅ Correct |
|:---------|:----------|
| C = consciousness | C = Capacity/Communication field |
| I = instinct | I = Information/Insulation field |
| "Universe is information" | "Information is a calculation tool" |
| UET predicts the future | UET simulates for preparation |

---

## 🔗 Related Files

- [`MATH_SPECIFICATION.md`](./MATH_SPECIFICATION.md) — Full mathematical details
- [`../Doc/DOMAIN_MAPPING.md`](../Doc/DOMAIN_MAPPING.md) — Extended domain mappings
- [`../Doc/KEY_CONCEPTS.md`](../Doc/KEY_CONCEPTS.md) — Entity/Field/Force/Equilibrium

---

*"สัญลักษณ์เดียว ความหมายหลากหลาย — แต่สมการเดียวกัน"*
