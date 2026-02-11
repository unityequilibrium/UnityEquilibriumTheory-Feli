# UET Extensions - Nonlocal Coupling

## 🌐 Nonlocal Coupling in UET

**Why Nonlocal Matters:**

Many real systems have **long-range interactions**:
- **Social Networks:** Influence spreads beyond neighbors (viral trends, information cascades)
- **Brain:** Long-range connections between distant regions
- **Economics:** Global markets affect local prices
- **Ecology:** Migration connects distant populations

**Local diffusion (∇²) is not enough!**

---

## 📐 Mathematical Formulation

### Standard UET (Local Coupling):
```
∂C/∂t = κ∇²C - ∂V/∂C - β(C(x) - I(x)) + s
                              ↑
                        Same location only
```

### UET with Nonlocal Coupling:
```
∂C/∂t = κ∇²C - ∂V/∂C - β∫K(x-x') I(x') dx' + s
                              ↑
                    Weighted average over ALL x'
```

**Kernel K(r):**
- `K(r)`: Coupling strength at distance r
- Normalized: ∫K(r)dr = 1

---

## 🔧 Kernel Functions

### 1. Local (Dirac Delta)
```
K(r) = δ(r)

Result: Standard UET (no nonlocal)
```

### 2. Gaussian Kernel
```
K(r) = (1/√(2πσ²)) exp(-r²/2σ²)

Parameters:
- σ: Interaction range
- r: Distance

Physical meaning: Smooth decay with distance
```

### 3. Exponential Kernel
```
K(r) = (1/2λ) exp(-|r|/λ)

Parameters:
- λ: Characteristic length scale

Physical meaning: Slower decay than Gaussian
```

### 4. Power-Law Kernel
```
K(r) = C / (1 + r)^α

Parameters:
- α: Decay exponent (α>dim for normalization)

Physical meaning: Long-range interactions (heavy tail)
```

### 5. Top-Hat Kernel
```
K(r) = {  1/(πR²)  if r < R
       {  0         if r ≥ R

Parameters:
- R: Interaction radius

Physical meaning: All-or-nothing (neighbors within R)
```

---

## 🔧 Implementation Strategy

### Discrete Convolution:

```python
class UETWithNonlocal:
    """UET model with nonlocal coupling."""
    
    def __init__(self, N=32, kappa=0.1, beta=0.5, s=0.0,
                 kernel_type='gaussian', kernel_sigma=2.0):
        self.N = N
        self.kappa = kappa
        self.beta = beta
        self.s = s
        self.kernel_type = kernel_type
        self.kernel_sigma = kernel_sigma
        
        # Pre-compute coupling kernel
        self.K = self._make_kernel()
        
        # Initialize fields
        self.C = np.random.randn(N, N) * 0.1 + 1.0
        self.I = np.random.randn(N, N) * 0.1 - 1.0
    
    def _make_kernel(self):
        """Create 2D coupling kernel."""
        N = self.N
        sigma = self.kernel_sigma
        
        # Distance from center
        x = np.arange(N) - N//2
        y = np.arange(N) - N//2
        X, Y = np.meshgrid(x, y)
        R = np.sqrt(X**2 + Y**2)
        
        if self.kernel_type == 'gaussian':
            K = np.exp(-R**2 / (2 * sigma**2))
        elif self.kernel_type == 'exponential':
            K = np.exp(-R / sigma)
        elif self.kernel_type == 'power_law':
            alpha = 3.0
            K = 1.0 / (1 + R)**alpha
        elif self.kernel_type == 'tophat':
            K = (R < sigma).astype(float)
        else:
            # Default: local (delta function approximation)
            K = np.zeros((N, N))
            K[N//2, N//2] = 1.0
        
        # Normalize
        K = K / np.sum(K)
        
        return K
    
    def _nonlocal_coupling(self, field):
        """Compute nonlocal coupling: ∫K(x-x')·field(x')dx'."""
        from scipy.signal import fftconvolve
        
        # Use FFT convolution for efficiency
        result = fftconvolve(field, self.K, mode='same')
        
        return result
    
    def step(self):
        """Evolve one timestep with nonlocal coupling."""
        C, I = self.C, self.I
        dt = 0.01
        
        # Nonlocal coupling term
        I_nonlocal = self._nonlocal_coupling(I)
        C_nonlocal = self._nonlocal_coupling(C)
        
        # Compute derivatives
        dC_dt = (
            self.kappa * laplacian_2d(C) -
            dV_dphi(C) -
            self.beta * (C - I_nonlocal) +  # ← Nonlocal I
            self.s
        )
        
        dI_dt = (
            self.kappa * laplacian_2d(I) -
            dV_dphi(I) -
            self.beta * (I - C_nonlocal)  # ← Nonlocal C
        )
        
        # Update
        self.C = C + dt * dC_dt
        self.I = I + dt * dI_dt
```

---

## 🎯 Use Cases

### 1. Social Network Influence

**Opinion spreads through network:**

```python
# Social media: Viral spread
model = UETWithNonlocal(
    kernel_type='power_law',  # Long-range influence
    kernel_sigma=5.0,         # Reach
    beta=0.8
)

# C = Public opinion
# I = Private belief
# K(r) = Social network structure

# Result: Viral cascades, echo chambers
```

