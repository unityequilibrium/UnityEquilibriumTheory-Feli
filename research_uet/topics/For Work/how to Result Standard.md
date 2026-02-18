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

You must specify both `topic_id` and `category` when initializing `UETMetricLogger` or getting a path.

### Case A: Full Logger (Recommended)

```python
from research_uet.core.uet_glass_box import UETMetricLogger

# ✅ CORRECT: Use topic_id + category
# Saves to: Result/_Logs/TIMESTAMP_Simulation/
log_logger = UETMetricLogger(
    "Simulation",
    topic_id="0.1",  # Your topic ID
    category="log"
)

# ✅ CORRECT: Use topic_id + category
# Saves to: Result/01_Showcase/
showcase_logger = UETMetricLogger(
    "Simulation",
    topic_id="0.1",  # Your topic ID
    category="showcase"
)

# ✅ CORRECT: Use topic_id + category
# Saves to: Result/02_Figures/
figures_logger = UETMetricLogger(
    "Simulation",
    topic_id="0.1",  # Your topic ID
    category="figures"
)
```

### Case B: Simple Script (Path Only)

```python
from research_uet.core.uet_glass_box import UETPathManager

# ✅ CORRECT: Get path to Result/01_Showcase
output_dir = UETPathManager.get_result_dir(
    topic_id="0.1",
    experiment_name="My_Test",
    category="showcase"
)
plt.savefig(output_dir / "Cool_Image.png")

# ✅ CORRECT: Get path to Result/02_Figures
output_dir = UETPathManager.get_result_dir(
    topic_id="0.1",
    experiment_name="My_Test",
    category="figures"
)
plt.savefig(output_dir / "parity_plot.png")

# ✅ CORRECT: Get path to Result/_Logs/TIMESTAMP_My_Test/
output_dir = UETPathManager.get_result_dir(
    topic_id="0.1",
    experiment_name="My_Test",
    category="log"
)
```

### ❌ WRONG: Legacy Patterns (Deprecated)

```python
# ❌ WRONG: Missing category parameter
logger = UETMetricLogger("Simulation", topic_id="0.1")

# ❌ WRONG: Using output_dir directly (bypasses standard)
result_dir = UETPathManager.get_result_dir("0.1", "Test", pillar="03_Research")
logger = UETMetricLogger("Test", output_dir=result_dir)

# ❌ WRONG: Saving directly to Result/ (not following standard)
plt.savefig("Result/output.png")
```

### Complete Example

```python
from research_uet.core.uet_glass_box import UETMetricLogger

def run_my_research():
    """Example research function with proper logging."""
    # Initialize loggers
    log_logger = UETMetricLogger(
        "My_Research_Logs",
        topic_id="0.1",
        category="log"
    )

    showcase_logger = UETMetricLogger(
        "My_Research_Showcase",
        topic_id="0.1",
        category="showcase"
    )

    figures_logger = UETMetricLogger(
        "My_Research_Figures",
        topic_id="0.1",
        category="figures"
    )

    # Run simulation and log data
    for step in range(100):
        # Your simulation code here
        omega = 1.0
        kinetic = 0.5
        potential = 0.5

        # Log step data (automatically saves to _Logs/)
        log_logger.log_step(
            step=step,
            time=step * 0.1,
            omega=omega,
            kinetic=kinetic,
            potential=potential
        )

        # Save figures every 20 steps
        if step % 20 == 0:
            # Your plotting code here
            # figures_logger.save_figure(plt.gcf(), f"step_{step}.png")
            pass

        # Save showcase every 50 steps
        if step % 50 == 0:
            # Your high-quality visualization code here
            # showcase_logger.save_figure(plt.gcf(), f"showcase_step_{step}.png")
            pass

    # Save reports
    log_logger.set_metadata({
        "topic_id": "0.1",
        "experiment_name": "My_Research",
        "total_steps": 100
    })

    log_logger.save_report()
    showcase_logger.save_report()
    figures_logger.save_report()

    print(f"Logs: {log_logger.run_dir}")
    print(f"Showcase: {showcase_logger.run_dir}")
    print(f"Figures: {figures_logger.run_dir}")
```

---

## 3. Rules of Engagement

1.  **Do NOT save to Root:** Never save files directly to `Result/`. 
2.  **Naming Matters:** Files in `01_Showcase` must have descriptive names (e.g., `Social_Proof.png`, not `img_01.png`).
3.  **Clean Up:** If `_Logs` gets too big (>1GB), it can be deleted. `01_Showcase` must NEVER be deleted.
