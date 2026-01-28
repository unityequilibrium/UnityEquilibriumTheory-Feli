"""
UET Central Parameter Module
============================
Single source of truth for all UET parameters.

Usage:
    from research_uet.core.uet_parameters import get_params, UETParams

    params = get_params("electroweak")
    print(params.kappa, params.beta)

Author: UET Research Team
Version: 0.8.7
Last Updated: 2026-01-13
"""

import os
from dataclasses import dataclass
from typing import Literal

# =============================================================================
# GLOBAL INTEGRITY KILL SWITCH (The Truth Auditor)
# =============================================================================
# Set environment variable UET_KILL_ENGINE=TRUE to bypass all calculation logic.
# If active, all Engines will return invalid results (0.0 or NaN).
# Research scripts that PASS while this is active are guilty of SHADOW MATH.
INTEGRITY_KILL_SWITCH = os.getenv("UET_KILL_ENGINE", "FALSE").upper() == "TRUE"

# =============================================================================
# FUNDAMENTAL CONSTANTS (CODATA 2018 / SI Exact)
# =============================================================================

HBAR = 1.054571817e-34  # Planck constant [J·s]
C = 299792458  # Speed of light [m/s]
G = 6.67430e-11  # Gravitational constant [m³/kg/s²]
K_B = 1.380649e-23  # Boltzmann constant [J/K]
ALPHA_EM = 1 / 137.035999  # Fine structure constant
M_SUN = 1.98847e30  # Solar Mass (kg) [IAU 2015]
H = 6.62607015e-34  # Planck constant [J·s]
E_CHARGE = 1.602176634e-19  # Elementary charge [C]
M_ELECTRON = 9.1093837015e-31  # Electron mass [kg]
EPSILON_0 = 8.8541878128e-12  # Vacuum permittivity [F/m]

# --- UET UNIT CONVERSIONS ---
C_KM_S = C / 1000.0  # Speed of light [km/s]
G_GALACTIC = 4.301e-6  # kpc (km/s)² / M_sun (Standardized UET Value)
RHO_COSMIC = 2.9e-16  # kg/m^3 (UET Vacuum Density - Pioneer/Fluid Frame)
H0 = 67.4  # km/s/Mpc (Planck 2018 - Global Baseline)

# --- UET BRIDGE CONSTANTS ---
FLUID_MOBILITY_BRIDGE = 1750.0  # Derived Informational-Physical Bridge for Topic 0.10

# Derived Planck units
L_PLANCK = (HBAR * G / C**3) ** 0.5  # Planck length
M_PLANCK = (HBAR * C / G) ** 0.5  # Planck mass
T_PLANCK = L_PLANCK / C  # Planck time

# =============================================================================
# UET SCALE-DEPENDENT PARAMETERS
# =============================================================================


@dataclass(frozen=True)
class UETParameters:
    """
    Authoritative container for UET parameters at a given scale.
    Matches the requirements of the UET Master Equation (All 12 Axioms).
    """

    kappa: float  # Gradient penalty (A3)
    beta: float  # Coupling constant (A2)
    alpha: float = 1.0  # Equilibrium stiffness (A1)
    gamma: float = 0.025  # Nonlinear stability (A1)
    C0: float = 1.0  # Vacuum Expectation Value (A1)
    gamma_J: float = 0.1  # Exchange rate (A4)
    W_N: float = 0.05  # Natural Will (A5)
    lambda_coherence: float = 0.01  # Layer coherence (A10)

    # === Astrophysical Constants (A7: Pattern Recurrence) ===
    RHO_UNITY: float = 5e7  # M_sun / kpc^3 (Pivot density)
    RATIO_0: float = 8.5  # Universal Halo Ratio pivot
    GAMMA_UET: float = 0.48  # Thermodynamic scaling index

    # === Context ===
    temperature: float = 293.15  # Kelvin
    scale: str = ""  # Scale name
    origin: str = ""  # Derivation source

    def __post_init__(self):
        """Standard detections for sabotaged parameters."""
        if INTEGRITY_KILL_SWITCH:
            # We must use object.__setattr__ because the dataclass is frozen
            for field_name in ["kappa", "beta", "alpha", "gamma", "C0"]:
                object.__setattr__(self, field_name, 0.0)


