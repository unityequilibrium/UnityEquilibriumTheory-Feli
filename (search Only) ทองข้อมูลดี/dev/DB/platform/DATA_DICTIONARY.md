# Platform Data Dictionary

> ⚠️ **Note:** This document has been superseded by [SMART_DATA_DICTIONARY](SMART_DATA_DICTIONARY.md)
> which includes Smart Config for UI integration.

> **Master Registry of System Values**
>
> This document centralizes all **Parameters** (Inputs) and **Metrics** (Outputs) used across the UET Platform.
> It enforces strict **Quantitative (QNT)** vs **Qualitative (QLT)** categorization.

---

## 1. Quantitative (QNT)
*Values that are measured, counted, or calculated numerically.*

### 1.1 Physical Domain (PHY)
Real-world physics quantities.

| ID | Label | Symbol | Unit | Range | Description |
|:---|:---|:---|:---|:---|:---|
| `time` | Simulation Time | $t$ | `s` | $t \ge 0$ | Current time in simulation. |
| `dt` | Time Step | $\Delta t$ | `s` | $0 < dt \ll T$ | Integration step size. |
| `mass` | Mass | $m$ | `kg` | $m > 0$ | Inertial mass of a body. |
| `position` | Position | $\mathbf{r}$ | `m` | $\mathbb{R}^3$ | Spatial coordinates $(x,y,z)$. |
| `velocity` | Velocity | $\mathbf{v}$ | `m/s` | $\mathbb{R}^3$ | Rate of change of position. |
| `total_energy` | Total Energy | $E$ | `J` | $\mathbb{R}$ | Sum of Kinetic + Potential. |
| `kinetic_energy`| Kinetic Energy | $K$ | `J` | $K \ge 0$ | Energy of motion ($\frac{1}{2}mv^2$). |
| `potential_energy`| Grav. Potential | $U$ | `J` | $U \le 0$ | Gravitational binding energy. |
| `angular_momentum`| Angular Momentum | $L$ | `kg·m²/s` | $\ge 0$ | Rotational momentum $|\mathbf{r} \times m\mathbf{v}|$. |
| `g_const` | Gravitational Const | $G$ | `m³/kg·s²`| $G \ge 0$ | Strength of gravity. |
| `c_light` | Speed of Light | $c$ | `m/s` | $c > 0$ | Relativistic limit scaling. |

### 1.2 UET Domain (UET)
Internal field theory values (Dimensionless or Normalized units).

| ID | Label | Symbol | Unit | Range | Description |
|:---|:---|:---|:---|:---|:---|
| `omega` | Omega Functional | $\Omega$ | `UET` | $\mathbb{R}$ | Landscape functional (NOT Energy). |
| `omega_grad` | Omega Gradient | $\nabla\Omega$ | `UET/s` | $\mathbb{R}$ | Rate of change of $\Omega$. |
| `c_field` | C-Field | $C$ | `UET` | $[0, 1]$ | Mean Consciousness field. |
| `i_field` | I-Field | $I$ | `UET` | $[0, 1]$ | Mean Interaction field. |
| `kappa` | Coupling | $\kappa$ | - | $[0, 2]$ | C-I interaction strength. |
| `beta` | Nonlinearity | $\beta$ | - | $[0, 2]$ | Quartic potential strength. |
| `tilt` | Symmetry Tilt | $s$ | - | $[-1, 1]$ | Asymmetry parameter. |
| `lambda` | Decay Length | $\lambda$ | - | $[0, 1]$ | Field interaction range. |
| `alpha` | Diffusion | $\alpha$ | - | $[0, 1]$ | Field propagation rate. |

### 1.3 Indicators & Counts (IND/CNT)
Simulation health, statistics, and utility values.

| ID | Label | Symbol | Unit | Range | Description |
|:---|:---|:---|:---|:---|:---|
| `stability_score` | Stability | $S$ | `%` | $0-100$ | Computed system health. |
| `energy_drift` | Energy Drift | $\delta E$ | `%` | $\ge 0$ | Relative error $(E_t - E_0)/E_0$. |
| `com_drift` | COM Drift | $v_{com}$ | `m/s` | $\ge 0$ | Drift velocity of Center of Mass. |
| `step_count` | Steps | $N$ | `#` | $\mathbb{Z}^+$ | Total integration steps. |
| `body_count` | Bodies | $N_{body}$ | `#` | $\mathbb{Z}^+$ | Number of entities. |
| `softening` | Softening | $\epsilon$ | `m` | $\ge 0$ | Gravity singularity prevention. |

### 1.4 Thermodynamic Domain (THM)
Energy distribution, heat, and information entropy.

| ID | Label | Symbol | Unit | Range | Description |
|:---|:---|:---|:---|:---|:---|
| `temperature` | Temperature | $T_{sys}$ | `K` | $T \ge 0$ | Average kinetic energy per degree of freedom. |
| `entropy` | Entropy | $S_{th}$ | `J/K` | $S \ge 0$ | Measure of disorder/information. |
| `heat_flow` | Heat Flow | $\dot{Q}$ | `W` | $\mathbb{R}$ | Rate of thermal energy transfer. |

### 1.5 Electromagnetic Domain (EM)
Electric charges and field interactions.

