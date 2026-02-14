# Release Checklist

## Pre-Release

- [ ] Pin environment
  ```powershell
  py -m pip freeze > requirements_frozen.txt
  py -V > PYTHON_VERSION.txt
  ```

- [ ] Verify aggregation
  ```powershell
  powershell -ExecutionPolicy Bypass -File .\run_all_cross_sweep.ps1 -Mode aggregate_only
  ```

- [ ] Smoke test (pick 1 baseline case)
  ```powershell
  py scripts/run_case.py --config runs_cross_s_delta_seed10/C_I/param_CI_sd_sp2_d1_seed0/*/config.json
  ```

## Export

- [ ] Export reports
  ```powershell
  powershell -ExecutionPolicy Bypass -File .\setup_reports.ps1
  ```

- [ ] Create code-only pack
  ```powershell
  powershell -ExecutionPolicy Bypass -File .\pack_code_only.ps1
  ```

## Verify

- [ ] Unzip to new folder and run verify
  ```powershell
  powershell -ExecutionPolicy Bypass -File .\verify_release.ps1
  ```

- [ ] Check `uet_code_only_pack.zip` size < 50 MB

## Final

- [ ] Update `CROSS_SWEEP_SUMMARY.md` with final observations
- [ ] Commit and tag: `git tag -a v0.1-seed10 -m "Cross sweep seed10 release"`
