# Topic 0.7: Neutrino Physics - Code

This module covers Neutrino Mass Hierarchy Proofs and PMNS Mixing Simulations.

## 5x4 Structure

```
Code/
  01_Engine/
    Engine_Neutrino.py         # Derives Hierarchy & Geo-Angles
    Engine_Mixing_Neutrino.py  # Simulates Oscillation (Migrated from 0.18)
  03_Research/
    Research_PMNS_Mixing.py    # Validates against NuFIT 5.2 Data
```

## 🚀 Run Commands

```powershell
cd c:\Users\santa\Desktop\lad\Lab_uet_harness_v0.9.0

# 1. Hierarchy Proof & Angle Derivation
python research_uet/topics/0.7_Neutrino_Physics/Code/01_Engine/Engine_Neutrino.py

# 2. Oscillation Simulation (P vs L)
python research_uet/topics/0.7_Neutrino_Physics/Code/01_Engine/Engine_Mixing_Neutrino.py

# 3. PMNS Matrix Validation
python research_uet/topics/0.7_Neutrino_Physics/Code/03_Research/Research_PMNS_Mixing.py
```

## 📊 Test Results

| Script | Tests | Status |
|--------|-------|--------|
| Engine_Neutrino.py | Hierarchy=Normal | PASS |
| Engine_Mixing_Neutrino.py | Oscillation Graph | PASS |
| Research_PMNS_Mixing.py | Angles & CP Phase | PASS |

**Total: All Critical Tests PASS**

## 🧬 Key Physics

```
P(theta) = sin^2(2*theta) * sin^2(1.27*Delta_m^2*L/E)
```

## ASCII Note
All Unicode replaced with ASCII for Windows compatibility.
