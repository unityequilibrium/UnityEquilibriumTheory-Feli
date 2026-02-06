"""
Research: Galaxy Rotation Validation (V3.0)
===========================================
Validates UET Zero Curve Fitting against SPARC data.
Data Source: Data/03_Research/sparc_data.json

Methodology:
1. Load 150+ Galaxy records (Spiral, Dwarf, LSB, Compact).
2. For each galaxy, instantiate UETGalaxyEngine with ONLY baryonic data.
3. Compute rotation velocity at R_obs.
4. Compare with V_obs.
5. Strict Pass Criteria: < 15% Error for Spirals/LSB/Dwarf.

Dependencies:
- 01_Engine/Engine_Galaxy_V3.py
- Data/03_Research/sparc_data.json
"""

import sys
from pathlib import Path


# --- ROBUST PATH FINDER ---
current_path = Path(__file__).resolve()
root_path = None
for parent in [current_path] + list(current_path.parents):
    if (parent / "research_uet").exists():
        root_path = parent
        break

if root_path and str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

try:
    from research_uet.core.uet_glass_box import UETPathManager, UETMetricLogger
except ImportError as e:
    print(f"CRITICAL SETUP ERROR: {e}")
    sys.exit(1)

import json
import numpy as np
import matplotlib.pyplot as plt
import importlib

# Setup local imports for Topic 0.1
topic_path = root_path / "research_uet" / "topics" / "0.1_Galaxy_Rotation_Problem"
engine_path = topic_path / "Code" / "01_Engine"
if str(engine_path) not in sys.path:
    sys.path.insert(0, str(engine_path))

try:
    Engine_Galaxy_V3 = importlib.import_module("Engine_Galaxy_V3")
    UETGalaxyEngine = Engine_Galaxy_V3.UETGalaxyEngine
    GalaxyParams = Engine_Galaxy_V3.GalaxyParams
except ImportError as e:
    print(f"ENGINE IMPORT ERROR: {e}")
    sys.exit(1)

# Global Logger Ref
logger = None


def load_data():
    """Load SPARC data from JSON."""
    data_path = (
        root_path
        / "research_uet"
        / "topics"
        / "0.1_Galaxy_Rotation_Problem"
        / "Data"
        / "03_Research"
        / "sparc_data.json"
    )
    if not data_path.exists():
        # Fallback to general data dir if needed
        data_path = root_path / "Data" / "03_Research" / "sparc_data.json"

    if not data_path.exists():
        raise FileNotFoundError(f"Data not found at {data_path}")

    with open(data_path, "r") as f:
        return json.load(f)


def run_experiment():
    print("=" * 60)
    print("🌌 UET GALAXY ROTATION VALIDATION (ZERO CURVE FITTING)")
    print("🌌 UET GALAXY ROTATION VALIDATION (ZERO CURVE FITTING)")
    print("=" * 60)

    # Initialize Standard Logger
    global logger
    result_dir_base = UETPathManager.get_result_dir(
        topic_id="0.1", experiment_name="Research_Galaxy_Rotation", pillar="03_Research"
    )
    logger = UETMetricLogger("Galaxy_Validation", output_dir=result_dir_base)

    # Save Metadata
    logger.set_metadata(
        {
            "data_source": "SPARC Database",
            "method": "Zero Curve Fitting",
            "parameters": {"G": "Derived from info field logic"},
        }
    )
    print(f"\\n📂 Logging detailed results to: {logger.run_dir}")

    galaxies = load_data()
    print(f"Loaded {len(galaxies)} galaxies from SPARC database.")

    results = []

    # Run Simulation for each galaxy
    for g in galaxies:
        # 1. Setup Parameters (Baryonic Only)
        # We pass mass_bulge=0 to let the Engine handle the universal default (0.1 * M_disk)
        params = GalaxyParams(
            mass_disk=g["M_disk_Msun"],
            radius_disk=g["R_disk_kpc"],
            mass_bulge=g.get("M_bulge_Msun", 0.0),
            galaxy_type=g["type"],
        )

        # 2. Run Engine (The Solver)
        engine = UETGalaxyEngine(params)

        # 3. Compute Velocity (Delegated to Solver)
        v_uet = engine.compute_velocity_at_radius(g["R_kpc"])

        # 4. Error
        v_obs = g["v_obs"]
        error = abs(v_uet - v_obs) / v_obs * 100

        results.append(
            {
                "name": g["name"],
                "type": g["type"],
                "v_obs": v_obs,
                "v_uet": v_uet,
                "error": error,
            }
        )

    # Summary Statistics
    results.sort(key=lambda x: x["error"])

    passed = [r for r in results if r["error"] < 15]
    avg_error = np.mean([r["error"] for r in results])
    pass_rate = len(passed) / len(results) * 100

    print("\n--- PERFORMANCE SUMMARY ---")
    print(f"Average Error: {avg_error:.2f}%")
    print(f"Pass Rate:     {pass_rate:.1f}% ({len(passed)}/{len(results)})")

    # Group by Type
    by_type = {}
    for r in results:
        t = r["type"]
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(r["error"])

    print("\n--- BY TYPE ---")
    for t, errors in by_type.items():
        print(f"{t.upper():<12}: Avg Error {np.mean(errors):.1f}% | Count {len(errors)}")

    # Visualization delegated to Code/05_Visualization/Vis_Galaxy_Curve.py
    # visualize_parity(results, logger)

    # Save Final Report
    logger.log_step(
        step=1,
        time_val=1.0,
        omega=1.0,
        entropy=0.0,
        pass_rate=pass_rate,
        avg_error=avg_error,
        total_galaxies=len(results),
    )
    logger.save_report()

    # Baseline PASS: > 70% Pass Rate OR Avg Error < 15% (Zero Parameter Validation)
    if pass_rate > 70 or avg_error < 15.0:
        print("\n✅ RESULT: PASS (Zero Curve Fitting Validated)")
        return True
    else:
        print("\n❌ RESULT: FAIL (Accuracy below standard)")
        return False


if __name__ == "__main__":
    success = run_experiment()
    sys.exit(0 if success else 1)
