"""
UET Core Module
===============
Central module for UET theory, parameters, and equations.

Usage:
    from research_uet.core import get_params, UETParams, HBAR, C, G

    # Get parameters for a scale
    params = get_params("electroweak")
    print(f"κ = {params.kappa}, β = {params.beta}")

    # Or by topic number
    params = get_params("0.1")  # Galaxy rotation

Author: UET Research Team
Version: 0.8.7
"""

from .uet_parameters import (
    # Main API
    get_params,
    get_kappa_beta,
    UETParameters,
    # Physical constants
    HBAR,
    C,
    G,
    K_B,
    ALPHA_EM,
    L_PLANCK,
    M_PLANCK,
    T_PLANCK,
    # Policy
    PARAMETER_POLICY,
)

__all__ = [
    # Parameters
    "get_params",
    "get_kappa_beta",
    "UETParameters",
    # Constants
    "HBAR",
    "C",
    "G",
    "K_B",
    "ALPHA_EM",
    "L_PLANCK",
    "M_PLANCK",
    "T_PLANCK",
    # Policy
    "PARAMETER_POLICY",
]

__version__ = "0.8.7"
