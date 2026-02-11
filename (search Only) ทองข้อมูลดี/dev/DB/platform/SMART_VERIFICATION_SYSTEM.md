# Smart Verification System - Production Level

> **Related Documents:**
> - [SMART_INDEX](design_system/SMART_INDEX.md) ← Smart System Master
> - [SMART_SIMULATION_DESIGN](design_system/SMART_SIMULATION_DESIGN.md) ← Simulation Engine
> - [BACKEND_ARCHITECTURE](BACKEND_ARCHITECTURE.md) ← Server Design
> - [DATABASE_SCHEMA](DATABASE_SCHEMA.md) ← Data Structures

> **Purpose:** Production-level verification system covering ALL aspects of the UET Platform
> **Last Updated:** 2024-12-24

---

## 🎯 Verification Levels

| Level | Name | Frequency | Gate |
|-------|------|-----------|------|
| **L0** | Sanity | Every commit | CI Required |
| **L1** | Unit | Every PR | CI Required |
| **L2** | Integration | Daily | Nightly Build |
| **L3** | Physics | Weekly | Release Gate |
| **L4** | Performance | Release | Production Gate |
| **L5** | Security | Release | Production Gate |

---

## 📋 L0: SANITY CHECKS (Every Commit)

### 0.1 Build Verification
```
□ TypeScript compiles without errors
□ ESLint passes with no errors
□ No console.log() in production code
□ All imports resolve correctly
□ No circular dependencies
```

### 0.2 Smart System Sanity
```
□ metrics.json is valid JSON
□ All metric IDs are unique
□ All equation parameters exist in metrics.json
□ UnitConverter.ts has no hardcoded values
□ All stores initialize without error
```

**Command:**
```powershell
bun run build && bun run lint
```

---

## 🧪 L1: UNIT TESTS (Every PR)

### 1.1 Smart Unit Converter
```
□ convert(1, 'kg', 'kg') === 1
□ convert(5.97e24, 'kg', 'earths') === 1.0 ± 0.001
□ convert(299792458, 'm/s', 'c') === 1.0 ± 0.001
□ Temperature conversion handles offset (K to C)
□ Unknown unit throws error
□ Null/undefined input handled
```

### 1.2 Smart Metric Registry
```
□ getMetrics() returns all 20+ metrics
□ getMetric('kappa') returns correct definition
□ getMetric('nonexistent') returns undefined
□ getVisibleMetrics() returns default_visible only
□ groupMetricsByPlotGroup() groups correctly
```

### 1.3 Smart Equation Registry
```
□ get('newton') returns Newton module
□ get('nonexistent') returns undefined
□ enable/disable toggles correctly
□ Compatibility check detects conflicts
□ Parameter loading from definition
```

### 1.4 Smart Stores
```
□ useUnitStore initializes empty
□ setPreference persists value
□ getPreference retrieves value
□ resetToDefaults clears all
□ localStorage integration works
```

### 1.5 Smart Components
```
□ SmartMetric renders value correctly
□ SmartMetric converts on unit change
□ ParameterCard respects min/max
□ ParameterCard shows warning
□ SmartChart throttles to 5fps
```

**Command:**
```powershell
bun test --coverage
```

---

## 🔗 L2: INTEGRATION TESTS (Daily)

### 2.1 Smart Data Flow
```
□ SimCoreV4 → TelemetryBuffer → SmartChart
□ EquationSelector → ParameterPanel auto-populate
□ Unit change → Chart axis update
□ Preference save → localStorage → reload
□ API /registry → Frontend MetricRegistry
```

### 2.2 Smart API Integration
```
□ GET /api/registry returns all metrics
□ GET /api/equations returns all equations
□ GET /api/preferences returns user prefs
□ PUT /api/preferences updates correctly
□ Error responses follow standard format
```

### 2.3 Database Integration
```
□ metric_registry table synced with JSON
□ equation_modules table has all equations
□ run_equations stores parameter values
□ telemetry_samples stores SI values only
□ Prisma migrations up to date
```

### 2.4 End-to-End Flow
```
□ Load page → MetricRegistry fetched
□ Select equation → Params auto-generated
□ Start simulation → Telemetry updates
□ Change unit → Display converts
□ Save run → Database persists
□ Reload → State restored
```

**Command:**
```powershell
bun run test:integration
```

---

## 🔬 L3: PHYSICS VERIFICATION (Weekly)

### 3.1 Invariant Checks
| Check | Formula | Tolerance | PASS Criteria |
|-------|---------|-----------|---------------|
| **Energy** | `\|E_t - E_0\| / \|E_0\|` | 1e-2 (1%) | Drift ≤ 1% |
| **Angular Momentum** | `\|L_t - L_0\| / \|L_0\|` | 1e-3 (0.1%) | Drift ≤ 0.1% |
| **COM Velocity** | `\|v_COM\|` | 1e-6 | Near zero |
| **NaN Detection** | Any NaN/Inf | 0 | None found |

### 3.2 Test Gates
| Gate | Scenario | Expected | Status |
|------|----------|----------|--------|
| **G0** | Determinism | Same seed → Same output | □ |
| **G0** | No NaN | 10000 steps without NaN | □ |
| **G1** | Inertial | r(t) = r₀ + v₀t ± 1e-10 | □ |
| **G2** | Kepler Circular | vs Analytic ± 1e-6 | □ |
| **G2** | Kepler Elliptic | vs Analytic ± 1e-5 | □ |
| **G3** | Convergence | dt/2 → error/4 | □ |
| **G4** | N-body Stress | 10 bodies stable | □ |
| **G4** | UET Field | (Expected Fail) | □ |

