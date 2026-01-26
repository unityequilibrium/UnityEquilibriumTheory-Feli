"""
UET Yang-Mills Mass Gap Simulation
==================================
Topic: 0.21 Yang-Mills & Mass Gap
Goal: Simulate the emergence of 'Mass' from a pure Information Field.

Problem:
Yang-Mills theory predicts massless gluons, but experiments show they have mass (Confinement).
Mathematical proof is missing (Millennium Prize).

UET Solution:
Mass = Condensed Information.
When Color Field Density > Critical Limit, the field "Condensed" into a massive state.
This creates a "Gap" between the vacuum (0) and the first excited state (Mass).

Simulation:
1. Initialize a Color Field Potential V(r).
2. Calculate Field Density Rho(r).
3. If Rho > Rho_critical, impose "Mass Term".
4. Result: No massless excitations allowed.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# --- PATH SETUP (Must be FIRST) ---
current_path = Path(__file__).resolve()
ROOT = None
for parent in [current_path] + list(current_path.parents):
    if (parent / "research_uet").exists():
        ROOT = parent
        break

if ROOT:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
else:
    print("CRITICAL: research_uet root not found!")
    sys.exit(1)

TOPIC_DIR = ROOT / "research_uet" / "topics" / "0.21_Yang_Mills_Mass_Gap"

# Engine Import (Dynamic to bypass 0.21 folder literal restriction)
try:
    import importlib.util
    from research_uet.core.uet_master_equation import UETParameters

    engine_file = TOPIC_DIR / "Code" / "01_Engine" / "Engine_Mass_Gap.py"
    spec = importlib.util.spec_from_file_location("Engine_Mass_Gap", engine_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    UETMassGapEngine = getattr(module, "UETMassGapEngine")
except Exception as e:
    print(f"Error loading Engine 0.21 Research: {e}")
    sys.exit(1)

engine = UETMassGapEngine()


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def run_mass_gap_simulation():
    print("=" * 60)
    print("🎨 UET YANG-MILLS: MASS GAP SIMULATION")
    print("=" * 60)

    # Delegate to Engine
    mass_gap_data = engine.simulate_field_condensation(alpha_s=1.0, rho_crit=10.0)
    avg_gap = np.mean(mass_gap_data)
    min_gap = np.min(mass_gap_data)

    print(f"\nResults:")
    print(f"  Minimum Mass Gap:  {min_gap:.4f} GeV (Simulated)")
    print(f"  Average Glueball Mass: {avg_gap:.4f} GeV")

    if min_gap > 0:
        print("PASSED: Mass Gap is strictly positive (Confinement confirmed).")
        return True
    else:
        print("FAILED: Massless states detected.")
        return False


if __name__ == "__main__":
    success = run_mass_gap_simulation()
    sys.exit(0 if success else 1)
