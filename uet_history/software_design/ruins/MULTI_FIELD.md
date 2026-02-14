# UET Extensions - Multi-field Networks

## 🔗 Multi-field Networks in UET

**Why More Than 2 Fields?**

Real systems often have **multiple interacting components**:
- **Neural Networks:** Many brain regions, not just 2
- **Ecosystems:** Predator-prey-plant (3+ species)
- **Economics:** Multiple markets, sectors, currencies
- **Social Networks:** Many individuals/groups
- **Gene Networks:** Multiple genes regulating each other

**C and I alone are not enough!**

---

## 📐 Mathematical Formulation

### Standard UET (2 Fields):
```
∂C/∂t = κ∇²C - ∂V/∂C - β(C - I) + s
∂I/∂t = κ∇²I - ∂V/∂I - β(I - C)
```

### Multi-field UET (N Fields):
```
∂Cᵢ/∂t = κᵢ∇²Cᵢ - ∂V/∂Cᵢ - Σⱼ βᵢⱼ(Cᵢ - Cⱼ) + sᵢ

for i = 1, 2, ..., N
```

**Coupling Matrix β:**
- `βᵢⱼ`: Coupling strength from field j to field i
- Can be asymmetric: βᵢⱼ ≠ βⱼᵢ
- Diagonal: βᵢᵢ = 0 (no self-coupling)

---

## 🎯 Network Topologies

### 1. Fully Connected
```
βᵢⱼ = β for all i ≠ j

All fields interact with each other equally
```

### 2. Ring/Chain
```
βᵢⱼ = β if |i-j| = 1, else 0

Linear chain or circular ring
```

### 3. Star Network
```
β₀ⱼ = β for all j ≠ 0
βᵢⱼ = 0 for i,j ≠ 0

One central hub connected to all others
```

### 4. Hierarchical
```
βᵢⱼ = β if i is parent/child of j

Tree-like structure
```

### 5. Random Network
```
βᵢⱼ = β with probability p, else 0

Erdős-Rényi random graph
```

### 6. Scale-Free
```
βᵢⱼ follows power-law degree distribution

Hubs with many connections
```

---

## 🔧 Implementation Strategy

```python
class UETMultiField:
    """UET model with N fields."""
    
    def __init__(self, n_fields=3, N=32, kappa=0.1, 
                 coupling_matrix=None, s=None, dt=0.01):
        self.n_fields = n_fields
        self.N = N
        self.kappa = kappa
        self.dt = dt
        
        # Coupling matrix (n_fields x n_fields)
        if coupling_matrix is None:
            # Default: fully connected with β=0.5
            self.beta = np.ones((n_fields, n_fields)) * 0.5
            np.fill_diagonal(self.beta, 0)  # No self-coupling
        else:
            self.beta = coupling_matrix
        
        # External drives
        if s is None:
            self.s = np.zeros(n_fields)
        else:
            self.s = s
        
        # Initialize fields
        self.fields = [
            np.random.randn(N, N) * 0.1 + (1 if i % 2 == 0 else -1)
            for i in range(n_fields)
        ]
    
    def step(self):
        """Evolve all fields one timestep."""
        # Compute derivatives for all fields
        derivatives = []
        
        for i in range(self.n_fields):
            C_i = self.fields[i]
            
            # Diffusion
            diff_term = self.kappa * laplacian_2d(C_i)
            
            # Potential
            pot_term = -dV_dphi(C_i)
            
            # Coupling with other fields
            coupling_term = np.zeros_like(C_i)
            for j in range(self.n_fields):
                if i != j:
                    coupling_term -= self.beta[i, j] * (C_i - self.fields[j])
            
            # External drive
            drive_term = self.s[i]
            
            # Total
            dC_dt = diff_term + pot_term + coupling_term + drive_term
            derivatives.append(dC_dt)
        
        # Update all fields
        for i in range(self.n_fields):
            self.fields[i] = self.fields[i] + self.dt * derivatives[i]
    
    def get_mean_values(self):
        """Get spatial mean of all fields."""
        return [np.mean(f) for f in self.fields]
```

---

## 🎯 Use Cases

### 1. Ecological Food Web

**3 species: Plant, Herbivore, Predator**