### 3.3 Smart Physics Integration
```
□ Equation toggle doesn't break invariants
□ Parameter change doesn't cause NaN
□ Multiple equations don't conflict
□ Unit conversion doesn't affect physics
□ Chart displays correct SI values
```

**Command:**
```powershell
bun run test:physics
```

---

## ⚡ L4: PERFORMANCE (Release)

### 4.1 Simulation Performance
| Metric | Target | Maximum |
|--------|--------|---------|
| Step computation | < 1ms | 5ms |
| 100 bodies | 60 FPS | 30 FPS min |
| 1000 bodies | 30 FPS | 15 FPS min |
| Memory usage | < 256MB | 512MB |

### 4.2 UI Performance
| Metric | Target | Maximum |
|--------|--------|---------|
| Initial load | < 2s | 5s |
| Chart update | < 16ms (60fps) | 33ms (30fps) |
| Unit conversion | < 1ms | 5ms |
| Parameter slider | No lag | < 16ms |

### 4.3 API Performance
| Endpoint | Target | Maximum |
|----------|--------|---------|
| GET /api/registry | < 50ms | 200ms |
| GET /api/telemetry | < 100ms | 500ms |
| POST /api/runs | < 200ms | 1s |
| Database query | < 10ms | 50ms |

### 4.4 Smart System Performance
```
□ TelemetryBuffer throttles to 5fps
□ SmartChart memoization working
□ Unit conversion uses cached factors
□ MetricRegistry singleton pattern
□ No memory leaks in simulation loop
```

**Commands:**
```powershell
bun run test:performance
bun run lighthouse
```

---

## 🔒 L5: SECURITY (Release)

### 5.1 Code Security
```
□ No eval() or Function() calls
□ No dangerouslySetInnerHTML with user input
□ No hardcoded secrets or API keys
□ All user input sanitized
□ No SQL injection vectors
□ No XSS vulnerabilities
```

### 5.2 Smart System Security
```
□ metrics.json has no executable code
□ UnitConverter.ts no eval for formulas
□ localStorage keys prefixed (collision prevention)
□ API endpoints validate all inputs
□ No sensitive data in console.log
```

### 5.3 Dependency Security
```
□ npm audit shows 0 critical vulnerabilities
□ npm audit shows 0 high vulnerabilities
□ All dependencies up to date
□ No deprecated packages
□ License compliance verified
```

### 5.4 Data Security
```
□ Telemetry stores SI only (no user data leak)
□ Preferences don't store PII
□ Export doesn't include secrets
□ Database connection encrypted
□ API uses HTTPS in production
```

**Commands:**
```powershell
npm audit
bun run test:security
```

---

## 📊 PRODUCTION CHECKLIST

### Pre-Release Gate
```
□ All L0-L5 tests passing
□ Code coverage > 80%
□ No critical bugs open
□ Documentation updated
□ CHANGELOG updated
□ Version bumped
```

### Smart System Release Gate
```
□ SMART_INDEX.md up to date
□ All 5 Smart docs current
□ metrics.json complete
□ All conversions verified
□ API endpoints documented
□ TypeScript types exported
```

### Deployment Verification
```
□ Docker build succeeds
□ Health endpoint returns healthy
□ Metrics endpoint returns data
□ Database migrations applied
□ Environment variables set
□ CORS configured correctly
```

---

## 🤖 AUTOMATED CI/CD

### GitHub Actions Workflow
```yaml
name: Smart Verification

on: [push, pull_request]

jobs:
  l0-sanity:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: bun install
      - run: bun run build
      - run: bun run lint
      
  l1-unit:
    needs: l0-sanity
    runs-on: ubuntu-latest
    steps:
      - run: bun test --coverage
      
  l2-integration:
    needs: l1-unit
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
    steps:
      - run: bun run test:integration
      
  l3-physics:
    needs: l2-integration
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: bun run test:physics
```

---

## 📈 TEST COVERAGE TARGETS

| Category | Target | Current |
|----------|--------|---------|
| Smart Components | 90% | □ |
| Smart Stores | 95% | □ |
| Smart Services | 85% | □ |
| Physics Engine | 80% | □ |
| API Routes | 75% | □ |
| **Overall** | **85%** | □ |

---

## 🚨 FAILURE PROTOCOL

### On Test Failure:
1. **L0 Fail** → Block merge, immediate fix required
2. **L1 Fail** → Block merge, fix before review
3. **L2 Fail** → Notify team, fix within 24h
4. **L3 Fail** → Investigate physics, may be expected
5. **L4 Fail** → Profile and optimize
6. **L5 Fail** → Immediate security review

### Smart System Failure:
| Failure Type | Severity | Action |
|--------------|----------|--------|
| Unit conversion wrong | HIGH | Block release |
| Metric missing | MEDIUM | Add to registry |
| Chart lag | LOW | Performance tune |
| Type error | HIGH | Fix immediately |

---

> **NOTE:** This verification system ensures production-ready quality.
> All tests must pass before any release to production.
