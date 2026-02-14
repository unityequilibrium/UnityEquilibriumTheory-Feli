# UET Extensions - Memory & History

## 🧠 Memory/History in UET

**Why Memory Matters:**

Many real systems have **history-dependent behavior**:
- **Materials:** Hysteresis (magnets, shape-memory alloys)
- **Ecology:** Population depends on past dynamics
- **Economics:** Path-dependent markets (lock-in effects)
- **Neural:** Learning, adaptation, memory consolidation
- **Climate:** Ocean heat content affects future dynamics

**Markovian (no memory) models miss this!**

---

## 📐 Mathematical Formulation

### Standard UET (Markovian):
```
∂C/∂t = f(C(t), I(t))
         ↑
    Only depends on CURRENT state
```

### UET with Memory:
```
∂C/∂t = f(C(t), I(t)) + ∫₀ᵗ K(t-t') C(t') dt'
                        ↑
                   Depends on PAST states
```

**Memory Kernel K(τ):**
- `K(τ)`: Memory weight at lag τ
- `τ`: Time lag
- Normalized: ∫₀^∞ K(τ)dτ = finite

---

## 🔧 Memory Kernel Types

### 1. No Memory (Markovian)
```
K(τ) = 0

Result: Standard UET
```

### 2. Exponential Memory
```
K(τ) = (γ/τ_mem) exp(-τ/τ_mem)

Parameters:
- τ_mem: Memory timescale
- γ: Memory strength

Physical meaning: Recent past matters most
```

### 3. Power-Law Memory
```
K(τ) = γ / (1 + τ)^α

Parameters:
- α: Decay exponent
- γ: Strength

Physical meaning: Long-term memory (heavy tail)
```

### 4. Oscillatory Memory
```
K(τ) = γ exp(-τ/τ_mem) cos(ω₀τ)

Parameters:
- ω₀: Oscillation frequency
- τ_mem: Decay time

Physical meaning: Reverberation, echoes
```

---

## 🔧 Implementation Strategy

### Discrete Convolution with History Buffer:

```python
from collections import deque

class UETWithMemory:
    """UET model with memory/history effects."""
    
    def __init__(self, N=32, kappa=0.1, beta=0.5, s=0.0,
                 memory_type='exponential', tau_mem=5.0, 
                 gamma=0.1, dt=0.01):
        self.N = N
        self.kappa = kappa
        self.beta = beta
        self.s = s
        self.memory_type = memory_type
        self.tau_mem = tau_mem
        self.gamma = gamma
        self.dt = dt
        
        # Memory buffer size
        self.buffer_size = int(5 * tau_mem / dt)  # 5x memory time
        
        # History buffers
        self.C_history = deque(maxlen=self.buffer_size)
        self.I_history = deque(maxlen=self.buffer_size)
        
        # Pre-compute memory kernel
        self.K_mem = self._make_memory_kernel()
        
        # Initialize fields
        self.C = np.random.randn(N, N) * 0.1 + 1.0
        self.I = np.random.randn(N, N) * 0.1 - 1.0
        
        # Fill history with initial state
        for _ in range(self.buffer_size):
            self.C_history.append(self.C.copy())
            self.I_history.append(self.I.copy())
    
    def _make_memory_kernel(self):
        """Create discrete memory kernel."""
        # Time lags
        t_lags = np.arange(self.buffer_size) * self.dt
        
        if self.memory_type == 'exponential':
            K = (self.gamma / self.tau_mem) * np.exp(-t_lags / self.tau_mem)
        elif self.memory_type == 'power_law':
            alpha = 2.0
            K = self.gamma / (1 + t_lags)**alpha
        elif self.memory_type == 'oscillatory':
            omega = 2 * np.pi / self.tau_mem  # Oscillation frequency
            K = self.gamma * np.exp(-t_lags / self.tau_mem) * np.cos(omega * t_lags)
        else:  # 'none'
            K = np.zeros(self.buffer_size)
            if self.buffer_size > 0:
                K[0] = 0.0  # No memory
        
        # Normalize
        K = K * self.dt  # Discrete integral approximation
        
        return K
    
    def _memory_integral(self, history):
        """Compute memory integral: ∫K(t-t')·field(t')dt'."""
        if len(history) < self.buffer_size:
            # Not enough history yet
            return np.zeros_like(self.C)
        
        # Convert history to array (oldest to newest)
        history_array = np.array(list(history))
        
        # Convolution (weighted sum over past)
        # K[0] = current, K[-1] = oldest
        K_reversed = self.K_mem[::-1]
        
        memory_term = np.sum([
            K_reversed[i] * history_array[i]
            for i in range(len(history_array))
        ], axis=0)
        
        return memory_term
    
    def step(self):
        """Evolve one timestep with memory."""
        C, I = self.C, self.I
        
        # Compute memory integrals
        C_memory = self._memory_integral(self.C_history)
        I_memory = self._memory_integral(self.I_history)
        
        # Compute derivatives
        dC_dt = (
            self.kappa * laplacian_2d(C) -
            dV_dphi(C) -
            self.beta * (C - I) +
            self.s +
            C_memory  # ← Memory term
        )
        
        dI_dt = (
            self.kappa * laplacian_2d(I) -
            dV_dphi(I) -
            self.beta * (I - C) +
            I_memory  # ← Memory term
        )
        
        # Update
        self.C = C + self.dt * dC_dt
        self.I = I + self.dt * dI_dt
        
        # Store current state in history
        self.C_history.append(self.C.copy())
        self.I_history.append(self.I.copy())
```

