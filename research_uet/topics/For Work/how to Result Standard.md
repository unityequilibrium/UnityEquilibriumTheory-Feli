# 💾 How to: Result & Output Standard

> **"Code is for Logic. Result is for Evidence."**

This document defines the **Triple-Green Output Standard** for all UET Topics.
It replaces the old "dump everything in one folder" approach.

---

## 1. The Directory Structure (Enforced by Engine)

Every `Result/` folder must follow this exact structure. 
**You do NOT create these folders manually.** The `UETMetricLogger` handles it.

```text
Result/
├── 01_Showcase/        # 🔥 THE BEST STUFF. Final Social Media visuals.
│   └── Research_Galaxy_Curve_Social.png
│
├── 02_Figures/         # 📊 Scientific Plots (Parity plots, basic charts).
│   └── parity_plot_v3.png
│
└── _Logs/             # 🗑️ Raw Dump (Timestamped folders).
    ├── 1769224832_Galaxy_Validation/
    └── 1769224833_Galaxy_Validation/
```

| Category | Folder | Purpose |
| :--- | :--- | :--- |
| **Showcase** | `01_Showcase` | High-quality assets for **Human Consumption** (Papers, Social Media). |
| **Figures** | `02_Figures` | Standard scientific plots for **Validation**. |
| **Logs** | `_Logs` | Raw data dumps for **Machine/Debugging** (Hidden). |

---

## 2. How to Write Code

You must specify the `category` when initializing `UETMetricLogger` or getting a path.

### Case A: Full Logger (Recommended)

```python
# Save to Result/_Logs/TIMESTAMP_Simulation/
logger = UETMetricLogger("Simulation", category="log") 

# Save to Result/01_Showcase/
logger = UETMetricLogger("Simulation", category="showcase") 
```

### Case B: Simple Script (Path Only)

```python
# Get path to Result/01_Showcase
output_dir = UETPathManager.get_result_dir(
    topic_id="0.1", 
    experiment_name="My_Test", 
    category="showcase"
)
plt.savefig(output_dir / "Cool_Image.png")
```

---

## 3. Rules of Engagement

1.  **Do NOT save to Root:** Never save files directly to `Result/`. 
2.  **Naming Matters:** Files in `01_Showcase` must have descriptive names (e.g., `Social_Proof.png`, not `img_01.png`).
3.  **Clean Up:** If `_Logs` gets too big (>1GB), it can be deleted. `01_Showcase` must NEVER be deleted.