# Define parameters for each physical scale
_SCALE_PARAMS = {
    # =========================================================================
    # PLANCK SCALE: Black holes, Quantum gravity
    # κ = 0.5 from Bekenstein-Hawking entropy: S = A/(4ℓ_P²)
    # =========================================================================
    "planck": UETParameters(
        kappa=0.5, beta=1.0, scale="planck", origin="Bekenstein bound (theory)"
    ),
    # =========================================================================
    # ELECTROWEAK SCALE: Particle physics, W/Z bosons, Higgs
    # Default theoretical values
    # =========================================================================
    "electroweak": UETParameters(
        kappa=0.5, beta=1.0, scale="electroweak", origin="Natural coupling O(1)"
    ),
    # =========================================================================
    # NUCLEAR SCALE: QCD, Strong force, Hadrons
    # κ calibrated to match α_s(M_Z) = 0.1179
    # =========================================================================
    "nuclear": UETParameters(
        kappa=0.57, beta=1.0, scale="nuclear", origin="Calibrated to α_s(M_Z)"
    ),
    # =========================================================================
    # ASTROPHYSICAL SCALE: Galaxy rotation, Clusters
    # κ = 0.1 from SPARC database (175 galaxies)
    # β = κ/2 from geometric derivation
    # =========================================================================
    "astrophysical": UETParameters(
        kappa=0.1,
        beta=0.05,
        scale="astrophysical",
        origin="SPARC calibration (DOI:10.3847/0004-6256/152/6/157)",
    ),
    # =========================================================================
    # MACROSCOPIC SCALE: Fluid dynamics, Neural dynamics
    # κ varies with Reynolds number
    # =========================================================================
    "macroscopic": UETParameters(
        kappa=0.1,
        beta=0.5,
        scale="macroscopic",
        origin="Fluid calibration (Poiseuille flow)",
    ),
    "fluid_low_re": UETParameters(
        kappa=0.01, beta=0.1, scale="fluid_low_re", origin="Low Reynolds number regime"
    ),
    "fluid_high_re": UETParameters(
        kappa=0.001,
        beta=0.01,
        scale="fluid_high_re",
        origin="High Reynolds number regime",
    ),
    # =========================================================================
    # GENERAL FALLBACK
    # =========================================================================
    "general": UETParameters(kappa=0.1, beta=0.1, scale="general", origin="Fallback/Default"),
    "General": UETParameters(kappa=0.1, beta=0.1, scale="general", origin="Fallback/Default"),
}

# Alias mapping for topic numbers
_TOPIC_SCALE_MAP = {
    "0.1": "astrophysical",
    "0.2": "planck",
    "0.3": "electroweak",
    "0.4": "electroweak",
    "0.5": "nuclear",
    "0.6": "electroweak",
    "0.7": "electroweak",
    "0.8": "electroweak",
    "0.9": "planck",
    "0.10": "macroscopic",
    "0.11": "electroweak",
    "0.12": "planck",
    "0.13": "electroweak",
    "0.14": "electroweak",
    "0.15": "astrophysical",
    "0.16": "nuclear",
    "0.17": "electroweak",
    "0.18": "electroweak",
    "0.19": "planck",
    "0.20": "electroweak",
    "0.21": "macroscopic",
    "0.22": "macroscopic",
    "0.24": "macroscopic",
}


def get_params(
    scale: str = "electroweak",
) -> UETParameters:
    """
    Get UET parameters for a given scale.

    Args:
        scale: One of "planck", "electroweak", "nuclear", "astrophysical",
               "macroscopic", "fluid_low_re", "fluid_high_re",
               or a topic number like "0.5"

    Returns:
        UETParameters object with kappa, beta, scale, origin

    Example:
        >>> params = get_params("electroweak")
        >>> print(params.kappa, params.beta)
        0.5 1.0

        >>> params = get_params("0.1")  # Galaxy rotation topic
        >>> print(params.kappa)
        0.1
    """
    # Check if it's a topic number
    if scale in _TOPIC_SCALE_MAP:
        scale = _TOPIC_SCALE_MAP[scale]

    if scale not in _SCALE_PARAMS:
        available = list(_SCALE_PARAMS.keys())
        raise ValueError(f"Unknown scale: {scale}. Available: {available}")

    return _SCALE_PARAMS[scale]


def get_kappa_beta(scale: str = "electroweak") -> tuple[float, float]:
    """Convenience function to get just κ and β."""
    p = get_params(scale)
    return p.kappa, p.beta


# =============================================================================
# DOCUMENTATION
# =============================================================================

PARAMETER_POLICY = """
╔══════════════════════════════════════════════════════════════════════╗
║                    NO PARAMETER FITTING POLICY                       ║
╠══════════════════════════════════════════════════════════════════════╣
║  UET parameters MUST be:                                             ║
║                                                                      ║
║  1. DERIVED from first principles (theory)                           ║
║  2. CALIBRATED ONCE on independent data                              ║
║  3. Defined in THIS registry (not hard-coded per test)               ║
║                                                                      ║
║  DO NOT use scipy.optimize to fit parameters per experiment!         ║
║  DO NOT change parameters to match specific data!                    ║
╚══════════════════════════════════════════════════════════════════════╝
"""


if __name__ == "__main__":
    print(PARAMETER_POLICY)
    print("\nAvailable scales:")
    for name, params in _SCALE_PARAMS.items():
        print(f"  {name}: κ={params.kappa}, β={params.beta} ({params.origin})")
