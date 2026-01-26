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
├── PDF_Downloads/             # ALL PDF files go here
└── Data_Source/               # JSON/BIB/TXT data files go here
```

---

## 2. 💾 The Output Standard (`Result/`)
**Goal:** strict containment. No leaks.

### ❌ Banned Behaviors
*   Writing to `research_uet/outputs` (Global Dump).
*   Writing to `research_uet/Result`.
*   Creating timestamped folders *every single run* (e.g., `17691122_Test`, `17691123_Test`).

### ✅ New Standard
*   **Target:** `topics/[TopicID]/Result/[ExperimentName]/`
*   **Mode:** Use `stable=True` in `UETPathManager`.
*   **Logger:** Use `flat_mode=True` in `UETMetricLogger`.

**Example Code:**
```python
output_dir = UETPathManager.get_result_dir(
    topic="0.1_Galaxy",
    name="Rotation_Test",
    stable=True  # <--- CRITICAL: Prevents timestamp flood
)
logger = UETMetricLogger("Rotation_Test", output_dir, flat_mode=True)
```

---

## 3. 🧹 Maintenance
*   **Legacy Folders:** If you see `_Archive` or `compact_galaxies` in `Ref/`, delete them if they are empty or redundant.
*   **Orphaned Logs:** Delete any `data_logs` folder found in the project root.
