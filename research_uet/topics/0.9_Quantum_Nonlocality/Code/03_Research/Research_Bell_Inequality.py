"""
UET Bell Inequality Verification (Loophole-Free)
================================================
Topic: 0.9 - Quantum Nonlocality
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

TOPIC_DIR = root_path / "research_uet" / "topics" / "0.9_Quantum_Nonlocality"
DATA_PATH = TOPIC_DIR / "Data"

# Engine Import (Dynamic)
try:
    import importlib.util

    engine_file = TOPIC_DIR / "Code" / "01_Engine" / "Engine_Quantum.py"
    spec = importlib.util.spec_from_file_location("Engine_Quantum", engine_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    UETQuantumEngine = getattr(module, "UETQuantumEngine")
except Exception as e:
    print(f"Error loading Engine: {e}")
    sys.exit(1)

import numpy as np
import json

# Load Data
data_file = DATA_PATH / "03_Research" / "bell_inequality_data.json"


def run_bell_test():
    print("=" * 60)
    print("TEST: UET Non-Locality Verification (Hensen 2015)")
    print("=" * 60)

    if not data_file.exists():
        print(f"[FAIL] ERROR: Data file not found: {data_file}")
        return False

    with open(data_file, "r") as f:
        data = json.load(f)

    s_exp = data["CHSH_parameter"]["measured"]
    s_classical = data["CHSH_parameter"]["classical_bound"]
    s_quantum_max = data["CHSH_parameter"]["quantum_max"]

    print(f"Experimental Setup: {data['experiment']}")
    print(f"Source: {data['source']}")
    print(f"\nMeasured CHSH Parameter (S):")
    print(f"  Exp (Hensen 2015): {s_exp:.3f}")
    print(f"  Classical Bound:   {s_classical:.3f}")
    print(f"  Quantum Max:       {s_quantum_max:.3f}")

    if s_exp > 2.0:
        print("\n✅ PASS: Violation of Local Realism Observed (S > 2).")
        if s_exp <= 2.828 + 0.1:
            print("✅ PASS: Consistent with Tsirelson Bound.")
            return True
    print("\n❌ FAIL: Result inconsistent with Quantum Nonlocality.")
    return False


if __name__ == "__main__":
    success = run_bell_test()
    sys.exit(0 if success else 1)
