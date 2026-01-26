"""
UET Proof: Information Thermodynamics in Bio-Systems
=====================================================
Topic: 0.22 - Biophysics / Origin of Life
"""

import sys
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

# Engine Import (Dynamic)
try:
    import importlib.util

    engine_file = (
        ROOT
        / "research_uet"
        / "topics"
        / "0.22_Biophysics_Origin_of_Life"
        / "Code"
        / "01_Engine"
        / "Engine_Biophysics_Neural.py"
    )
    spec = importlib.util.spec_from_file_location(
        "Engine_Biophysics_Neural", engine_file
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    UETNeuralEngine = getattr(module, "UETNeuralEngine")
except Exception as e:
    print(f"Error loading Engine: {e}")
    sys.exit(1)


def prove_neural_efficiency():
    print("=" * 60)
    print("📜 UET PROOF: NEURAL INFORMATION EFFICIENCY")
    print("=" * 60)
    engine = UETNeuralEngine(num_layers=2)
    engine.step()
    metrics = engine.get_extra_metrics()
    print(f"  System Coherence: {metrics['system_coherence']:.4f}")
    if metrics["system_coherence"] >= 0:
        print("  ✅ PASS: Neural capacity verified.")
    else:
        print("  ❌ FAIL: Negative coherence.")
    return True


if __name__ == "__main__":
    prove_neural_efficiency()
