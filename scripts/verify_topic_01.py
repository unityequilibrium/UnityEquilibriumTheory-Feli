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
    / "research_uet/topics/0.1_Galaxy_Rotation_Problem/Code/01_Engine/Engine_Galaxy_V3.py"
)

spec = importlib.util.spec_from_file_location("Engine_Galaxy_V3", engine_path)
mod = importlib.util.module_from_spec(spec)
sys.modules["Engine_Galaxy_V3"] = mod
spec.loader.exec_module(mod)

UETGalaxyEngine = mod.UETGalaxyEngine
GalaxyParams = mod.GalaxyParams


def test_axiomatic_galaxy():
    print("Testing Axiomatic Galaxy Engine (Post-Refactor)")

    # Sample Galaxy: NGC 1560 (Dwarf, Low Density)
    params = GalaxyParams(mass_disk=1.0e9, radius_disk=1.3, mass_bulge=0.0)

    engine = UETGalaxyEngine(params)

    print(f"Galaxy Type: {params.galaxy_type}")
    print(f"M_baryon: {params.mass_disk:.2e} M_sun")
    print(f"Derived Gamma (Axiomatic): {engine.gamma_dynamic:.4f}")
    print(f"Halo Ratio (M_I/M_B): {engine.M_I_ratio:.2f}")
    print(f"Total Info Mass: {engine.M_I_total:.2e} M_sun")

    # Compute curve - wider range to check flat rotation
    radii = np.linspace(0.1, 15.0, 10)
    velocities = engine.compute_curve(radii)

    print("\nRotation Curve:")
    print(f"{'Radius (kpc)':>12} | {'Velocity (km/s)':>16}")
    print("-" * 32)
    for r, v in zip(radii, velocities):
        print(f"{r:>12.2f} | {v:>16.2f}")


if __name__ == "__main__":
    test_axiomatic_galaxy()
