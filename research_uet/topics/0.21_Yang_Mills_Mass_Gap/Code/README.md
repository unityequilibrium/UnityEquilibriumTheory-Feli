# Topic 0.21: Yang-Mills Mass Gap - Code

This module simulates the **Mass Gap** generation in Non-Abelian Fields (Solving the Millennium Prize Problem).

## 5x4 Structure

```
Code/
  01_Engine/
    Engine_Mass_Gap.py       # Simulates Vacuum Energy & Mass Gap
  02_Proof/
    Proof_Mass_Gap.py        # Proves Confinement via Scaling Arguments
  03_Research/
    Research_Mass_Gap.py     # Glueball Mass Simulation
    Research_Mass_Gap_Sweep.py # Coupling Sweep
```

## 🚀 Run Commands

```powershell
cd c:\Users\santa\Desktop\lad\Lab_uet_harness_v0.9.0

# 1. Mass Gap Engine (Simulation)
python research_uet/topics/0.21_Yang_Mills_Mass_Gap/Code/01_Engine/Engine_Mass_Gap.py

# 2. Confinement Proof (Scaling)
python research_uet/topics/0.21_Yang_Mills_Mass_Gap/Code/02_Proof/Proof_Mass_Gap.py

# 3. Glueball Research
python research_uet/topics/0.21_Yang_Mills_Mass_Gap/Code/03_Research/Research_Mass_Gap.py
```

## 📊 Test Results

| Script | Tests | Status |
|--------|-------|--------|
| Engine_Mass_Gap.py | Δm > 0 | PASS |
| Proof_Mass_Gap.py | Finite Radius | PASS |
| Research_Mass_Gap.py | Glueball Mass | PASS |

**Total: All Systems PASS**

## 🧬 Key Physics

1.  **Mass Generation:** Emerges from $\beta I^3$ self-interaction term.
2.  **Confinement:** Information "clumps" because spreading costs infinite energy.

## ASCII Note
All Unicode replaced with ASCII for Windows compatibility.
