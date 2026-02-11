# Layout Contract
## Layer B — Layout Constants & Rules

---

## 📐 Core Constants

**Source:** `lib/layoutConstants.ts`

```typescript
export const LAYOUT = {
  TOPNAV_HEIGHT: 48,
  LEFT_PANEL_WIDTH: 300,
  RIGHT_PANEL_WIDTH: 300,
  DOCK_HEIGHT: 240,
  
  Z_INDEX: {
    CANVAS: 0,
    SIDE_PANELS: 10,
    DOCK: 20,
    HUD: 30,
    MODAL: 100,
    SHOW_BUTTONS: 150,
  },
  
  ANIMATION: {
    PANEL_DURATION: 300,
    EASE: 'ease-out',
  }
};
```

---

## 🖼️ Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                      TopNav (48px, z:50)                        │
├───────────────┬───────────────────────────────┬─────────────────┤
│  Left Panel   │     Simulation Canvas         │  Right Panel    │
│   (300px)     │     (z:0, FIXED, 100%)        │    (300px)      │
│   z:10        │                               │    z:10         │
│   overlay     │        [HUD z:30]             │    overlay      │
│               │                               │                 │
├───────────────┴───────────────────────────────┴─────────────────┤
│                    Bottom Dock (240px, z:20)                    │
│                         overlay                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Panel States

### Collapsed State (with icons)
| Panel | Icon | Action ID |
|-------|------|-----------|
| Left (Output) | 📊 | `panel_left_show` |
| Right (Studio) | 🧮 | `panel_right_show` |
| Bottom (Dock) | 📈 | `dock_show` |

### Expanded State
| Panel | Width/Height | Scrollable | Action ID |
|-------|--------------|------------|-----------|
| Left (Output) | 300px | ✅ Yes | `panel_left_hide` |
| Right (Studio) | 300px | ✅ Yes | `panel_right_hide` |
| Bottom (Dock) | 240px | No | `dock_hide` |

---

## 📑 Studio Panel — Collapsible Tabs

**Each section is independently collapsible:**

| Tab | Icon | ID | Default |
|-----|------|-----|---------|
| EQUATIONS | 🧮 | `studio_equations` | Expanded |
| PARAMS | ⚙️ | `studio_params` | Expanded |
| INITIAL | 🎲 | `studio_initial` | Collapsed |
| NOTES | 📝 | `studio_notes` | Collapsed |

**Behavior:**
- Click header to toggle [▼]/[▶]
- State persisted to localStorage
- ❌ **NO View toggle** — 2D/3D/4D fixed at sim creation

---

## 📊 Bottom Dock — Plotly Graphs

**Layout:** 3-column grid of Plotly charts

| Feature | Supported |
|---------|-----------|
| Zoom/Pan | ✅ |
| Hover tooltips | ✅ |
| Export PNG | ✅ |
| Metric selector chips | ✅ |
| Time scrubber | ✅ |

---

## 🪟 Modals

| Modal | Action ID | Location |
|-------|-----------|----------|
| Export | `output_export` | Output Panel |
| Web Settings | `platform_settings_open` | TopNav ⚙️ |
| Smart Settings | `smart_settings_open` | Settings Modal |
| Add Equation | `sim_add_equation` | Studio Panel |
| Preset Preview | `gallery_preset_open` | Gallery Card |

---

## 🎯 Layout Rules

### Canvas Rules
1. **Fixed position** - Never moves or resizes
2. **z-index: 0** - Always behind panels
3. **Full viewport** - Fills available space

### Panel Rules
1. **Overlay mode** - Panels float over canvas
2. **CSS transform** - Use translateX/Y for animation
3. **No resize** - Fixed widths, toggle only

### Z-Index Hierarchy
| Layer | Z-Index | Components |
|-------|---------|------------|
| Canvas | 0 | Simulation view |
| Panels | 10 | Left/Right panels |
| Dock | 20 | Bottom dock |
| HUD | 30 | Playback controls |
| Modal | 100 | Dialogs |
| Buttons | 150 | SHOW buttons |

---

**Layer:** B — Frontend Structure

