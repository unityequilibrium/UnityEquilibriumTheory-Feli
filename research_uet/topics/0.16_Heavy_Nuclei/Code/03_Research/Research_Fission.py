"""
UET Research: Nuclear Fission Simulation
========================================
Topic: 0.16 Heavy Nuclei

Simulates the fission of Uranium-235 into Barium-141 and Krypton-92.
Verifies that UET predicts energy release (Exothermic) correctly.

Reaction: n + U-235 -> Ba-141 + Kr-92 + 3n + Energy
"""

import sys
from pathlib import Path

# --- ROBUST PATH FINDER ---
current_path = Path(__file__).resolve()
root_path = None
for parent in [current_path] + list(current_path.parents):
    if (parent / "research_uet").exists():
        root_path = parent
        break

if root_path and str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

# Dynamic Engine Import
try:
    import importlib.util
    engine_file = (
        root_path
        / "research_uet"
        / "topics"
        / "0.16_Heavy_Nuclei"
        / "Code"
        / "01_Engine"
        / "Engine_Heavy_Nuclei.py"
    )
    spec = importlib.util.spec_from_file_location("Engine_Heavy_Nuclei", engine_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    UETHeavyNucleiEngine = getattr(module, "UETHeavyNucleiEngine")
except Exception as e:
    print(f"Engine Import Error: {e}")
    sys.exit(1)

def run_fission_sim():
    print("=" * 60)
    print("☢️  UET RESEARCH: NUCLEAR FISSION (U-235)")
    print("=" * 60)
    
    engine = UETHeavyNucleiEngine()
    
    # Target: U-235
    Z_parent, A_parent = 92, 235
    be_parent = engine.compute_binding_energy(Z_parent, A_parent)
    
    # Products: Ba-141 + Kr-92
    Z_frag1, A_frag1 = 56, 141
    Z_frag2, A_frag2 = 36, 92
    
    be_frag1 = engine.compute_binding_energy(Z_frag1, A_frag1)
    be_frag2 = engine.compute_binding_energy(Z_frag2, A_frag2)
    
    total_be_parent = be_parent
    total_be_products = be_frag1 + be_frag2
    
    energy_released = total_be_products - total_be_parent
    
    print(f"  Parent (U-235) BE:      {be_parent:.1f} MeV")
    print(f"  Products (Ba+Kr) BE:    {total_be_products:.1f} MeV")
    print("-" * 30)
    print(f"  Energy Released:        {energy_released:.1f} MeV")
    
    # Standard output is ~170-200 MeV
    if 100 < energy_released < 250:
        print("\n  ✅ PASS: Fission is Exothermic (Matches Physics)")
        return True
    else:
        print("\n  ❌ FAIL: Energy release out of physical range")
        return False

if __name__ == "__main__":
    run_fission_sim()
