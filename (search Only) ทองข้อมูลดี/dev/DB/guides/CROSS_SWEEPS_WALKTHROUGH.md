# Cross-sweep walkthrough (seed10)

This note explains how to reproduce and how to interpret the three cross-sweeps:

- beta × k_ratio
- beta × delta
- s × delta (optional but already executed)

## 1) Run (one-command)

From repo root (PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_cross_sweep.ps1
```

If you already have raw runs and only want to re-aggregate:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_cross_sweep.ps1 -Mode aggregate_only
```

Outputs:
- `runs_cross_*_seed10/validation_transient_v3.json`
- `runs_cross_*_seed10/validation_bias_v2.json`
- `runs_cross_*_seed10/UET_final_summary_v2.csv`

## 2) What was fixed in v2 aggregation

- `delta` was previously NaN because it lived inside nested quartic pots.
- v2 adds:
  - `delta_C`, `delta_I`
  - `s_C`, `s_I`, and `s_tilt` (if you computed a merged field)
- `OmegaT` is optional (missing column no longer fails).
- `t_relax_flag` marks whether `t_relax` is informative.

## 3) What to check (Definition of Done)

For each sweep:
- expected rows = grid_points × seeds (typically 30 × 10 = 300)
- `accepted == 1` for all rows
- `delta` and/or `delta_C/delta_I` not NaN when relevant
- `s_C/s_I/s_tilt` not NaN for s-sweeps

## 4) Summary of observed behavior (current runs)

- Vote/grade is seed-locked for these grids:
  - Seeds {0,2,4} consistently land in BIAS_I
  - The remaining seeds land in BIAS_C
  - So frac(BIAS_C)=0.7 across the grids
- `s × delta` shows strong structure in Omega and in common-mode (mean_C and mean_I move together with s).
- `t_relax` is often NOT_INFORMATIVE in these runs (band satisfied immediately).

## 5) Where to put artifacts

Recommended:

```
reports/
  cross_sweeps/
    seed10/
      (phase maps png)
      (agg csv)
      summary notes
```

Keep `runs_*` for raw results, and `reports/*` for light artifacts to share/review.