**Physical meaning:**
- Power-law: "Hubs" have wide influence
- β: Peer pressure strength
- Result: Opinion polarization, viral spreading

---

### 2. Neural Long-Range Connections

**Brain regions communicate across distance:**

```python
# Brain: Cortical networks
model = UETWithNonlocal(
    kernel_type='exponential',  # Long-range connections
    kernel_sigma=10.0,          # Axon reach
    beta=0.5
)

# C = Local excitation
# I = Distal inhibition
# K(r) = White matter connectivity

# Result: Synchronized activity, large-scale patterns
```

**Examples:**
- Default mode network
- Attention networks
- Memory consolidation

---

### 3. Global Economic Markets

**Local prices affected by global markets:**

```python
# Economics: Global trade
model = UETWithNonlocal(
    kernel_type='gaussian',  # Smooth global influence
    kernel_sigma=20.0,       # Trade network reach
    beta=0.3
)

# C = Local price
# I = Global price index
# K(r) = Trade network strength

# Result: Price synchronization, global shocks
```

---

### 4. Ecological Migration

**Species migrate between patches:**

```python
# Ecology: Meta-population
model = UETWithNonlocal(
    kernel_type='tophat',   # Migration radius
    kernel_sigma=5.0,       # Dispersal distance
    beta=0.2
)

# C = Prey density
# I = Predator density
# K(r) = Migration kernel

# Result: Spatial coexistence, traveling waves
```

---

## 📊 Kernel Comparison

| Kernel | Shape | Range | Use Case |
|--------|-------|-------|----------|
| **Delta** | Spike at r=0 | Local only | Standard UET |
| **Gaussian** | Bell curve | Medium | Neural, diffusion |
| **Exponential** | Smooth decay | Long | Physical interactions |
| **Power-law** | Heavy tail | Very long | Social networks |
| **Top-hat** | Flat then zero | Fixed radius | Migration, neighborhoods |

---

## 🔬 Effects of Nonlocal Coupling

### Effect 1: Pattern Formation

**Nonlocal → New patterns!**

```
Local coupling: Turing patterns (stripes, spots)
Nonlocal coupling: Complex patterns (labyrinths, hexagons)
```

### Effect 2: Synchronization

**Long-range → Sync distant regions:**

```
Local: Only neighbors sync
Nonlocal: Global synchronization possible
```

### Effect 3: Traveling Waves

**Nonlocal enables wave propagation:**

```
Wave speed depends on K(r) shape
Power-law K → Super-diffusion (fast waves)
```

---

## ⚠️ Computational Considerations

### 1. Complexity

```
Local coupling: O(N²) per timestep
Nonlocal (naive): O(N⁴) per timestep  ← Expensive!
Nonlocal (FFT): O(N² log N)  ← Much better!
```

**Use FFT convolution for efficiency!**

### 2. Boundary Conditions

```python
# Periodic boundaries (FFT default)
from scipy.signal import fftconvolve
result = fftconvolve(field, K, mode='same')

# Or: scipy.ndimage.convolve for other boundary conditions
from scipy.ndimage import convolve
result = convolve(field, K, mode='wrap')  # periodic
```

### 3. Kernel Size

```
Small kernel (σ ~ 1-2): Fast, local-like
Medium kernel (σ ~ 5-10): Balanced
Large kernel (σ > N/4): Slow, truly nonlocal
```

---

## 🎓 Domain Interpretations

### Neural:
```
K(r) = White matter connectivity matrix
σ = Axon length scale

Typical: σ ≈ 5-20 grid points
```

### Social Networks:
```
K(r) = Friendship/follower network
α = Network degree distribution exponent

Typical: α ≈ 2-3 (scale-free networks)
```

### Economics:
```
K(r) = Trade/information network
σ = Market integration scale

Typical: σ ≈ global (all markets connected)
```

---

## 🔗 Combination with Other Extensions

### Nonlocal + Delays:
```
∂C/∂t = ... - β∫K(x-x') I(x',t-τ) dx'
```
→ Delayed nonlocal coupling (realistic neural)

### Nonlocal + Stochastic:
```
∂C/∂t = ... - β∫K(x-x') I(x') dx' + σξ(t)
```
→ Noisy long-range interactions

### Nonlocal + Multi-field:
```
∂Cᵢ/∂t = ... - Σⱼ∫Kᵢⱼ(x-x') Cⱼ(x') dx'
```
→ Network of nonlocal fields

---

## 🚀 Implementation Tips

### 1. Kernel Design

```python
def make_kernel_2d(N, kernel_type, params):
    """Factory for 2D kernels."""
    # ... (see implementation above)
    return K
```

### 2. Efficient Convolution

```python
# Use scipy for FFT convolution
from scipy.signal import fftconvolve

def convolve_2d(field, kernel):
    return fftconvolve(field, kernel, mode='same')
```

### 3. Kernel Visualization

```python
# Always plot your kernel!
plt.imshow(K, cmap='hot')
plt.colorbar()
plt.title('Coupling Kernel K(r)')
```

---

## 📈 Expected Behaviors

| Kernel Range (σ) | Pattern | Sync |
|------------------|---------|------|
| Small (σ<2) | Local Turing | None |
| Medium (σ~5) | Complex patterns | Regional |
| Large (σ>10) | Global modes | Global |

---

*Nonlocal coupling: Think globally, act locally!*
