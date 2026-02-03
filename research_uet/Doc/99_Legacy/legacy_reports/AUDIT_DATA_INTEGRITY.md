# 🛡️ Data Integrity Audit: Real vs Synthetic

**Date:** 2026-01-25
**Objective:** Identify and Purge "Hallucinated/Synthetic" Data across all 24 Topics.
**Standard:** All data must be loaded from external sources (JSON/CSV) or cited constants. No `np.random` for core claims.

---

## 🚦 Status Overview (Topics 0.1 - 0.24)

| Topic | Data Status | Verdict | Action Required |
|:---|:---|:---:|:---|
| **0.1 Galaxy** | ✅ Real (SPARC) | **PASS** | None |
| **0.2 Black Hole** | ⚠️ Theoretical | **WARN** | Need Event Horizon Telescope Data? |
| **0.3 Hubble** | ✅ Real (Cosmic Chron) | **PASS** | None |
| **0.4 Supercond** | ✅ Real (NIMS) | **PASS** | None |
| **0.5 Nuclear** | ✅ Real (AME2020) | **PASS** | None |
| **0.6 Electroweak** | ⚠️ Theoretical | **WARN** | Load Particle Masses (PDG) |
| **0.7 Neutrino** | ✅ Real (NuFit 5.2) | **PASS** | None |
| **0.8 Muon g-2** | ⚠️ Theoretical | **WARN** | Load Fermilab Results |
| **0.9 Nonlocality** | ⚠️ Simulation | **WARN** | Load Bell Test Data? |
| **0.10 Fluid** | ✅ Real (Ghia 1982) | **PASS** | None |
| **0.11 Phase** | ✅ Real (NIST Webbook) | **PASS** | None |
| **0.12 Vacuum** | ⚠️ Theoretical | **WARN** | Casimir Effect Data? |
| **0.13 Thermo** | ⚠️ Theoretical | **WARN** | - |
| **0.15 Cluster** | ⚠️ Synthetic | **FAIL** | Load Chandra/X-ray Data |
| **0.16 Heavy Nuclei** | ✅ Real (AME2020) | **PASS** | None |
| **0.17 Mass Gen** | ⚠️ Synthetic | **FAIL** | Load Lepton Masses |
| **0.19 Gravity** | ⚠️ Theoretical | **WARN** | - |
| **0.20 Atomic** | ✅ Real (NIST) | **PASS** | None |
| **0.21 Yang-Mills** | ⚠️ Lattice Sim | **WARN** | Load Lattice QCD Data? |
| **0.22 Biophysics** | ✅ Real (Bonn EEG) | **PASS** | None |
| **0.23 Unity Link** | ⚠️ Mixed (SPARC used) | **Partial** | Formalize Transfer Learning |
| **0.24 AI** | ⚠️ Toy Model | **FAIL** | Load Real LLM Weights/Benchmarks |

---

## 🧹 Purge & Replace Plan (Batch 3)

### Group B: Remaining Purge Targets
The final clusters of "Fake Data" to destroy:

1.  **0.24 AI:** Replace random tokens with actual GPT-2 small weights/outputs.
2.  **0.17 Mass Generation:** Load Koide Formula masses from PDG (Particle Data Group).
3.  **0.15 Cluster Dynamics:** Load Chandra X-ray Profiles (Vikhlinin et al. 2006).

### Group C: Theoretical/Simulation Topics (Audit Only)
Topics like 0.10 (Fluid) and 0.21 (Yang-Mills) are "Simulations" by definition.
*   **Action:** Ensure boundary conditions match standard benchmarks (Ghia 1982 for Fluid).
*   **Status:** 0.10 Fluid is now VALIDATED against Ghia 1982.

---

## 🧪 Implementation Strategy

**ALL** data downloaders must be:
1.  Python Scripts in `Data/`.
2.  Reproducible (URLs or Standard Libraries).
3.  Checked into `Data/Download_Log.json` (New Requirement).
