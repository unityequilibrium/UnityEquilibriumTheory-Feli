# Code-Only Pack Manifest

## Included ✅

| Item | Description |
|------|-------------|
| `scripts/` | All Python scripts |
| `matrices/` | Parameter sweep CSVs |
| `docs/` | Documentation |
| `*.py` | Root Python files |
| `*.ps1` | PowerShell scripts |
| `*.md` | Markdown docs (README, HANDOFF, etc.) |
| `requirements*.txt` | Dependencies |
| `PYTHON_VERSION.txt` | Python version lock |
| `pyproject.toml` | Package config |
| `reports/cross_sweeps/CROSS_SWEEP_SUMMARY.md` | Summary only |

## Excluded ❌

| Item | Reason |
|------|--------|
| `runs_*/` | Large simulation data (~GB) |
| `.venv/` / `venv/` | Virtual environment |
| `__pycache__/` | Python cache |
| `*.egg-info/` | Build artifacts |
| `logs/*.log` | Runtime logs |
| `*.zip` | Generated packs |

## Expected Size

- Code-only pack: **< 10 MB**
- Full repo with runs: **> 1 GB**
