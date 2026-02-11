# Smart Data Dictionary

> **Related Documents:**
> - [SMART_INDEX](design_system/SMART_INDEX.md) ← Master Index
> - [SMART_SYSTEM_DESIGN](design_system/SMART_SYSTEM_DESIGN.md) ← Parameter System
> - [SMART_UNIT_COMPONENT](design_system/SMART_UNIT_COMPONENT.md) ← Unit Converter
> - [SMART_PLOTLY_DESIGN](design_system/SMART_PLOTLY_DESIGN.md) ← Charts

> **Master Registry of All Metrics, Parameters, and Units**  
> ใช้เป็น Single Source of Truth สำหรับทั้ง Database และ Frontend

---

## 1. Quantitative (QNT) - ค่าที่วัดได้

### 1.1 Physical Domain (PHY) - ฟิสิกส์พื้นฐาน

| ID | Label | Symbol | Unit | Range | Smart Config |
|:---|:---|:---|:---|:---|:---|
| `time` | Simulation Time | $t$ | `s` | $t \ge 0$ | `{ locked: false, format: 'decimal' }` |
| `dt` | Time Step | $\Delta t$ | `s` | $0 < dt \ll T$ | `{ locked: false, step: 0.001 }` |
| `mass` | Mass | $m$ | `kg` | $m > 0$ | `{ units: ['kg', 'Earths', 'Suns'] }` |
| `position` | Position | $\mathbf{r}$ | `m` | $\mathbb{R}^3$ | `{ units: ['m', 'km', 'AU', 'ly'] }` |
| `velocity` | Velocity | $\mathbf{v}$ | `m/s` | $\mathbb{R}^3$ | `{ units: ['m/s', 'km/h', 'Mach', '%c'] }` |
| `total_energy` | Total Energy | $E$ | `J` | $\mathbb{R}$ | `{ units: ['J', 'kWh', 'TNT', 'eV'], chart: true }` |
| `kinetic_energy`| Kinetic Energy | $K$ | `J` | $K \ge 0$ | `{ chart: true }` |
| `potential_energy`| Grav. Potential | $U$ | `J` | $U \le 0$ | `{ chart: true }` |
| `angular_momentum`| Angular Momentum | $L$ | `kg·m²/s` | $\ge 0$ | `{ chart: true }` |
| `g_const` | Gravitational Const | $G$ | `m³/kg·s²`| $G \ge 0$ | `{ locked: true }` |
| `c_light` | Speed of Light | $c$ | `m/s` | $c > 0$ | `{ locked: true, warning: 'Physical constant' }` |

### 1.2 UET Domain - ทฤษฎี Unified Equilibrium

| ID | Label | Symbol | Unit | Range | Smart Config |
|:---|:---|:---|:---|:---|:---|
| `omega` | Omega Functional | $\Omega$ | `UET` | $\mathbb{R}$ | `{ chart: true, warning: 'NOT Energy!' }` |
| `omega_grad` | Omega Gradient | $\nabla\Omega$ | `UET/s` | $\mathbb{R}$ | `{ chart: true }` |
| `c_field` | C-Field | $C$ | `UET` | $[0, 1]$ | `{ chart: true }` |
| `i_field` | I-Field | $I$ | `UET` | $[0, 1]$ | `{ chart: true }` |
| `kappa` | Coupling | $\kappa$ | - | $[0, 2]$ | `{ slider: true, step: 0.01 }` |
| `beta` | Nonlinearity | $\beta$ | - | $[0, 2]$ | `{ slider: true, step: 0.01 }` |
| `tilt` | Symmetry Tilt | $s$ | - | $[-1, 1]$ | `{ slider: true, step: 0.01 }` |
| `lambda` | Decay Length | $\lambda$ | - | $[0, 1]$ | `{ warning_if: 'value === 0', warning: 'May cause instability' }` |
| `alpha` | Diffusion | $\alpha$ | - | $[0, 1]$ | `{ slider: true }` |

### 1.3 Indicators & Counts (IND/CNT)

