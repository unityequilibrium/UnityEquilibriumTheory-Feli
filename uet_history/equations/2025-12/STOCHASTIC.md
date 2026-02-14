# UET Extensions - Stochastic Dynamics

## 🎲 Stochastic Noise in UET

**Why Noise Matters:**

Real systems have **random fluctuations**:
- **Neural:** Synaptic noise, ion channel stochasticity
- **Economics:** Random market shocks, unexpected news
- **Biology:** Molecular noise, genetic mutations
- **Climate:** Weather variability, volcanic eruptions

**Deterministic models miss this!**

---

## 📐 Mathematical Formulation

### Standard UET (Deterministic):
```
∂C/∂t = κ∇²C - ∂V/∂C - β(C-I) + s
∂I/∂t = κ∇²I - ∂V/∂I - β(I-C)
```

### Stochastic UET (with Noise):
```
∂C/∂t = κ∇²C - ∂V/∂C - β(C-I) + s + σ_C·ξ_C(x,t)
∂I/∂t = κ∇²I - ∂V/∂I - β(I-C) + σ_I·ξ_I(x,t)
```

**New Parameters:**
- `σ_C`: Noise strength for C field
- `σ_I`: Noise strength for I field
- `ξ(x,t)`: White noise (Gaussian, mean=0, variance=1)

**Properties of ξ:**
```
⟨ξ(x,t)⟩ = 0                           (zero mean)
⟨ξ(x,t)ξ(x',t')⟩ = δ(x-x')δ(t-t')     (uncorrelated)
```

---

## 🔧 Implementation Strategy

### 1. Euler-Maruyama Method

**Stochastic differential equations need special treatment:**

```python
# Deterministic Euler:
C_new = C + dt * f(C)

# Stochastic Euler-Maruyama:
C_new = C + dt * f(C) + sqrt(dt) * σ * ξ
                                  ↑
                              Important!
```

**Why `sqrt(dt)`?**
- Noise scales with √dt (Wiener process)
- Ensures correct variance in limit dt→0

---

### 2. Implementation

```python
class UETWithNoise:
    """UET model with stochastic noise."""
    
    def __init__(self, N=32, kappa=0.1, beta=0.5, s=0.0,
                 sigma_C=0.0, sigma_I=0.0, dt=0.01):
        self.N = N
        self.kappa = kappa
        self.beta = beta
        self.s = s
        self.sigma_C = sigma_C
        self.sigma_I = sigma_I
        self.dt = dt
        
        # Initialize fields
        self.C = np.random.randn(N, N) * 0.1 + 1.0
        self.I = np.random.randn(N, N) * 0.1 - 1.0
    
    def step(self):
        """Evolve one timestep with noise (Euler-Maruyama)."""
        C, I = self.C, self.I
        dt = self.dt
        
        # Deterministic part
        dC_det = (
            self.kappa * laplacian_2d(C) -
            dV_dphi(C) -
            self.beta * (C - I) +
            self.s
        )
        
        dI_det = (
            self.kappa * laplacian_2d(I) -
            dV_dphi(I) -
            self.beta * (I - C)
        )
        
        # Stochastic part (white noise)
        noise_C = np.random.randn(self.N, self.N)
        noise_I = np.random.randn(self.N, self.N)
        
        # Euler-Maruyama update
        self.C = C + dt * dC_det + np.sqrt(dt) * self.sigma_C * noise_C
        self.I = I + dt * dI_det + np.sqrt(dt) * self.sigma_I * noise_I
```

---

## 🎯 Use Cases

### 1. Neural Noise (Ion Channel Stochasticity)

**Neurons are noisy!**

```python
# Neural model with synaptic noise
model = UETWithNoise(
    sigma_C=0.1,  # Excitatory noise
    sigma_I=0.05, # Inhibitory noise (less noisy)
    beta=1.0
)

# Result: Irregular spiking, realistic neural activity
```

**Physical meaning:**
- σ_C: Random opening/closing of ion channels
- σ_I: Spontaneous neurotransmitter release
- Noise → Variability in spike timing

---

### 2. Market Volatility

**Markets have random shocks:**

```python
# Economics: Random news/events
model = UETWithNoise(
    sigma_C=0.2,  # Price volatility
    sigma_I=0.05, # Value is more stable
    beta=0.5
)

# Result: Realistic price fluctuations, volatility clustering
```

**Examples:**
- Unexpected earnings reports
- Political events
- Natural disasters

---

### 3. Molecular Noise (Gene Expression)

**Small numbers → Big fluctuations:**

```python
# Biology: Stochastic gene expression
model = UETWithNoise(
    sigma_C=0.3,  # mRNA noise (low copy number)
    sigma_I=0.1,  # Protein noise (higher copy)
    beta=0.3
)

# Result: Cell-to-cell variability, phenotypic diversity
```

