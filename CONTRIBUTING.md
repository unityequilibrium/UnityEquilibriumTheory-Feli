# 🤝 Contributing to Unity Equilibrium Theory

![Status](https://img.shields.io/badge/Tests-100%25_Green-brightgreen)
![Standard](https://img.shields.io/badge/Standard-Triple_Green-success)
![Rigor](https://img.shields.io/badge/Rigor-Zero_Curve_Fitting-orange)

> **"Data is the final arbiter. If the math implies a parameter you cannot derive from first principles, it is wrong."**

---

## 📋 Table of Contents

- [🤝 Contributing to Unity Equilibrium Theory](#-contributing-to-unity-equilibrium-theory)
  - [📋 Table of Contents](#-table-of-contents)
  - [🌟 The "Triple-Green" Standard](#-the-triple-green-standard)
  - [⚖️ Scientific Integrity Laws](#️-scientific-integrity-laws)
    - [1. Zero Curve Fitting (The "Iron Rule")](#1-zero-curve-fitting-the-iron-rule)
    - [2. No "Shadow Math"](#2-no-shadow-math)
    - [3. Real Data Mandate](#3-real-data-mandate)
  - [🏗️ The 5x4 Grid Architecture](#️-the-5x4-grid-architecture)
  - [� Coding Standards (OpSec \& Portability)](#-coding-standards-opsec--portability)
    - [1. Robust Path Finding (`UETPathManager`)](#1-robust-path-finding-uetpathmanager)
    - [2. Robust Imports](#2-robust-imports)
    - [3. Visual Evidence](#3-visual-evidence)
  - [� Workflow: Adding a New Topic](#-workflow-adding-a-new-topic)
  - [� Glass Box \& Logging](#-glass-box--logging)

---

## 🌟 The "Triple-Green" Standard

Every Topic in UET (e.g., `0.1_Galaxy_Rotation`) MUST achieve 3 badges to be considered "Complete":

1.  **[Status: PASS]** - All validation scripts pass with high accuracy vs real data.
2.  **[Standard: Extreme Simplicity]** - Code is readable, minimal, and fully transparent.
3.  **[Architecture: 5x4 Grid]** - File structure strictly follows the 5-layer model.

If a PR breaks any of these, it will be rejected.

---

## ⚖️ Scientific Integrity Laws

### 1. Zero Curve Fitting (The "Iron Rule")
You are **FORBIDDEN** from introducing "tuned parameters" (e.g., `fudge_factor = 1.25`) to match data.
*   **Allowed:** Constants derived from Physics (G, c, h) or UET Core (Kappa=0.05, Beta=0.1).
*   **Prohibited:** Arbitrary multipliers used to fix errors for a specific dataset.

### 2. No "Shadow Math"
*   **Definition:** Hiding physics calculations inside `helper.py` or obscure loops while the main script looks clean.
*   **Rule:** All Physics Logic (The Master Equation) MUST be visible in `01_Engine` or the Main Research Script.

### 3. Real Data Mandate
*   **Rule:** Every topic must validate against **EXTERNAL** peer-reviewed data (SPARC, LIGO, CERN).
*   **Proof:** You must include the DOI reference in the `README.md` and the data file in `Data/`.

---

## 🏗️ The 5x4 Grid Architecture

Every Topic must follow this EXACT folder structure:

```
0.XX_Topic_Name/
│
├── Code/                   # The Logic Layer
│   ├── 01_Engine/          # Core Physics Class (Reusable)
│   ├── 02_Proof/           # Mathematical Derivations
│   ├── 03_Research/        # Main Validation Scripts (Real Data)
│   └── 04_Competitor/      # Comparison vs Standard Model
│
├── Data/                   # The Evidence Layer
│   └── (CSV/JSON files from external sources)
│
├── Doc/                    # The Narrative Layer
│   ├── ANALYSIS_Template.md
│   └── (Theory explanations)
│
├── Ref/                    # The Citation Layer
│   ├── References.bib      # DOIs and Metadata
│   └── *.pdf               # Original Research Papers
│
└── Result/                 # The Proof Layer
    └── (Generated PNG/PDFs from Code/)
```

---

## � Coding Standards (OpSec & Portability)

### 1. Robust Path Finding (`UETPathManager`)
**NEVER** use hardcoded paths (e.g., `C:/Users/...`). Use the Glass Box Path Manager:
```python
from research_uet.core.uet_glass_box import UETPathManager

# Correct way to save a result
result_dir = UETPathManager.get_result_dir("0.1", "Experiment_Name")
plt.savefig(result_dir / "Figure_1.png")
```

### 2. Robust Imports
Use dynamic imports where possible to avoid rigid folder dependencies.
```python
# Standard UET Import Block
import sys
from pathlib import Path
root = Path(__file__).resolve().parents[3] # Adjust depth as needed
sys.path.append(str(root))
```

### 3. Visual Evidence
Every **Research Script** must output a **Visualization** (PNG) to `Result/`. 
*   Text-only output is considered "Draft".
*   "Silent Scripts" (no output) are considered "Broken".

---

## � Workflow: Adding a New Topic

1.  **Scaffold**: Create the 5x4 Grid folders.
2.  **Ingest**: Download real data to `Data/`.
3.  **Engine**: Write `Engine_TopicName.py` implementing the Master Equation.
4.  **Research**: Write `Research_TopicName.py` to run the Engine against Data.
5.  **Visualize**: Plot specific graphs comparing `Prediction` vs `Observation`.
6.  **Document**: Write `README.md` following the **Triple-Green Template**.

---

## � Glass Box & Logging

The system uses a "Flight Recorder" called **Glass Box**.
*   **Log Location**: `data_logs/` (at project root).
*   **Usage**: Heavy simulations (Time-Series) automatically log here.
*   **Policy**: Do not commit large log files to Git. (They are ignored via `.gitignore`).

---

> **By contributing to UET using these standards, you are helping build a verifiable, unified future for physics.**
