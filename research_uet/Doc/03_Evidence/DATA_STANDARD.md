# 💾 UET Data Standard (The "No-Synthetic" Rule)

> **Core Principle:**
> UET is a scientific theory, not a video game.
> We **DO NOT** make up data (`np.random`).
> We **LOAD** data from verifiable external sources.

---

## 🌍 Approved Data Sources

| Domain | Source | Format | Topic |
|:---|:---|:---|:---|
| **Cosmology** | SPARC (Galaxies), Planck 2018 (CMB) | JSON/CSV | 0.1, 0.3 |
| **Nuclear** | AME2020 (Atomic Mass Evaluation) | TXT | 0.16, 0.5 |
| **Atomic** | NIST Atomic Spectra Database | CSV | 0.20 |
| **Biophysics** | Bonn University EEG Dataset | TXT | 0.22 |
| **Particle** | Particle Data Group (PDG) | CSV | 0.7, 0.17 |

---

## 🚫 Forbidden Functions

The following functions are **BANNED** in `Code/01_Engine` unless used for Monte Carlo Integration (not Data Generation):

*   `np.random.rand()` (for creating fake stars/particles)
*   `random.uniform()` (for making up coefficients)
*   Hardcoded lists like `data = [10, 20, 30]` (Magic Numbers)

---

## 🛠️ formatting

All external data must live in the `Data/` folder of the respective topic.
Every `Data/` folder MUST have a `Download_*.py` script that fetches the data from the internet.

**Example Structure:**
```
0.20_Atomic_Physics/
  Data/
    Download_NIST.py       <-- The Origin
    NIST_Hydrogen.csv      <-- The Evidence
  Code/
    01_Engine/
      Engine_Hydrogen.py   <-- The Consumer
```
