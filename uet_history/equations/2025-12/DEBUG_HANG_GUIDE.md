# DEBUG_HANG_GUIDE (Windows/PowerShell)

Use one-line PowerShell commands (avoid \ line-continuation).

## Quick debug: run only 2 cases with progress + timeout
```powershell
cd uet_harness_v0_1
$env:PYTHONPATH="."
python scripts/run_suite.py --matrix matrices/UET_v0_8_5_pre_Tier1_PASS_matrix.csv --out runs_debug --max_cases 2 --progress_every_s 2 --wall_timeout_s 120
```

## Single case
```powershell
$env:PYTHONPATH="."
python scripts/run_case.py --case_id smoke --model C_only --params "kappa=1,M=1,V=quartic(a=1,delta=1,s=0)" --N 32 --dt 0.001 --T 0.1 --seed 0 --out runs_debug --progress_every_s 2 --wall_timeout_s 120
```
