# Equation Input Modes Specification
## Layer D — Engine Input Contract

**Last Updated:** 2024-12-24  
**Status:** 📋 NEW

---

## Overview

Equations in the Smart System can receive input data in two modes:

| Mode | Description | Use Case |
|------|-------------|----------|
| **Parameters Mode** | Individual numeric values via sliders/inputs | Interactive exploration, real-time tuning |
| **Matrix Mode** | Array/Matrix data via file import or paste | Batch processing, field data, precomputed inputs |

---

## 1. Parameters Mode (✅ Implemented)

### Description

User inputs individual numeric values through UI controls (sliders, number inputs).

### UI Components

```
┌─────────────────────────────────────────────────────────────┐
│  SMART PARAMETERS                                           │
├─────────────────────────────────────────────────────────────┤
│  κ (Kappa)             [====●=======] 0.30                  │
│  Coupling strength to equilibrium                           │
│                                                             │
│  β (Beta)              [====●=======] 0.50                  │
│  Damping coefficient                                        │
│                                                             │
│  s (Bias)              [====●=======] 0.00                  │
│  Symmetry breaking bias                                     │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```mermaid
flowchart LR
    A[User] -->|slides| B[ParameterSlider]
    B -->|setEquationParams| C[simStoreV4]
    C -->|params| D[SimCoreV4]
    D -->|step| E[EquationModule.step]
```

### Interface

```typescript
// Current parameter input interface
interface EquationParameter {
    id: string;
    label: string;
    symbol?: string;      // e.g., "κ", "β"
    defaultValue: number;
    min: number;
    max: number;
    step: number;
    unit: string;
    unitMode: UnitMode;
}
```

---

## 2. Matrix Mode (❌ Not Yet Implemented)

### Description

User provides pre-computed field data (C-field, I-field, stress tensor) instead of computing from parameters. This is useful for:
- Importing simulation results from external tools
- Testing with known field configurations
- Batch processing without real-time calculation

### UI Components (Proposed)

```
┌─────────────────────────────────────────────────────────────┐
│  MATRIX INPUT                                               │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐    │
│  │  📁 Import from File...                             │    │
│  │     Supports: .json, .csv, .npy                     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  📋 Paste Matrix Data                               │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │ [[0.5, 0.3, 0.2],                           │    │    │
│  │  │  [0.4, 0.6, 0.1],                           │    │    │
│  │  │  [0.3, 0.2, 0.5]]                           │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  Matrix Info:                                               │
│  • Dimensions: 3×3                                          │
│  • Type: C-field                                            │
│  • Unit Mode: uet_internal                                  │
│                                                             │
│  [Apply Matrix] [Clear]                                     │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow (Proposed)

```mermaid
flowchart LR
    A[File/Paste] -->|parse| B[MatrixParser]
    B -->|validate| C[MatrixValidator]
    C -->|setFieldData| D[simStoreV4]
    D -->|fieldData| E[SimCoreV4]
    E -->|injectField| F[EquationModule]
```

### Interface (Proposed)

```typescript
// Matrix input interface
interface MatrixInput {
    /** Type of field: C-field, I-field, stress, etc. */
    fieldType: 'C_field' | 'I_field' | 'stress_tensor' | 'custom';
    
    /** Matrix dimensions */
    dimensions: number[];  // e.g., [100, 100] for 2D grid
    
    /** The actual data */
    data: number[] | number[][] | number[][][];
    
    /** Unit information */
    unitMode: UnitMode;
    unit: string;
    
    /** Source metadata */
    source?: {
        fileName?: string;
        importedAt: number;
        format: 'json' | 'csv' | 'npy';
    };
}

// Extension to EquationModule
interface EquationModuleWithMatrix extends EquationModule {
    /** Whether this equation supports matrix input */
    supportsMatrixInput: boolean;
    
    /** Supported field types */
    supportedFields: string[];
    
    /** Inject pre-computed field data */
    injectFieldData(matrix: MatrixInput): void;
    
    /** Get current field for export */
    exportFieldData(): MatrixInput | null;
}
```

---

## 3. Combined Mode (Future)

User can mix parameters and matrix:
- Use matrix for initial field
- Use parameters to modify/evolve the field

```
Initial Field (Matrix) + Parameters → Evolved Field
```

---

## Implementation Priority

| Task | Priority | Dependencies |
|------|----------|--------------|
| Parameters Mode | ✅ Done | - |
| Matrix Parser (JSON) | P2 | - |
| Matrix Validator | P2 | Parser |
| Matrix Import UI | P2 | Parser, Validator |
| Field Injection | P2 | All above |
| Export Field | P3 | Field Injection |
| Combined Mode | P3 | All above |

---

## Validation Rules

### For Matrix Input

1. **Dimension Check**: Matrix dimensions must match equation expectations
2. **Value Range**: All values must be in valid range for field type
3. **Completeness**: No NaN or undefined values allowed
4. **Unit Consistency**: Unit mode must match equation's expected input

```typescript
interface MatrixValidationResult {
    valid: boolean;
    errors: {
        type: 'dimension' | 'range' | 'nan' | 'unit';
        message: string;
        location?: string;
    }[];
}
```

---

## Cross-References

- [EQUATION_SYSTEM_DESIGN.md](./EQUATION_SYSTEM_DESIGN.md) — Main equation architecture
- [SMART_FULL_SYSTEM.md](../SMART_FULL_SYSTEM.md) — Overall Smart System
- [types.ts](../../frontend/src/lib/equations/types.ts) — Type definitions

---

**Layer:** D — Flow Engine  
**Component Owner:** SimCoreV4, EquationRegistry