---

## 🎯 Use Cases

### 1. Hysteresis (Materials)

**Path-dependent magnetization:**

```python
# Materials: Ferromagnetic hysteresis
model = UETWithMemory(
    memory_type='exponential',
    tau_mem=10.0,  # Relaxation time
    gamma=0.3,     # Hysteresis strength
    beta=0.5
)

# C = Magnetization
# I = Internal field
# Memory → Hysteresis loop

# Result: Different paths give different outcomes
```

**Physical meaning:**
- Memory of past magnetic states
- Remanence (residual magnetization)
- Coercivity (resistance to demagnetization)

---

### 2. Neural Adaptation

**Synaptic plasticity:**

```python
# Neuroscience: Spike-timing-dependent plasticity
model = UETWithMemory(
    memory_type='exponential',
    tau_mem=50.0,   # Adaptation timescale (ms)
    gamma=0.2,      # Plasticity strength
    beta=1.0
)

# C = Neural activity
# I = Adaptation current
# Memory → Learning

# Result: Response changes based on history
```

**Examples:**
- Long-term potentiation (LTP)
- Long-term depression (LTD)
- Habituation, sensitization

---

### 3. Economic Path Dependence

**Market lock-in effects:**

```python
# Economics: Technology lock-in
model = UETWithMemory(
    memory_type='power_law',  # Long-term effects
    tau_mem=100.0,  # Historical inertia
    gamma=0.15,
    beta=0.3
)

# C = Market share
# I = Intrinsic value
# Memory → Lock-in

# Result: QWERTY keyboard, VHS vs Betamax
```

---

### 4. Climate Ocean Memory

**Thermal inertia:**

```python
# Climate: Ocean heat storage
model = UETWithMemory(
    memory_type='exponential',
    tau_mem=1000.0,  # Decades (in timesteps)
    gamma=0.05,
    beta=0.1
)

# C = Atmosphere temperature
# I = Ocean temperature
# Memory → Committed warming

# Result: Delayed response to emissions
```

---

## 📊 Memory Effects

### Effect 1: Hysteresis

**Different paths → Different outcomes:**

```
Path A: C↑ then C↓ → Final state 1
Path B: C↓ then C↑ → Final state 2

State 1 ≠ State 2  (history matters!)
```

### Effect 2: Adaptation

**Response weakens with repeated stimulation:**

```
First stimulus: Large response
Repeated stimuli: Smaller response (adaptation)
```

### Effect 3: Reverberation

**Oscillatory memory → Echoes:**

```
Impulse → Decaying oscillations
(like ringing a bell)
```

---

## ⚠️ Computational Considerations

### 1. Memory Cost

```
Memory buffer: O(N² × buffer_size)

Large τ_mem → Large buffer → More RAM

Solution: Truncate old history
```

### 2. Computational Cost

```
Memory integral: O(N² × buffer_size) per timestep

Solution: Use FFT for long kernels (if applicable)
```

### 3. Numerical Stability

```
Long memory can accumulate errors

Solution:
- Periodic reinitialization
- Error control
- Smaller dt
```

---

## 🎓 Domain Interpretations

### Materials Science:
```
τ_mem = Relaxation time
γ = Hysteresis strength

Typical: τ_mem ~ seconds to hours
```

### Neuroscience:
```
τ_mem = Synaptic time constant
γ = Plasticity rate

Typical: τ_mem ~ 10-1000 ms
```

### Economics:
```
τ_mem = Market memory
γ = Lock-in strength

Typical: τ_mem ~ years to decades
```

---

## 🔗 Combination with Other Extensions

### Memory + Delays:
```
∂C/∂t = ... - β(C(t) - I(t-τ)) + ∫K(t-t')C(t')dt'
```
→ Both feedforward delay AND feedback memory

### Memory + Stochastic:
```
∂C/∂t = ... + ∫K(t-t')C(t')dt' + σξ(t)
```
→ Noisy path-dependent dynamics

### Memory + Nonlocal:
```
∂C/∂t = ... + ∫∫K_time(t-t') K_space(x-x') C(x',t') dx'dt'
```
→ Spatiotemporal memory

---

## 🚀 Implementation Tips

### 1. Choose Buffer Size Wisely

```python
# Rule of thumb: 5x memory timescale
buffer_size = int(5 * tau_mem / dt)

# Too small: Truncated memory
# Too large: Wasted RAM
```

### 2. Efficient Storage

```python
# Use deque for automatic old-value removal
from collections import deque
history = deque(maxlen=buffer_size)
```

### 3. Kernel Visualization

```python
# Always plot your kernel!
plt.plot(t_lags, K_mem)
plt.xlabel('Time lag τ')
plt.ylabel('Memory weight K(τ)')
```

---

## 📈 Expected Behaviors

| Memory Type | Effect | Use Case |
|-------------|--------|----------|
| None | Markovian | Standard dynamics |
| Exponential | Recent bias | Adaptation, relaxation |
| Power-law | Long memory | Lock-in, path dependence |
| Oscillatory | Echoes | Reverberation, waves |

---

*Memory: The past shapes the future!*
