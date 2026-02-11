# GeoSim Preset Specifications
## UET Platform - GeoSim Presets

**Last Updated:** 2024-12-25  
**Purpose:** Document GeoSim simulation presets

---

## Preset List

| preset_id | Room | Name | Equations | Map Center |
|-----------|------|------|-----------|------------|
| `bangkokRushHour` | geoSimBangkok | Bangkok Rush Hour | trafficOSM, trafficFlow | 13.7563, 100.5018 |
| `bkkPM25` | geoSimPM25 | Bangkok PM2.5 | diffusion, navierStokes | 13.7563, 100.5018 |
| `thaiFlood2011` | geoSimFlood | Thailand Flood 2011 | navierStokes, wave | 14.0, 100.5 |

---

## Preset Details

### bangkokRushHour
```typescript
{
  id: 'bangkokRushHour',
  name: 'Bangkok Rush Hour',
  room: 'geoSimBangkok',
  equations: ['trafficOSM', 'trafficFlow'],
  params: {
    vehicleCount: 500,
    rushHourMultiplier: 2.0,
    timeOfDay: '08:00'
  },
  geoConfig: {
    center: [13.7563, 100.5018],
    zoom: 13,
    mapStyle: 'osm'
  }
}
```

### bkkPM25
```typescript
{
  id: 'bkkPM25',
  name: 'Bangkok PM2.5 Dispersion',
  room: 'geoSimPM25',
  equations: ['diffusion', 'navierStokes'],
  params: {
    initialPM25: 50,
    windDirection: 45,
    windSpeed: 2.5
  },
  geoConfig: {
    center: [13.7563, 100.5018],
    zoom: 11,
    mapStyle: 'osm'
  }
}
```

### thaiFlood2011
```typescript
{
  id: 'thaiFlood2011',
  name: 'Thailand Flood 2011',
  room: 'geoSimFlood',
  equations: ['navierStokes', 'wave'],
  params: {
    riverDischarge: 4000,
    rainIntensity: 50,
    damLevel: 0.8
  },
  geoConfig: {
    center: [14.0, 100.5],
    zoom: 9,
    bounds: [[13.0, 99.5], [15.5, 101.5]],
    mapStyle: 'terrain'
  }
}
```

---

## Traceability

- Room Registry: `REGISTRIES/registries_spec.md`
- Metric Registry: `REGISTRIES/registries_spec.md#geosim-metrics`
- Component: `B_FRONTEND/geosim_canvas.md`
