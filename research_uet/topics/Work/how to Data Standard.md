# 💽 How to: Data Standard

> **"Data is the Fuel. Code is the Engine."**

This document defines the standard for the `Data/` directory in every UET Topic.

---

## 1. The Golden Rule
**Data must mirror Code.**
If you have a script in `Code/03_Research/`, its data MUST live in `Data/03_Research/`.

### ❌ WRONG (The "Messy Drawer")
*   `Data/mixed_data.json` (No structure)
*   `Ref/Data_Source/nasa_data.csv` (Don't hide data in Ref!)
*   `Code/myscript_data.txt` (Don't put data in Code!)

### ✅ RIGHT (The 5x4 Mirror)
```text
Data/
├── 01_Engine/       # Constants, Unit Conversions (e.g., uet_constants_v2.json)
├── 02_Proof/        # Analytical benchmarks (e.g., theoretical_values.csv)
├── 03_Research/     # 🔥 REAL WORLD DATA (e.g., sparc_rotation_curves.json)
└── 04_Competitor/   # Baseline data (e.g., standard_model_predictions.csv)
```

---

## 2. File Formats
*   **Preferred:** `.json` (Structured, readable, good for Python `dict`).
*   **Scientific:** `.csv` / `.txt` (For raw arrays/matrices).
*   **Binary:** `.npy` / `.h5` (Only for massive datasets >100MB).

---

## 3. Provenance (Where did it come from?)
Every Data file should ideally have a companion `README.txt` or metadata inside the JSON key `_meta` explaining:
1.  **Source:** (e.g., NASA SPARC Database)
2.  **DOI/Link:** (e.g., doi.org/10.xxxx)
3.  **Date:** When was it downloaded?

---

## 4. Usage in Code
Don't hardcode paths. Use `UETPathManager` to find data dynamically.

```python
# GOOD:
data_root = UETPathManager.get_path("Data", "03_Research")
data_file = data_root / "sparc_data.json"

# BAD:
data_file = "../../../Data/sparc_data.json"
```
