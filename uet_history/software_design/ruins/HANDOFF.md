# UET Harness - Handoff Document

## สถานะโดยรวม: ~80% Complete

---

## ✅ สิ่งที่ทำเสร็จแล้ว

### 1. Core Solver Enhancement
- **เพิ่ม `mean_C`, `mean_I`, `bias_CI`** ใน `timeseries.csv`
- ไฟล์ที่แก้: `uet_core/solver.py` (บรรทัด 297-306, 330-340)
- ใช้วัด symmetry breaking / การเลือกข้าง

### 2. Validation Scripts
| Script | Function |
|--------|----------|
| `scripts/validate_transient_v3.py` | Transient metrics (t_relax, slope_init, AUC_E_norm) |
| `scripts/validate_bias.py` | Bias grading (SYM/BIAS_C/BIAS_I) |
| `scripts/validate_bias_v2.py` | Enhanced - extracts s from nested potC/potI |
| `scripts/aggregate_final_summary.py` | Combines all metrics into one CSV |
| `scripts/plot_phase_beta_s.py` | Phase map plotting |

### 3. Parameter Sweeps Completed

| Parameter | Runs | Status | Key Finding |
|-----------|------|--------|-------------|
| `s` | 140 | ✅ PASS | s>0→BIAS_C, s<0→BIAS_I, s=0→random |
| `beta` | 70 | ✅ PASS | Coupling strength affects bias locking |
| `k_ratio` | 70 | ✅ PASS | kC/kI affects field balance |
| `kappa` | 60 | ✅ PASS | Surface tension effects |
| `delta` | 120 | ✅ PASS | Potential depth effects |
| `asym` | 120 | ✅ PASS | Asymmetry in potentials |
| `Mr (MC/MI)` | 80 | ✅ PASS | Timescale ratio signature |
| `Mscale/Meq` | 60 | ✅ PASS | Overall mobility scaling |

### 4. Cross Sweeps Completed

| Cross Sweep | Runs | Status | Output |
|-------------|------|--------|--------|
| `beta × s` | 250 | ✅ PASS | `runs_betaXs/` |
| `beta × s (a=-1)` | 250 | ✅ PASS | `runs_cross_CI_beta_s_aNeg1_seed10/` |

---

## 🔸 งานที่เหลือ

### ชั้น A: จำเป็น (ก่อนสรุปว่า UET ผ่าน)

- [x] Phase map beta×s ด้วย Strength = P_BIAS_C - P_BIAS_I *(ข้อมูลมีใน `phase_prob.csv`)*

### ชั้น B: Cross sweeps เพิ่มเติม

- [ ] `beta × k_ratio` - สร้าง matrix + run
- [ ] `beta × delta` - สร้าง matrix + run  
- [ ] `s × delta` (optional) - phase boundary hunting

### ชั้น C: Release/Clean

- [ ] Schema update รองรับ mean/bias/transient columns
- [ ] รวมคำสั่ง run→validate→plot เป็น ps1 เดียว
- [ ] README สำหรับ reproduce

---

## 📁 ไฟล์สำคัญ

### Scripts
```
scripts/
├── run_suite.py              # รัน simulation matrix
├── validate_suite.py         # Equilibrium validation
├── validate_transient_v3.py  # Transient metrics
├── validate_bias_v2.py       # Bias/symmetry breaking validation
├── aggregate_final_summary.py # รวมทุก metric เป็น 1 ไฟล์
└── plot_phase_beta_s.py      # Phase map plotting
```

### Key Results
```
runs_betaXs/
├── betaXs_UET_final_summary.csv  # Full summary (250 runs)
├── phase_prob.csv                # Phase probabilities by (beta, s_tilt)
├── phase_P_BIAS_C.png            # Heatmap
└── validation_*.csv              # Various validations

runs_param_CI_s_v2/
├── CI_s_bias_v2.csv              # s sweep with bias grades
└── UET_final_summary.csv         # Full summary
```

---

## 🚀 Quick Commands

### รัน cross sweep ใหม่
```powershell
python scripts/run_suite.py --matrix matrices/YOUR_MATRIX.csv --out runs_YOUR_DIR
python scripts/aggregate_final_summary.py --runs runs_YOUR_DIR --out runs_YOUR_DIR/UET_final_summary.csv
```

### สร้าง phase probability table
```powershell
$df = Import-Csv runs_YOUR_DIR/UET_final_summary.csv
$df | Group-Object beta,s_tilt | ForEach-Object {
  $N = $_.Count
  $c = ($_.Group | ? grade_bias -eq "BIAS_C").Count
  $i = ($_.Group | ? grade_bias -eq "BIAS_I").Count
  [pscustomobject]@{ beta=$_.Name.Split(',')[0]; s_tilt=$_.Name.Split(',')[1]; P_BIAS_C=$c/$N; P_BIAS_I=$i/$N; Strength=($c-$i)/$N }
} | Export-Csv runs_YOUR_DIR/phase_prob.csv -NoTypeInformation
```

### Plot heatmap
```powershell
python -c "
import pandas as pd; import matplotlib.pyplot as plt
df = pd.read_csv('runs_YOUR_DIR/phase_prob.csv')
piv = df.pivot(index='beta', columns='s_tilt', values='Strength')
plt.imshow(piv.values, cmap='RdBu_r', vmin=-1, vmax=1)
plt.colorbar(label='Strength (C-I)')
plt.savefig('runs_YOUR_DIR/phase_strength.png', dpi=200)
"
```

---

## 📊 Key Findings

1. **s parameter** = tilt ที่ควบคุมทิศทางการเลือกข้าง (symmetry breaking)
   - s > 0 → mean_C, mean_I เป็น POS
   - s < 0 → mean_C, mean_I เป็น NEG
   - s = 0 → random (50/50)

2. **bias_CI vs sign_C/sign_I**
   - `sign_C`, `sign_I` = ขั้ว (+/-) ของแต่ละ field
   - `bias_CI` = ใครเด่นกว่า (C vs I)
   - ในหลายกรณี C ≈ I ทำให้ bias_CI ≈ 0 แม้ sign จะชัด

3. **Phase map แบน** เพราะ BIAS_C:BIAS_I ratio คล้ายกันทุก cell → ควร plot Strength แทน mean grade

---

*Last updated: 2025-12-19*