```python
# Ecology: Food chain
model = UETMultiField(
    n_fields=3,
    coupling_matrix=np.array([
        [0,    0.2,  0],     # Plant eaten by herbivore
        [-0.3, 0,    0.4],   # Herbivore eats plant, eaten by predator
        [0,   -0.5,  0]      # Predator eats herbivore
    ])
)

# fields[0] = Plant density
# fields[1] = Herbivore density
# fields[2] = Predator density

# Result: Lotka-Volterra 3-species dynamics
```

**Asymmetric couplings:**
- Plant ← Herbivore (negative, plant eaten)
- Herbivore ← Plant (positive, food)
- Herbivore ← Predator (negative, eaten)
- Predator ← Herbivore (positive, food)

---

### 2. Brain Network

**Multiple brain regions:**

```python
# Neuroscience: Default mode network (DMN)
n_regions = 5  # PCC, mPFC, IPL, etc.

# Connectivity matrix from neuroimaging
beta_matrix = np.array([
    [0,   0.8, 0.5, 0.3, 0.2],
    [0.8, 0,   0.6, 0.4, 0.3],
    [0.5, 0.6, 0,   0.7, 0.4],
    [0.3, 0.4, 0.7, 0,   0.6],
    [0.2, 0.3, 0.4, 0.6, 0]
])

model = UETMultiField(
    n_fields=n_regions,
    coupling_matrix=beta_matrix
)

# Result: Synchronized network activity
```

---

### 3. Multi-Currency Market

**Exchange rate dynamics:**

```python
# Economics: USD, EUR, JPY, GBP
n_currencies = 4

# Trade network (symmetric)
beta_matrix = np.array([
    [0,   0.5, 0.3, 0.4],  # USD
    [0.5, 0,   0.4, 0.6],  # EUR
    [0.3, 0.4, 0,   0.2],  # JPY
    [0.4, 0.6, 0.2, 0]     # GBP
])

model = UETMultiField(
    n_fields=n_currencies,
    coupling_matrix=beta_matrix
)

# Result: Exchange rate fluctuations, arbitrage
```

---

### 4. Gene Regulatory Network

**Multiple genes:**

```python
# Biology: Gene regulation
n_genes = 6

# Regulation matrix (can be asymmetric)
# Positive = activation, Negative = repression
beta_matrix = np.array([
    [ 0,   0.5, -0.3,  0,    0,    0],   # Gene 1
    [-0.4, 0,    0.6,  0,    0,    0],   # Gene 2
    [ 0.3, 0,    0,   -0.5,  0,    0],   # Gene 3
    [ 0,   0,    0.4,  0,    0.7,  0],   # Gene 4
    [ 0,   0,    0,    0,    0,   -0.6], # Gene 5
    [ 0,   0,    0,    0,    0.5,  0]    # Gene 6
])

model = UETMultiField(
    n_fields=n_genes,
    coupling_matrix=beta_matrix
)

# Result: Gene expression oscillations, switches
```

---

## 📊 Network Analysis

### 1. Synchronization

**How synchronized are the fields?**

```python
def synchronization_index(fields):
    """Measure of synchronization (0=none, 1=perfect)."""
    n_fields = len(fields)
    pairwise_corr = []
    
    for i in range(n_fields):
        for j in range(i+1, n_fields):
            corr = np.corrcoef(fields[i].flatten(), fields[j].flatten())[0, 1]
            pairwise_corr.append(abs(corr))
    
    return np.mean(pairwise_corr)
```

### 2. Hub Detection

**Which fields are most connected?**

```python
def find_hubs(coupling_matrix):
    """Find highly connected fields."""
    degree = np.sum(np.abs(coupling_matrix), axis=1)
    hub_threshold = np.mean(degree) + np.std(degree)
    hubs = np.where(degree > hub_threshold)[0]
    return hubs
```

### 3. Community Detection

**Which fields form groups?**

```python
def detect_communities(coupling_matrix):
    """Simple community detection via spectral clustering."""
    from sklearn.cluster import SpectralClustering
    
    # Convert to similarity matrix
    similarity = np.abs(coupling_matrix)
    
    # Cluster
    clustering = SpectralClustering(n_clusters=2, affinity='precomputed')
    labels = clustering.fit_predict(similarity)
    
    return labels
```

---

## 🔬 Emergent Behaviors

### 1. Consensus

**All fields converge to same value:**

