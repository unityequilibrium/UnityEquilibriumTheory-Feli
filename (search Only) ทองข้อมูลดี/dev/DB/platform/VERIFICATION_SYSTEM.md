# 🔬 UET Verification System - Technical Documentation

> **Purpose**: This document explains the mathematical verification system for transparency and auditability.

---

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VERIFICATION SYSTEM                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│   │ invariants  │  │   kepler    │  │  scenarios  │        │
│   │ .ts         │  │   .ts       │  │  .ts        │        │
│   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│          │                │                │                │
│          v                v                v                │
│   ┌─────────────────────────────────────────────────┐      │
│   │              testRunner.ts                       │      │
│   │     (Orchestrates verification steps)            │      │
│   └─────────────────────────────────────────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 1️⃣ Invariants Module (`invariants.ts`)

### Purpose
Checks physical conservation laws that must hold in any valid N-body simulation.

### Mathematical Checks

#### A. Total Energy Conservation
```
E_total = KE + PE

KE = Σ ½mᵢvᵢ²         (Kinetic Energy)
PE = -Σ Gmᵢmⱼ/rᵢⱼ     (Potential Energy)

Drift = |E_current - E_initial| / |E_initial|
PASS: Drift ≤ tolerance (default: 1%)
```

#### B. Angular Momentum Conservation
```
L_total = Σ rᵢ × pᵢ = Σ mᵢ(rᵢ × vᵢ)

Drift = |L_current - L_initial| / |L_initial|
PASS: Drift ≤ tolerance (default: 0.1%)
```

#### C. Center-of-Mass Velocity Conservation
```
v_COM = Σ(mᵢvᵢ) / Σmᵢ

PASS: v_COM remains constant (within tolerance 1e-6)
```

#### D. NaN/Infinity Detection
```
PASS: No NaN or Infinity in any position/velocity/mass value
```

### Default Tolerances
| Check | Tolerance | Meaning |
|-------|-----------|---------|
| Energy | 1e-2 (1%) | Acceptable for Leapfrog integrator |
| Angular Momentum | 1e-3 (0.1%) | Stricter than energy |
| COM Velocity | 1e-6 | Near machine precision |

---

## 2️⃣ Kepler Oracle (`kepler.ts`)

### Purpose
Provides **exact analytic solutions** for 2-body Keplerian orbits. This is the mathematical ORACLE used to validate numerical integrators.

### Key Equations

#### Orbital Elements Extraction
```
μ = G(m₁ + m₂)                     (Standard gravitational parameter)
h = r × v                          (Specific angular momentum)
e = (v × h)/μ - r/|r|              (Eccentricity vector)
ε = |v|²/2 - μ/|r|                 (Specific orbital energy)
a = -μ/(2ε)                        (Semi-major axis)
n = √(μ/a³)                        (Mean motion)
```

#### Kepler's Equation (Newton-Raphson Solver)
```
M = E - e·sin(E)    (Mean anomaly = Eccentric anomaly relation)

Solved iteratively:
E_next = E - (E - e·sin(E) - M) / (1 - e·cos(E))
Tolerance: 1e-12, Max iterations: 50
```

#### Orbit Classification
| Eccentricity | Orbit Type |
|--------------|------------|
| e = 0 | Circular |
| 0 < e < 1 | Elliptic (bound) |
| e = 1 | Parabolic |
| e > 1 | Hyperbolic |

---

## 3️⃣ Test Scenarios (`scenarios.ts`)

### Gate Structure

| Gate | Name | Purpose |
|------|------|---------|
| **G0** | Sanity | Determinism + No NaN |
| **G1** | Inertial | Free body: r(t) = r₀ + v₀t (EXACT) |
| **G2** | Kepler | 2-body orbits vs analytic solution |
| **G3** | Convergence | dt halving → error/4 (2nd order) |
| **G4** | Stress | N-body, PN correction, UET field |

### Specific Scenarios

#### G0: Sanity Tests
- `sanity_determinism`: Same seed → identical output
- `sanity_no_nan`: Long run without NaN/Inf

#### G1: Inertial Test
- `inertial_1body`: G=0, position must be exactly r₀ + v₀t
- Tolerance: 1e-10 (machine precision)

#### G2: Kepler 2-Body
- `kepler_2body_circular`: e=0, compare vs Kepler solver
- `kepler_2body_elliptic`: e=0.5, harder to integrate

#### G3: Convergence Test
- Run with dt, dt/2, dt/4
- Expected: error ratio ~4 (confirms 2nd order integrator)

#### G4: Advanced Tests
- `nbody_stress_10`: 10-body random system
- `pn_mercury_smoke`: Post-Newtonian precession
- `uet_field_smoke`: UET field computation (EXPECTED_FAIL)

---

## 4️⃣ Test Runner (`testRunner.ts`)

### Execution Flow
```
1. Initialize InvariantChecker with scenario's G and tolerances
2. Clone initial body state
3. Main loop:
   a. Execute leapfrog step
   b. Every N steps: check invariants
   c. If 2-body: compare with Kepler solution
4. Generate TestResult with PASS/FAIL/EXPECTED_FAIL
```

### Leapfrog Integrator
```
// Acceleration calculation
aᵢ = Σⱼ G·mⱼ(rⱼ-rᵢ)/|rⱼ-rᵢ|³

// Velocity update
vᵢ(t+dt) = vᵢ(t) + aᵢ·dt

// Position update  
rᵢ(t+dt) = rᵢ(t) + vᵢ(t+dt)·dt
```

### Softening
```
dist = max(|r|, 0.5)    // Prevents singularity at r=0
```

---

## 5️⃣ Result Status

| Status | Meaning |
|--------|---------|
| **PASS** | All checks within tolerance |
| **FAIL** | At least one check exceeded tolerance |
| **EXPECTED_FAIL** | Scenario marked as expected to fail (e.g., UET experiments) |
| **PENDING** | Not yet run |
| **RUNNING** | Currently executing |

---

## 📁 Source Files

| File | Lines | Purpose |
|------|-------|---------|
| [invariants.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/oracle/invariants.ts) | 367 | Conservation law checks |
| [kepler.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/oracle/kepler.ts) | 371 | 2-body analytic solver |
| [scenarios.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/oracle/scenarios.ts) | 376 | Test scenario registry |
| [testRunner.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/oracle/testRunner.ts) | 374 | Execution engine |

---

## ✅ Transparency Statement

This verification system:
1. Uses **standard physics equations** (Newtonian mechanics, Kepler's laws)
2. Implements **known-good algorithms** (Newton-Raphson, Leapfrog)
3. Compares against **exact analytic solutions** where available
4. Provides **configurable tolerances** for flexibility
5. Generates **detailed reports** including failure reasons

All source code is available for audit in the `frontend/src/lib/oracle/` directory.
