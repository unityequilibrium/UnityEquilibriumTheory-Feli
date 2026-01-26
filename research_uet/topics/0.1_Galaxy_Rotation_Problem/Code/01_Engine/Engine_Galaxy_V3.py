import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class GalaxyParams:
    mass_disk: float
    radius_disk: float
    mass_bulge: float = 0.0
    mass_gas: float = 0.0
    redshift: float = 0.0
    name: str = "Unknown"
    galaxy_type: str = "Unknown"


# ==============================================================================
# 🌌 UET GALAXY ROTATION ENGINE (Engine_Galaxy_V3.py)
# ==============================================================================
# CONTEXT:
# This engine implements the Unified Electricity Theory (UET) solution to the
# Galaxy Rotation Problem (Topic 0.1).
#
# CORE HYPOTHESIS:
# - Dark Matter is NOT required.
# - The "missing mass" is Information Mass (M_I) arising from Electromagnetic
#   Information Coupling in the Galactic Interaction Field.
#
# KEY MECHANISMS:
# 1. Baryonic Reference Frame (RHO_UNITY):
#    - The "Density of Unity" scales with the local galactic environment.
#    - V5.2 Update: Density now includes Bulge Mass (M_d + M_b) to correctly
#      identify Compact galaxies.
#
# 2. Information Scaling Law (The UET Ratio):
#    - Ratio = RATIO_0 * (rho_b / RHO_UNITY) ^ -gamma
#
# 3. Surgical Correction (V5.2 Density Refinement):
#    - Ultrafaint (< 0.005): 20.0x Multiplier (Strong Damping)
#    - Compact (> 10.0): 8.0x Multiplier (Moderate Damping)
#    - Standard (The Rest): 4.5x Multiplier (Goldilocks Zone)
# ==============================================================================

# Universal Constants (UET Framework)
G_GALACTIC = 4.30e-6  # kpc km^2/s^2 M_sun^-1

# Integrity Check
INTEGRITY_KILL_SWITCH = False  # Set True to disable engine for testing


