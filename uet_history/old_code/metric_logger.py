"""
UET Metric Logger (Glass Box System)
====================================
Transforms UET simulations from "Black Box" to "Glass Box".
Logs internal state at every time step for transparent visualization.
"""

import numpy as np
import json
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Any
from pathlib import Path
import time


@dataclass
class UETStepData:
    """
    The Atom of Trust: Represents the exact state of the universe at time t.
    """

    step: int
    time: float
    omega: float  # The Master Metric (Target to minimize)
    kinetic: float  # Energy (Cost of change)
    potential: float  # Structure (Stored energy)
    entropy: float  # Information density
    gradient_norm: float  # Rate of evolution (|∇C|)

    # Optional fields for deeper inspection
    max_density: float = 0.0
    min_density: float = 0.0

    # Check for stability
    is_stable: bool = True

    def to_dict(self):
        return asdict(self)


class UETMetricLogger:
    """
    Central logger for UET simulations.
    Hooks into any solver (Fluid, Galaxy, Quantum) to record the 'Heartbeat'.
    """

    def __init__(self, simulation_name: str, output_dir: Optional[str] = "data_logs"):
        self.simulation_name = simulation_name
        self.timestamp_str = f"{int(time.time())}"

        # Create a unique folder for THIS run
        self.run_id = f"{self.timestamp_str}_{simulation_name}"

        # Determine base directory: Use provided output_dir or default
        base_path = Path(output_dir) if output_dir else Path("data_logs")
        self.run_dir = base_path / self.run_id

        self.run_dir.mkdir(parents=True, exist_ok=True)

        self.history: List[UETStepData] = []
        self.snapshots: List[UETStepData] = []
        self.snapshot_interval = 100
        self.start_time = time.time()
        self.step_count = 0
        self.metadata = {}

        print(f"🔍 UET Glass Box: Logging to '{self.run_dir}'")

    def log_step(
        self,
        step: int,
        time_val: float,
        omega: float,
        kinetic: float = 0.0,
        potential: float = 0.0,
        entropy: float = 0.0,
        gradient: float = 0.0,
        field_c: Optional[np.ndarray] = None,
    ):
        """
        Record a single heartbeat of the simulation.
        """
        # Calculate field stats if provided
        max_c = float(np.max(field_c)) if field_c is not None else 0.0
        min_c = float(np.min(field_c)) if field_c is not None else 0.0

        # Check stability (User Metric: "Don't blow up")
        stable = not (np.isnan(omega) or np.isinf(omega))

        data = UETStepData(
            step=step,
            time=time_val,
            omega=float(omega),
            kinetic=float(kinetic),
            potential=float(potential),
            entropy=float(entropy),
            gradient_norm=float(gradient),
            max_density=max_c,
            min_density=min_c,
            is_stable=stable,
        )

        self.history.append(data)

        # 2b. Validation (Anti-Crash Logic)
        from research_uet.core.validation import UETValidator

        # Calculate dOmega if possible
        dOmega = 0.0
        if len(self.history) > 1:
            dOmega = self.history[-1].omega - self.history[-2].omega

        # Validation Logic specifically for time-series metrics
        scale = max(1.0, abs(omega))
        tol = UETValidator.DOMEGA_TOL_REL * scale + UETValidator.DOMEGA_TOL_ABS

        if dOmega > tol:
            print(f"⚠️ [UET Safety] Energy Violation: dOmega={dOmega:.2e}")

        # Real-time sanity check
        if not stable:
            print(f"❌ CRITICAL FAILURE at step {step}: System Instability Detected!")

    def set_metadata(self, params: Dict[str, Any]):
        """Save simulation parameters for reproducibility."""
        self.metadata = params

    def save_report(self) -> str:
        """
        Export the full history to a transparent JSON file.
        Returns the path to the report.
        """
        duration = time.time() - self.start_time
        filename = self.log_dir / f"{self.simulation_name}_{int(time.time())}.json"

        report = {
            "simulation": self.simulation_name,
            "timestamp": time.ctime(self.start_time),
            "duration_seconds": duration,
            "metadata": self.metadata,
            "total_steps": len(self.history),
            "final_state": self.history[-1].to_dict() if self.history else None,
            "history": [d.to_dict() for d in self.history],
        }

        with open(filename, "w") as f:
            json.dump(report, f, indent=2)

        print(f"📄 UET Glass Box Report saved: {filename}")
        print(f"📊 Total Steps Logged: {len(self.history)}")
        return str(filename)

    def summary(self):
        """Print a concise summary for the console."""
        if not self.history:
            return "No data logged."

        start = self.history[0]
        end = self.history[-1]
        delta_omega = end.omega - start.omega

        print("\n" + "=" * 50)
        print(f"🔎 SIMULATION DIAGNOSTICS: {self.simulation_name}")
        print("=" * 50)
        print(f"Steps: {len(self.history)}")
        print(
            f"Ω Evolution: {start.omega:.4f} -> {end.omega:.4f} (Delta: {delta_omega:.4f})"
        )
        print(f"Stability:   {'✅ STABLE' if end.is_stable else '❌ UNSTABLE'}")
        print("=" * 50 + "\n")
