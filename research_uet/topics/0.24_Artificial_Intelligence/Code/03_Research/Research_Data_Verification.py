"""
Research Data Verification (Scientific Standard)
================================================
Topic: 0.24 Artificial Intelligence
Proof: Knowledge Verification as Thermodynamic Equilibrium

Standardization Compliance:
1. Inherits UETBaseSolver (Standard Life Cycle)
2. Uses UETParameters (Beta = Knowledge Pressure)
3. Ingests REAL User Data (foundation_basics.txt)

Methodology:
- Treats the Knowledge Base as a "Gas" of Information tokens.
- A "Query" injects energy (Attention).
- The system must settle into strict Equilibrium (Low Entropy answer) or stay Disordered (High Entropy/Unknown).
"""

import sys
import numpy as np
from pathlib import Path
from typing import Dict, Any, List

# --- ROBUST PATH FINDER (Standard) ---
current_path = Path(__file__).resolve()
root_path = None
for parent in [current_path] + list(current_path.parents):
    if (parent / "research_uet").exists():
        root_path = parent
        break

if root_path and str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

# --- UET CORE IMPORTS ---
from research_uet.core.uet_base_solver import UETBaseSolver
from research_uet.core.uet_parameters import get_params
from research_uet.core.uet_glass_box import UETMetricLogger


class DataVerificationSolver(UETBaseSolver):
    """
    Standardized Knowledge Verification Agent.
    Replaces the ad-hoc 'Research_Real_Data_V2.py'.
    """

    def __init__(self, query: str = "Test", **kwargs):
        super().__init__(
            name="Data_Verification_Protocol",
            topic="0.24_Artificial_Intelligence",
            pillar="03_Research",
            dt=1.0,
            **kwargs,
        )
        self.query = query
        self.knowledge_base = []
        self.matches = []
        self.entropy = 1.0  # Initial Uncertainty
        self.params = get_params("macroscopic")  # Neural/Network scale

        # Locate Foundation Data (User's Brain)
        # Assuming fixed path as per user instruction, or finding relative
        self.data_path = Path(r"c:\Users\santa\Desktop\Data\00_Foundation\foundation_basics.txt")

    def post_step_physics(self):
        """Simulation Lifecycle"""
        step = self.step_count

        if step == 0:
            self._ingest_real_data()
        elif step == 1:
            self._calculate_search_thermodynamics()
        elif step == 2:
            self._verify_equilibrium()

    def _ingest_real_data(self):
        """Step 1: Ingest Matter (Text)"""
        print(f"\n📂 STEP 1: INGESTING KNOWLEDGE BASE...")
        if not self.data_path.exists():
            print(f"❌ Critical Error: Foundation Data not found at {self.data_path}")
            self.entropy = 5.0  # Max Chaos
            return

        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                # Filter noise (comments, empty lines)
                self.knowledge_base = [l.strip() for l in f if l.strip() and not l.startswith("#")]
            print(f"   ► Ingested {len(self.knowledge_base)} knowledge atoms.")
            self.log_metric("knowledge_atoms", len(self.knowledge_base))

        except Exception as e:
            print(f"❌ Error Reading Data: {e}")

    def _calculate_search_thermodynamics(self):
        """
        Step 2: Apply Query Energy
        Equation: E_state = -Match_Score (Higher match = Lower Energy state)
        Prob = exp(-beta * E)
        """
        print(f"\n⚡ STEP 2: APPLYING QUERY ENERGY ('{self.query}')...")
        print(f"   ► Beta (Focus/Temperature): {self.params.beta}")

        if not self.knowledge_base:
            return

        scores = []
        candidates = []

        # Simple Resonance Model (Keyword Overlap)
        query_tokens = set(self.query.lower().split())

        for line in self.knowledge_base:
            # 1. Exact Energy Match (Lowest Energy)
            if self.query == line:
                energy = -200.0  # Perfect Identity
            elif self.query in line:
                energy = -100.0  # Substring Inclusion
            else:
                # 2. Resonance Match (Partial)
                line_tokens = set(line.lower().split())
                overlap = len(query_tokens.intersection(line_tokens))
                energy = -(overlap * 20.0)

            # Background Noise Energy (0)
            if energy > -0.1:
                energy = 0.0

            scores.append(energy)
            candidates.append(line)

        # Calculate Partition Function Z = sum(exp(-beta * E))
        beta = self.params.beta
        # Increase beta for "Adult" focus if needed, but use param default for now

        energies = np.array(scores)
        # Boltzmann Factors
        boltzmann = np.exp(-beta * energies)
        Z = np.sum(boltzmann)

        # Probabilities
        probs = boltzmann / (Z + 1e-10)

        # Calculate Shannon Entropy of the distribution
        # S = - sum(p log p)
        # Filter p > 0
        valid_p = probs[probs > 1e-6]
        self.entropy = -np.sum(valid_p * np.log2(valid_p))

        # Identify Top States (Answers)
        top_indices = np.argsort(probs)[-3:][::-1]  # Top 3

        print(f"   ► Search Entropy: {self.entropy:.4f} bits")

        for idx in top_indices:
            p = probs[idx]
            if p > 0.05:  # Significance threshold
                print(f"   ► [{p*100:.1f}%] {candidates[idx][:60]}...")
                self.matches.append(candidates[idx])

    def _verify_equilibrium(self):
        """Step 3: Verification Verdict"""
        print(f"\n⚖️ STEP 3: EQUILIBRIUM VERIFICATION")

        # Thresholds derived from UET Parameters
        # Gamma = Stability
        stable_entropy = 1.0 / (self.params.gamma + 0.1)
        # Just use simple logic for now: Low entropy = Good

        if self.entropy < 1.0:
            verdict = "VERIFIED FACT"
        elif self.entropy < 2.5:
            verdict = "AMBIGUOUS / RELATED"
        else:
            verdict = "UNKNOWN / CHAOS"

        print(f"   ► Final System State: {verdict}")
        print(f"   ► Entropy: {self.entropy:.4f}")

        self.log_metric("final_entropy", self.entropy)
        self.log_metric("verdict", verdict)


if __name__ == "__main__":
    import argparse

    # Standalone test
    print("🤖 SYSTEM: Initializing Research Data Verification Protocol...")
    # Use a specific full sentence to test "Zero Entropy" (Perfect Equilibrium)
    solver = DataVerificationSolver(query="แมว วิ่ง ความรู้")
    solver.run(steps=3)
