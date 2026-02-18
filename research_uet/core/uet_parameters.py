"""
UET Central Parameter Module
============================
Single source of truth for all UET parameters.

Usage:
    from research_uet.core.uet_parameters import get_params, UETParams

    params = get_params("electroweak")
    print(params.kappa, params.beta)

Author: UET Research Team
Version: 0.9.0
Last Updated: 2026-01-13
"""

import os
import math
from dataclasses import dataclass
from typing import Literal, Optional

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
# FIRST-PRINCIPLES CALCULATION (Landauer Principle)
# =============================================================================

LANDAUER_CONSTANT = math.log(2)  # ln(2) for Landauer coupling


def calculate_beta_landauer(temperature: float = 293.15) -> float:
    """
    Calculate β from Landauer Principle (First Principles).

    β = k_B * T * ln(2)

    This is the minimum energy cost per bit of information processing,
    derived from thermodynamics and validated experimentally (Bérut 2012).

    Args:
        temperature: System temperature in Kelvin (default: room temperature 293.15K)

    Returns:
        β in Joules (energy per bit)

    Reference:
        - Landauer (1961): Irreversibility and heat generation
        - Bérut et al. (2012): Experimental verification (DOI: 10.1103/PhysRevLett.109.180601)
    """
    return K_B * temperature * LANDAUER_CONSTANT


def calculate_kappa_from_beta(beta: float, information_density: float) -> float:
    """
    Calculate κ from β and information density (First Principles).

    κ = β / ρ_info

    Where ρ_info is the information density (bits/m³).

    This represents the "information inertia" - how much energy is required
    to change information content per unit volume.

    Args:
        beta: Energy per bit (Joules) from calculate_beta_landauer()
        information_density: Information density (bits/m³)

    Returns:
        κ (dimensionless gradient penalty coefficient)

    Reference:
        - UET Topic 0.13: Thermodynamic Bridge validation
        - Unity Scale Link: Information-Physical coupling
    """
    if information_density <= 0:
        raise ValueError("information_density must be positive")
    return beta / information_density


def calculate_scaling_ratio(scale_from: float, scale_to: float) -> float:
    """
    Calculate scaling factor for parameter transformation between scales.

    Based on thermodynamic scaling laws from Topic 0.13:
    - Temperature: T ∝ scale^(-2/3)
    - Information density: ρ ∝ scale^(-3)

    Args:
        scale_from: Source scale (meters)
        scale_to: Target scale (meters)

    Returns:
        Scaling factor to multiply parameters by

    Reference:
        - Topic 0.13: Thermodynamic scaling exponent = 2/3
        - Unity Scale Link: Scale bridge calculations
    """
    temp_ratio = (scale_to / scale_from) ** (-2.0 / 3.0)
    density_ratio = (scale_from / scale_to) ** 3.0
    return temp_ratio * density_ratio


def derive_parameters_first_principles(
    scale: float,
    temperature: float,
    information_density: float,
) -> UETParameters:
    """
    Derive UET parameters from first principles using Landauer coupling.

    This is the PRIMARY method for calculating parameters, replacing
    hardcoded values with physically-derived quantities.

    Args:
        scale: Characteristic length scale (meters)
        temperature: System temperature (Kelvin)
        information_density: Information density (bits/m³)

    Returns:
        UETParameters with derived kappa, beta, and context

    Example:
        >>> params = derive_parameters_first_principles(1e-3, 300, 1e18)
        >>> print(f"β = {params.beta:.2e} J")
        >>> print(f"κ = {params.kappa:.4f}")
    """
    # Calculate from first principles
    beta = calculate_beta_landauer(temperature)
    kappa = calculate_kappa_from_beta(beta, information_density)

    # Construct parameters
    return UETParameters(
        kappa=kappa,
        beta=beta,
        temperature=temperature,
        scale=f"{scale:.2e}m",
        origin="First-Principles (Landauer)",
    )

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


# =============================================================================
# DOMAIN-SPECIFIC PRESETS (with First-Principles Derivation)
# =============================================================================

_DOMAIN_PRESETS = {
    "quantum": {
        "scale": 1e-9,  # meters (nanometer)
        "temperature": 4.2,  # K (liquid helium)
        "info_density": 1e15,  # bits/m³
        "description": "Quantum systems (nanoscale)",
    },
    "nuclear_binding": {
        "scale": 1e-15,  # meters (femtometer)
        "temperature": 1e12,  # K (nuclear temperature)
        "info_density": 1e20,  # bits/m³
        "description": "Nuclear binding (QCD scale)",
    },
    "fluid": {
        "scale": 1e-3,  # meters (millimeter)
        "temperature": 300,  # K (room temperature)
        "info_density": 1e18,  # bits/m³
        "description": "Fluid dynamics (mesoscale)",
    },
    "galactic": {
        "scale": 1e20,  # meters (galactic scale)
        "temperature": 2.7,  # K (CMB temperature)
        "info_density": 1e10,  # bits/m³
        "description": "Galactic rotation (cosmological)",
    },
    "biological": {
        "scale": 1e-6,  # meters (micrometer)
        "temperature": 310,  # K (body temperature)
        "info_density": 1e16,  # bits/m³
        "description": "Biological systems (cellular)",
    },
}


