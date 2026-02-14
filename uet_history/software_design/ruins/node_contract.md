# Node Contract Specification
## UET Platform - Node Standard Interface

**Version:** 1.0  
**Last Updated:** 2024-12-25  
**Layer:** D (Flow/Engine)

---

# 1. Port Types

```typescript
type PortType = 
  | 'number'
  | 'vector3'
  | 'matrix'
  | 'particles'      // WorldState
  | 'telemetry'      // MetricStream
  | 'scene'          // Three.js Scene
  | 'text'           // String/Markdown
  | 'report'         // Test Result
  | 'command';       // Terminal Command

interface Port {
  id: string;
  name: string;
  type: PortType;
  required: boolean;
  multiple?: boolean;
}
```

---

# 2. Unit Categories

```typescript
type UnitCategory = 'QNT' | 'QLT';

// QNT (Quantitative) - มีหน่วย SI
type QNTUnit = 'J' | 'kg' | 'm' | 's' | 'm/s' | 'N' | 'rad' | '%';

// QLT (Qualitative) - label/state
type QLTValue = 'PASS' | 'FAIL' | 'WARN' | string;

interface UnitSpec {
  category: UnitCategory;
  unit?: QNTUnit;
  format?: string;  // '0.000' (QNT) or null (QLT)
}
```

---

# 3. Cost Specification

```typescript
interface CostSpec {
  cpu_ms_per_tick: number;    // ประมาณ CPU time
  gpu_ms_per_frame?: number;  // ถ้าใช้ GPU
  mem_estimate: number;       // bytes
  bandwidth_out: number;      // points/sec
}
```

---

# 4. Update Modes

```typescript
type UpdateMode = 
  | 'event'    // trigger เมื่อมี input
  | 'tick'     // ทุก sim step
  | 'frame'    // ทุก render frame
  | 'batch';   // สะสม N แล้วค่อยทำ
```

---

# 5. Trace Hooks

```typescript
interface TraceHooks {
  lastInput: any;
  lastOutput: any;
  latency: number;        // ms
  status: 'idle' | 'running' | 'blocked' | 'error';
  queueLength: number;
}
```

---

# 6. Complete Node Interface

```typescript
interface NodeSpec {
  // Identity
  id: string;
  type: string;
  title: string;
  
  // I/O
  inputs: Port[];
  outputs: Port[];
  
  // Config
  params: ParamDef[];
  locks: string[];        // locked in test mode
  
  // Units
  units: UnitSpec;
  
  // Determinism
  deterministic: boolean;
  requiresSeed: boolean;
  
  // Performance
  cost: CostSpec;
  updateMode: UpdateMode;
  
  // Error Handling
  errorTypes: string[];
  
  // Runtime
  trace: TraceHooks;
  
  // Persistence
  persistence: {
    saveToDb: boolean;
    fields: string[];
  };
}
```

---

# 7. Example Nodes

## 7.1 Equation Node

```typescript
const newtonNode: NodeSpec = {
  id: 'newton-1',
  type: 'equation',
  title: 'Newton Gravity',
  inputs: [{ id: 'state', type: 'particles', required: true }],
  outputs: [{ id: 'forces', type: 'vector3', required: true }],
  params: [
    { id: 'G', type: 'number', default: 6.674e-11 }
  ],
  locks: ['G'],
  units: { category: 'QNT', unit: 'N' },
  deterministic: true,
  requiresSeed: false,
  cost: { cpu_ms_per_tick: 2, mem_estimate: 1024, bandwidth_out: 0 },
  updateMode: 'tick',
  errorTypes: ['DIVIDE_BY_ZERO'],
  trace: { lastInput: null, lastOutput: null, latency: 0, status: 'idle', queueLength: 0 },
  persistence: { saveToDb: false, fields: [] }
};
```

## 7.2 Metric Node

```typescript
const energyNode: NodeSpec = {
  id: 'energy-1',
  type: 'metric',
  title: 'Total Energy',
  inputs: [{ id: 'state', type: 'particles', required: true }],
  outputs: [{ id: 'value', type: 'telemetry', required: true }],
  params: [],
  locks: [],
  units: { category: 'QNT', unit: 'J', format: '0.000e+0' },
  deterministic: true,
  requiresSeed: false,
  cost: { cpu_ms_per_tick: 0.5, mem_estimate: 256, bandwidth_out: 60 },
  updateMode: 'tick',
  errorTypes: [],
  trace: { lastInput: null, lastOutput: null, latency: 0, status: 'idle', queueLength: 0 },
  persistence: { saveToDb: true, fields: ['value'] }
};
```

---

**Status:** 📋 SPEC LOCKED