| ID | Label | Symbol | Unit | Range | Description |
|:---|:---|:---|:---|:---|:---|
| `charge` | Electric Charge | $q$ | `C` | $\mathbb{R}$ | Fundamental charge of particle. |
| `electric_field` | Electric Field | $\mathbf{E}$ | `V/m` | $\mathbb{R}^3$ | Force per unit charge. |
| `magnetic_field` | Magnetic Field | $\mathbf{B}$ | `T` | $\mathbb{R}^3$ | Magnetic flux density. |
| `voltage` | Electric Potential | $\phi$ | `V` | $\mathbb{R}$ | Potential energy per unit charge. |

### 1.6 Quantum Domain (QT)
Atomic scale wave mechanics and probabilities.

| ID | Label | Symbol | Unit | Range | Description |
|:---|:---|:---|:---|:---|:---|
| `wavefunction` | Wavefunction | $\psi$ | `ampl` | $\mathbb{C}$ | Complex probability amplitude. |
| `prob_density` | Probability | $|\psi|^2$ | `1/m³` | $\ge 0$ | Particle localization probability. |
| `planck` | Planck Constant | $\hbar$ | `J·s` | const | Action quantum scale. |
| `eigen_energy` | Eigen Energy | $E_n$ | `eV` | $\mathbb{R}$ | Quantized energy level. |

### 1.7 Numerical Relativity (BSSN)
Spacetime curvature and evolution variables.

| ID | Label | Symbol | Unit | Range | Description |
|:---|:---|:---|:---|:---|:---|
| `lapse` | Lapse Function | $\alpha$ | - | $> 0$ | Time dilation factor (slicing). |
| `shift` | Shift Vector | $\beta^i$ | `c` | $\mathbb{R}^3$ | Spatial coordinate drift. |
| `metric` | Metric Tensor | $\gamma_{ij}$ | - | Sym | Spatial geometry of the slice. |
| `curvature` | Extrinsic Curv. | $K_{ij}$ | `1/m` | Sym | Warping of the slice in bulk. |

---

## 2. Qualitative (QLT)
*Values that are categorical, descriptive, or configuration modes.*

### 2.1 Identity & Config
Entity properties and run settings.

| ID | Label | Type | Options / Format | Description |
|:---|:---|:---|:---|:---|
| `run_id` | Run ID | `UUID` | String | Unique run identifier. |
| `scenario_name` | Scenario | `String` | e.g. "Kepler 2-Body" | Name of the test case. |
| `unit_mode` | Unit System | `Enum` | `physical`, `uet_internal` | Active measuring system. |
| `integrator` | Integrator | `Enum` | `leapfrog`, `rk4` | Numerical method utilized. |
| `body_color` | Color | `Hex` | `#RRGGBB` | Visualization color. |
| `equation_role` | Role | `Enum` | `driver`, `observer` | Component behavior mode. |

### 2.2 Status & Logic
Boolean states and result classifications.

| ID | Label | Type | Options | Description |
|:---|:---|:---|:---|:---|
| `test_status` | Status | `Enum` | `PASS`, `FAIL`, `WARN` | Outcome of a verification test. |
| `is_energy` | Is Energy? | `Bool` | `true`, `false` | Distinguishes $\Omega$ from $E$. |
| `converged` | Converged | `Bool` | `true`, `false` | Check for mathematical stability. |
| `persisted` | DB Saved | `Bool` | `true`, `false` | Write-to-disk status. |

---

## 3. Practical Usage Strategy: "The Lens System"
To make these complex units easy and usable, we do NOT show everything at once. We use **Contextual Lenses**.

### 3.1 The Three Lenses
| Lens Mode | Target User | Visible Domains | Goal |
|:---|:---|:---|:---|
| **🔭 Macro Lens** | General User | `PHY` (Speed, Mass), `THM` (Temp), `IND` (Status) | "Understand the World" (Human Scale). |
| **🧲 Field Lens** | Engineer | `EM` (Volts), `UET` (Fields), `PHY` (Forces) | Visualize invisible interactions/forces. |
| **🔬 Deep Lens** | Researcher | `QT` (Psi), `BSSN` (Curvature), `IND` (Debug) | Analyze the "Code of Reality" (Atomic/Space). |

### 3.2 Relatable Anchors (making it "Real")
Raw numbers are hard to grasp. We standardized **Comparison Units**:

- **Mass**: Display `5.97e24 kg` as **`1.0 Earths`** ($M_{\oplus}$).
- **Energy**: Display Joules as **`TNT equivalent`** or **`Hiroshimas`** for impact.
- **Speed**: Display `m/s` as **`Mach`** or **`%c`** (Speed of Light).
- **Temp**: Display Kelvin with **`C`** (Celsius) tooltip context.

### 3.3 Smart Formatting Rules
1.  **Auto-Ranging**: Always use SI Prefixes (`k`, `M`, `G`). Ex: `10,000 V` $\to$ `10 kV`.
2.  **Significant Digits**:
    - **Macro**: 2 decimal places (e.g., `12.50 kg`).
    - **Deep**: Scientific notation (e.g., `6.626e-34`).
3.  **Color Coding**:
    - **Stable/Safe**: <span style="color:green">Green</span>
    - **High Energy/Danger**: <span style="color:red">Red</span>
    - **Cold/Quantum**: <span style="color:cyan">Cyan</span>
