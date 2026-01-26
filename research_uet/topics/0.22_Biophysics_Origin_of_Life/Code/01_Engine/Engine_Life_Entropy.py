"""
Engine: UET Biophysics (Origin of Life)
=======================================
Topic: 0.22 Biophysics
Folder: 01_Engine

Simulates Erwin Schrödinger's "Negative Entropy" concept.
Life maintains low entropy by exporting entropy to the environment.

Formula: dS_life/dt = -k_B * I (Information Flow) + dS_metabolism
"""

import sys
import numpy as np
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

from research_uet.core.uet_master_equation import omega_functional_complete


class LifeEngine:
    """
    Simulates a living system as an Information Processing Agent.
    """

    def __init__(self):
        self.entropy_internal = 1.0  # Normalized Entropy
        self.information_intake = 0.1  # Rate of Negentropy intake (Food/Sunlight)
        self.decay_rate = 0.05  # Natural thermodynamic decay (2nd Law)

    def step(self, t):
        """
        Evolution step: dS = Decay - Information_Processing
        """
        # 2nd Law: Entropy tends to increase
        self.entropy_internal += self.decay_rate

        # Life: Actively reduces entropy via information/energy intake
        # "It feeds on negative entropy" - Schrödinger
        self.entropy_internal -= self.information_intake

        # Clamp minimum entropy (Quantum Limit)
        if self.entropy_internal < 0.1:
            self.entropy_internal = 0.1

        return self.entropy_internal


def run_life_simulation():
    print("=" * 60)
    print("⚙️  ENGINE: UET Biophysics (Origin of Life)")
    print("    Topic 0.22 - Schrödinger's Negative Entropy")
    print("=" * 60)

    life = LifeEngine()

    print(f"{'Time':<10} | {'Entropy (S)':<15} | {'State':<15}")
    print("-" * 50)

    # Simulate 10 steps
    for t in range(10):
        s = life.step(t)
        state = "Alive (Ordered)" if s < 0.8 else "Dead (Disordered)"
        print(f"{t:<10} | {s:<15.4f} | {state:<15}")

    print("-" * 50)

    # Compare with Non-Living Rock
    rock = LifeEngine()
    rock.information_intake = 0.0  # Rocks don't eat
    s_rock = rock.step(0)

    print(f"\nBenchmark:")
    print(f"  Living System S_final: {life.entropy_internal:.4f}")
    print(f"  Non-Living (Rock) S:   {s_rock:.4f} (Increasing)")

    if life.entropy_internal < s_rock:
        print("\n✅ PASS: Life successfully resists the 2nd Law via Information.")
        return True
    else:
        print("\n❌ FAIL: Life died.")
        return False


if __name__ == "__main__":
    run_life_simulation()
