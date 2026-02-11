# Test Registry Specification
## Layer REGISTRIES — Test Gates & Scenarios

**Version:** 1.0  
**Last Updated:** 2025-12-25  
**Layer:** REGISTRIES

---

## 1. Overview

Test Registry defines validation gates and test scenarios for simulation verification.

---

## 2. Test Gate Definitions

| Gate | Name | Level | Purpose |
|------|------|-------|---------|
| G0 | Data/Schema | L0 | Compile-time checks |
| G1 | Runner | L1 | Runtime start |
| G2 | Oracle | L2 | Physics validation |
| G3 | Integration | L3 | API/DB checks |
| G4 | UI | L4 | E2E flow |

---

## 3. Gate Specifications

### G0: Data/Schema

```typescript
interface G0Test {
  gate_id: 'G0';
  checks: [
    'metric_registry_complete',
    'schema_valid',
    'types_compile'
  ];
  pass_criteria: 'all_pass';
}
```

### G1: Runner

```typescript
interface G1Test {
  gate_id: 'G1';
  checks: [
    'deterministic',
    'no_nan_inf',
    'snapshot_works'
  ];
  tolerances: {
    determinism: 1e-10;
    energy_drift: 1e-6;
  };
}
```

### G2: Oracle

```typescript
interface G2Test {
  gate_id: 'G2';
  scenarios: [
    'inertial_1body',
    'kepler_2body',
    'dt_convergence'
  ];
  tolerances: {
    position: 1e-6;
    velocity: 1e-6;
    convergence_order: 2;
  };
}
```

### G3: Integration

```typescript
interface G3Test {
  gate_id: 'G3';
  checks: [
    'api_save_creates_run',
    'telemetry_persisted',
    'notes_synced'
  ];
}
```

### G4: UI

```typescript
interface G4Test {
  gate_id: 'G4';
  checks: [
    'metric_checkbox_to_dock',
    'plot_group_overlay',
    'save_export_left_only'
  ];
}
```

---

## 4. Test Scenarios

| Scenario | Gate | Description | Expected |
|----------|------|-------------|----------|
| inertial_1body | G2 | Single body, no forces | Constant velocity |
| kepler_2body | G2 | Sun-planet orbit | Analytic match |
| dt_convergence | G2 | Error vs dt | Order 2 |
| energy_conservation | G1 | Closed system | |ΔE| < 1e-6 |

---

## 5. TypeScript Interface

```typescript
interface TestGateDefinition {
  gate_id: 'G0' | 'G1' | 'G2' | 'G3' | 'G4';
  name: string;
  level: 'L0' | 'L1' | 'L2' | 'L3' | 'L4';
  checks: string[];
  tolerances?: Record<string, number>;
  scenarios?: string[];
  pass_criteria: 'all_pass' | 'majority' | 'any';
}

const TEST_GATES: TestGateDefinition[] = [
  {
    gate_id: 'G0',
    name: 'Data/Schema',
    level: 'L0',
    checks: ['metric_registry_complete', 'schema_valid'],
    pass_criteria: 'all_pass'
  },
  // ... more gates
];
```

---

## 6. Traceability

| This Doc | Links To |
|----------|----------|
| Gate levels | global_rules.md R7 |
| Oracle tests | lib/oracle/ |
| Test runner | lib/oracle/testRunner.ts |

---

**Status:** ✅ SPEC LOCKED
