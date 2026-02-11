# LAB UI Design Specification v3.0

## Core Architecture Principle

> **Simulator = Full-screen FIXED Background (z-index: 0)**  
> **UI Panels = Floating Overlays on TOP (z-index: 10+)**  
> **Panels do NOT resize the canvas - they OVERLAY it**  
> **Settings = Verification View (See [SMART_SETTINGS_DESIGN](SMART_SETTINGS_DESIGN.md))**

---

## Layout Grid System

### Z-Index Hierarchy

| Layer | Component | Z-Index | Notes |
|-------|-----------|---------|-------|
| 0 | Simulation Canvas | 0 | Always fullscreen, never resized |
| 1 | Floating Side Panels | 10 | Left/Right overlays |
| 2 | Bottom Dock | 20 | Slides up from bottom, overlays canvas |
| 3 | Simulation HUD | 30 | Always visible, top center |
| 4 | Modals/Dialogs | 100 | Export modal, etc. |
| 5 | Floating SHOW Buttons | 150 | Edge buttons when panels collapsed |

### Panel Size Constraints

```
┌─────────────────────────────────────────────────────────────────┐
│                         TOP NAV (48px fixed)                    │
├───────────────┬───────────────────────────────┬─────────────────┤
│  LEFT PANEL   │      SIMULATION CANVAS        │  RIGHT PANEL    │
│   (300px)     │      (100% - FIXED BG)        │    (300px)      │
│   overlay     │                               │    overlay      │
│               │                               │                 │
│               │         [HUD z:30]            │                 │
│               │                               │                 │
├───────────────┴───────────────────────────────┴─────────────────┤
│                    BOTTOM DOCK (240px max)                      │
│                    overlay - slides up                          │
└─────────────────────────────────────────────────────────────────┘
```

| Panel | Width/Height | Min | Max | Default State |
|-------|--------------|-----|-----|---------------|
| Left Panel | **300px** fixed | 280px | 400px | Collapsed |
| Right Panel | **300px** fixed | 280px | 400px | Expanded |
| Bottom Dock | **240px** height | 180px | 50% viewport | Collapsed |
| Top Nav | **48px** fixed | - | - | Always visible |

---

## Panel Behavior Specification

### 1. Simulation Canvas (Background Layer)

```css
.simulation-canvas {
    position: fixed;
    inset: 48px 0 0 0;  /* Below TopNav */
    z-index: 0;
    width: 100%;
    height: calc(100vh - 48px);
    /* NEVER RESIZED BY PANELS */
}
```

### 2. Side Panels (Overlay Mode)

```css
.left-panel {
    position: fixed;
    left: 0;
    top: 48px;
    bottom: 0;
    width: 300px;
    z-index: 10;
    transform: translateX(-100%);  /* Collapsed */
}

.left-panel.open {
    transform: translateX(0);  /* Expanded */
}
```

### 3. Bottom Dock (Slide-Up Overlay)

```css
.bottom-dock {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    height: 240px;
    z-index: 20;
    transform: translateY(100%);  /* Collapsed */
}

.bottom-dock.open {
    transform: translateY(0);  /* Expanded */
}
```

---

## Animation Standards

| Action | Duration | Easing | Property |
|--------|----------|--------|----------|
| Panel Slide In | 300ms | `ease-out` | transform |
| Panel Slide Out | 200ms | `ease-in` | transform |
| Button Hover | 150ms | `ease` | opacity, scale |
| Modal Fade | 200ms | `ease` | opacity |

---

## Button Placement Rules

### HIDE Buttons (Inside Panel Header)
- Position: Top-right of panel header (40px height)
- Always visible: `shrink-0 whitespace-nowrap`
- Style: Cyan tactical text `[◀ HIDE]` / `[HIDE ▶]`

### SHOW Buttons (Floating Edge)
- Position: Fixed to screen edge when panel collapsed
- Z-Index: 150 (above everything except modals)
- Style: Glass pill button with arrow indicator

```
[▶ SHOW OUTPUT]     ← Left edge, vertical center
[SHOW STUDIO ◀]     ← Right edge, vertical center  
[▲ SHOW GRAPHS]     ← Bottom edge, horizontal center
```

---

## Implementation Checklist

### Priority 1: Layout Architecture ✅ COMPLETE
- [x] Change from `react-resizable-panels` grid to CSS overlay positioning
- [x] Make Simulation Canvas `position: fixed` (true background)
- [x] Side panels use `transform: translateX()` for show/hide
- [x] Bottom dock uses `transform: translateY()` for show/hide

### Priority 2: Fixed Panel Sizes ✅ COMPLETE
- [x] Left Panel: 300px fixed width
- [x] Right Panel: 300px fixed width
- [x] Bottom Dock: 240px default height

### Priority 3: Animation Polish ✅ COMPLETE
- [x] Add CSS transitions for panel slides
- [x] Remove resize handles (no resizing needed)
- [x] Ensure HUD stays centered regardless of panels

### Priority 4: Feature Alignment (from Reference Design)
- [x] **HUD**: Add 2D/3D/4D Dimension Toggle buttons ✅
- [x] **HUD**: Add Settings gear icon ✅
- [x] **Right Panel**: Add [+ Add Equation] button ✅
- [x] **Right Panel**: Add DT Slider (time step) ✅
- [x] **Right Panel**: Add Softening Slider ✅
- [ ] **Left Panel**: Add Sparkline mini-graphs to MetricCards
- [ ] **Bottom Dock**: Add metric tabs (Live Graph, Energy, Momentum)

---

## CSS Tokens

```css
:root {
    /* Layout */
    --topnav-height: 48px;
    --panel-width: 300px;
    --dock-height: 240px;
    
    /* Colors */
    --bg-primary: #0f0f14;
    --glass-bg: rgba(10, 10, 14, 0.85);
    --glass-border: rgba(78, 205, 196, 0.3);
    --glass-blur: blur(16px);
    --accent-cyan: #4ecdc4;
    
    /* Panel */
    --panel-radius: 0px;  /* Edge-aligned, no radius */
    --panel-shadow: 4px 0 20px rgba(0, 0, 0, 0.5);
    
    /* Animation */
    --panel-slide-in: 300ms ease-out;
    --panel-slide-out: 200ms ease-in;
}
```

---

## Reference Design Alignment

**Overall Score: 80%**

| Component | Status | Missing |
|-----------|--------|---------|
| Layout | ✅ 100% | - |
| HUD | ⚠️ 70% | 2D/3D/4D toggle |
| Right Panel | ⚠️ 60% | Sliders, +Equation |
| Left Panel | ⚠️ 70% | Sparklines |
| Bottom Dock | ⚠️ 80% | Metric tabs |
