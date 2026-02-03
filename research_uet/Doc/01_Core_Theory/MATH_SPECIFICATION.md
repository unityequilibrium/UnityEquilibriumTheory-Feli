# 📐 UET Mathematical Specification

> **Complete mathematical foundation of the Unity Equilibrium Theory**  
> **Version**: 0.8.7 | Merged from v0.9.0 MATH_CORE.md  
> **Status**: Paper-ready

---

## 1. Energy Functional

### 1.1 Single Field (C-only Model)

For a single order parameter field $C(\mathbf{x}, t)$ on a periodic domain $\Omega = [0, L]^d$:

$$\Omega[C] = \int_\Omega \left[ V(C) + \frac{\kappa}{2}|\nabla C|^2 \right] d\mathbf{x}$$

where:
- $V(C)$ is the Landau potential (local bulk energy)
- $\frac{\kappa}{2}|\nabla C|^2$ is the gradient energy (surface tension)

### 1.2 Quartic Landau Potential

$$V(u) = \frac{a}{2}u^2 + \frac{\delta}{4}u^4 - su$$

| Parameter | Physical Meaning | Typical Range |
|:----------|:-----------------|:--------------|
| $a$ | Quadratic coefficient | $a < 0$ for double-well |
| $\delta$ | Quartic coefficient | $\delta > 0$ for boundedness |
| $s$ | External field / tilt | Controls symmetry breaking |

**Critical Points:** For $s = 0$, the minima are at $u^* = \pm\sqrt{-a/\delta}$ when $a < 0$.

### 1.3 Coupled Fields (C-I Model)

For two coupled fields $C(\mathbf{x}, t)$ and $I(\mathbf{x}, t)$:

$$\Omega[C, I] = \int_\Omega \left[ V_C(C) + V_I(I) - \beta C \cdot I + \frac{\kappa_C}{2}|\nabla C|^2 + \frac{\kappa_I}{2}|\nabla I|^2 \right] d\mathbf{x}$$

### 1.4 Full 7-Term Functional (v0.9.0)

$$\Omega[C,I,J] = \int d^3x \left[ \underbrace{V(C)}_{\text{A1}} + \underbrace{\frac{\kappa}{2}|\nabla C|^2}_{\text{A3}} + \underbrace{\beta C \cdot I}_{\text{A2}} + \underbrace{\gamma_J (J_{in} - J_{out}) \cdot C}_{\text{A4}} + \underbrace{W_N |\nabla \Omega|}_{\text{A5}} + \underbrace{\beta_U V_{game}}_{\text{A8}} + \underbrace{\lambda \Sigma (C_i - C_j)^2}_{\text{A10}} \right]$$

---

## 2. Energy Decomposition

$$\Omega = \Omega_{\text{pot}} + \Omega_{\text{coup}} + \Omega_{\text{grad}}$$

| Component | Definition | Physical Meaning |
|:----------|:-----------|:-----------------|
| $\Omega_{\text{pot}}$ | $\int [V_C(C) + V_I(I)] d\mathbf{x}$ | Bulk potential energy |
| $\Omega_{\text{coup}}$ | $\int [-\beta C \cdot I] d\mathbf{x}$ | Coupling energy |
| $\Omega_{\text{grad}}$ | $\int \frac{1}{2}[\kappa_C|\nabla C|^2 + \kappa_I|\nabla I|^2] d\mathbf{x}$ | Gradient (surface) energy |

---

## 3. Dynamics

### 3.1 Gradient Flow (Model A / Allen-Cahn)

$$\frac{\partial C}{\partial t} = -M_C \frac{\delta\Omega}{\delta C} = -M_C \mu_C$$

$$\frac{\partial I}{\partial t} = -M_I \frac{\delta\Omega}{\delta I} = -M_I \mu_I$$

where the chemical potentials are:

$$\mu_C = V'_C(C) - \beta I - \kappa_C \nabla^2 C$$
$$\mu_I = V'_I(I) - \beta C - \kappa_I \nabla^2 I$$

### 3.2 Energy Dissipation (Lyapunov Property)

**Theorem 1 (Energy Monotonicity):** Along solutions of the gradient flow:

