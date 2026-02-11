# Interaction Rules
## Layer A — Click/Drag/Hover Behaviors

---

## 🖱️ Click Interactions

### Navigation Clicks

| Element | Action | Result |
|---------|--------|--------|
| Logo (TopNav) | Click | Navigate to Home |
| HOME link | Click | Navigate to / |
| GALLERY link | Click | Navigate to /gallery |
| LAB link | Click | Navigate to /lab |
| DIAGNOSTICS link | Click | Navigate to /diagnostics |

### HUD Clicks

| Element | Action | Result |
|---------|--------|--------|
| ▶ Play | Click | Start simulation |
| ⏸ Pause | Click | Pause simulation |
| ⏭ Step | Click | Single step forward |
| ⟲ Reset | Click | Reset to initial state |
| 2D/3D/4D | Click | Change dimension mode |

### Panel Clicks

| Element | Action | Result |
|---------|--------|--------|
| [HIDE] | Click | Collapse panel with animation |
| [SHOW OUTPUT] | Click | Expand left panel |
| [SHOW STUDIO] | Click | Expand right panel |
| [▲ SHOW GRAPHS] | Click | Expand bottom dock |

### Settings Clicks

| Element | Action | Result |
|---------|--------|--------|
| ⚙️ Settings | Click | Open PlatformSettingsModal |
| EXPORT | Click | Open ExportModal |

---

## 🔄 Drag Interactions

### Sliders

| Element | Action | Result |
|---------|--------|--------|
| DT Slider | Drag | Change time step (0.001-0.1) |
| Softening Slider | Drag | Change softening parameter |
| Speed Slider | Drag | Change playback speed |

### 3D Canvas

| Action | Result |
|--------|--------|
| Drag (left button) | Rotate camera |
| Drag (right button) | Pan camera |
| Scroll wheel | Zoom in/out |

---

## 🎯 Hover Interactions

### Buttons

| Element | Hover Effect |
|---------|--------------|
| TopNav buttons | Background highlight, cursor pointer |
| HUD buttons | Border glow, color change |
| Panel buttons | Opacity/scale change |

### Cards

| Element | Hover Effect |
|---------|--------------|
| Project cards | Lift effect (shadow), border glow |
| Quick start cards | Scale up, color shift |

---

## ⌨️ Keyboard Interactions

| Key | Action | Context |
|-----|--------|---------|
| Space | Play/Pause toggle | Lab page |
| R | Reset simulation | Lab page |
| Escape | Close modal | Any modal open |
| Arrow keys | Camera movement | Lab page (future) |

---

**Source:** [UX_FLOWS_AND_INTERACTIONS.md](../../platform/design_system/UX_FLOWS_AND_INTERACTIONS.md)  
**Layer:** A — UX/UI Intent
