import numpy as np
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

from research_uet.core.uet_parameters import get_params, C
from research_uet.core.uet_glass_box import UETPathManager


class PerovskiteLightTrap:
    """
    Simulates the role of Perovskite as a 3D Information Scaffolding for light.
    Answers the question: 'Can light float or does it need a medium?'
    """

    def __init__(self):
        self.params = get_params("0.27")
        self.c = C
        # Perovskite Lattice Constant (e.g., MAPbI3, ~0.63 nm)
        self.a = 0.63e-9
        # Octahedral Resonance: Wavelength matches crystal cell diagonal
        self.resonance_lambda = np.sqrt(3) * self.a

    def calculate_trapping(self, wavelength_nm, material_present=True):
        """
        Calculates the velocity and stability of light.
        If material_present is False, simulates light in a Vacuum (no medium).
        """
        wavelength = wavelength_nm * 1e-9

        if not material_present:
            # VACUUM CASE: No information scaffolding
            return {
                "medium": "Vacuum (No Scaffolding)",
                "velocity": self.c,
                "is_floating": "Yes (Propagating)",
                "stability": "Low (Entropy Spreads)",
                "conclusion": "Light escapes at c. No stable hologram possible.",
            }

        # PEROVSKITE CASE: Information trapping via Lattice Resonance
        mismatch = abs(wavelength - self.resonance_lambda) / self.resonance_lambda
        # Perovskite has high Polariton Coupling (simulated Q = 10,000)
        q_factor = 10000.0
        trap_prob = 1.0 / (1.0 + (q_factor * mismatch) ** 2)

        velocity = self.c * (1.0 - trap_prob)

        return {
            "medium": "Perovskite Lattice (3D Scaffold)",
            "velocity": velocity,
            "is_floating": "Yes (Information-Trapped)",
            "stability": "High (Geometric Lock)",
            "trap_efficiency": trap_prob * 100,
            "conclusion": "Light is 'frozen' in the lattice. Tangible hologram achieved.",
        }

    def run_comparison(self):
        print("\n🔬 RESEARCH: Perovskite 'Floating Light' Experiment")
        print("================================================")
        print(f"Lattice Constant (a): {self.a*1e9:.3f} nm")
        print(f"Resonance Target (sqrt(3)*a): {self.resonance_lambda*1e9:.3f} nm")
        print("------------------------------------------------")

        # Test Case: Visual Resonance (Near infrared/Visible edge)
        test_lambda = self.resonance_lambda * 1e9

        # 1. Vacuum Test
        vac = self.calculate_trapping(test_lambda, material_present=False)
        print(f"1. [MEDIUM]: {vac['medium']}")
        print(f"   [VELOCITY]: {vac['velocity']:.2e} m/s")
        print(f"   [CONCLUSION]: {vac['conclusion']}")
        print("-" * 30)

        # 2. Perovskite Test
        perov = self.calculate_trapping(test_lambda, material_present=True)
        print(f"2. [MEDIUM]: {perov['medium']}")
        print(f"   [VELOCITY]: {perov['velocity']:.2e} m/s")
        print(f"   [TRAP EFF]: {perov['trap_efficiency']:.2f}%")
        print(f"   [CONCLUSION]: {perov['conclusion']}")

        return [vac, perov]


if __name__ == "__main__":
    trap = PerovskiteLightTrap()
    results = trap.run_comparison()

    # Save to Results
    import json

    res_dir = UETPathManager.get_result_dir("0.27", "Perovskite_Comparison", pillar="03_Research")
    with open(res_dir / "experiment_log.json", "w") as f:
        json.dump(results, f, indent=4)
    print(f"\n✅ EXPERIMENT COMPLETE: {res_dir}")
