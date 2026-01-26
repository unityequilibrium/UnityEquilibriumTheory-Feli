import numpy as np
import sys
from pathlib import Path
import importlib.util

# Path setup
repo_root = Path("c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7")
sys.path.insert(0, str(repo_root))

# Direct file loading
engine_path = (
    repo_root
    / "research_uet/topics/0.2_Black_Hole_Physics/Code/01_Engine/Engine_BlackHole.py"
)

spec = importlib.util.spec_from_file_location("Engine_BlackHole", engine_path)
mod = importlib.util.module_from_spec(spec)
sys.modules["Engine_BlackHole"] = mod
spec.loader.exec_module(mod)

UETBlackHoleSolver = mod.UETBlackHoleSolver


def test_axiomatic_bh():
    print("Testing Axiomatic Black Hole Engine (Post-Refactor)")

    solver = UETBlackHoleSolver()

    # Check Coupling k
    k = solver.solve_coupling_k()
    print(f"Cosmological Coupling (k): {k:.2f}")

    # Internal Structure Check
    print("\nSimulating Internal Structure:")
    Mass_Msun = 10.0
    radii, pot, safe, r_stable = solver.solve_internal_structure(Mass_Msun=Mass_Msun)

    print(f"Mass: {Mass_Msun} M_sun")
    print(f"Singularity Prevented: {safe}")
    print(f"Stable Radius: {r_stable:.2e} m")

    if k == 3.0:
        print("\n✅ Integrity Check: k is Pure Axiomatic (3.0)")
    else:
        print(f"\n❌ Integrity Check: k is {k} (Expected 3.0)")


if __name__ == "__main__":
    test_axiomatic_bh()
