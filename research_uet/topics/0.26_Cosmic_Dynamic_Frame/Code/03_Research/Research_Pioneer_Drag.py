"""
Research_Pioneer_Drag.py
========================
Topic 0.26: The Dynamic Universe
Hypothesis: Pioneer 10/11 deceleration is caused by Cosmic Fluid Drag.

Target Anomaly: a_P = -8.74e-10 m/s^2
Spacecraft Mass: ~250 kg
Velocity: ~12,000 m/s (approx escape velocity at >20 AU)
Area: ~6.0 m^2 (High Gain Antenna facing direction of motion?)
      Note: Antenna points to Earth, motion is away.
      Effective Drag Area depends on angle. Let's assume A ~ 5 m^2.

Physics:
    F_drag = 0.5 * Cd * rho * A * v^2
    a_drag = F_drag / m

Goal:
    Find 'rho' (Cosmic Density) required to match a_P.
    Compare this 'rho' with known Galactic Halo Density (Dark Matter density).

    If rho_required ~= rho_halo, then Dark Matter is just the Drag of the Vacuum!
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# --- ROBUST PATH FINDING ---
current_path = Path(__file__).resolve()
root_path = None
for parent in [current_path] + list(current_path.parents):
    if (parent / "research_uet").exists():
        root_path = parent
        break

if root_path and str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from research_uet.core.uet_glass_box import UETPathManager


def run_pioneer_simulation():
    print("🚀 PIONEER ANOMALY SIMULATION (Topic 0.26)")
    print("Hypothesis: Space is a Fluid. Rockets experience Drag.\n")

    # 1. Constants (Pioneer 10 approx parameters)
    mass = 241.0  # kg (dry mass approx)
    area = 5.0  # m^2 (Effective cross-section)
    velocity = 12000.0  # m/s (Cruise velocity)
    a_target = 8.74e-10  # m/s^2 (The Anomaly to explain)
    Cd = 2.0  # Drag Coeff (Sphere/Plate approx for turbulent wake)

    print(f"Spacecraft Parameters:")
    print(f"  Mass: {mass} kg")
    print(f"  Velocity: {velocity} m/s")
    print(f"  Target Deceleration: {a_target:.2e} m/s^2")

    # 2. Solver: Find necessary Density (rho)
    # a = (0.5 * Cd * rho * A * v^2) / m
    # rho = (2 * m * a) / (Cd * A * v^2)

    rho_required = (2 * mass * a_target) / (Cd * area * velocity**2)

    print(f"\n🧪 CALCULATION:")
    print(f"  Required Cosmic Density (rho): {rho_required:.4e} kg/m^3")

    # 3. Validation: Compare with Benchmarks
    # A. Interstellar Medium (ISM): ~1 atom/cm^3 ~ 1.67e-27 kg / 1e-6 m^3 = 1.67e-21 kg/m^3
    # B. Dark Matter Halo (Standard Model): ~0.3 GeV/cm^3 ~ 5e-25 kg/m^3
    # C. UET Fluid Density (Effective): ???

    benchmarks = {
        "Interstellar Medium (ISM)": 1.0e-21,
        "Dark Matter Halo (Near Earth)": 5.3e-22,
        "Sufficiently Dense Nebula": 1.0e-18,
        "Perfect Vacuum": 0.0,
    }

    print("\n📊 BENCHMARK COMPARISON:")
    match_found = False
    best_match = None
    min_diff = float("inf")

    for name, val in benchmarks.items():
        diff = abs(np.log10(rho_required) - np.log10(val)) if val > 0 else 999
        print(f"  vs {name}: {val:.2e} (Log Diff: {diff:.2f})")

        if diff < 1.0:  # Within 1 order of magnitude
            match_found = True
            best_match = name

        if diff < min_diff:
            min_diff = diff
            best_match_all = name

    # 4. Result Interpretation
    print(f"\n🔍 CONCLUSION:")
    if match_found:
        print(f"✅ MATCH FOUND! The required density matches '{best_match}'.")
        print("   This strongly suggests the anomaly IS drag from this medium.")
    else:
        print(f"❌ NO EXACT MATCH. Required density is closer to '{best_match_all}'.")
        print(
            "   The required density is significantly higher/lower than standard vacuum."
        )

    print("\n📝 IMPLICATION:")
    if rho_required > 1e-20:
        print("   The spacecraft implies a 'Thick' Aether/Fluid.")
    elif rho_required < 1e-24:
        print("   The spacecraft implies a very 'Thin' Medium (Dark Matter range!).")

    # 5. Visualization
    # Plot Acceleration vs Density Range
    densities = np.logspace(-24, -18, 100)
    accels = (0.5 * Cd * densities * area * velocity**2) / mass

    plt.figure(figsize=(10, 6))
    plt.loglog(densities, accels, label="Fluid Drag Law", color="blue")
    plt.axhline(
        y=a_target, color="red", linestyle="--", label="Pioneer Anomaly (8.74e-10)"
    )
    plt.axvline(
        x=rho_required,
        color="green",
        linestyle=":",
        label=f"Required Density ({rho_required:.1e})",
    )

    # Plot Benchmarks
    for name, val in benchmarks.items():
        if val > 0:
            plt.plot(val, (0.5 * Cd * val * area * velocity**2) / mass, "o", label=name)

    plt.xlabel("Cosmic Density (kg/m^3)")
    plt.ylabel("Deceleration (m/s^2)")
    plt.title("Pioneer Anomaly vs Cosmic Fluid Density")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()

    # Save
    result_dir = UETPathManager.get_result_dir(
        "0.26", "Pioneer_Experiment", "03_Research"
    )
    result_dir.mkdir(parents=True, exist_ok=True)
    plot_path = result_dir / "pioneer_density_match.png"
    plt.savefig(plot_path)
    print(f"   Plot saved to: {plot_path}")

    # Save Metadata with results for AI readback
    with open(result_dir / "experiment_result.txt", "w") as f:
        f.write(f"Required_Density: {rho_required:.4e}\n")
        f.write(f"Benchmark_Match: {best_match}\n")
        f.write(f"Anomaly_Explained: {match_found}\n")

    return rho_required


if __name__ == "__main__":
    run_pioneer_simulation()
