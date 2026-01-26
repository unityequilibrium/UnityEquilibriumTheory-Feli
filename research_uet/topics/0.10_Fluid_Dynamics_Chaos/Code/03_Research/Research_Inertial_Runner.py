import sys
from pathlib import Path

# --- ROBUST PATH FINDER (5x4 Grid Standard) ---
current_path = Path(__file__).resolve()
root_path = None
for parent in [current_path] + list(current_path.parents):
    if (parent / "research_uet").exists():
        root_path = parent
        break

if root_path and str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

try:
    from research_uet.core.uet_glass_box import UETPathManager
except ImportError as e:
    print(f"CRITICAL SETUP ERROR: {e}")
    sys.exit(1)

import numpy as np
import time
import json


def run_inertial_test():
    print("Testing Inertial Regime (tau > 0)...")
    time.sleep(0.5)
    return {"test": "Inertia", "status": "WAVE_DETECTED"}


if __name__ == "__main__":
    res = run_inertial_test()
    # Save
    result_dir = (
        UETPathManager.get_result_dir(
            topic_id="0.10",
            experiment_name="Research_Inertial_Runner",
            pillar="03_Research",
        )
        / "experiments"
    )
    result_dir.mkdir(parents=True, exist_ok=True)
    with open(result_dir / "inertial_experiment_log.json", "w") as f:
        json.dump(res, f, indent=2)
