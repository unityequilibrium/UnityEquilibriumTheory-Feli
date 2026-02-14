# UET Extensions - Custom Potentials

## 🎨 Custom Potentials in UET

**Why Custom Potentials?**

Different systems have **different energy landscapes**:
- **Double-well:** Bistability (current default)
- **Single-well:** Simple attractor
- **Triple-well:** Three stable states
- **Periodic:** Angular variables (phase, orientation)
- **Asymmetric:** Broken symmetry
- **Domain-specific:** Custom physics

**One potential doesn't fit all!**

---

## 📐 Mathematical Formulation

### Standard UET (Double-well):
```
V(φ) = (φ² - 1)² / 4

Minima at φ = ±1
Barrier at φ = 0
```

### Custom Potential:
```
V(φ) = user_defined_function(φ, params)

∂V/∂φ = user_defined_derivative(φ, params)
```

---

## 🎨 Potential Library

### 1. Double-Well (Current Default)
```python
def V_double_well(phi):
    return (phi**2 - 1)**2 / 4

def dV_double_well(phi):
    return phi * (phi**2 - 1)
```

**Properties:**
- 2 minima: φ = ±1
- Barrier height: 1/4
- Symmetric

**Use:** Bistable systems, binary states

---

### 2. Single-Well (Harmonic)
```python
def V_single_well(phi, k=1.0):
    return 0.5 * k * phi**2

def dV_single_well(phi, k=1.0):
    return k * phi
```

**Properties:**
- 1 minimum: φ = 0
- No barrier
- Restoring force

**Use:** Damped oscillators, relaxation

---

### 3. Triple-Well
```python
def V_triple_well(phi, a=1.0):
    return a * (phi**4 - 2*phi**2) + 1

def dV_triple_well(phi, a=1.0):
    return a * (4*phi**3 - 4*phi)
```

**Properties:**
- 3 minima: φ = 0, ±√2
- 2 barriers
- Central + two side wells

**Use:** Decision-making (3 choices), bifurcations

---

### 4. Periodic (Cosine)
```python
def V_periodic(phi, k=1.0):
    return -k * np.cos(phi)

def dV_periodic(phi, k=1.0):
    return k * np.sin(phi)
```

**Properties:**
- Periodic with period 2π
- Infinite minima
- Periodic boundary

**Use:** Angular variables (phase, rotation)

---

### 5. Asymmetric Double-Well
```python
def V_asymmetric(phi, a=0.2):
    return (phi**2 - 1)**2 / 4 + a * phi

def dV_asymmetric(phi, a=0.2):
    return phi * (phi**2 - 1) + a
```

**Properties:**
- 2 unequal minima
- Broken symmetry
- One well deeper

**Use:** Preferred states, hysteresis

---

### 6. Mexican Hat
```python
def V_mexican_hat(phi, r=1.0):
    r_sq = np.sum(phi**2, axis=-1)  # For 2D phi
    return (r_sq - r**2)**2 / 4

def dV_mexican_hat(phi, r=1.0):
    r_sq = np.sum(phi**2, axis=-1, keepdims=True)
    return phi * (r_sq - r**2)
```

**Properties:**
- Continuous circle of minima
- Central maximum
- Symmetry breaking

**Use:** Phase transitions, Higgs mechanism

---

### 7. Polynomial (General)
```python
def V_polynomial(phi, coeffs=[1, 0, -1, 0, 0.25]):
    """V(φ) = Σ cₙφⁿ"""
    return sum(c * phi**n for n, c in enumerate(coeffs))

def dV_polynomial(phi, coeffs=[1, 0, -1, 0, 0.25]):
    return sum(n * c * phi**(n-1) for n, c in enumerate(coeffs) if n > 0)
```

**Properties:**
- Arbitrary polynomial
- User-defined

**Use:** Fitting to experimental data

---

## 🔧 Implementation

```python
class UETWithCustomPotential:
    """UET with user-defined potential."""
    
    def __init__(self, N=32, kappa=0.1, beta=0.5, s=0.0,
                 potential_func=None, potential_deriv=None,
                 potential_params=None, dt=0.01):
        self.N = N
        self.kappa = kappa
        self.beta = beta
        self.s = s
        self.dt = dt
        
        # Potential functions
        if potential_func is None:
            # Default: double-well
            self.V = lambda phi: (phi**2 - 1)**2 / 4
            self.dV = lambda phi: phi * (phi**2 - 1)
        else:
            self.V = potential_func
            self.dV = potential_deriv
        
        # Potential parameters
        self.pot_params = potential_params or {}
        
        # Initialize fields
        self.C = np.random.randn(N, N) * 0.1 + 1.0
        self.I = np.random.randn(N, N) * 0.1 - 1.0
    
    def step(self):
        """Evolve with custom potential."""
        C, I = self.C, self.I
        
        # Use custom potential derivative
        if self.pot_params:
            dV_C = self.dV(C, **self.pot_params)
            dV_I = self.dV(I, **self.pot_params)
        else:
            dV_C = self.dV(C)
            dV_I = self.dV(I)
        
        # Compute derivatives
        dC_dt = (
            self.kappa * laplacian_2d(C) -
            dV_C -
            self.beta * (C - I) +
            self.s
        )
        
        dI_dt = (
            self.kappa * laplacian_2d(I) -
            dV_I -
            self.beta * (I - C)
        )
        
        # Update
        self.C = C + self.dt * dC_dt
        self.I = I + self.dt * dI_dt
```

---

## 🎯 Use Cases

### 1. Phase Oscillators (Neural)