$$\frac{d\Omega}{dt} = -\int_\Omega \left[ M_C |\mu_C|^2 + M_I |\mu_I|^2 \right] d\mathbf{x} \leq 0$$

**Corollary:** $\Omega$ is a Lyapunov functional; stationary points are characterized by $\mu_C = \mu_I = 0$.

---

## 4. The Value Equation

### 4.1 Definition

$$\mathcal{V} = -\Delta\Omega$$

**Meaning**: Value is the reduction in disequilibrium per step.

### 4.2 Feedback Loop

```
System (state)  →  Change (action)  →  Did Ω drop? (feedback)
                                              │
                        Yes ──────────────────┼──────────── No
                         ↓                                   ↓
                   System learned                  Something's wrong
                   (𝒱 > 0)                        (check parameters)
```

---

## 5. Stability and Coercivity

### 5.1 Coercivity Condition

**Theorem 2 (Coercivity):** For the quartic potential, $\Omega$ is coercive if and only if:
1. $\delta > 0$ (quartic term positive)
2. $\kappa > 0$ (gradient penalty positive)
3. $|\beta| < \sqrt{\delta_C \delta_I}$ (coupling not too strong)

### 5.2 Numerical Stability

**CFL-type Condition:** For explicit treatment of reaction term:

$$\Delta t \leq \frac{C_{\text{CFL}}}{M \cdot L_V}$$

where $L_V = \sup_{u}|V''(u)|$ is the Lipschitz constant.

---

## 6. Phase Classification

### 6.1 Order Parameter

$$\langle C \rangle = \frac{1}{|\Omega|} \int_\Omega C(\mathbf{x}) d\mathbf{x}$$

### 6.2 Phase Labels

| Phase | Condition | Physical Meaning |
|:------|:----------|:-----------------|
| **BIAS_C** | $\langle C \rangle > \theta$ and $\langle C \rangle > \langle I \rangle$ | C-dominant |
| **BIAS_I** | $\langle I \rangle > \theta$ and $\langle I \rangle > \langle C \rangle$ | I-dominant |
| **SYM** | Otherwise | Symmetric/disordered |

Default threshold: $\theta = 0.1$

---

## 7. Dimensional Analysis

### 7.1 Characteristic Scales

| Quantity | Scale | Expression |
|:---------|:------|:-----------|
| Length | $\xi$ | $\xi = \sqrt{\kappa/|a|}$ (correlation length) |
| Energy | $\epsilon$ | $\epsilon = a^2/\delta$ (barrier height) |
| Time | $\tau$ | $\tau = 1/(M|a|)$ (relaxation time) |

---

## 8. Physical Constants (Production)

From `uet_master_equation.py`:

| Parameter | Symbol | Canonical Value | Physical Origin |
|:----------|:------:|:----------------|:----------------|
| **Landauer Limit** | $\beta$ | $k_B T \ln 2$ | Minimum Energy of Information |
| **Space Cost** | $\kappa$ | $L_P^2 / 4$ | Bekenstein-Hawking Entropy |
| **Vacuum Density** | $\Sigma_{crit}$ | $1.37 \times 10^9 M_\odot/\text{kpc}^2$ | Holographic Bound / $\Lambda$ |
| **Natural Will** | $W_N$ | $0.05$ | Structure Persistence factor |
| **Exchange Rate** | $\gamma_J$ | $0.1$ | Semi-open system flux |

---

## 9. References

1. Landau, L.D. (1937). "On the theory of phase transitions."
2. Ginzburg, V.L. & Landau, L.D. (1950). "On the theory of superconductivity."
3. Allen, S.M. & Cahn, J.W. (1979). "A microscopic theory for antiphase boundary motion."
4. Chen, L.Q. (2002). "Phase-field models for microstructure evolution." *Annu. Rev. Mater. Res.*
5. Bérut, A. et al. (2012). "Experimental verification of Landauer's principle." *Nature.*

---

## 🔗 Related Files

- [`SYMBOL_GLOSSARY.md`](./SYMBOL_GLOSSARY.md) — Symbol definitions
- [`uet_master_equation.py`](./uet_master_equation.py) — Implementation
- [`../Doc/Term-by-Term.md`](../Doc/Term-by-Term.md) — Physical interpretation

---

*"Mathematics is the language; Physics is the meaning"*
