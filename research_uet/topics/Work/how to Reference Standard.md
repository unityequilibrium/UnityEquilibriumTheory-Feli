# 📋 How to: Reference & Output Standards
> "A clean lab is a happy lab."

This document defines the **directory structure standards** for all UET Research Topics (e.g., `0.1_Galaxy...`, `0.20_Atomic...`).

---

## 1. 📂 The Reference Standard (`Ref/`)
**Goal:** Remove clutter. One folder ends.

### ❌ Old Structure (Do NOT use)
Complexity for complexity's sake.
*   `Ref/01_Engine/` (Empty?)
*   `Ref/03_Research/` (Hidden deeper)
*   `Ref/03_Research/black_holes/image.jpg` (Too nested)

### ✅ New Standard (Flat & Clean)
Everything essential is visible at the root of `Ref/`.
```text
Ref/
├── BIBLIOGRAPHY_ANALYSIS.md   # Why these papers matter to UET
├── REFERENCES.py              # Python registry for code integration
├── Download_Ref_Script.py     # Automation script (optional)
└── PDF_Downloads/             # ALL PDF files go here
```

---

## 2. 💾 The Output Standard (`Result/`)
**Goal:** Strict containment. No leaks.

See the dedicated guide for full details:
👉 [`how to Result Standard.md`](./how%20to%20Result%20Standard.md)

**A Quick Summary:**
*   **Target:** `topics/[TopicID]/Result/`
*   **Showcase:** `01_Showcase/` (Social Media, Final Papers)
*   **Figures:** `02_Figures/` (Validation Plots)
*   **Logs:** `_Logs/` (Raw Data)
*   **Code:** Use `category="showcase"` in `UETMetricLogger`.

---

## 3. 🧹 Maintenance
*   **Legacy Folders:** If you see `_Archive` or `compact_galaxies` in `Ref/`, delete them if they are empty or redundant.
*   **Orphaned Logs:** Delete any `data_logs` folder found in the project root.
