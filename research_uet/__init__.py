"""
UET Research Package
====================
Root package for the Unity Equilibrium Theory codebase.

Exposes "Hero Features" for easy access:
- uet.fluid: Fluid Dynamics Engine (800x Faster)
- uet.math: Mathnicry Engine (Riemann/Millennium)
- uet.complexity: Complex Systems Engine
- uet.core: Core Physics Master Equation
"""

import sys
import os
import importlib.util


def _import_from_path(name, relative_path):
    """
    Import a module directly from a file path, bypassing package naming rules.
    relative_path is relative to this __init__.py file.
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, relative_path)

        # Check if file exists
        if not os.path.exists(file_path):
            return None

        spec = importlib.util.spec_from_file_location(name, file_path)
        if spec is None:
            return None

        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        return None


# 1. Core Physics
try:
    from research_uet.core import uet_master_equation as core
except ImportError:
    core = None

# 2. Hero Feature: Fluid Dynamics (Topic 0.10)
fluid_2d = _import_from_path(
    "uet.fluid.engine2d", "topics/0.10_Fluid_Dynamics_Chaos/Code/01_Engine/Engine_UET_2D.py"
)
fluid_3d = _import_from_path(
    "uet.fluid.engine3d", "topics/0.10_Fluid_Dynamics_Chaos/Code/01_Engine/Engine_UET_3D.py"
)

if fluid_2d:

    class FluidNamespace:
        """Namespace for Fluid Dynamics tools."""

        Engine2D = fluid_2d.UETFluidSolver
        Engine3D = fluid_3d.UETFluid3D if fluid_3d else None
        solve_2d = fluid_2d.run_demo

    fluid = FluidNamespace()
else:
    fluid = None

# 3. Hero Feature: Mathnicry (Topic 0.18)
riemann = _import_from_path(
    "uet.math.riemann", "topics/0.18_Mathnicry/Code/01_Engine/Engine_Riemann_Field.py"
)
sha256 = _import_from_path(
    "uet.math.sha256", "topics/0.18_Mathnicry/Code/01_Engine/Engine_SHA256_Native.py"
)

if riemann and sha256:

    class MathNamespace:
        """Namespace for Mathematical Physics tools."""

        RiemannEngine = riemann.RiemannFieldEngine
        SHA256 = sha256  # Expose the module, not a class

    math = MathNamespace()
else:
    math = None

# 4. Hero Feature: Complexity (Topic 0.14)
complexity_engine = _import_from_path(
    "uet.complexity", "topics/0.14_Complex_Systems/Code/01_Engine/Engine_Complexity.py"
)

if complexity_engine:

    class ComplexityNamespace:
        """Namespace for Complex Systems tools."""

        ComplexityEngine = complexity_engine.UETComplexityEngine

    complexity = ComplexityNamespace()
else:
    complexity = None
