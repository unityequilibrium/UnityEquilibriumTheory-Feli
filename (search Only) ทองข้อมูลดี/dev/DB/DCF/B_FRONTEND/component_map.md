# Component Map
## Layer B — All Frontend Components

---

## 📁 Component Hierarchy

```
frontend/src/
├── app/                    # Next.js pages (3 ONLY per R1.1)
│   ├── page.tsx           # Home
│   ├── gallery/page.tsx   # Gallery
│   └── lab/page.tsx       # Lab
│
├── components/
│   ├── shared/
│   │   └── TopNav.tsx     # Global navigation
│   ├── modals/
│   │   ├── AddEquationModal.tsx      # ✅ Created
│   │   └── PlatformSettingsModal.tsx # ✅ Created
│   ├── canvas/
│   │   ├── CanvasView.tsx         # ✅ Node graph view
│   │   ├── GraphBrowser.tsx       # ✅ Browse saved graphs
│   │   └── AIChatNode.tsx         # ✅ AI chat node
│   └── gallery/
│       └── SystemTicker.tsx
│
├── features/simulation/
│   ├── SimulationHUD.tsx  # Playback controls
│   ├── GraphDock.tsx      # Telemetry charts
│   ├── GeoSimCanvas.tsx   # ✅ GeoSim map renderer
│   ├── MetricCards.tsx    # Metric display
│   └── components/
│       ├── ExportModal.tsx
│       ├── NotesTab.tsx
│       ├── ParameterCard.tsx
│       ├── SmartParameterPanel.tsx
│       └── SmartWarning.tsx
│
├── lib/
│   └── GraphCompiler.ts   # ✅ NodeGraph → SimConfig bridge
│
└── shell/
    ├── LabShell.tsx       # Lab page layout
    ├── AppTokens.ts       # Design tokens
    └── IconButton.tsx     # Reusable button
```

---

## 🧩 Component Details

### Global Components

| Component | File | Purpose | Props |
|-----------|------|---------|-------|
| TopNav | shared/TopNav.tsx | Navigation bar | roomTitle?, onToggleExport? |
| SystemTicker | gallery/SystemTicker.tsx | Scrolling status | - |

### Shell Components

| Component | File | Purpose | Props |
|-----------|------|---------|-------|
| LabShell | shell/LabShell.tsx | Lab page wrapper | children |
| IconButton | shell/IconButton.tsx | Reusable button | icon, onClick, etc. |

### Simulation Components

| Component | File | Purpose | Props |
|-----------|------|---------|-------|
| SimulationHUD | features/simulation/SimulationHUD.tsx | Playback controls | - (uses store) |
| GraphDock | features/simulation/GraphDock.tsx | Telemetry graphs | isOpen, onToggle |
| MetricCards | features/simulation/MetricCards.tsx | Metrics display | metrics[] |

### Modal Components

| Component | File | Purpose |
|-----------|------|---------|
| ExportModal | features/simulation/components/ExportModal.tsx | Export run data |
| PlatformSettingsModal | components/modals/PlatformSettingsModal.tsx | ✅ Platform settings |
| AddEquationModal | components/modals/AddEquationModal.tsx | ✅ Add equations |

---

## ⚠️ CRITICAL RULE: Registry-First

> **AddEquationModal MUST read from EquationRegistry, NOT hardcode templates.**
> 
> Any modal that displays dynamic data (equations, metrics, rooms) MUST query
> the appropriate registry instead of using static arrays.

---

## 🔗 Full Details

See [COMPONENT_REGISTRY.md](../../platform/COMPONENT_REGISTRY.md) for complete specs.

---

**Layer:** B — Frontend Structure

