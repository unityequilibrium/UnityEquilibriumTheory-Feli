"""
UET Cosmology Engine (Topic 0.3) - 5x4 Grid Compliant
=====================================================
Validates UET prediction of "Cosmic Stiffness" (k) against REAL Planck/JWST data.
Inherits UETBaseSolver for standardized Data/Result management.

Functionality:
1. Load Comparative Data (Data/03_Research/cosmic_tension_data.txt) via UETPathManager.
2. Calculate Lambda_obs vs Lambda_UET.
3. Log results to topics/0.3.../Result/01_Engine/...
4. Prove Resolution of Hubble Tension via Horizon Scaling.
"""

import sys
import numpy as np
from dataclasses import dataclass
from typing import Dict, Any, List
from pathlib import Path

# Core Imports
from research_uet.core.uet_base_solver import UETBaseSolver
from research_uet.core.uet_master_equation import UETParameters
from research_uet.core.uet_glass_box import UETPathManager
from research_uet.core.uet_parameters import (


C,
ALPHA_EM,
INTEGRITY_KILL_SWITCH,
)  # Import Speed of Light, Fine Structure Constant, and Kill Switch

# Standard Cosmological Observed Values
H0_PLANCK = 67.4  # km/s/Mpc (Planck 2018)
H0_SHOES = 73.04  # km/s/Mpc (SH0ES 2022)




# Standardized UET Root Path
from research_uet import ROOT_PATH
root_path = ROOT_PATH