| ID | Label | Symbol | Unit | Range | Smart Config |
|:---|:---|:---|:---|:---|:---|
| `stability_score` | Stability | $S$ | `%` | $0-100$ | `{ format: 'percent', color_code: true }` |
| `energy_drift` | Energy Drift | $\delta E$ | `%` | $\ge 0$ | `{ warning_if: 'value > 0.01' }` |
| `com_drift` | COM Drift | $v_{com}$ | `m/s` | $\ge 0$ | `{ format: 'scientific' }` |
| `step_count` | Steps | $N$ | `#` | $\mathbb{Z}^+$ | `{ computed: true, formula: 'T / dt' }` |
| `body_count` | Bodies | $N_{body}$ | `#` | $\mathbb{Z}^+$ | `{ readonly: true }` |
| `softening` | Softening | $\epsilon$ | `m` | $\ge 0$ | `{ slider: true }` |

### 1.4 Thermodynamic Domain (THM)

| ID | Label | Symbol | Unit | Range | Smart Config |
|:---|:---|:---|:---|:---|:---|
| `temperature` | Temperature | $T_{sys}$ | `K` | $T \ge 0$ | `{ units: ['K', 'C', 'F'] }` |
| `entropy` | Entropy | $S_{th}$ | `J/K` | $S \ge 0$ | `{ format: 'scientific' }` |
| `heat_flow` | Heat Flow | $\dot{Q}$ | `W` | $\mathbb{R}$ | `{ chart: true }` |

### 1.5 Electromagnetic Domain (EM)

| ID | Label | Symbol | Unit | Range | Smart Config |
|:---|:---|:---|:---|:---|:---|
| `charge` | Electric Charge | $q$ | `C` | $\mathbb{R}$ | `{}` |
| `electric_field` | Electric Field | $\mathbf{E}$ | `V/m` | $\mathbb{R}^3$ | `{}` |
| `magnetic_field` | Magnetic Field | $\mathbf{B}$ | `T` | $\mathbb{R}^3$ | `{}` |
| `voltage` | Electric Potential | $\phi$ | `V` | $\mathbb{R}$ | `{ units: ['V', 'kV', 'MV'] }` |

### 1.6 Quantum Domain (QT)

| ID | Label | Symbol | Unit | Range | Smart Config |
|:---|:---|:---|:---|:---|:---|
| `wavefunction` | Wavefunction | $\psi$ | `ampl` | $\mathbb{C}$ | `{}` |
| `prob_density` | Probability | $|\psi|^2$ | `1/m³` | $\ge 0$ | `{ chart: true }` |
| `planck` | Planck Constant | $\hbar$ | `J·s` | const | `{ locked: true }` |
| `eigen_energy` | Eigen Energy | $E_n$ | `eV` | $\mathbb{R}$ | `{}` |

### 1.7 Numerical Relativity (BSSN)

| ID | Label | Symbol | Unit | Range | Smart Config |
|:---|:---|:---|:---|:---|:---|
| `lapse` | Lapse Function | $\alpha$ | - | $> 0$ | `{}` |
| `shift` | Shift Vector | $\beta^i$ | `c` | $\mathbb{R}^3$ | `{}` |
| `metric` | Metric Tensor | $\gamma_{ij}$ | - | Sym | `{}` |
| `curvature` | Extrinsic Curv. | $K_{ij}$ | `1/m` | Sym | `{}` |

---

## 2. Qualitative (QLT) - ค่าที่เป็น Category/Config

### 2.1 Identity & Config

| ID | Label | Type | Options | Smart Config |
|:---|:---|:---|:---|:---|
| `run_id` | Run ID | `UUID` | String | `{ readonly: true }` |
| `scenario_name` | Scenario | `String` | e.g. "Kepler 2-Body" | `{ input: true }` |
| `unit_mode` | Unit System | `Enum` | `physical`, `uet_internal` | `{ dropdown: true }` |
| `integrator` | Integrator | `Enum` | `leapfrog`, `rk4` | `{ dropdown: true }` |
| `body_color` | Color | `Hex` | `#RRGGBB` | `{ color_picker: true }` |
| `equation_role` | Role | `Enum` | `driver`, `observer`, `coupled` | `{ dropdown: true }` |

