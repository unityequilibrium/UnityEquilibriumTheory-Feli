# UET Cross-Sweep Report (seed10)

## Inputs

- UET_final_summary__beta_k_ratio_seed10.csv
- UET_final_summary__beta_delta_seed10.csv
- UET_final_summary__s_delta_seed10.csv

## Coverage & integrity checks

### beta_k_ratio

- runs_total: **300** (grid_points=30 × seeds=10)

- accepted==1 for all runs: **True**

- OmegaT all NaN: **True** (transient metric not present in summaries)

- t_relax unique values: **1** (currently constant)

- axis rows: `[0.0, 0.1, 0.3, 1.0, 3.0]`

- axis cols: `[0.1, 0.3, 1.0, 3.0, 10.0, 30.0]`

### beta_delta

- runs_total: **300** (grid_points=30 × seeds=10)

- accepted==1 for all runs: **True**

- OmegaT all NaN: **True** (transient metric not present in summaries)

- t_relax unique values: **1** (currently constant)

- axis rows: `[0.0, 0.1, 0.3, 1.0, 3.0]`

- axis cols: `[0.01, 0.1, 0.3, 1.0, 3.0, 10.0]`

### s_delta

- runs_total: **300** (grid_points=30 × seeds=10)

- accepted==1 for all runs: **True**

- OmegaT all NaN: **True** (transient metric not present in summaries)

- t_relax unique values: **1** (currently constant)

- axis rows: `[-2.0, -1.0, 0.0, 1.0, 2.0]`

- axis cols: `[0.01, 0.1, 0.3, 1.0, 3.0, 10.0]`


## Key observations

### 1) Vote/grade is seed-locked (in these 3 sweeps)

- Fraction(BIAS_C) is **0.7** everywhere (7/10 seeds), Fraction(BIAS_I) is **0.3** everywhere (3/10 seeds).

- Seeds that consistently land in **BIAS_I**: **{0,2,4}**. All other seeds land in **BIAS_C**.

- This means `grade_bias` is not sensitive to beta/delta/k_ratio/s for these grids; it behaves like a deterministic function of the seed under the current setup.


### 2) `delta` column is empty in summaries (but delta exists in case_id)

- `delta` is NaN in all 3 files; for plotting we parsed delta from `case_id` (`..._d0p3_...`).

- Recommended patch (later): extend `aggregate_final_summary.py` to parse `delta` and `s` from `case_id` into explicit columns.


### 3) Dynamics/energy signals

- **beta×k_ratio** and **beta×delta**: mean(Omega) and mean_C/mean_I are small-magnitude (~1e-4–1e-3) and vary mildly across the grid.

- **s×delta (beta=0.5)**: strong structured dependence in Omega and in the *common-mode* (mean_C and mean_I move together with s). Delta affects the amplitude.

- Bias difference `bias_CI` is essentially `mean_C - mean_I` (correlation ~1.0), but its grid dependence remains weak compared to the common-mode shift in s×delta.


## Deliverables

- Aggregated per-grid CSVs:

  - `agg_beta_k_ratio_seed10.csv`

  - `agg_beta_delta_seed10.csv`

  - `agg_s_delta_seed10.csv`

- Phase-map PNGs (mean over seeds):

  - `phase_beta_k_ratio__Omega.png`

  - `phase_beta_delta__Omega.png`

  - `phase_s_delta__Omega.png`

  - `phase_s_delta__common_mode.png`

  - `phase_beta_k_ratio__fracBIAS_C.png`

  - `phase_beta_delta__fracBIAS_C.png`

  - `phase_s_delta__fracBIAS_C.png`


- `phase_beta_k_ratio__Omega__k_ratio.png`

- `phase_beta_k_ratio__fracBIAS_C__k_ratio.png`

## Suggested next work (after plotting)

1) Patch aggregator to populate `delta` (and `s`) as explicit columns.

2) Investigate why `OmegaT` is always NaN and why `t_relax` is constant.

3) If the goal is **parameter-sensitive C-vs-I selection**, consider whether the current `grade_bias` rule is too seed-dominated (but do this only after you lock the reporting pipeline).


### Note on beta×k_ratio axis
- `case_id` contains `_r...` where `k_ratio = r^2` (because kC=r, kI=1/r). For plotting, prefer the explicit `k_ratio` column.
