# 📉 The Inertia Gap: Why UET isn't (yet) CFD-Ready

## The User's Question
> "Why can't it maintain precision at that [aerospace] level?"

This is the most critical question for UET's application utility.

## The Difference: Honey vs. Water

### 1. UET Current Model (Gradient Flow)
UET currently uses the simplest path to equilibrium: **Steepest Descent**.
$$ \mathbf{v} = -M \nabla \mu $$
Velocity is proportional to the driving force (Chemical Potential $\mu$).
*   **Physics:** This is **Aristotelian Dynamics** ($F \propto v$) or "Overdamped Motion".
*   **Analogy:** Moving a spoon through thick honey. If you stop pushing, the spoon stops instantly.
*   **Result:** It is **100% Stable** (no overshoot), but it kills "momentum".

### 2. Real Fluids (Navier-Stokes)
Real fluids follow **Newtonian Dynamics**:
$$ \rho \left( \frac{\partial \mathbf{v}}{\partial t} + \mathbf{v} \cdot \nabla \mathbf{v} \right) = -\nabla P + \dots $$
Force causes **Acceleration** ($F = ma$).
*   **Physics:** Includes **Inertia**.
*   **Analogy:** Throwing a baseball. If you stop pushing, the ball keeps flying.
*   **Result:** It can oscillate, swirl, and create complex **Turbulence** (Vortices that maintain their own life).

## Why Aerospace Needs Inertia
Aircraft fly because of:
1.  **Circulation (Lift):** Air must "overshoot" the wing and curl back.
2.  **Vortex Shedding (Drag):** Vortices persist behind the wing.

UET's "Honey Mode" smooths these out instantly. It predicts the *average* flow well, but misses the *inertial* details that determine if a plane stalls or flies perfectly.

## Can UET Fix This?
Yes. We need to upgrade the Master Equation from **Diffusion (Parabolic)** to **Wave-Diffusion (Hyperbolic)** by adding an inertial memory term:
$$ \tau \frac{\partial^2 C}{\partial t^2} + \frac{\partial C}{\partial t} = \dots $$
This is the **Telegrapher's Equation** extension, which restores Inertia. This is a Phase 6 roadmap item ("Inertial UET").
