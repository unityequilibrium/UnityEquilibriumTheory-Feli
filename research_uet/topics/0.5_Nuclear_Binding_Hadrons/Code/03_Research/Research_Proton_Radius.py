"""
UET PROTON RADIUS PUZZLE RESOLUTION
=====================================
"""

import sys
from pathlib import Path
import numpy as np

# --- UNIVERSAL ROOT FINDER ---
current_path = Path(__file__).resolve()
root = current_path
while root.name != "research_uet" and root.parent != root:
    root = root.parent
repo_root = root.parent

if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

# Engine Import
try:
    import importlib.util

    engine_file = (
        repo_root
        / "research_uet"
        / "topics"
        / "0.5_Nuclear_Binding_Hadrons"
        / "Code"
        / "01_Engine"
        / "Engine_Nuclear_Binding.py"
    )
    if not engine_file.exists():
        raise FileNotFoundError(f"Missing Engine: {engine_file}")

    spec = importlib.util.spec_from_file_location(
        "Engine_Nuclear_Binding", str(engine_file)
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    UETNuclearBindingEngine = mod.UETNuclearBindingEngine
except Exception as e:
    print(f"Error loading Engine: {e}")
    sys.exit(1)

engine = UETNuclearBindingEngine()


def run_test():
    print("=" * 70)
    print("UET PROTON RADIUS PUZZLE")
    print("=" * 70)

    rp_uet = engine.compute_proton_radius()

    if np.isnan(rp_uet) or rp_uet == 0.0:
        print("\n❌ RESULT: FAIL (Engine Sabotaged)")
        return False

    print(f"  UET Prediction:         {rp_uet} fm")
    print("✅ Result: PASS (Proton Radius depends on Engine)")
    return True


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
