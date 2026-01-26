# Topic 0.19: Gravity & General Relativity - Code

This module validates the **Thermodynamic Origin of Gravity** and the **Weak Equivalence Principle**.

## 5x4 Structure

```
Code/
  01_Engine/
    Engine_Gravity_GR.py       # Thermodynamic Gravity Solver (Calculates g, r_s)
  02_Proof/
    Proof_Equivalence_Principle.py # Proves m_i = m_g Axiom
  03_Research/
    Research_G_Constant.py     # Validates G against CODATA 2018
```

## Run Commands

```powershell
cd c:\Users\santa\Desktop\lad\Lab_uet_harness_v0.8.7

# 1. Gravity Engine (Thermodynamic Calculation)
python research_uet/topics/0.19_Gravity_GR/Code/01_Engine/Engine_Gravity_GR.py

# 2. Equivalence Principle Proof
python research_uet/topics/0.19_Gravity_GR/Code/02_Proof/Proof_Equivalence_Principle.py

# 3. G Constant Validation
python research_uet/topics/0.19_Gravity_GR/Code/03_Research/Research_G_Constant.py
```

## Test Results

| Script | Tests | Status |
|--------|-------|--------|
| Engine_Gravity_GR.py | Earth/Moon/Sun g | PASS |
| Proof_Equivalence_Principle.py | η = 0.0 (Identity) | PASS |
| Research_G_Constant.py | G Value Consistency | PASS |

**Total: All Systems PASS**

## key Concepts

1.  **Entropic Gravity:** $\mathbf{g} = -c^2 \nabla (\ln \Omega)$
2.  **Equivalence:** Inertia and Gravity act on the same Information Field -> Identity is Tautology.

## ASCII Note
All Unicode replaced with ASCII for Windows compatibility.
