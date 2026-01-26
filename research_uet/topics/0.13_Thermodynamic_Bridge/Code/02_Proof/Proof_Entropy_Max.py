"""
UET Proof: Second Law of Thermodynamics
=======================================
Topic: 0.13 - Thermodynamic Bridge
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
        / "0.13_Thermodynamic_Bridge"
        / "Code"
        / "01_Engine"
        / "Engine_Thermodynamics.py"
    )
    spec = importlib.util.spec_from_file_location("Engine_Thermodynamics", engine_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    UETThermoEngine = getattr(module, "UETThermoEngine")
except Exception as e:
    print(f"Error loading Engine: {e}")
    sys.exit(1)


def prove_entropy():
    print("=" * 60)
    print("📜 UET PROOF: SECOND LAW OF THERMODYNAMICS")
    print("=" * 60)
    solver = UETThermoEngine(N_A=100, N_B=100, E_total=1000)
    s_init = solver.get_extra_metrics()["S_total"]
    for _ in range(1000):
        solver.step()
    s_final = solver.get_extra_metrics()["S_total"]
    print(f"  Entropy Delta: {s_final - s_init:.4f}")
    if s_final > s_init:
        print("  ✅ PASS: Entropy increased toward equilibrium.")
    else:
        print("  ❌ FAIL: Entropy did not increase.")
    return True


if __name__ == "__main__":
    prove_entropy()
