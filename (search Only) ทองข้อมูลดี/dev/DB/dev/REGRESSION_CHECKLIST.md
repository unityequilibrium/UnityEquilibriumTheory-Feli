# Regression checklist (lightweight)

Goal: detect silent breakage after refactors, without rerunning everything.

## A) Smoke test: aggregate-only
- Command:
  - `run_all_cross_sweep.ps1 -Mode aggregate_only`
- Expect:
  - completes without error
  - each sweep writes `UET_final_summary_v2.csv`
  - plots are generated under `runs_cross_*_seed10/plots/`

## B) Coverage sanity
For each `UET_final_summary_v2.csv`:
- expected rows = 300 (30 grid points × 10 seeds)
- `accepted == 1` for all rows
- `delta_C/delta_I` not NaN in delta-sweeps
- `s_tilt` not NaN in s-sweep

## C) Baseline quick rerun (small)
Pick ONE small matrix (e.g. 5–10 cases) and:
- run_suite → validate → aggregate
- compare:
  - fraction accepted
  - summary column presence (delta/s fields)
  - basic ranges for Omega, mean_C, mean_I (no huge jumps)

## D) Determinism (optional)
Rerun a tiny subset with fixed seeds and confirm the grade/summary is stable.
