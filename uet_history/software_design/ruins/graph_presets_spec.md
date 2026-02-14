# Graph Presets Specification
## REGISTRIES - Node Graph Presets

**Version:** 1.0  
**Last Updated:** 2025-12-25  
**Layer:** REGISTRIES

---

## 1. Purpose

Map Room → NodeGraph presets for Canvas View

---

## 2. Schema

```typescript
interface GraphPreset {
    roomId: string;           // Links to roomRegistry
    nodes: NodeInstance[];    // Pre-configured nodes
    edges: Edge[];            // Pre-configured connections
}
```

---

## 3. Current Presets (2/62)

| roomId | Nodes | Edges | Status |
|--------|-------|-------|--------|
| `solarSystem` | 10 | 10 | ✅ Implemented |
| `threeBody` | 5 | 4 | ✅ Implemented |

---

## 4. Node Layout (solarSystem)

```
Clock → World → Newton  → Integrator → Energy → Plot
              → UET    ↗            → Omega  ↗
                                    → Renderer

AI Copilot (standalone)
```

---

## 5. Node Types Used

| Type | Count | Purpose |
|------|-------|---------|
| sim-driver | 2 | Clock, World State |
| equation | 2 | Newton, UET |
| integrator | 1 | Leapfrog |
| metric | 2 | Energy, Omega |
| plot | 2 | Plot, 3D Renderer |
| ai-chat | 1 | AI Copilot |

---

## 6. File Location

```
frontend/src/lib/graphPresets.ts
```

---

## 7. Usage

```typescript
import { getGraphPreset } from '@/lib/graphPresets';

const graph = getGraphPreset(roomId);
// Returns { nodes, edges } or empty graph
```

---

## 8. Traceability

| This Doc | Links To |
|----------|----------|
| roomId | REGISTRIES/registries_spec.md roomRegistry |
| NodeSpec | D_FLOW_ENGINE/node_contract.md |
| Canvas rendering | B_FRONTEND/smart_system.md |

---

**Status:** ⚠️ PARTIAL (2/62 presets implemented)