```
Strong coupling → All Cᵢ → C*
```

### 2. Clustering

**Fields form groups:**

```
Weak long-range coupling → Clusters
```

### 3. Waves

**Traveling patterns across network:**

```
Ring topology + delays → Traveling waves
```

### 4. Chimera States

**Coexistence of sync and async:**

```
Some fields synchronized, others not
```

---

## ⚠️ Computational Considerations

### 1. Scaling

```
2 fields: O(N²) per timestep
N fields: O(N² × n_fields²) per timestep

Large networks → Expensive!
```

### 2. Memory

```
Memory: n_fields × N² × sizeof(float)

Example: 100 fields, 64×64 grid
→ 100 × 4096 × 4 bytes ≈ 1.6 MB
```

### 3. Sparse Networks

**For large, sparse networks:**

```python
# Use sparse matrix for coupling
from scipy.sparse import csr_matrix

beta_sparse = csr_matrix(beta_matrix)

# Coupling computation
for i in range(n_fields):
    coupling = beta_sparse[i].dot(field_vector)
```

---

## 🎓 Domain Interpretations

### Neuroscience:
```
n_fields = Brain regions (10-100)
βᵢⱼ = Structural/functional connectivity

Typical: n_fields ~ 10-100
```

### Ecology:
```
n_fields = Species (3-20)
βᵢⱼ = Interaction matrix (predation, competition)

Typical: n_fields ~ 3-20
```

### Economics:
```
n_fields = Markets/sectors (5-50)
βᵢⱼ = Trade/correlation matrix

Typical: n_fields ~ 5-50
```

---

## 🔗 Combination with Other Extensions

### Multi-field + Delays:
```
∂Cᵢ/∂t = ... - Σⱼ βᵢⱼ(Cᵢ(t) - Cⱼ(t-τᵢⱼ))
```
→ Network with heterogeneous delays

### Multi-field + Nonlocal:
```
∂Cᵢ/∂t = ... - Σⱼ βᵢⱼ∫K(x-x')Cⱼ(x')dx'
```
→ Spatially extended network

### Multi-field + Stochastic:
```
∂Cᵢ/∂t = ... - Σⱼ βᵢⱼ(Cᵢ - Cⱼ) + σᵢξᵢ(t)
```
→ Noisy network dynamics

---

## 🚀 Implementation Tips

### 1. Coupling Matrix Design

```python
def make_coupling_matrix(n_fields, topology='fully_connected', strength=0.5):
    """Factory for coupling matrices."""
    beta = np.zeros((n_fields, n_fields))
    
    if topology == 'fully_connected':
        beta = np.ones((n_fields, n_fields)) * strength
        np.fill_diagonal(beta, 0)
    
    elif topology == 'ring':
        for i in range(n_fields):
            beta[i, (i+1) % n_fields] = strength
            beta[i, (i-1) % n_fields] = strength
    
    elif topology == 'star':
        beta[0, :] = strength
        beta[:, 0] = strength
        np.fill_diagonal(beta, 0)
    
    elif topology == 'random':
        prob = 0.3  # Connection probability
        beta = (np.random.rand(n_fields, n_fields) < prob) * strength
        np.fill_diagonal(beta, 0)
    
    return beta
```

### 2. Efficient Update

```python
# Vectorize field updates
fields_array = np.array(self.fields)  # Shape: (n_fields, N, N)

# Coupling term (vectorized)
coupling = np.einsum('ij,jkl->ikl', 
                     -self.beta, 
                     fields_array - fields_array[:, None])
```

### 3. Visualization

```python
def visualize_network(coupling_matrix):
    """Visualize network structure."""
    import networkx as nx
    
    # Create graph
    G = nx.from_numpy_array(coupling_matrix)
    
    # Draw
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, 
            node_color='lightblue', 
            node_size=500,
            font_size=10,
            width=[abs(coupling_matrix[u,v])*5 for u,v in G.edges()])
```

---

## 📈 Expected Behaviors

| Topology | Synchronization | Waves | Clusters |
|----------|-----------------|-------|----------|
| Fully connected | High | No | No |
| Ring | Medium | Yes | No |
| Star | High (hub) | No | Hub+spokes |
| Random | Medium | Maybe | Yes |
| Hierarchical | Layered | No | Yes |

---

*Multi-field: From pairs to networks!*