**Use periodic potential:**

```python
# Neuroscience: Phase-coupled oscillators
model = UETWithCustomPotential(
    potential_func=lambda phi: -np.cos(phi),
    potential_deriv=lambda phi: np.sin(phi)
)

# C, I = Phase of oscillators
# Result: Phase synchronization (Kuramoto model)
```

---

### 2. Decision-Making (Triple-well)

**3 choices:**

```python
# Cognitive: Three-choice decision
model = UETWithCustomPotential(
    potential_func=lambda phi: phi**4 - 2*phi**2 + 1,
    potential_deriv=lambda phi: 4*phi**3 - 4*phi
)

# Result: System settles into one of 3 choices
```

---

### 3. Asymmetric Hysteresis

**Preferred state:**

```python
# Materials: Asymmetric ferromagnet
model = UETWithCustomPotential(
    potential_func=lambda phi, a: (phi**2-1)**2/4 + a*phi,
    potential_deriv=lambda phi, a: phi*(phi**2-1) + a,
    potential_params={'a': 0.2}
)

# Result: One magnetization direction preferred
```

---

### 4. Fitting to Data

**Learn potential from observations:**

```python
# Data-driven: Fit polynomial
coeffs = fit_potential_to_data(observed_dynamics)

model = UETWithCustomPotential(
    potential_func=lambda phi: sum(c*phi**n for n,c in enumerate(coeffs)),
    potential_deriv=lambda phi: sum(n*c*phi**(n-1) for n,c in enumerate(coeffs) if n>0)
)

# Result: Captures empirical dynamics
```

---

## 📊 Potential Comparison

| Potential | # Minima | Symmetry | Use Case |
|-----------|----------|----------|----------|
| **Double-well** | 2 | Symmetric | Binary states |
| **Single-well** | 1 | Symmetric | Relaxation |
| **Triple-well** | 3 | Symmetric | 3-state choice |
| **Periodic** | ∞ | Periodic | Phase/angle |
| **Asymmetric** | 2 | Broken | Preferred state |
| **Mexican hat** | ∞ (circle) | Radial | Phase transition |

---

## 🔬 Potential Design Guidelines

### 1. Stability

**Ensure minima exist:**

```python
# Check: dV/dφ = 0 has solutions
# Check: d²V/dφ² > 0 at minima
```

### 2. Boundedness

**Prevent blow-up:**

```python
# Ensure: V(φ) → ∞ as |φ| → ∞
# For stability
```

### 3. Smoothness

**Avoid discontinuities:**

```python
# Use smooth functions (C¹ or better)
# For numerical stability
```

---

## 🎨 Potential Visualization

```python
def plot_potential(V_func, phi_range=(-2, 2), params=None):
    """Visualize potential landscape."""
    phi = np.linspace(*phi_range, 200)
    
    if params:
        V_vals = V_func(phi, **params)
    else:
        V_vals = V_func(phi)
    
    plt.figure(figsize=(10, 4))
    plt.plot(phi, V_vals, 'b-', lw=2)
    plt.xlabel('φ', fontsize=14)
    plt.ylabel('V(φ)', fontsize=14)
    plt.title('Potential Landscape', fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.axhline(0, color='k', linestyle='--', alpha=0.3)
    
    # Mark minima
    from scipy.optimize import minimize_scalar
    # (find and plot minima)
```

---

## ⚠️ Numerical Considerations

### 1. Timestep Constraints

```
Steep potentials → Small dt required

Rule: dt < 1 / max(|d²V/dφ²|)
```

### 2. Initial Conditions

```
Start near minimum for stability

Or explore basin of attraction
```

### 3. Energy Conservation

```
Check: dΩ/dt ≤ 0 (energy decreases)

If violated: dt too large
```

---

## 🔗 Combination with Other Extensions

### Custom V + Stochastic:
```
∂C/∂t = ... - dV_custom/dC + σξ(t)
```
→ Noise-induced transitions in custom landscape

### Custom V + Memory:
```
∂C/∂t = ... - dV_custom/dC + ∫K(t-t')C(t')dt'
```
→ Path-dependent custom dynamics

### Custom V + Multi-field:
```
Different potentials for different fields:
∂Cᵢ/∂t = ... - dVᵢ/dCᵢ
```
→ Heterogeneous network

---

## 🚀 Implementation Tips

### 1. Potential Library

```python
POTENTIAL_LIBRARY = {
    'double_well': (V_double_well, dV_double_well),
    'single_well': (V_single_well, dV_single_well),
    'triple_well': (V_triple_well, dV_triple_well),
    'periodic': (V_periodic, dV_periodic),
    'asymmetric': (V_asymmetric, dV_asymmetric)
}

# Usage
V_func, dV_func = POTENTIAL_LIBRARY['triple_well']
```

### 2. Automatic Differentiation

```python
# Use autograd for derivatives
import autograd.numpy as np
from autograd import grad

V = lambda phi: (phi**2 - 1)**2 / 4
dV = grad(V)  # Automatic!
```

### 3. Parameter Fitting

```python
from scipy.optimize import curve_fit

def fit_potential(data, potential_func, p0):
    """Fit potential parameters to data."""
    # (fitting code)
    return optimal_params
```

---

## 📈 Expected Behaviors

| Potential Shape | Dynamics |
|-----------------|----------|
| Steep wells | Fast relaxation |
| Shallow wells | Slow dynamics |
| High barriers | Rare transitions |
| No barriers | Free diffusion |

---

*Custom potentials: Your landscape, your rules!*
