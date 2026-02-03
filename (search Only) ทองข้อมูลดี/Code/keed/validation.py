import numpy as np
import math
from dataclasses import dataclass
from typing import Dict, Any, Tuple, Optional


@dataclass
class ValidationResult:
    is_valid: bool
    status: str  # "PASS", "WARN", "FAIL"
    reason: str
    metrics: Dict[str, float]


class UETValidator:
    """
    Implements the 'Anti-Crash' logic extracted from legacy grade_runs.py.
    Safety limits are based on stability thresholds observed in v0.9.0.
    """

    # Thresholds from grade_runs.py
    C_MAX_FAIL = 50.0  # Field blowup limit
    DT_COLLAPSE_FAIL = 1e-6  # Relative dt collapse limit
    DT_COLLAPSE_WARN = 1e-3
    DOMEGA_TOL_ABS = 1e-12  # Energy monotonicity tolerances
    DOMEGA_TOL_REL = 1e-8
    DOMEGA_WARN_REL = 1e-10

    @staticmethod
    def check_state(
        C: np.ndarray,
        I: Optional[np.ndarray] = None,
        step_info: Optional[Dict[str, float]] = None,
    ) -> ValidationResult:
        """
        Comprehensive safety check for a single simulation step.
        """
        reasons = []
        metrics = {}
        status = "PASS"

        # 1. Finite Check (NaN/Inf)
        if not np.isfinite(C).all():
            return ValidationResult(False, "FAIL", "nan_inf_detected_in_C", {})
        if I is not None and not np.isfinite(I).all():
            return ValidationResult(False, "FAIL", "nan_inf_detected_in_I", {})

        # 2. Blowup Check (Legacy: max_abs_C > 50.0)
        max_c = np.max(np.abs(C))
        metrics["max_abs_C"] = float(max_c)
        if max_c > UETValidator.C_MAX_FAIL:
            return ValidationResult(
                False,
                "FAIL",
                f"field_blowup(max_C={max_c:.2f} > {UETValidator.C_MAX_FAIL})",
                metrics,
            )

        # 3. Time Step Check (if info provided)
        if step_info:
            dt_curr = step_info.get("dt", 0.0)
            dt_nom = step_info.get("dt_nominal", 0.0)
            if dt_nom > 0:
                ratio = dt_curr / dt_nom
                metrics["dt_ratio"] = ratio
                if ratio < UETValidator.DT_COLLAPSE_FAIL:
                    return ValidationResult(
                        False, "FAIL", f"dt_collapse({ratio:.2e})", metrics
                    )
                elif ratio < UETValidator.DT_COLLAPSE_WARN:
                    status = "WARN"
                    reasons.append(f"dt_collapse_risk({ratio:.2e})")

            # 4. Monotonicity Check (Energy Decrease)
            dOmega = step_info.get("dOmega", float("-inf"))
            Omega = step_info.get("Omega", 1.0)
            metrics["dOmega"] = dOmega

            # Allow small fluctuations within numerical noise
            # Legacy: tol_inc = th["dOmega_tol_rel"] * scale + th["dOmega_tol_abs"]
            scale = max(1.0, abs(Omega))
            tol = UETValidator.DOMEGA_TOL_REL * scale + UETValidator.DOMEGA_TOL_ABS
            warn_tol = (
                UETValidator.DOMEGA_WARN_REL * scale + UETValidator.DOMEGA_TOL_ABS
            )

            if dOmega > tol:
                return ValidationResult(
                    False,
                    "FAIL",
                    f"energy_violation(dOmega={dOmega:.2e} > {tol:.2e})",
                    metrics,
                )
            elif dOmega > warn_tol:
                status = "WARN"
                reasons.append(f"monotonicity_wiggle(dOmega={dOmega:.2e})")

        return ValidationResult(True, status, "|".join(reasons), metrics)
