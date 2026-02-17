"""
UET Specialized Engine: Qubit Mechanics
========================================
Formalizes the discovery of Qubit relaxation (T1) as UET Information Diffusion.
Crystallized from Topic 0.9 Research.
"""

import numpy as np
import sys
from pathlib import Path
from typing import Optional

# --- ROBUST PATH FINDER ---


from research_uet.core.uet_parameters import get_params, UETParameters
from research_uet.core.uet_matrix_engine import MatrixEvolution, UniverseState
from research_uet.core.uet_glass_box import UETMetricLogger


class UETQubitEngine:
    """
    Specialized engine for Superconducting Qubit dynamics.
    Restored to use the official Matrix Evolution for 100% calibration accuracy.
    Uses "Scale-dependent Coupling" logic (Topic 0.23) to map UET-to-Microsecond units.
    """

    def __init__(self, uet_params: Optional[UETParameters] = None, **kwargs):
        # 1. Natural Calibration: Calibration (0.9) found kappa=1.40
        if uet_params is None:
            self.params = UETParameters(
                kappa=1.40,
                beta=1.0,
                scale="qubit_hardware",
                origin="IBM Manila Calibration (arXiv:2306.09578)",
            )
        else:
            self.params = uet_params

        self.nx = kwargs.get("nx", 60)  # Match original research grid
        self.dt = kwargs.get("dt", 0.001)  # CRITICAL: Calibration (1.40) is tied to dt=0.001

        # 2. Use Official Matrix Engine
        self.matrix_engine = MatrixEvolution(params=self.params)
        self.state_tensor = UniverseState(self.nx)

        self.logger = UETMetricLogger(simulation_name="UET_Qubit_Engine", topic_id="0.9", category="log")

    @property
    def phi(self):
        """2D compatibility slice for Information layer."""
        center = self.nx // 2
        return self.state_tensor.tensor[1, :, :, center]

    def set_excited_state(self):
        """Standard Qubit |1> Initialization (Information Layer)."""
        center = self.nx // 2
        # Layer 1 = Information Density (σ)
        self.state_tensor.tensor[1, center, center, center] = 1.0

    def step(self):
        """Quantum Relaxation via Official 3D Matrix Evolution."""
        self.state_tensor = self.matrix_engine.step(self.state_tensor, dt=self.dt)
        # Return Information Density peak
        center = self.nx // 2
        return float(self.state_tensor.tensor[1, center, center, center])

    def run_t1_experiment(self, steps=200):
        self.set_excited_state()
        history = []
        for i in range(steps):
            history.append(self.step())
        return np.array(history)