class UETGalaxyEngine:
    def __init__(self, gal_params: pd.Series):
        """
        Initialize the engine with galaxy parameters from SPARC database.
        """
        self.gal_params = gal_params
        self.gamma_dynamic = 0.5  # Will be solved per galaxy
        self.M_I_total = 0.0
        self.M_I_ratio = 1.0
        self.c = 10.0  # Concentration parameter (Emergent NFW)
        self.R_I = 100.0  # Information Halo Scale (kpc)

        # Pre-compute Information Halo properties based on Baryonics
        self._derive_information_halo()

    def _derive_information_halo(self, gamma_override=None):
        """
        Derives the Emergent Information Halo properties from Baryonic Mass.
        Implements UET Axiom A2: Mass-Information Equivalence.
        """
        # Load Baryonic Data
        M_d = self.gal_params.mass_disk
        M_b = self.gal_params.mass_bulge
        M_gas = self.gal_params.mass_gas
        R_d = self.gal_params.radius_disk

        # Total Baryonic Mass
        M_baryon = M_d + M_b + M_gas

        # Local Density Estimation (The Core of UET's "Glass Box")
        # V5.2: Use MEAN BARYONIC DENSITY (Disk + Bulge)
        z = self.gal_params.redshift

        # 1. Baryonic Density Metrics
        vol = (4 / 3) * np.pi * R_d**3
        rho_local = (M_d + M_b) / (vol + 1e-10)

        # 2. ADAPTIVE LOCAL CALIBRATION (Topic 0.1 - V5.2 Density Refinement)
        # STANDARD: 4.5x (Safe Harbor for Spiral/LSB)
        # CORRECTION: Targeted terms using Total Baryonic Density

        # 2. ADAPTIVE LOCAL CALIBRATION (Topic 0.1 - V5.3 Class-Based Correction)
        # We use explicit Galaxy Types to handle regimes with overlapping densities.
        g_type = self.gal_params.galaxy_type.lower()

        # 2. ADAPTIVE LOCAL CALIBRATION (Topic 0.1 - V5.4 Hybrid Refinement)
        # Combine Type hints with Physical Density checks for maximum precision.
        g_type = self.gal_params.galaxy_type.lower()
        multiplier = 4.5  # Default Standard (Spiral/LSB)

        if "dwarf" in g_type or "ultrafaint" in g_type:
            # Only apply strong damping if PHYSICALLY faint
            if rho_local < 5e7:
                multiplier = 20.0
            else:
                multiplier = 4.5
        elif "compact" in g_type:
            # Only apply damping if PHYSICALLY dense
            if rho_local > 1e8:
                multiplier = 8.0
            else:
                multiplier = 4.5

        RHO_UNITY = rho_local * multiplier
        RATIO_0 = 1.2

        # Redshift scaling
        omega_m = 0.315
        omega_l = 0.685
        h_ratio = np.sqrt(omega_m * (1 + z) ** 3 + omega_l)
        RATIO_0_Z = RATIO_0 * h_ratio

        # 3. GAMMA DYNAMICS (Axiom A2: Interaction Coupling)
        if gamma_override is not None:
            self.gamma_dynamic = gamma_override
        else:
            # Baseline coupling guess (UET Axiom A2)
            # Must remain positive and within astrophysical bounds [0.4, 0.8]
            log_density_ratio = np.log10(RHO_UNITY / (rho_local + 1e-10))
            self.gamma_dynamic = 0.5 + 0.1 * log_density_ratio

        # Physical Enclosure: Extended range for Dwarf support
        self.gamma_dynamic = np.clip(self.gamma_dynamic, 0.38, 0.95)

        # 4. Universal Information Ratio (UET Scaling Law)
        # Ratio = RATIO_0 * (rho / rho_u) ^ -gamma
        self.M_I_ratio = RATIO_0_Z * (rho_local / (RHO_UNITY + 1e-10)) ** (
            -self.gamma_dynamic
        )
        self.M_I_ratio = np.clip(self.M_I_ratio, 0.1, 50.0)

        # 5. Total Information Mass
        self.M_I_total = self.M_I_ratio * M_d

        # 6. NFW-equivalent Concentration (Emergent Geometry)
        self.c = 12.0 * (self.M_I_total / 1e12) ** (-0.1)  # Standard cosmology scaling
        self.R_I = 25.0 * R_d  # Halo scale extends well beyond disk (Diffuse)

    def optimize_coupling(
        self, radii: List[float], v_obs: List[float], v_err: List[float]
    ):
        """
        Production Feature:
        Finds the exact Information Coupling (Gamma) that minimizes Chi-Squared
        against REAL OBSERVATIONAL DATA.
        """
        best_gamma = 0.5
        best_chi2 = float("inf")

        # Sweep Gamma (WIDENED RANGE: 0.1 - 0.9)
        for g in np.linspace(0.1, 0.9, 81):
            self._derive_information_halo(gamma_override=g)
            chi2 = 0.0
            for r, v, err in zip(radii, v_obs, v_err):
                v_pred = self.compute_velocity_at_radius(r)
                chi2 += ((v_pred - v) / err) ** 2

            if chi2 < best_chi2:
                best_chi2 = chi2
                best_gamma = g

        # Apply best fit
        self._derive_information_halo(gamma_override=best_gamma)
        return best_gamma, best_chi2

    def compute_velocity_at_radius(self, r_kpc: float) -> float:
        """
        Compute total orbital velocity at radius r.
        V = sqrt( G * (M_bulge + M_disk + M_Info) / r )
        """
        if r_kpc <= 0:
            return 0.0

        if INTEGRITY_KILL_SWITCH:
            return float("nan")

        G = G_GALACTIC
        R_d = self.gal_params.radius_disk
        M_d = self.gal_params.mass_disk
        M_b = self.gal_params.mass_bulge

        # 1. Disk Contribution (Freeman Disk approximation)
        x = r_kpc / R_d
        M_disk_enc = M_d * (1 - (1 + x) * np.exp(-x))

        # 2. Bulge Contribution (Point mass / Sphere)
        M_bulge_enc = M_b
        if r_kpc < 1.0:
            M_bulge_enc *= (r_kpc / 1.0) ** 3

        # 3. Information Field Contribution (Local Density Integration)
        # Replaces NFW profile with pure Emergent Mass: M_I(r) = Integral( dM_b * Ratio(rho) )
        M_I_enc = self._integrate_information_mass(r_kpc)

        # 4. Total Mass
        M_total = M_disk_enc + M_bulge_enc + M_I_enc

        return np.sqrt(G * M_total / r_kpc)

    def _integrate_information_mass(self, r_target: float) -> float:
        """
        Numerically integrates the Information Mass up to radius r_target.
        Correctly handles Disk (flat) and Bulge (spherical) baryonic sources.
        Ratio(r) = RATIO_0 * (rho_b(r) / rho_unity) ^ -gamma
        Using Local Calibration for Galactic Scales.
        """
        dr = 0.1  # Integration step (kpc)
        m_info_sum = 0.0
        r_current = 0.1

        R_d = self.gal_params.radius_disk
        M_d = self.gal_params.mass_disk
        M_b = self.gal_params.mass_bulge

        # Adaptive Calibration (Consistent with _derive_information_halo)
        # V5.2 Density Refinement
        vol_ref = (4 / 3) * np.pi * R_d**3
        rho_mean_gal = (M_d + M_b) / (vol_ref + 1e-10)

        # Adaptive Calibration (Consistent with _derive_information_halo)
        # V5.4 Hybrid Refinement
        g_type = self.gal_params.galaxy_type.lower()
        multiplier = 4.5  # Default

        if "dwarf" in g_type or "ultrafaint" in g_type:
            if rho_mean_gal < 5e7:
                multiplier = 20.0
            else:
                multiplier = 4.5
        elif "compact" in g_type:
            if rho_mean_gal > 1e8:
                multiplier = 8.0
            else:
                multiplier = 4.5

        rho_unity = rho_mean_gal * multiplier
        ratio_0 = 1.2

        # Redshift scaling
        z = self.gal_params.redshift
        h_ratio = np.sqrt(0.315 * (1 + z) ** 3 + 0.685)
        ratio_pivot = ratio_0 * h_ratio

        while r_current < r_target:
            # 1. Disk Contribution (Exponential Density)
            # Area element: 2 * pi * r * dr
            sigma_r = (M_d / (2 * np.pi * R_d**2)) * np.exp(-r_current / R_d)
            dM_b_disk = sigma_r * (2 * np.pi * r_current * dr)

            # Volume density for UET Ratio calculation
            h_z = 0.2 * R_d  # Typical scale height
            rho_disk = sigma_r / (2 * h_z + 1e-10)

            # 2. Bulge Contribution (Point-like/Sphere)
            # Volume element: 4 * pi * r^2 * dr
            dM_b_bulge = 0.0
            rho_bulge = 0.0
            if r_current < 1.0:
                rho_bulge = M_b / ((4 / 3) * np.pi * 1.0**3)
                dM_b_bulge = rho_bulge * (4 * np.pi * r_current**2 * dr)

            rho_b = rho_disk + rho_bulge
            rho_safe = max(rho_b, 1e-12)

            # 3. UET Scaling Law
            # We use the dynamic gamma solved per galaxy
            ratio = ratio_pivot * (rho_safe / rho_unity) ** (-self.gamma_dynamic)

            # Clamp for numerical stability (LSB support)
            ratio = np.clip(ratio, 0.01, 100.0)

            # 4. Integrate Information Mass
            # Ratio applies to the local baryonic mass increment
            dM_I = (dM_b_disk + dM_b_bulge) * ratio
            m_info_sum += dM_I

            r_current += dr

        return m_info_sum
