# GeoSimCanvas Component Specification
## UET Platform - Map-Based Simulation Canvas

**Last Updated:** 2024-12-25  
**Purpose:** Document the GeoSim canvas component for map-based simulations

---

## Overview

GeoSimCanvas is the rendering layer for geosim room types. It replaces the standard 3D canvas with an interactive map.

---

## Component Interface

```typescript
interface GeoSimCanvasProps {
  room: RoomDefinition;          // Must be type: 'geosim'
  geoConfig: GeoConfig;          // Map configuration
  equations: EquationModule[];   // Active equations
  onMetricUpdate: (metrics: Map<string, number>) => void;
}

interface GeoConfig {
  center: [number, number];      // [lat, lon]
  zoom: number;
  bounds?: [[number, number], [number, number]];
  mapStyle?: 'osm' | 'satellite' | 'terrain';
}
```

---

## Layer Structure

| Layer | Z-Index | Content |
|-------|---------|---------|
| Base Map | 0 | OpenStreetMap tiles |
| Data Layer | 10 | Simulation data overlay |
| UI Overlay | 20 | Controls, legend |

---

## Map Providers

| Provider | Style | Use Case |
|----------|-------|----------|
| OpenStreetMap | osm | Default streets |
| MapTiler | satellite | Aerial view |
| Stamen | terrain | Elevation |

---

## Data Rendering

### Traffic Mode
- Road segments colored by congestion
- Vehicle markers (optional)
- Flow arrows

### Pollution Mode
- Heatmap overlay
- Particle animation
- Wind direction arrows

### Flood Mode
- Water level gradient
- Flow vectors
- Terrain contours

---

## Integration Points

| Action ID | Effect |
|-----------|--------|
| `geosim_zoom_in` | Zoom map in |
| `geosim_zoom_out` | Zoom map out |
| `geosim_center` | Reset to center |
| `geosim_toggle_layer` | Show/hide data layer |

---

## Dependencies

- Leaflet or MapLibre GL
- OpenStreetMap tiles
- Equation modules: trafficOSM, diffusion, navierStokes, wave

---

## Installation

```bash
# Install Leaflet
bun add leaflet react-leaflet
bun add -D @types/leaflet

# Required CSS in app/layout.tsx or globals.css
import 'leaflet/dist/leaflet.css';
```

---

## Canvas Switching Logic

LabShell must conditionally render canvas based on room type:

```typescript
// In LabShell.tsx
function SimulationCanvas({ room }: { room: RoomDefinition }) {
    if (room.type === 'geosim') {
        return <GeoSimCanvas room={room} />;
    }
    return <Sim3DCanvas room={room} />;  // Default 3D
}
```

**Rules:**
1. `room.type === 'geosim'` → render GeoSimCanvas
2. `room.type === 'sim3d'` → render Sim3DCanvas
3. `room.type === 'test_terminal'` → render TestTerminal

---

## Implementation Status

| Feature | Status | Notes |
|---------|--------|-------|
| Component structure | ✅ | GeoSimCanvas.tsx exists |
| Placeholder render | ✅ | Grid + center marker |
| Map controls | ✅ | zoom/center/layer buttons |
| Metric simulation | ✅ | Mock data per room type |
| Leaflet integration | ⚠️ | Pending package install |
| Canvas switching | ⚠️ | Pending LabShell update |
| Real OSM tiles | ❌ | Future |

---

## Traceability

- Room Registry: `REGISTRIES/registries_spec.md#geosim`
- Action Map: `B_FRONTEND/action_map.md`
- Flow Engine: `D_FLOW_ENGINE/runner_logic.md`

