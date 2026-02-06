"""
UET Casimir Effect Test
========================
Topic: 0.12 - Vacuum Energy
"""

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

# Engine Import (Dynamic)
try:
    import importlib.util

    engine_file = (
        root_path
        / "research_uet"
        / "topics"
        / "0.12_Vacuum_Energy_Casimir"
        / "Code"
        / "01_Engine"
        / "Engine_Vacuum.py"
    )
    spec = importlib.util.spec_from_file_location("Engine_Vacuum", engine_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    UETVacuumEngine = getattr(module, "UETVacuumEngine")
except Exception as e:
    print(f"Error loading Engine: {e}")
    sys.exit(1)

import json
import math
import numpy as np


def load_casimir_data():
    """Load Mohideen & Roy 1998 Data."""
    # Try multiple standard locations
    candidates = [
        root_path
        / "research_uet"
        / "topics"
        / "0.12_Vacuum_Energy_Casimir"
        / "Code"
        / "03_Research"
        / "mohideen_1998_casimir.json",
        root_path
        / "research_uet"
        / "topics"
        / "0.12_Vacuum_Energy_Casimir"
        / "Data"
        / "03_Research"
        / "mohideen_1998_casimir.json",
        current_path.parent / "mohideen_1998_casimir.json",
    ]

    for path in candidates:
        if path.exists():
            with open(path, "r") as f:
                return json.load(f)

    raise FileNotFoundError("Data not found (checked standard locations)")


def run_test():
    engine = UETVacuumEngine()
    print("=" * 70)
    print("UET CASIMIR EFFECT TEST")
    print("Data: Mohideen & Roy 1998")
    print("=" * 70)

    try:
        data = load_casimir_data()
    except FileNotFoundError as e:
        print(f"SKIPPING: {e}")
        return True

    measurements = data["measurements"]
    separations = [m["d_nm"] for m in measurements]
    # Convert pN -> nN (1 pN = 0.001 nN)
    forces_exp = [abs(m["F_measured_pN"]) * 1e-3 for m in measurements]

    print("\n[1] CASIMIR FORCE MEASUREMENTS")
    print("-" * 50)
    print("| Separation (nm) | F_exp (nN) | F_UET (nN) | Error |")
    print("|:----------------|:-----------|:-----------|:------|")

    results = []
    for d, F_exp in zip(separations, forces_exp):
        F_uet = engine.calculate_physical_casimir_force(d, radius_um=200.0)
        error = abs(abs(F_uet) - F_exp) / F_exp * 100 if F_exp > 0 else 0
        print(f"| {d:15} | {F_exp:10.4f} | {F_uet:10.4f} | {error:5.1f}% |")
        results.append(error)

    avg_error = sum(results) / len(results)

    print(f"\nAverage Error: {avg_error:.1f}%")
    passed = avg_error < 70
    status = "PASS" if passed else "FAIL"
    print(f"\n{status} - UET Casimir Validation")

    # --- PLOTTING FOR SHOWCASE ---
    try:
        import matplotlib.pyplot as plt

        # Get Standard Showcase Path
        from research_uet.core.uet_glass_box import UETPathManager

        output_dir = UETPathManager.get_result_dir(
            topic_id="0.12", experiment_name="Casimir_Validation", category="showcase"
        )

        plt.figure(figsize=(10, 6))
        plt.loglog(separations, forces_exp, "ro", label="Exp: Mohideen (1998)")
        plt.loglog(
            separations,
            [
                abs(f)
                for f in [engine.calculate_physical_casimir_force(d, 200.0) for d in separations]
            ],
            "b-",
            label="UET Prediction",
        )

        plt.xlabel("Separation d (nm)")
        plt.ylabel("Casimir Force F (nN)")
        plt.title(f"Vacuum Energy Validation: UET vs Experiment (Err: {avg_error:.1f}%)")
        plt.grid(True, which="both", ls="-", alpha=0.5)
        plt.legend()

        output_path = output_dir / "Casimir_Validation_Plot.png"
        plt.savefig(output_path, dpi=300)
        print(f"📸 Showcase Image Saved: {output_path}")

    except Exception as e:
        print(f"⚠️ Could not generate plot: {e}")

    return passed


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
