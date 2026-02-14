# UET Implementation Specification

**Version:** 0.9  
**Purpose:** Reproducible research, CI/CD, and deployment guide

---

## 1. Repository Structure

```
uet_harness_v0_1/
├── 📁 uet_min_pack/           # Core package (pip installable)
│   └── uet_core/
│       ├── __init__.py
│       ├── solver.py          # Main simulation loop
│       ├── energy.py          # Ω functional + decomposition
│       ├── potentials.py      # Quartic Landau potential
│       ├── operators.py       # Spectral operators
│       ├── variational.py     # Chemical potentials
│       ├── coercivity.py      # Stability checks
│       ├── snapshot_exporter.py   # Field export
│       └── demo_card_generator.py # Demo Card HTML
│
├── 📁 scripts/                # Command-line tools
│   ├── run_case.py           # Single case runner
│   ├── run_suite.py          # Batch runner
│   ├── run_atlas.py          # Parameter sweep
│   ├── run_with_snapshots.py # Demo runner
│   ├── generate_gallery.py   # Gallery generator
│   └── mi_card_generator.py  # MI Card tool
│
├── 📁 docs/                   # Documentation
│   ├── MATH_CORE.md          # Mathematical specification
│   ├── MI_CARD_TEMPLATE.md   # Modeling interface
│   └── example_mi_card.json  # Example MI Card
│
├── 📁 runs_*/                 # Output directories (gitignored)
│   ├── case_XXXX/
│   │   ├── config.json
│   │   ├── summary.json
│   │   ├── timeseries.csv
│   │   ├── snapshots/
│   │   └── demo_card/
│   └── ...
│
├── 📄 README.md               # Project overview
├── 📄 HANDOFF.md              # Status handoff document
├── 📄 requirements_frozen.txt # Locked dependencies
├── 📄 PYTHON_VERSION.txt      # Python version
├── 📄 setup.py                # Package setup
├── 📄 .gitignore              # Git exclusions
├── 📄 LICENSE                 # MIT License
└── 📄 run_all.ps1             # Master run script
```

---

## 2. Configuration Schema

### 2.1 Case Config (`config.json`)

```json
{
  "case_id": "case_0001",
  "run_id": "seed_42",
  "model": "C_I",
  "domain": {
    "L": 10.0,
    "dim": 2,
    "bc": "periodic"
  },
  "grid": {
    "N": 64
  },
  "time": {
    "dt": 0.01,
    "T": 10.0,
    "max_steps": 2000,
    "tol_abs": 1e-10,
    "tol_rel": 1e-10,
    "backtrack": {
      "factor": 0.5,
      "max_backtracks": 20
    }
  },
  "params": {
    "potC": {"type": "quartic", "a": -1.0, "delta": 1.0, "s": 0.3},
    "potI": {"type": "quartic", "a": -1.0, "delta": 1.0, "s": 0.3},
    "beta": 0.5,
    "kC": 0.5,
    "kI": 0.5,
    "MC": 1.0,
    "MI": 1.0
  }
}
```

### 2.2 Matrix Config (`matrix.csv`)

```csv
case_id,model,grid,dt,T,seed,params
case_0001,C_I,64,0.01,10.0,42,"{...}"
case_0002,C_I,64,0.01,10.0,43,"{...}"
...
```

---

## 3. Validators

### 3.1 Pre-run Validators

| Validator | Function | File |
|-----------|----------|------|
| Coercivity Check | `check_C_only()`, `check_CI()` | `coercivity.py` |
| Config Schema | Validate JSON structure | `run_case.py` |
| Parameter Bounds | Ensure physical validity | `coercivity.py` |

### 3.2 Runtime Validators

| Check | Condition | Action |
|-------|-----------|--------|
| NaN/Inf | `np.isfinite(C).all()` | FAIL immediately |
| Blowup | `max(abs(C)) > cap` | FAIL immediately |
| Energy Increase | `dΩ > tol` | Backtrack |
| Wall Timeout | `elapsed > limit` | FAIL with reason |

### 3.3 Post-run Validators

| Status | Conditions |
|--------|------------|
| **PASS** | Completed, Ω monotonic, no warnings |
| **WARN** | Completed but heavy backtracking (>100) |
| **FAIL** | Blowup, NaN, timeout, or energy increase |

---

## 4. Aggregators

### 4.1 Summary Aggregation

```python
# Collect all summary.json files
summaries = glob("runs_*/*/summary.json")

# Create master DataFrame
df = pd.DataFrame([json.load(open(f)) for f in summaries])

# Export
df.to_csv("master_summary.csv", index=False)
```

