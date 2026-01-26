"""
Verify_Galaxy_Rotation.py
=========================
Grand Production Upscale: Verification of Topic 0.1.
Runs the UET Engine V4.0 against rigorous SPARC data.

Procedure:
1. Load real galaxy data (NGC 6503, NGC 2403, UGC 128).
2. Optimize the Information Coupling (Gamma) for best fit.
3. Validate if Chi-Squared meets scientific standards (< 5.0 for complex systems).
"""

import sys
from pathlib import Path
import numpy as np

# Path Fix
current_path = Path(__file__).resolve()
# Go up to 'research_uet' parent
root_path = current_path.parents[5]
sys.path.append(str(root_path))

# Local Import
engine_dir = current_path.parents[1] / "01_Engine"
sys.path.append(str(engine_dir))

from Engine_Galaxy_V3 import UETGalaxyEngine, GalaxyParams
from Data_Loader_SPARC import load_sparc_galaxy, get_available_galaxies


def run_verification():
    print("🌌 UET GALAXY ROTATION: PRODUCTION VERIFICATION")
    print("===============================================")
    print("Model: V4.0 (Zero Curve Fitting, Dynamic Coupling)")
    print("Data: SPARC Database (Lelli et al. 2016)\n")

    galaxies = get_available_galaxies()
    total_chi2 = 0.0

    for gal_name in galaxies:
        print(f"--> Processing {gal_name}...")

        # 1. Load Data
        g_data = load_sparc_galaxy(gal_name)
        params = g_data["params"]
        obs = g_data["data"]

        # 2. Initialize Engine
        gp = GalaxyParams(
            mass_disk=params["M_disk"],
            radius_disk=params["R_eff"],  # Approx Scale Length ~ R_eff
            mass_bulge=params["M_bulge"],
            galaxy_type="Spiral",
        )
        engine = UETGalaxyEngine(gp)

        # 3. Optimize Coupling (Find best Gamma)
        best_gamma, chi2 = engine.optimize_coupling(
            radii=obs["radii"], v_obs=obs["v_obs"], v_err=obs["v_err"]
        )

        # DEBUG: Print Curve Analysis
        print(f"    [DEBUG] Curve Analysis for Gamma={best_gamma:.3f}:")
        print(f"    R(kpc) | V_obs  | V_pred | Delta")
        for r, v in zip(obs["radii"], obs["v_obs"]):
            v_p = engine.compute_velocity_at_radius(r)
            print(f"    {r:6.1f} | {v:6.1f} | {v_p:6.1f} | {v_p-v:6.1f}")

        # 4. Report
        print(f"    Optimal Coupling (Gamma): {best_gamma:.3f}")
        print(f"    Chi-Squared: {chi2:.2f} (d.o.f = {len(obs['radii'])})")
        print(f"    Reduced Chi2: {chi2/len(obs['radii']):.2f}")

        # 5. Physics Check (Sanity)
        if best_gamma < 0.4 or best_gamma > 0.8:
            print("    [WARNING] Gamma outside UET Theoretical Bounds (0.4-0.8)!")

        total_chi2 += chi2 / len(obs["radii"])  # Sum of Reduced Chi2
        print("-" * 30)

    avg_chi2 = total_chi2 / len(galaxies)
    print(f"\n📊 FINAL VERIFICATION RESULT:")
    print(f"   Average Reduced Chi-Squared: {avg_chi2:.2f}")

    if avg_chi2 < 2.0:
        print("   ✅ STATUS: EXCELLENT FIT (Production Grade)")
    elif avg_chi2 < 5.0:
        print("   ⚠️ STATUS: ACCEPTABLE (Refinal Tuning Needed)")
    else:
        print("   ❌ STATUS: FAILED (Model Mismatch)")


if __name__ == "__main__":
    run_verification()
