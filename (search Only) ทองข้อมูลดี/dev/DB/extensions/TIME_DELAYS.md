# UET Extensions - Time Delays

## 🕐 Time Delays in UET

**Why Time Delays Matter:**

Many real systems have **delayed responses**:
- **Neural:** Action potential takes time to propagate
- **Economics:** Market reactions lag behind news
- **Biology:** Gene expression has transcription delays
- **Climate:** Ocean temperature responds slowly to atmosphere

---

## 📐 Mathematical Formulation

### Standard UET (No Delay):
```
∂C/∂t = κ∇²C - ∂V/∂C - β(C(t) - I(t)) + s
∂I/∂t = κ∇²I - ∂V/∂I - β(I(t) - C(t))
```

### UET with Time Delays:
```
∂C/∂t = κ∇²C - ∂V/∂C - β(C(t) - I(t-τ_CI)) + s
∂I/∂t = κ∇²I - ∂V/∂I - β(I(t) - C(t-τ_IC))
```

**Parameters:**
- `τ_CI`: Delay from I → C (how long C waits for I's signal)
- `τ_IC`: Delay from C → I (how long I waits for C's signal)

---

## 🔧 Implementation Strategy

### 1. History Buffer

**Need to store past values:**

```python
class UETModelWithDelay:
    def __init__(self, tau_CI=0.0, tau_IC=0.0, dt=0.01):
        self.tau_CI = tau_CI
        self.tau_IC = tau_IC
        self.dt = dt
        
        # Calculate buffer size
        self.buffer_size_CI = int(tau_CI / dt) + 1
        self.buffer_size_IC = int(tau_IC / dt) + 1
        
        # History buffers (circular)
        self.C_history = deque(maxlen=self.buffer_size_CI)
        self.I_history = deque(maxlen=self.buffer_size_IC)
    
    def step(self, C, I):
        # Store current values
        self.C_history.append(C.copy())
        self.I_history.append(I.copy())
        
        # Get delayed values
        if len(self.I_history) >= self.buffer_size_CI:
            I_delayed = self.I_history[0]  # Oldest value
        else:
            I_delayed = I  # Not enough history, use current
        
        if len(self.C_history) >= self.buffer_size_IC:
            C_delayed = self.C_history[0]
        else:
            C_delayed = C
        
        # Compute derivatives with delays
        dC_dt = (self.kappa * laplacian(C) 
                 - dV_dC(C) 
                 - self.beta * (C - I_delayed)  # ← Delayed I
                 + self.s)
        
        dI_dt = (self.kappa * laplacian(I)
                 - dV_dI(I)
                 - self.beta * (I - C_delayed))  # ← Delayed C
        
        # Update
        C_new = C + self.dt * dC_dt
        I_new = I + self.dt * dI_dt
        
        return C_new, I_new
```

---

## 🎯 Use Cases

### 1. Neural Oscillations

**Without delay:** Stable equilibrium
**With delay:** Oscillations!

```python
# Neural model with synaptic delay
model = UETModelWithDelay(
    tau_CI=0.5,  # Inhibition delayed by 0.5 time units
    tau_IC=0.1,  # Excitation delayed by 0.1
    beta=1.0
)

# Result: Oscillatory neural activity (alpha waves, etc.)
```

**Physical meaning:**
- τ_CI: Time for inhibitory signal to reach excitatory neurons
- τ_IC: Time for excitatory signal to reach inhibitory neurons
- Different delays → different oscillation frequencies

---

### 2. Economic Cycles

**Market price C lags behind fundamental value I:**

```python
# Economics: Price adjusts slowly to value
model = UETModelWithDelay(
    tau_CI=2.0,  # Price takes 2 time units to respond to value
    tau_IC=0.1,  # Value responds quickly to price
    beta=0.5
)

# Result: Boom-bust cycles, overshooting
```

---

### 3. Predator-Prey Dynamics

**Predator population I lags behind prey C:**

```python
# Biology: Predator growth delayed by reproduction time
model = UETModelWithDelay(
    tau_CI=0.0,   # Prey responds immediately to predators
    tau_IC=5.0,   # Predators take time to reproduce
    beta=0.3
)

# Result: Classic Lotka-Volterra oscillations
```

---

## ⚠️ Stability Considerations

**Time delays can destabilize systems!**

### Stability Criterion (Linear Analysis):

For small delays:
```
System stable if: β·τ < π/2
```

**Intuition:**
- Small delay (τ → 0): Stable
- Large delay (τ → ∞): Unstable (oscillations or chaos)
- Critical delay: τ_crit ≈ π/(2β)

---

## 🔬 Demo: Delayed Neural Oscillator

```python
import numpy as np
from collections import deque

def demo_delayed_oscillator():
    """Show how delay creates oscillations."""
    
    # Setup
    N = 64
    C = np.random.randn(N, N) * 0.1 + 1.0
    I = np.random.randn(N, N) * 0.1 - 1.0
    
    # Parameters
    tau = 1.0  # Delay time
    dt = 0.01
    beta = 1.0
    kappa = 0.1
    
    # History buffer
    buffer_size = int(tau / dt)
    I_history = deque([I.copy() for _ in range(buffer_size)], 
                      maxlen=buffer_size)
    
    # Simulate
    for step in range(1000):
        # Get delayed I
        I_delayed = I_history[0]
        
        # Update C with delayed I
        dC = (kappa * laplacian(C) 
              - dV_dC(C) 
              - beta * (C - I_delayed))
        C += dt * dC
        
        # Update I with current C
        dI = (kappa * laplacian(I)
              - dV_dI(I)
              - beta * (I - C))
        I += dt * dI
        
        # Store current I
        I_history.append(I.copy())
        
        # Plot every 10 steps
        if step % 10 == 0:
            plot_fields(C, I, step)
    
    # Result: Oscillations in C and I!
```

---

## 📊 Expected Behaviors

| Delay τ | β | Behavior |
|---------|---|----------|
| 0 | Any | Stable equilibrium |
| Small | Small | Damped oscillations |
| Medium | Medium | Sustained oscillations |
| Large | Large | Chaos / instability |

---

## 🎓 Domain Interpretations

### Neural:
```
τ_CI = Synaptic delay (inhibitory → excitatory)
τ_IC = Synaptic delay (excitatory → inhibitory)

Typical values: 1-10 ms
```

### Economics:
```
τ_CI = Information processing time
τ_IC = Market reaction time

Typical values: days to months
```

### Climate:
```
τ_CI = Ocean thermal inertia
τ_IC = Atmosphere response time

Typical values: years to decades
```

---

## 🚀 Next Steps

1. **Implement in core UET**
   - Add `tau_CI`, `tau_IC` parameters
   - Add history buffers
   - Update solver

2. **Create demo**
   - Neural oscillator
   - Economic cycles
   - Show stability transition

3. **Documentation**
   - When to use delays
   - How to choose τ values
   - Stability guidelines

---

## 🔗 Connection to Other Extensions

**Delays + Stochastic:**
```
∂C/∂t = ... - β(C(t) - I(t-τ)) + σξ(t)
```
→ Delayed stochastic oscillator (realistic neural noise)

**Delays + Multi-field:**
```
∂Cᵢ/∂t = ... - Σⱼ βᵢⱼ(Cᵢ(t) - Cⱼ(t-τᵢⱼ))
```
→ Network with heterogeneous delays

---

*Time delays: Simple addition, profound consequences!*
