# Cross Sweeps Walkthrough

## Quick Start

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run all cross-sweeps (matrix → simulate → aggregate)
powershell -ExecutionPolicy Bypass -File .\run_all_cross_sweep.ps1

# 3. Or just re-aggregate existing results
powershell -ExecutionPolicy Bypass -File .\run_all_cross_sweep.ps1 -Mode aggregate_only
```

---

## Sweep Summary (seed10)

| Sweep | Axes | Runs Dir | Summary File |
|-------|------|----------|--------------|
| β × k_ratio | beta=[0.1,0.5,1,2,5], k_ratio=[0.1,0.5,1,2,10] | `runs_cross_beta_k_ratio_seed10/` | `UET_final_summary_v2.csv` |
| β × δ | beta=[0.1,0.5,1,2,5], delta=[0.01,0.1,0.3,1,3,10] | `runs_cross_beta_delta_seed10/` | `UET_final_summary_v2.csv` |
| s × δ | s=[-2,-1,0,1,2], delta=[0.01,0.1,0.3,1,3,10] | `runs_cross_s_delta_seed10/` | `UET_final_summary_v2.csv` |

---

## Key Output Columns

| Column | Description |
|--------|-------------|
| `delta`, `delta_C`, `delta_I` | Λ (cosmological constant) from potC/potI |
| `s_C`, `s_I`, `s_tilt` | Tilt parameter |
| `k_ratio` | kC/kI ratio |
| `grade_bias` | SYM / BIAS_C / BIAS_I |
| `t_relax` | Relaxation time (5% band) |
| `t_relax_flag` | OK / NOT_INFORMATIVE |

---

## Regression Check

To verify results match previous runs:
1. Pick one baseline case (e.g., `param_CI_sd_sp2_d1_seed0`)
2. Re-run with same seed
3. Compare `Omega`, `bias_CI` values (should match within floating-point tolerance)
