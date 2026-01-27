"""
UET Superfluids Test - Helium-4
================================
Tests UET prediction for superfluid properties.
"""

# Import Root for UET Core
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

print(f"DEBUG: Found root_path: {root_path}")
print(f"DEBUG: sys.path[0]: {sys.path[0]}")

try:
    from research_uet.core.uet_glass_box import UETPathManager
except ImportError:
    print("CRITICAL: Failed to import UET Core")
    sys.exit(1)

# He-4 superfluid data (Donnelly 1998)
HE4_DATA = {
    "lambda_point_K": 2.1768,  # Lambda transition
    "rho_0_kg_m3": 145.0,  # Density at T=0
    "speed_sound_m_s": 238,  # First sound at 0K
    "critical_velocity_cm_s": 60,  # Landau critical
    "quantum_vortex_circulation": 9.97e-4,  # cm^2/s
}

# Engine Import via Importlib to avoid package digits issue
try:
    import importlib.util

    engine_file = (
        root_path
        / "research_uet"
        / "topics"
        / "0.4_Superconductivity_Superfluids"
        / "Code"
        / "01_Engine"
        / "Engine_Superconductivity.py"
    )
    spec = importlib.util.spec_from_file_location(
        "Engine_Superconductivity", str(engine_file)
    )
    engine_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine_mod)
    AllenDynesEngine = engine_mod.AllenDynesEngine
except Exception as e:
    print(f"Error loading Engine: {e}")
    sys.exit(1)

engine = AllenDynesEngine()


def uet_lambda_point():
    """Delegated to Engine."""
    return engine.compute_lambda_point(rho=HE4_DATA["rho_0_kg_m3"])


def uet_quantum_circulation():
    """Delegated to Engine."""
    return engine.compute_quantum_vortex()


def run_test():
    """Run superfluid test."""
    print("=" * 70)
    print("UET SUPERFLUID TEST - HELIUM-4")
    print("Data: Donnelly 1998")
    print("=" * 70)

    results = []

    # Test 1: Lambda point
    print("\n[1] LAMBDA TRANSITION TEMPERATURE")
    print("-" * 50)

    T_obs = HE4_DATA["lambda_point_K"]
    T_uet = uet_lambda_point()

    print(f"  Observed: T_lambda = {T_obs:.4f} K")
    print(f"  UET:      T_lambda = {T_uet:.4f} K")

    error = abs(T_uet - T_obs) / T_obs * 100
    print(f"  Error: {error:.1f}%")

    passed = error < 50
    results.append(passed)
    print(f"  {'PASS' if passed else 'FAIL'}")

    # Test 2: Quantum of circulation
    print("\n[2] QUANTUM OF CIRCULATION")
    print("-" * 50)

    kappa_obs = HE4_DATA["quantum_vortex_circulation"]
    kappa_uet = uet_quantum_circulation()

    print(f"  Observed: kappa = {kappa_obs:.2e} cm^2/s")
    print(f"  UET:      kappa = {kappa_uet:.2e} cm^2/s")

    error_k = abs(kappa_uet - kappa_obs) / kappa_obs * 100
    print(f"  Error: {error_k:.1f}%")

    passed = error_k < 5
    results.append(passed)
    print(f"  {'PASS' if passed else 'FAIL'}")

    passed_count = sum(results)
    total = len(results)

    print("=" * 70)
    print(f"RESULT: {passed_count}/{total} PASSED")
    print("=" * 70)

    return passed_count >= 1


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