### 2.2 Status & Logic

| ID | Label | Type | Options | Smart Config |
|:---|:---|:---|:---|:---|
| `test_status` | Status | `Enum` | `PASS`, `FAIL`, `WARN` | `{ color_code: true }` |
| `is_energy` | Is Energy? | `Bool` | `true`, `false` | `{ warning: 'Ω is NOT energy by default' }` |
| `converged` | Converged | `Bool` | `true`, `false` | `{}` |
| `persisted` | DB Saved | `Bool` | `true`, `false` | `{ readonly: true }` |

---

## 3. Smart Unit Conversion Map

### 3.1 Compatible Units (from Database)

```json
{
  "mass": {
    "base": "kg",
    "units": [
      { "id": "kg", "label": "kg", "factor": 1 },
      { "id": "earths", "label": "Earths (M⊕)", "factor": 1.674e-25 },
      { "id": "suns", "label": "Suns (M☉)", "factor": 5.03e-31 },
      { "id": "saturns", "label": "Saturns", "factor": 1.76e-27 }
    ]
  },
  "velocity": {
    "base": "m/s",
    "units": [
      { "id": "m/s", "label": "m/s", "factor": 1 },
      { "id": "km/h", "label": "km/h", "factor": 3.6 },
      { "id": "mach", "label": "Mach", "factor": 0.00291 },
      { "id": "c", "label": "% c", "factor": 3.336e-9 }
    ]
  },
  "energy": {
    "base": "J",
    "units": [
      { "id": "J", "label": "J", "factor": 1 },
      { "id": "kWh", "label": "kWh", "factor": 2.778e-7 },
      { "id": "tnt", "label": "tons TNT", "factor": 2.39e-10 },
      { "id": "eV", "label": "eV", "factor": 6.242e18 }
    ]
  },
  "temperature": {
    "base": "K",
    "units": [
      { "id": "K", "label": "K", "factor": 1 },
      { "id": "C", "label": "°C", "offset": -273.15 },
      { "id": "F", "label": "°F", "formula": "(K - 273.15) * 9/5 + 32" }
    ]
  }
}
```

---

## 4. Lens System (ระดับการแสดงผล)

| Lens Mode | Target User | Visible Domains | Smart Filter |
|:---|:---|:---|:---|
| **🔭 Macro** | General User | `PHY`, `THM`, `IND` | `{ lens: 'macro', default_visible: true }` |
| **🧲 Field** | Engineer | `EM`, `UET`, `PHY` | `{ lens: 'field' }` |
| **🔬 Deep** | Researcher | `QT`, `BSSN`, `IND` | `{ lens: 'deep', format: 'scientific' }` |

---

## 5. Smart Formatting Rules

### 5.1 Auto-Ranging (SI Prefixes)
```
10,000 V → 10 kV
0.000001 m → 1 μm
5,970,000,000,000,000,000,000,000 kg → 5.97 Yg
```

### 5.2 Format by Lens
| Lens | Format | Example |
|------|--------|---------|
| Macro | 2 decimal | `12.50 kg` |
| Field | 4 significant | `1.234e+10` |
| Deep | Full scientific | `6.62607015e-34` |

### 5.3 Color Coding
| Condition | Color | CSS |
|-----------|-------|-----|
| Stable/Safe | 🟢 Green | `#4ade80` |
| Warning | 🟡 Yellow | `#fbbf24` |
| Danger/High Energy | 🔴 Red | `#f87171` |
| Cold/Quantum | 🔵 Cyan | `#4ecdc4` |

---

> **Note:** ไฟล์นี้เป็น Single Source of Truth  
> หากต้องการเพิ่ม Metric ใหม่ ให้เพิ่มที่นี่แล้ว sync กับ `metrics.json`
