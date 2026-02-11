# Room Template Specification

**Purpose:** กำหนด fields ที่ทุก Room ต้องมี เพื่อให้ Smart Sync ทำงานได้

---

## 1. Room Definition Interface

```typescript
interface RoomDefinition {
    // === Required Fields ===
    room_id: string;              // Unique ID: 'solarSystem', 'geoSimBangkok'
    type: RoomType;               // 'sim3d' | 'geosim' | 'test_terminal'
    title: string;                // Display: '☀️ Solar System'
    description: string;          // Tooltip/help text
    icon: string;                 // Icon ID for UI
    tags: string[];               // Search/filter tags

    // === Smart Sync Fields ===
    defaultModules: string[];     // Equations enabled on room entry
    defaultMetrics: string[];     // Metrics shown in dock
    defaultPreset?: string;       // Body positions (optional)

    // === Permissions ===
    permissions: {
        saveToDB: boolean;        // Can save to gallery
        export: boolean;          // Can export JSON
        edit: boolean;            // Can modify params
    };

    // === Type-Specific (Optional) ===
    geoConfig?: GeoConfig;        // Only for geosim rooms
}
```

---

## 2. Room Types

| Type | Renderer | Use Case |
|------|----------|----------|
| `sim3d` | Three.js 3D | N-body, ดาวเคราะห์, UET test |
| `geosim` | Leaflet Map | Traffic, PM2.5, Flood |
| `test_terminal` | Console | Oracle test gates |

---

## 3. Smart Sync Fields Explained

### defaultModules
```
เมื่อ user เลือก room → enabledEquations = ['uet', ...room.defaultModules]
```
| Room | defaultModules |
|------|----------------|
| solarSystem | `['newton']` |
| uetTest | `['newton', 'uet']` |
| geoSimBangkok | `['trafficOSM', 'trafficFlow']` |

### defaultMetrics
```
เมื่อ user เลือก room → dock แสดง metrics เหล่านี้
```
| Room | defaultMetrics |
|------|----------------|
| solarSystem | `['total_energy', 'kinetic_energy', 'potential_energy']` |
| geoSimBangkok | `['avg_speed', 'congestion_index', 'flow_rate']` |

### defaultPreset
```
เมื่อ user เลือก room → apply preset (body positions, initial conditions)
```
| Room | Preset | Description |
|------|--------|-------------|
| solarSystem | solarSystemV2 | ตำแหน่ง Sun + 8 planets |
| threeBody | figure8 | 3 bodies in figure-8 orbit |
| geoSimBangkok | bangkokRushHour | Rush hour traffic config |

---

## 4. Template Examples

### sim3d Room
```typescript
{
    room_id: 'galaxyMerger',
    type: 'sim3d',
    title: '🌌 Galaxy Merger',
    description: 'Two galaxies collide simulation',
    icon: 'galaxy',
    tags: ['sim', 'galaxy', 'nbody'],
    
    defaultModules: ['newton', 'darkMatter'],
    defaultMetrics: ['total_energy', 'angular_momentum'],
    defaultPreset: 'twoGalaxies',
    
    permissions: { saveToDB: true, export: true, edit: true }
}
```

### geosim Room
```typescript
{
    room_id: 'geoSimEarthquake',
    type: 'geosim',
    title: '🌋 Earthquake Simulation',
    description: 'Seismic wave propagation',
    icon: 'earthquake',
    tags: ['geosim', 'disaster', 'wave'],
    
    defaultModules: ['waveEquation'],
    defaultMetrics: ['wave_amplitude', 'propagation_speed'],
    
    permissions: { saveToDB: true, export: true, edit: true },
    geoConfig: {
        center: [13.7, 100.5],
        zoom: 10,
        mapStyle: 'terrain'
    }
}
```

---

## 5. Validation Rules

| Field | Rule |
|-------|------|
| room_id | Unique, lowercase, no spaces |
| type | Must be valid RoomType |
| defaultModules | Must exist in equationRegistry |
| defaultMetrics | Must exist in metricRegistry |
| defaultPreset | Must exist in presetRegistry (if specified) |
| geoConfig | Required if type === 'geosim' |

---

## 6. Adding New Room Checklist

1. ☐ Define room in roomRegistry.ts
2. ☐ Create preset if needed (presetRegistry.ts)
3. ☐ Ensure equations exist (equationRegistry.ts)
4. ☐ Ensure metrics exist (metricRegistry.ts)
5. ☐ Test Room dropdown → Smart Sync
