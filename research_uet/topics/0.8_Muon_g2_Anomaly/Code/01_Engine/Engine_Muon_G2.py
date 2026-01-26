"""
Engine: UET Muon g-2 Anomaly Solver
===================================
Central solver for muon anomalous magnetic moment using UET.

Topic: 0.8 Muon g-2 Anomaly
Scale: electroweak (kappa=0.5, beta=1.0)
Standard: Core-compliant (uses uet_parameters.py)
"""

import numpy as np
import sys
from pathlib import Path
from dataclasses import dataclass

# Path setup
Scripts_DIR = Path(__file__).resolve().parent
root_path = None
for parent in [Scripts_DIR] + list(Scripts_DIR.parents):
    if (parent / "research_uet").exists():
        root_path = parent
        break

if root_path and str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

try:
    from research_uet.core.uet_parameters import (
        get_params,
        UETParameters,
        INTEGRITY_KILL_SWITCH,
        ALPHA_EM,
    )
    from research_uet.core.uet_base_solver import UETBaseSolver

    UET_PARAMS = get_params("electroweak")
    KAPPA = UET_PARAMS.kappa
    BETA = UET_PARAMS.beta
except ImportError:
    KAPPA = 0.5
    BETA = 1.0
    ALPHA_EM = 1 / 137.036
    from research_uet.core.uet_base_solver import UETBaseSolver

ALPHA = ALPHA_EM
M_MU = 105.6584  # Muon mass [MeV]
M_E = 0.511  # Electron mass [MeV]

# Experimental Data (Fermilab 2023)
A_MU_EXP = 1.16592061e-3
A_MU_SM = 1.16591810e-3
DELTA_A_EXP = 2.49e-9
DELTA_A_ERR = 0.48e-9


@dataclass
class MuonG2Result:
    a_mu_uet: float
    a_mu_exp: float
    a_mu_sm: float
    delta_a: float
    delta_a_uet: float
    sigma_deviation: float


class UETMuonG2Solver(UETBaseSolver):
    """
    UET Muon g-2 Anomaly Solver.

    Axiomatic Derivation:
    The anomaly Δa_μ is the residual self-information flux of the
    manifold twisted at the electroweak scale (m_μ/M_W).

    Δa_μ(UET) = β × (3/2)² × α² × (m_μ/M_W)² × 4π
    """

    def __init__(self, kappa: float = None, beta: float = None, uet_params=None):
        if uet_params:
            p = uet_params
        else:
            p = UETParameters(
                kappa=kappa if kappa else KAPPA, beta=beta if beta else BETA
            )

        super().__init__(
            nx=1,
            ny=1,
            dt=1.0,
            params=p,
            name="MuonG2Solver",
            topic="0.8_Muon_g-2_Anomaly",
            pillar="01_Engine",
        )

    def calculate_uet_correction(self) -> float:
        if getattr(self, "INTEGRITY_KILL_SWITCH", False):
            return float("nan")

        m_W = 80379.0  # W boson mass [MeV]
        mass_ratio = M_MU / m_W
        spin_factor = 2.25  # (1 + 1/2)^2
        loop_factor = (ALPHA**2) * (mass_ratio**2) * (4 * np.pi)
        return self.params.beta * spin_factor * loop_factor

    def solve(self) -> MuonG2Result:
        delta_a_uet = self.calculate_uet_correction()
        sigma_deviation = abs(delta_a_uet - DELTA_A_EXP) / DELTA_A_ERR
        return MuonG2Result(
            a_mu_uet=A_MU_SM + delta_a_uet,
            a_mu_exp=A_MU_EXP,
            a_mu_sm=A_MU_SM,
            delta_a=DELTA_A_EXP,
            delta_a_uet=delta_a_uet,
            sigma_deviation=sigma_deviation,
        )


def main():
    print("=" * 70)
    print("UET MUON g-2 ENGINE (Standardized)")
    print("=" * 70)
    solver = UETMuonG2Solver()
    result = solver.solve()
    print(f"  Experimental Δa_μ: {result.delta_a:.2e}")
    print(f"  UET Prediction Δa_μ: {result.delta_a_uet:.2e}")
    print(f"  Deviation: {result.sigma_deviation:.2f}σ")
    print("=" * 70)
    return result.sigma_deviation < 2.0


if __name__ == "__main__":
    main()
