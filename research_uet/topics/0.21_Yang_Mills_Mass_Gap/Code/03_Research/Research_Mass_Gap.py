"""
UET Yang-Mills Mass Gap Simulation
==================================
Topic: 0.21 Yang-Mills & Mass Gap
Goal: Simulate the emergence of 'Mass' from a pure Information Field.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import importlib.util
from pathlib import Path

# --- ROBUST IMPORT SETUP ---
script_path = Path(__file__).resolve()
project_root = script_path.parents[5]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from research_uet.core.uet_glass_box import UETPathManager

    # Dynamic Import for Engine (Standard Pattern)
    engine_path = script_path.parents[1] / "01_Engine" / "Engine_Mass_Gap.py"
    spec = importlib.util.spec_from_file_location("Engine_Mass_Gap", engine_path)
    eng_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(eng_mod)
    UETMassGapEngine = eng_mod.UETMassGapEngine
except Exception as e:
    print(f"CRITICAL SETUP ERROR: {e}")
    sys.exit(1)

engine = UETMassGapEngine()


def run_mass_gap_simulation():
    print("=" * 60)
    print("🎨 UET YANG-MILLS: MASS GAP SIMULATION")
    print("=" * 60)

    # Delegate to Engine
    # alpha_s = Coupling Strength, rho_crit = Density Threshold
    mass_gap_data = engine.simulate_field_condensation(alpha_s=1.0, rho_crit=10.0)

    # Analyze
    avg_gap = np.mean(mass_gap_data)
    min_gap = np.min(mass_gap_data)

    print(f"\nResults:")
    print(f"  Minimum Mass Gap:  {min_gap:.4f} GeV (Simulated)")
    print(f"  Average Glueball Mass: {avg_gap:.4f} GeV")

    # --- VISUALIZATION ---
    result_dir = UETPathManager.get_result_dir("0.21", "Mass_Gap_Condensed", "03_Research")

    plt.figure(figsize=(10, 6))
    plt.plot(mass_gap_data, label="Glueball Mass State", color="purple", linewidth=2)
    plt.axhline(y=min_gap, color="r", linestyle="--", label=f"Min Gap: {min_gap:.3f} GeV")
    plt.axhline(y=0, color="k", linestyle="-", linewidth=1)

    plt.title("UET Mass Gap Emergence (Field Condensation)")
    plt.xlabel("Field Sample")
    plt.ylabel("Mass (GeV)")
    plt.legend()
    plt.grid(True, alpha=0.3)

    save_path = result_dir / "Fig_Mass_Gap_Emergence.png"
    plt.savefig(save_path)
    plt.close()
    print(f"  > Visualization Saved: {save_path}")

    if min_gap > 0:
        print("PASSED: Mass Gap is strictly positive (Confinement confirmed).")
        return True
    else:
        print("FAILED: Massless states detected.")
        return False


if __name__ == "__main__":
    success = run_mass_gap_simulation()
    sys.exit(0 if success else 1)