---

### 4. Climate Variability

**Weather is chaotic:**

```python
# Climate: Random weather fluctuations
model = UETWithNoise(
    sigma_C=0.05, # Temperature noise
    sigma_I=0.02, # Ocean is less noisy
    beta=0.1
)

# Result: Year-to-year variability, extreme events
```

---

## 📊 Noise Effects

### Effect 1: Noise-Induced Transitions

**Noise can push system over barriers!**

```
Without noise:
  System stuck in local minimum

With noise:
  System can escape → explore other states
```

**Example:** Genetic switches, decision-making

---

### Effect 2: Stochastic Resonance

**Noise + Signal = Enhanced detection!**

```
Weak signal alone: Not detected
Noise alone: Random
Signal + Noise: Signal amplified!
```

**Example:** Sensory neurons, climate cycles

---

### Effect 3: Noise-Induced Oscillations

**Noise can create oscillations in stable systems:**

```
Deterministic: Stable equilibrium
+ Noise: Fluctuations around equilibrium
+ Nonlinearity: Coherent oscillations!
```

**Example:** Circadian rhythms, business cycles

---

## ⚠️ Numerical Considerations

### 1. Timestep Constraint

**Noise requires smaller dt:**

```
Deterministic: dt ≈ 0.01 OK
Stochastic: dt ≈ 0.001 better

Rule: dt << 1/σ²
```

### 2. Ensemble Averaging

**Single trajectory is noisy → Average many:**

```python
# Run N_ensemble simulations
trajectories = []
for _ in range(N_ensemble):
    model = UETWithNoise(sigma_C=0.1)
    model.run()
    trajectories.append(model.C)

# Average
C_mean = np.mean(trajectories, axis=0)
C_std = np.std(trajectories, axis=0)
```

### 3. Noise Types

**Different noise models:**

```python
# 1. White noise (current)
ξ(t) ~ N(0,1), uncorrelated

# 2. Colored noise (future extension)
ξ(t) has correlation time τ_corr

# 3. Multiplicative noise (future)
dC/dt = ... + σ·C·ξ(t)  # Noise ∝ C
```

---

## 🔬 Demo: Noise-Induced Escape

```python
def demo_noise_escape():
    """Show how noise helps escape local minimum."""
    
    # Setup: Double-well potential
    # Two minima at C = ±1
    
    # 1. No noise: Stuck in one well
    model_no_noise = UETWithNoise(sigma_C=0.0)
    model_no_noise.C[:] = -1.0  # Start at C=-1
    
    for _ in range(1000):
        model_no_noise.step()
    
    # Result: Still at C ≈ -1 (stuck!)
    
    # 2. With noise: Can escape
    model_with_noise = UETWithNoise(sigma_C=0.5)
    model_with_noise.C[:] = -1.0
    
    for _ in range(1000):
        model_with_noise.step()
    
    # Result: Sometimes jumps to C ≈ +1 (escaped!)
```

---

## 📈 Expected Behaviors

| Noise σ | Effect |
|---------|--------|
| 0 | Deterministic (smooth) |
| Small (0.01-0.1) | Small fluctuations |
| Medium (0.1-0.5) | Significant variability |
| Large (>0.5) | Dominated by noise |

---

## 🎓 Domain Interpretations

### Neural:
```
σ_C = Ion channel noise
σ_I = Synaptic noise

Typical: σ ≈ 0.05-0.2
```

### Economics:
```
σ_C = Market volatility
σ_I = Fundamental uncertainty

Typical: σ ≈ 0.1-0.5
```

### Biology:
```
σ_C = Molecular noise (mRNA)
σ_I = Protein noise

Typical: σ ≈ 0.1-0.3
```

---

## 🔗 Combination with Other Extensions

### Noise + Delays:
```
∂C/∂t = ... - β(C(t) - I(t-τ)) + σξ(t)
```
→ Delayed stochastic oscillator (realistic neural)

### Noise + Multi-field:
```
∂Cᵢ/∂t = ... - Σⱼ βᵢⱼ(Cᵢ-Cⱼ) + σᵢξᵢ(t)
```
→ Noisy network dynamics

---

## 🚀 Next Steps

1. **Implement in core**
   - Add `sigma_C`, `sigma_I` parameters
   - Euler-Maruyama solver
   - Ensemble averaging tools

2. **Create demos**
   - Noise-induced escape
   - Stochastic resonance
   - Ensemble statistics

3. **Documentation**
   - When to use noise
   - How to choose σ
   - Numerical stability

---

*Noise: From nuisance to feature!*
