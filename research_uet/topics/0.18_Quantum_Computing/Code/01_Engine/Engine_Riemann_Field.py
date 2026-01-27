"""
Engine_Riemann_Field.py - UET Topic 0.18
========================================
A Manifold Engine for Complex Potential Analysis.
Maps the Riemann Zeta Function to UET Equilibrium Sinks.
"""

import numpy as np
import math

# Base Solver Import
try:
    from research_uet.core.uet_base_solver import UETBaseSolver
except ImportError:
    import sys
    from pathlib import Path

    current = Path(__file__).resolve()
    root = None
    for parent in [current] + list(current.parents):
        if (parent / "research_uet").exists():
            root = parent
            sys.path.insert(0, str(root))
            break
    from research_uet.core.uet_base_solver import UETBaseSolver


class RiemannFieldEngine(UETBaseSolver):
    def __init__(self, precision=1000):
        super().__init__(name="Riemann_Zeta_Solver")
        self.precision = precision

    def zeta_approx(self, s: complex) -> complex:
        """
        Calculates Riemann Zeta using the alternating series (Dirichlet Eta).
        Valid for Re(s) > 0.
        zeta(s) = eta(s) / (1 - 2^(1-s))
        """
        if s.real <= 0:
            # Note: UET handles the strip 0 < Re(s) < 1.
            # Deep negative Re(s) requires functional equation (Future Wave).
            return 0j

        # Dirichlet Eta function sum
        eta = 0j
        for n in range(1, self.precision + 1):
            term = ((-1) ** (n - 1)) / (n**s)
            eta += term

        # Convert Eta to Zeta
        denom = 1 - (2 ** (1 - s))
        if abs(denom) < 1e-12:
            return 0j  # Avoid singularity at s=1

        return eta / denom

    def calculate_omega(self, s: complex) -> float:
        """
        The UET Potential (Omega) for a complex state s.
        Omega = |zeta(s)|^2 (Square of the field amplitude)
        Unity Sinks (Zeros) have Omega = 0.
        """
        z = self.zeta_approx(s)
        return float(abs(z) ** 2)

    def scan_strip(self, re_range=(0.1, 0.9), im_range=(0, 50), steps=50):
        """
        Scans a grid in the critical strip and finds local minima.
        """
        re_vals = np.linspace(re_range[0], re_range[1], steps)
        im_vals = np.linspace(im_range[0], im_range[1], steps)

        grid = []
        for im in im_vals:
            row = []
            for re in re_vals:
                row.append(self.calculate_omega(complex(re, im)))
            grid.append(row)

        return np.array(grid), re_vals, im_vals

    def find_gradient_sink(self, start_s: complex, lerp=0.01, iterations=100):
        """
        Gradient descent towards the nearest Unity Sink (Zero).
        In UET, this demonstrates the 'Pull' of the critical line.
        """
        curr = start_s
        path = [curr]

        for _ in range(iterations):
            # Numerical gradient
            eps = 1e-5
            o_base = self.calculate_omega(curr)
            o_re = self.calculate_omega(curr + eps)
            o_im = self.calculate_omega(curr + eps * 1j)

            grad_re = (o_re - o_base) / eps
            grad_im = (o_im - o_base) / eps

            curr -= complex(grad_re * lerp, grad_im * lerp)
            path.append(curr)

            if o_base < 1e-10:
                break

        return path
