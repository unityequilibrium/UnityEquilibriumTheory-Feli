# 🧪 UET Core Framework: The Master Equation

> **"One Equation to Rule Them All."**

This folder (`research_uet/`) contains the **Core Physics Logic** that powers all 25 research topics.

At the heart of everything is the **UET Master Equation** (sometimes referred to as the Unified Framework or Dyer-Derivative form).

---

## 🔑 The Equation for Researchers

If you want to apply UET to your own research (Physics, AI, or Economics), you must understand this functional:

$$ \Omega[C,I] = \int \left( \underbrace{V(C)}_{\text{Energy}} + \underbrace{\frac{\kappa}{2}|\nabla C|^2}_{\text{Geometry}} + \underbrace{\beta C \cdot I}_{\text{Information}} + \underbrace{\gamma_J \nabla \cdot J}_{\text{Exchange}} \right) d^3x $$

### 1. The Terms (How to Apply)

| Term | Component | Python Interpretation | Application |
|:-----|:----------|:----------------------|:------------|
| **$V(C)$** | **Potential Energy** | `potential_V(C)` | Defines the "Cost of Being". Use quartic potential for Phase Transitions. |
| **$\kappa (\nabla C)^2$** | **Geometric Tension** | `gradient_term(C)` | "Smoothness Cost". High $\kappa$ = Rigid space (General Relativity). Low $\kappa$ = Quantum foam. |
| **$\beta C \cdot I$** | **Info Coupling** | `information_coupling()` | **THE KEY**. Mass ($C$) is drag caused by Information ($I$). $\beta$ is the coupling constant ($k_B T$). |
| **$\nabla \cdot J$** | **Open Exchange** | `semi_open_exchange()` | Inflow/Outflow. Used for non-equilibrium thermodynamics (Life/Econ). |

### 2. The Algorithm (How it Evolves)

The universe runs a global optimization loop (Lyapunov Stability):

1.  **Calculate State**: Measure current $C$ (Capacity/Mass) and $I$ (Information/Entropy).
2.  **Compute $\Omega$**: Sum all costs (Energy + Tension + Info).
3.  **Minimize**: The system naturally flows "downhill" to reduce $\Omega$.
    *   $dC/dt = -\nabla \Omega$

---

## 📂 Folder Structure

*   **`core/`**: The brain. Contains `uet_master_equation.py` (The Solver).
*   **`topics/`**: The evidence. 25 domains proving this equation works.
*   **`Figures/`**: LaTeX papers and generated graphs.

## 📂 System Architecture (Directory Map)

Navigation guide for the `research_uet/` ecosystem:

### 1. The Engine (`/core`)
*   **Path**: [`research_uet/core/`](./core/)
*   **Purpose**: Contains the **Source Code** of the Master Equation.
*   **Key File**: `uet_master_equation.py` (The Python implementation of $\Omega$).
*   **Role**: All 25 research topics import logic from here. If you change this, you change the universe.

### 2. The Evidence (`/topics`)
*   **Path**: [`research_uet/topics/`](./topics/)
*   **Purpose**: The **25 Research Domains** (Galaxy Rotation, AI, Economics, etc.).
*   **Structure**: Each folder contains `Code/` (Proof), `Doc/` (Analysis), and `Result/` (Logs).
*   **Style Guide**: See [`how to README.md`](./topics/Work/how%20to%20README.md) for the "Platinum Standard" layout.

### 3. The Documentation (`/docs`)
*   **Path**: [`research_uet/docs/`](./docs/)
*   **Purpose**: Detailed technical manuals, API references, and theoretical backgrounders.
*   **Use Case**: For developers wanting to fork or extend the framework.

### 4. The Paper (`/paper`)
*   **Path**: [`research_uet/paper/`](./paper/)
*   **Purpose**: The LaTeX source for the academic publication.
*   **Goal**: Generates the final PDF for submission (e.g., arXiv).

### 5. The Tools (`/scripts`)
*   **Path**: [`research_uet/scripts/`](./scripts/)
*   **Purpose**: Utility scripts for global tasks.
*   **Examples**:
    *   `audit_documentation_coverage.py`: Checks for missing docs.
    *   `run_all_tests.py`: The master switch to verify everything.

---

To run a simulation using the Master Equation:

```python
from research_uet.core.uet_master_equation import UETMasterEquation
import numpy as np

# 1. Initialize Engine
engine = UETMasterEquation()

# 2. Define State (e.g., a Particle)
C = np.exp(-((np.linspace(-5, 5, 100))**2))  # Gaussian Matter Wave
I = np.random.rand(100) * 0.1                # Information Field (Noise)

# 3. Evolve (Minimize Omega)
for t in range(100):
    C = engine.step(C, I=I, dt=0.01)
    
    # 4. Measure Value (Efficiency)
    omega = engine.compute_omega(C, I=I)
    print(f"Time {t}: Balance (Ω) = {omega:.4f}")
```

---

## ⚖️ The Philosophy: Thermodynamics of Ethics

This technical framework proves a moral truth:

*   **$\Omega$ (Balance)** is the goal.
*   **$C$ (Connection)** creates potential.
*   **$I$ (Isolation)** creates cost.

To optimize any system (Code, Society, Galaxy), you must **Increase Connection ($C$) while minimizing the Cost of Isolation ($I$)**.

---
*UET Core Team | v0.9.0*