def get_params_first_principles(domain_name: str) -> UETParameters:
    """
    Get UET parameters for a domain using first-principles calculation.

    This is the RECOMMENDED method for obtaining parameters, as it uses
    physically-derived quantities rather than hardcoded values.

    Args:
        domain_name: One of "quantum", "nuclear_binding", "fluid", "galactic", "biological"

    Returns:
        UETParameters with calculated kappa, beta, and context

    Example:
        >>> params = get_params_first_principles("fluid")
        >>> print(f"κ = {params.kappa:.4f}, β = {params.beta:.2e} J")
    """
    if domain_name not in _DOMAIN_PRESETS:
        available = list(_DOMAIN_PRESETS.keys())
        raise ValueError(f"Unknown domain: {domain_name}. Available: {available}")

    preset = _DOMAIN_PRESETS[domain_name]
    return derive_parameters_first_principles(
        scale=preset["scale"],
        temperature=preset["temperature"],
        information_density=preset["info_density"],
    )


# =============================================================================
# LEGACY PARAMETER REGISTRY (Backward Compatibility)
# =============================================================================

# Define parameters for each physical scale (LEGACY - use first-principles instead)
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
    "0.25": "macroscopic",
    "0.26": "astrophysical",
    "0.27": "macroscopic",
    "0.28": "macroscopic",
    "0.29": "macroscopic",
    "0.30": "macroscopic",
    "0.31": "astrophysical",
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
║           UET PARAMETER CALCULATION POLICY (UPDATED)                ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  PRIMARY METHOD: First-Principles Calculation                       ║
║  ──────────────────────────────────────────────────────────────   ║
║  Use derive_parameters_first_principles() or get_params_first_      ║
║  principles() for calculating parameters from physical laws:         ║
║                                                                      ║
║    β = k_B * T * ln(2)           (Landauer Principle)                ║
║    κ = β / ρ_info                (Information-Physical coupling)     ║
║                                                                      ║
║  Domain presets available: quantum, nuclear_binding, fluid,         ║
║  galactic, biological                                          ║
║                                                                      ║
║  LEGACY METHOD: Hardcoded Registry (Backward Compatibility)          ║
║  ──────────────────────────────────────────────────────────────   ║
║  Legacy _SCALE_PARAMS are kept for existing code, but new code       ║
║  should use first-principles calculation.                          ║
║                                                                      ║
║  PROHIBITED:                                                        ║
║  - DO NOT use scipy.optimize to fit parameters per experiment!      ║
║  - DO NOT change parameters to match specific data!                 ║
║  - DO NOT use "shadow math" (bypassing UET_KILL_ENGINE)             ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""


if __name__ == "__main__":
    print("=" * 70)
    print("UET PARAMETER CALCULATION - FIRST PRINCIPLES DEMONSTRATION")
    print("=" * 70)

    print(PARAMETER_POLICY)

    print("\n" + "=" * 70)
    print("FIRST-PRINCIPLES CALCULATION EXAMPLES")
    print("=" * 70)

    # Example 1: Landauer Principle at room temperature
    print("\n[1] Landauer Principle at 300K:")
    beta_room = calculate_beta_landauer(300)
    beta_ev = beta_room / E_CHARGE
    print(f"    β = {beta_room:.4e} J = {beta_ev:.6f} eV")
    print(f"    Expected: 0.017921 eV (Topic 0.13 validation)")
    print(f"    Status: {'PASS' if abs(beta_ev - 0.017921) < 0.001 else 'FAIL'}")

    # Example 2: Domain-specific parameters
    print("\n[2] Domain-Specific Parameters (First-Principles):")
    domains = ["quantum", "fluid", "galactic", "biological"]
    for domain in domains:
        params = get_params_first_principles(domain)
        print(f"    {domain}:")
        print(f"        κ = {params.kappa:.6f}")
        print(f"        β = {params.beta:.4e} J")
        print(f"        scale = {params.scale}, origin = {params.origin}")

    # Example 3: Scaling between domains
    print("\n[3] Scaling Example (quantum → fluid):")
    scale_factor = calculate_scaling_ratio(1e-9, 1e-3)
    print(f"    Scale factor: {scale_factor:.4e}")
    print(f"    (κ at fluid scale) = (κ at quantum scale) × {scale_factor:.4e}")

    print("\n" + "=" * 70)
    print("LEGACY PARAMETER REGISTRY (Backward Compatibility)")
    print("=" * 70)
    print("\nAvailable legacy scales:")
    for name, params in _SCALE_PARAMS.items():
        print(f"  {name}: κ={params.kappa}, β={params.beta} ({params.origin})")

    print("\n" + "=" * 70)
    print("RECOMMENDATION: Use first-principles calculation for new code!")
    print("=" * 70)
