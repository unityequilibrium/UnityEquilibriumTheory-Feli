"""
UET Superconductivity Experiment: Tc Prediction
===============================================
Tests UET predictions for critical temperature Tc against McMillan 1968 Data.
ALL-IN-ONE: Contains Logic + Data Loading + Verification.
"""

import json
import sys
import math
from pathlib import Path

# --- ROBUST PATH FINDER ---
current_path = Path(__file__).resolve()
ROOT = None
for parent in [current_path] + list(current_path.parents):
    if (parent / "research_uet" / "core").exists():
        ROOT = parent
        break

if ROOT:
    print(f"DEBUG: ROOT found at {ROOT}")
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
        print(f"DEBUG: Added ROOT to sys.path")
else:
    print("CRITICAL: research_uet root not found!")
    sys.exit(1)

repo_root = ROOT

# Correctly cast to Path for division operator
repo_root = Path(repo_root)

try:
    try:
        from research_uet.core.uet_glass_box import UETPathManager, UETMetricLogger
    except ImportError:
        from core.uet_glass_box import UETPathManager, UETMetricLogger
except ImportError as e:
    print(f"CRITICAL SETUP ERROR: {e}")
    sys.exit(1)


import importlib.util

# Use importlib to bypass syntax error with "0.4" in path
engine_path = (
    repo_root
    / "research_uet"
    / "topics"
    / "0.4_Superconductivity_Superfluids"
    / "Code"
    / "01_Engine"
    / "Engine_Superconductivity.py"
)
spec = importlib.util.spec_from_file_location("Engine_Superconductivity", str(engine_path))
engine_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine_mod)
AllenDynesEngine = engine_mod.AllenDynesEngine


class SuperconductivitySolver:
    """Wrapper calling the V3.2 Master Engine."""

    def __init__(self):
        self.engine = AllenDynesEngine(kappa=0.5, beta=0.25)
        self.material_data = {}

    def set_material(self, name, mat_data):
        self.material_data = mat_data
        self.material_data["name"] = name

    def find_critical_temperature(self):
        return self.engine.compute_Tc(
            self.material_data.get("omega_log_K", 100),
            self.material_data.get("lambda_ep", 0.5),
            self.material_data.get("mu_star", 0.12),
            mat_data=self.material_data,
        )

    # =============================================================================
    # PART 2: THE EXPERIMENT (RUN & VERIFY)
    # =============================================================================


def load_tc_data():
    """Load superconductor Tc data."""
    data_path = (
        repo_root
        / "research_uet"
        / "topics"
        / "0.4_Superconductivity_Superfluids"
        / "Data"
        / "03_Research"
        / "comprehensive_superconductor_data.json"
    )
    if data_path.exists():
        with open(data_path) as f:
            data = json.load(f)
            return data.get("superconductors", [])
    else:
        # Fallback Data (McMillan 1968 Subset)
        return [
            {
                "name": "Al",
                "Tc_exp_K": 1.18,
                "omega_log_K": 210,
                "lambda_ep": 0.38,
                "crystal_system": "FCC",
            },
            {
                "name": "Pb",
                "Tc_exp_K": 7.19,
                "omega_log_K": 52,
                "lambda_ep": 1.12,
                "crystal_system": "FCC",
            },
            {
                "name": "Hg",
                "Tc_exp_K": 4.15,
                "omega_log_K": 47,
                "lambda_ep": 1.62,
                "crystal_system": "Rhombohedral",
            },
            {
                "name": "Sn",
                "Tc_exp_K": 3.72,
                "omega_log_K": 128,
                "lambda_ep": 0.60,
                "crystal_system": "BCT",
            },
        ]


def run_experiment():
    print("=" * 60)
    print("UET SUPERCONDUCTIVITY EXPERIMENT")
    print("Data: McMillan 1968")
    print("=" * 60)

    # Initialize Standard Logger
    result_dir_base = UETPathManager.get_result_dir(
        topic_id="0.4",
        experiment_name="Research_Superconductivity",
        pillar="03_Research",
    )
    logger = None
    try:
        logger = UETMetricLogger("Superconductivity_Integrity", output_dir=result_dir_base)
        print(f"📂 Results: {logger.run_dir}")
    except Exception:
        pass

    sc_data = load_tc_data()

    print(f"\n{'Element':<7} | {'Tc_obs':<10} | {'Tc_UET':<10} | {'Error':<6}")
    print("-" * 50)

    total_error = 0
    count = 0
    solver = SuperconductivitySolver()
    results = []

    for mat in sc_data:
        name = mat.get("name", "Unknown")
        # Ensure we have the required UET metadata
        if "crystal_system" not in mat:
            mat["crystal_system"] = "unknown"
        if "atomic_mass" not in mat and "atomic_mass_avg" not in mat:
            mat["atomic_mass"] = 50

        Tc_obs = mat.get("Tc_exp_K", 0)
        solver.set_material(name, mat)
        Tc_uet = solver.find_critical_temperature()

        error = abs(Tc_uet - Tc_obs) / Tc_obs * 100 if Tc_obs > 0 else 0
        status = "✅" if error < 20 else "❌"

        print(f"{name:<12} | {Tc_obs:<8.2f} | {Tc_uet:<8.2f} | {error:<5.1f}% {status}")

        results.append((name, error))
        total_error += error
        count += 1

    if count == 0:
        print("No valid data points.")
        return False

    avg_error = total_error / count
    print("-" * 50)
    print(f"Average Error: {avg_error:.1f}%")

    # Save Final Report
    if logger:
        logger.log_step(
            step=1,
            time_val=1.0,
            omega=1.0,
            extra_metrics={"avg_error": avg_error, "count": count},
        )
        logger.save_report()

    if avg_error < 35:
        print("\n✅ SUCCESS: Structural coherence law verified (Non-empirical).")
        return True
    else:
        print("\n❌ NOTICE: Structural model requires further refinement.")
        return False


if __name__ == "__main__":
    success = run_experiment()
    if success:
        print("\n1/1 PASS")
    sys.exit(0 if success else 1)
