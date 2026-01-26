"""
Test: Gravitational Constant G
==============================
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

# Engine Import via Importlib to avoid SyntaxError with '0.19'
try:
    import importlib.util

    engine_file = (
        repo_root
        / "research_uet"
        / "topics"
        / "0.19_Gravity_GR"
        / "Code"
        / "01_Engine"
        / "Engine_Gravity_GR.py"
    )
    if not engine_file.exists():
        raise FileNotFoundError(f"Missing Engine: {engine_file}")

    spec = importlib.util.spec_from_file_location("Engine_Gravity_GR", str(engine_file))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    UETGravityEngine = mod.UETGravityEngine
except Exception as e:
    print(f"Error loading Engine: {e}")
    sys.exit(1)

engine = UETGravityEngine()
PLANCK = engine.get_planck_units()


def uet_estimate_G():
    return PLANCK["G"]


def test_gravitational_constant():
    print("=" * 60)
    print("Test: Gravitational Constant G")
    print("=" * 60)

    G_exp = 6.67430e-11
    G_uet = uet_estimate_G()

    if np.isnan(G_uet) or G_uet == 0:
        print("  ❌ FAIL: Engine sabotaged.")
        return False

    error_percent = abs(G_uet - G_exp) / G_exp * 100
    print(f"CODATA 2018: G = {G_exp:.5e}")
    print(f"UET Derived: G = {G_uet:.5e}")
    print(f"Error: {error_percent:.5f}%")

    passed = error_percent < 0.1
    print(f"Result: {'✅ PASS' if passed else '❌ FAIL'}")
    return passed


if __name__ == "__main__":
    success = test_gravitational_constant()
    sys.exit(0 if success else 1)
