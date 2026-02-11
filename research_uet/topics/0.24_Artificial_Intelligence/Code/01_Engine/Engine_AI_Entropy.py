"""
Engine: UET AI Entropy (Thought Thermodynamics)
===============================================
Topic: 0.24 Artificial Intelligence
Folder: 01_Engine

Measures the 'Quality of Thought' through Entropy.
Hypothesis:
  - Low Entropy (High Order) = Coherent, Logical thought.
  - High Entropy (Disorder) = Hallucination, Confusion.
  - Zero Entropy = Rigid, Repetitive loops (Dead thought).

Optimal Intelligence lies at the 'Critical Point' (Edge of Chaos).
"""

import sys
import numpy as np
import math
from pathlib import Path

# --- ROBUST PATH FINDER ---


# Base Solver Import
try:
    from research_uet.core.uet_base_solver import UETBaseSolver
except ImportError:
    from research_uet.core.uet_base_solver import UETBaseSolver


class AIEntropyEngine(UETBaseSolver):
    """
    Simulates the entropy of token probability distributions.
    """

    def __init__(self):
        super().__init__(name="AI_Thought_Thermodynamics")

    def calculate_entropy(self, probabilities):
        """Shannon Entropy: H = -sum(p * log(p))"""
        probabilities = np.array(probabilities)
        # Avoid log(0)
        probabilities = np.clip(probabilities, 1e-10, 1.0)
        entropy = -np.sum(probabilities * np.log2(probabilities))
        return entropy

    def evaluate_thought_quality(self, entropy):
        """Classifies the state of the AI based on entropy."""
        if entropy < 0.5:
            return "Rigid/Repetitive (Zero Creativity)"
        elif 0.5 <= entropy <= 1.5:
            return "OPTIMAL (Coherent & Creative)"
        elif entropy > 2.5:
            return "Hallucination (Chaos)"
        else:
            return "Average"


def run_ai_entropy_simulation():
    print("=" * 60)
    print("⚙️  ENGINE: UET AI Entropy (Thought Thermodynamics)")
    print("============================================================")

    engine = AIEntropyEngine()

    # Scenarios represented by token variations (e.g., next-token probs)
    scenarios = [
        ("Deterministic (p=1.0)", [1.0, 0.0, 0.0, 0.0]),
        ("High Confidence", [0.8, 0.1, 0.05, 0.05]),
        ("Balanced (Creative)", [0.4, 0.3, 0.2, 0.1]),
        (" confused/Uniform", [0.25, 0.25, 0.25, 0.25]),
        ("Chaotic/Random", [0.1] * 10),  # Flat distribution
    ]

    print(f"{'Scenario':<25} | {'Entropy (H)':<12} | {'Verdict':<30}")
    print("-" * 75)

    for name, probs in scenarios:
        # Normalize just in case
        probs = np.array(probs) / np.sum(probs)
        h = engine.calculate_entropy(probs)
        verdict = engine.evaluate_thought_quality(h)

        print(f"{name:<25} | {h:<12.4f} | {verdict:<30}")

    print("-" * 75)
    print("Conclusion: Intelligence is a thermodynamic optimization process.")
    print("            It seeks to minimize entropy (confusion) while maintaining")
    print("            enough entropy for creativity (avoiding rigidity).")
    return True


if __name__ == "__main__":
    run_ai_entropy_simulation()