### 4.2 Phase Map Aggregation

```python
# Group by sweep parameters
phase_map = df.pivot_table(
    index="s",
    columns="beta",
    values="phase",
    aggfunc=lambda x: x.mode()[0]
)
```

---

## 5. Quality Gates

### 5.1 What Counts as PASS

A simulation **PASSES** if:

1. ✅ No NaN or Inf values detected
2. ✅ No blowup (max field value < cap)
3. ✅ Energy is monotonically decreasing (within tolerance)
4. ✅ Simulation completes within wall time
5. ✅ Backtracking count < 100 (otherwise WARN)

### 5.2 Why These Gates

| Gate | Rationale |
|------|-----------|
| **NaN/Inf** | Numerical instability, invalid results |
| **Blowup** | Physical solution unbounded, model failure |
| **Energy Monotone** | Gradient flow property, theory validation |
| **Wall Timeout** | Practical resource limit |
| **Backtracking** | Efficiency metric, stiff system indicator |

---

## 6. Reproducibility

### 6.1 Environment Lock

```bash
# Create environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\Activate.ps1

# Install locked deps
pip install -r requirements_frozen.txt
pip install -e ./uet_min_pack
```

### 6.2 Seed Management

```python
# Deterministic initialization
rng = np.random.default_rng(seed=42)
C = rng.normal(0.0, 0.1, size=(N, N))
```

### 6.3 Code Hash

```python
import hashlib

def compute_code_hash(files):
    h = hashlib.sha256()
    for f in sorted(files):
        h.update(open(f, "rb").read())
    return h.hexdigest()[:12]
```

---

## 7. CI/CD Configuration

### 7.1 GitHub Actions Workflow

Create `.github/workflows/test.yml`:

```yaml
name: UET Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements_frozen.txt
        pip install -e ./uet_min_pack
    
    - name: Run quick test
      run: |
        python scripts/run_with_snapshots.py \
          --case-id ci_test \
          --model C_I \
          --N 16 --T 1 \
          --out runs_ci
    
    - name: Verify output
      run: |
        test -f runs_ci/ci_test/summary.json
        python -c "import json; d=json.load(open('runs_ci/ci_test/summary.json')); assert d['status']=='PASS'"
```

### 7.2 Pre-commit Hooks

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.2.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=120]
```

---

## 8. Release Checklist

### 8.1 Before Release

- [ ] All tests pass
- [ ] README updated
- [ ] HANDOFF.md current
- [ ] Version bumped
- [ ] CHANGELOG updated
- [ ] requirements_frozen.txt updated

### 8.2 Release Process

```bash
# 1. Create release branch
git checkout -b release/v0.9.0

# 2. Update version
echo "0.9.0" > VERSION

# 3. Build code-only pack
python scripts/pack_code_only.py

# 4. Tag and push
git tag -a v0.9.0 -m "Release 0.9.0"
git push origin v0.9.0

# 5. Create GitHub release with:
#    - uet_code_only_pack.zip (code)
#    - uet_reports_seed10.zip (artifacts, optional)
```

---

## 9. Troubleshooting

### 9.1 Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: uet_core` | Package not installed | `pip install -e ./uet_min_pack` |
| `FAIL: COERCIVITY_DELTA_NEG` | δ < 0 | Use δ > 0 for bounded potential |
| `FAIL: ENERGY_INCREASE` | Stiff system | Reduce dt, increase backtrack limit |
| `FAIL: BLOWUP` | Unbounded solution | Check coercivity conditions |
| Slow simulation | Large grid | Reduce N or use shorter T for testing |

### 9.2 Debug Mode

```bash
python scripts/run_case.py config.json \
  --progress-every-steps 10 \
  --wall-timeout 60
```

---

## 10. Performance Guidelines

### 10.1 Grid Size Recommendations

| Purpose | Grid N | Notes |
|---------|--------|-------|
| CI/Quick test | 16-32 | Fast, pattern visible |
| Development | 48-64 | Good balance |
| Production | 128-256 | High resolution |
| Publication | 256-512 | Maximum quality |

### 10.2 Typical Runtimes

| N | T=10 | T=100 |
|---|------|-------|
| 32 | ~2s | ~20s |
| 64 | ~8s | ~80s |
| 128 | ~30s | ~5min |
| 256 | ~2min | ~20min |

*(Times on modern CPU, single-threaded)*