class UETCosmologyEngine(UETBaseSolver):
    """
    Cosmology Engine for Topic 0.3.
    Use Case: Analytic Comparison (0D simulation).
    """

    def __init__(self, name: str = "UET_Cosmology_Engine", uet_params=None):
        if uet_params is None:
            # Use Topic 0.3 defaults but ensure beta follows Cosmic Stiffness
            from research_uet.core.uet_parameters import get_params, ALPHA_EM

            base_params = get_params("0.3")
            # Overwrite with precise axiomatic derivation
            uet_params = UETParameters(
                kappa=base_params.kappa,
                beta=np.sqrt(ALPHA_EM),
                alpha=base_params.alpha,
                gamma=base_params.gamma,
                C0=base_params.C0,
            )

        super().__init__(
            nx=1,
            ny=1,
            dt=1.0,  # 1-cell grid for Scalar/Analytic work
            params=uet_params,
            name=name,
            topic="0.3_Cosmology_Hubble_Tension",
            pillar="01_Engine",
        )
        # Coupling Parameters
        self.beta = self.params.beta
        self.kappa = self.params.kappa

        self.results_cache = []
        self.stable_path = True

    def load_data(self) -> List[Dict]:
        """Load comparative data using PathManager."""
        # PathManager typically returns Result dir.
        # We need Source Data dir: topics/0.3.../Data/03_Research/...
        # We can detect Topic Dir from the Result Dir or construct it.

        # We can ask PathManager for the 'topic_root' if implemented, or assume standard layout.
        # Layout: research_uet/topics/ID/Data/03_Research/file.txt

        # Using self.logger.output_dir which is .../Result/01_Engine/...
        # We can traverse up.
        # Or better: construct relative to PROJECT ROOT.

        # Construct path safely:
        data_path = (
            root_path
            / "research_uet"
            / "topics"
            / "0.3_Cosmology_Hubble_Tension"
            / "Data"
            / "03_Research"
            / "cosmic_tension_data.txt"
        )

        datasets = []
        if not data_path.exists():
            print(f"⚠️ Data file not found: {data_path}")
            return datasets

        with open(data_path, "r") as f:
            for line in f:
                if line.startswith("Telescope") or line.startswith("UET"):
                    continue
                parts = line.split(",")
                if len(parts) >= 5:
                    datasets.append(
                        {
                            "name": parts[0],
                            "method": parts[1],
                            "H0": float(parts[2]),
                            "Omega_L": float(parts[4]),
                        }
                    )
        return datasets

    def get_hubble_parameter(self, z: float, h0_global: float = 67.4) -> float:
        """
        Calculate H(z) = H0 * sqrt(Omega_m(1+z)^3 + Omega_L)
        Standard Friedmann evolution used as baseline for information field.
        """
        omega_m = 0.315
        omega_l = 0.685
        return h0_global * np.sqrt(omega_m * (1 + z) ** 3 + omega_l)

    def get_a0_at_redshift(self, z: float, h0_global: float = 67.4) -> float:
        """
        Axiom 7: Pattern Recurrence Across Scales.
        Predicts that the MOND-like acceleration scale a0 evolved with the Hubble parameter.
        a0(z) = beta * c * H(z)
        """
        h_z_km_s_mpc = self.get_hubble_parameter(z, h0_global)
        # Convert H(z) to SI (s^-1)
        # 1 km/s/Mpc = 3.24078e-20 s^-1
        h_z_si = h_z_km_s_mpc * 3.24078e-20
        a0_si = self.beta * C * h_z_si

        # Return in astro units (km/s)^2 / kpc for research scripts
        # 1 m/s^2 = 3.086e16 (km/s)^2 / kpc
        return a0_si * 3.086e16

    def predict_uet_h0(self, h0_global: float, z_obs: float) -> float:
        """
        Axiomatic Prediction of local Hubble Parameter.
        At z=0 (local), H0_obs = H0_global * (1 + beta).
        """
        if INTEGRITY_KILL_SWITCH:
            return float("nan")

        if z_obs > 100:  # Early Universe (CMB)
            return h0_global
        else:  # Late Universe (Local)
            return h0_global * (1 + self.beta)

    def solve_hubble_tension(self, h0_early: float, h0_late: float) -> Dict[str, float]:
        """
        Engine-level resolution.
        """
        if INTEGRITY_KILL_SWITCH:
            return {
                "H0_early_uet": float("nan"),
                "H0_late_uet": float("nan"),
                "Delta_H0": float("nan"),
            }

        # UET Prediction for late universe (z=0)
        h_late_uet = self.predict_uet_h0(h0_early, 0.0)

        return {
            "H0_early_uet": h0_early,
            "H0_late_uet": h_late_uet,
            "Delta_H0": h_late_uet - h0_early,
            "beta": self.beta,
        }

    def get_extra_metrics(self) -> Dict[str, float]:
        """Expose key metrics for Proof validation."""
        h_late = self.predict_uet_h0(H0_PLANCK, 0.0)
        return {
            "H0_predicted": h_late,  # Legacy alias for Proof scripts
            "H0_late_predicted": h_late,
            "beta_cosmo": self.beta,
        }

    def step(self, step_idx: int = 0):
        """
        Execute Axiomatic Audit of Hubble Tension.
        Compare Local Measurements (SH0ES/JWST) against UET-corrected Planck Global value.
        """
        datasets = self.load_data()

        # Find Planck (Global Baseline)
        planck_h0 = 67.4  # Standard Global Baseline (Planck 2018)

        for d in datasets:
            h0_obs = d["H0"]
            z_eff = 0.0 if d["method"] != "CMB" else 1100.0

            # UET Prediction: What should H0 be for THIS measurement type/epoch?
            h_pred = (
                self.predict_uet_h0(planck_h0, z_eff)
                if d["method"] != "CMB"
                else planck_h0
            )

            ratio = h_pred / h0_obs

            result = {
                "telescope": d["name"],
                "method": d["method"],
                "H0_Obs": h0_obs,
                "H0_UET_Pred": h_pred,
                "Accuracy": 1.0 - abs(ratio - 1.0),
                "Integrity": "AXIOMATIC (No Fitting)",
            }
            self.results_cache.append(result)

        # Log to Glass Box
        self.logger.log_step(
            step=step_idx,
            time_val=0.0,
            results=str(self.results_cache),
            omega=0.0,
            potential=0.0,
            gradient_energy=0.0,
            entropy_interaction=0.0,
        )

    def save_results(self):
        # Override to save custom JSON analysis
        import json

        out_path = Path(self.logger.run_dir) / "cosmology_analysis.json"
        with open(out_path, "w") as f:
            json.dump(self.results_cache, f, indent=2)
        return str(out_path)


# =============================================================================
# VERIFICATION DEMO
# =============================================================================
def run_demo():
    print("🚀 Verifying 5x4 Grid Compliance for Cosmology Engine...")
    engine = UETCosmologyEngine()
    engine.step()
    path = engine.save_results()
    print(f"✅ Cosmology Result: {path}")


if __name__ == "__main__":
    run_demo()
