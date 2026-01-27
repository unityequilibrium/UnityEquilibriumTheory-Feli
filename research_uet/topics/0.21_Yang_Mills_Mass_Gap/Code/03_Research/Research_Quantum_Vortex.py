"""
Research_Quantum_Vortex.py
==========================
Topic: 0.21 Yang-Mills Mass Gap
Hypothesis: "Mass is the Kinetic Energy of a Stable Quantum Vortex."
Goal: Find the minimum circulation (Gamma) required for stability.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path

# --- ENVIRONMENT SETUP ---
script_path = Path(__file__).resolve()
project_root = script_path.parents[5]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from research_uet.core.uet_glass_box import UETPathManager
except ImportError:
    print("CRITICAL: UET Core not found.")
    sys.exit(1)


def run_research():
    print("🌪️ RESEARCH: QUANTUM VORTEX STABILITY (COUPLING SWEEP)")
    print("-----------------------------------------------------")

    # Parameters
    RHO_VACUUM = 2.9e-16
    VISCOSITY_MU = 1.0e-20

    # Sweep Coupling Efficiency
    couplings = np.logspace(-20, -10, 20)
    gamma = 1.0
    radius = 1e-15
    epsilon = 0.1 * radius

    required_k = None

    # For Plotting
    stable_tracker = []

    print(f"{'Coupling (k)':<20} | {'Status'}")
    print("-" * 40)

    for k in couplings:
        energy = 0.5 * RHO_VACUUM * (gamma**2) * radius
        dt = 0.01
        status = "DEAD"

        # Track energy for one specific interesting case (e.g. near transition)
        energy_history = []

        for t in range(500):
            p_loss = VISCOSITY_MU * (gamma**2) * radius / (epsilon**2)
            p_gain = k * (gamma**4) / radius

            dE = (p_gain - p_loss) * dt
            energy += dE
            energy_history.append(energy)

            if energy <= 0:
                break
            if p_gain > p_loss:
                status = "STABLE"
                break

        print(f"{k:<20.2e} | {status}")

        if status == "STABLE":
            required_k = k
            stable_tracker = energy_history  # Keep the stable trace
            break  # Stop after finding first stable point

    # --- VISUALIZATION ---
    result_dir = UETPathManager.get_result_dir("0.21", "Quantum_Vortex", "03_Research")

    plt.figure(figsize=(10, 6))
    if stable_tracker:
        plt.plot(stable_tracker, label="Vortex Energy (Stable)", color="green")
    else:
        plt.text(0.5, 0.5, "No Stable Vortex Found", ha="center")

    plt.title(f"Quantum Vortex Stability (Coupling k={required_k:.2e})")
    plt.xlabel("Time Step")
    plt.ylabel("Vortex Energy")
    plt.legend()
    plt.grid(True)

    save_path = result_dir / "Fig_Vortex_Stability.png"
    plt.savefig(save_path)
    plt.close()
    print(f"\n  > Visualization Saved: {save_path}")

    print("\n🔍 ANALYSIS:")
    if required_k:
        print(f"✅ STABLE VORTEX created at Coupling k >= {required_k:.2e}")
    else:
        print("❌ Coupling still too weak.")


if __name__ == "__main__":
    run_research()
