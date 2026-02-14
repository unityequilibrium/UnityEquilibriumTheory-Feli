# GRID LAYOUT DESIGN SYSTEM
## Universal Equilibrium Platform - Master Layout Standard v1.0

> **เอกสารนี้คือมาตรฐานหลักสำหรับ Layout Architecture ของ Platform ทั้งหมด**
> ทุกหน้า ทุก component ต้องปฏิบัติตามมาตรฐานนี้

---

## 📐 Core Layout Philosophy

### The Iron Rules

1. **Content Layer Separation** - ทุก layer ต้องมี z-index ที่ชัดเจนและไม่ทับกัน
2. **Fixed vs Overlay Principle** - Background layer ต้อง fixed, ทุก UI ต้อง overlay
3. **No Resize Cascade** - การเปิด/ปิด panels ต้องไม่ทำให้ content อื่น resize
4. **Predictable Sizing** - ทุก component ต้องมีขนาดที่กำหนดไว้ชัดเจน

---

## 🏛️ Page Shell Architecture

### Universal Page Shell Structure

ทุกหน้าในระบบต้องมีโครงสร้างดังนี้:

```
┌─────────────────────────────────────────────────────────────────┐
│                    TOP NAV (48px, z:50, fixed)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    CONTENT AREA (flex-1)                        │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │              PAGE-SPECIFIC LAYOUT                       │   │
│   │           (Home, Gallery, Lab, etc.)                    │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                   FOOTER (optional, z:10)                       │
└─────────────────────────────────────────────────────────────────┘
```

### Page Types

| Page Type | Layout Mode | Panels | Special Features |
|-----------|-------------|--------|------------------|
| **Portal** (Home) | Single Column | None | Hero, Bento Grid |
| **Browser** (Gallery) | Scrollable Grid | Filter Bar | Bento Cards |
| **Workspace** (Lab) | Overlay Panels | Left, Right, Bottom | Fixed Background |
| **Utility** (Diagnostics) | Simple Form | None | Data Tables |

---

## 📏 Sizing Constants

### Global Constants

```typescript
const LAYOUT = {
    // Top Navigation
    topNav: {
        height: 48,                    // px
        zIndex: 50,
    },
    
    // Side Panels (Overlay Mode)
    sidePanel: {
        width: 300,                    // px (fixed)
        minWidth: 280,                 // px (for responsive)
        maxWidth: 400,                 // px (for large screens)
        zIndex: 10,
    },
    
    // Bottom Dock
    bottomDock: {
        height: 240,                   // px (default)
        minHeight: 180,                // px
        maxHeight: '50vh',             // max 50% of viewport
        zIndex: 20,
    },
    
    // Floating Buttons
    floatingButtons: {
        zIndex: 150,
    },
    
    // Modals
    modal: {
        zIndex: 100,
        backdrop: 'rgba(0, 0, 0, 0.8)',
    },
    
    // Animation
    animation: {
        slideIn: 300,                  // ms
        slideOut: 200,                 // ms
        easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
    },
} as const;
```

---

## 🎭 Z-Index Hierarchy

### Complete Z-Index Map

```
z-index: 0     │ Background Layer (Simulation Canvas, Hero Images)
z-index: 1-9   │ Content Elements (Cards, Lists)
z-index: 10    │ Side Panels (Left/Right Overlays)
z-index: 20    │ Bottom Dock (Graph Dock)
z-index: 30    │ HUD (Simulation Controls)
z-index: 40    │ Tooltips, Dropdowns
z-index: 50    │ Top Navigation (Always visible)
z-index: 100   │ Modals, Dialogs
z-index: 150   │ Floating Show/Hide Buttons
z-index: 200   │ Critical Alerts, Toast Notifications
```

---

## 📱 Responsive Breakpoints

```css
/* Mobile First Approach */
:root {
    --breakpoint-sm: 640px;   /* Small phones */
    --breakpoint-md: 768px;   /* Tablets */
    --breakpoint-lg: 1024px;  /* Laptops */
    --breakpoint-xl: 1280px;  /* Desktops */
    --breakpoint-2xl: 1536px; /* Large monitors */
}
```

### Panel Behavior by Breakpoint

| Breakpoint | Left Panel | Right Panel | Bottom Dock |
|------------|------------|-------------|-------------|
| < 768px | Hidden | Hidden | Bottom Sheet |
| 768-1024px | Overlay 280px | Overlay 280px | 180px |
| > 1024px | Overlay 300px | Overlay 300px | 240px |

---

## 🔲 Panel System Standard

### Panel States

```typescript
type PanelState = 'open' | 'collapsed';

interface PanelConfig {
    id: string;
    position: 'left' | 'right' | 'bottom';
    defaultState: PanelState;
    size: number;            // px
    transitions: {
        open: string;        // CSS transform for open state
        collapsed: string;   // CSS transform for collapsed state
    };
}
```

### Side Panel CSS Pattern

```css
.side-panel {
    position: fixed;
    top: 48px;                        /* Below TopNav */
    bottom: 0;
    width: 300px;
    z-index: 10;
    
    /* Glass Effect */
    background: rgba(10, 10, 14, 0.98);
    backdrop-filter: blur(16px);
    
    /* Animation */
    transition: transform 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Left Panel */
.side-panel--left {
    left: 0;
    border-right: 1px solid rgba(78, 205, 196, 0.3);
}

.side-panel--left.collapsed {
    transform: translateX(-100%);
}

/* Right Panel */
.side-panel--right {
    right: 0;
    border-left: 1px solid rgba(78, 205, 196, 0.3);
}

.side-panel--right.collapsed {
    transform: translateX(100%);
}
```

### Bottom Dock CSS Pattern

```css
.bottom-dock {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    height: 240px;
    z-index: 20;
    
    /* Glass Effect */
    background: rgba(10, 10, 14, 0.98);
    backdrop-filter: blur(16px);
    border-top: 1px solid rgba(78, 205, 196, 0.3);
    
    /* Animation */
    transition: transform 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

.bottom-dock.collapsed {
    transform: translateY(100%);
}
```

---

## 🎯 Panel Header Standard

### Header Structure

```tsx
<div className="panel-header">
    <div className="panel-header__title">
        Panel Title
    </div>
    <div className="panel-header__actions">
        <button className="panel-header__hide-btn">
            [◀ HIDE]
        </button>
    </div>
</div>
```

### Header CSS

```css
.panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 40px;                     /* Fixed height */
    padding: 0 16px;
    
    background: rgba(0, 0, 0, 0.4);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    
    /* Overflow Protection */
    flex-shrink: 0;
    min-width: 0;
}

.panel-header__title {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: rgba(113, 113, 122, 1);    /* zinc-500 */
    
    /* Truncate if too long */
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.panel-header__hide-btn {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: rgba(78, 205, 196, 0.8);   /* cyan-400/80 */
    
    /* Never shrink or wrap */
    flex-shrink: 0;
    white-space: nowrap;
}
```

---

## 🔘 Floating Button Standard

### Show Button Pattern

```tsx
{!panelOpen && (
    <button
        onClick={() => setPanelOpen(true)}
        className="floating-show-btn floating-show-btn--left"
    >
        [▶ SHOW OUTPUT]
    </button>
)}
```

### Button Positions

| Panel | Position | Transform |
|-------|----------|-----------|
| Left | `left: 0; top: 50%;` | `-translate-y-1/2` |
| Right | `right: 0; top: 50%;` | `-translate-y-1/2` |
| Bottom | `bottom: 0; left: 50%;` | `-translate-x-1/2` |

### Button CSS

```css
.floating-show-btn {
    position: fixed;
    z-index: 150;
    
    padding: 12px 16px;
    
    background: rgba(10, 10, 15, 0.9);
    backdrop-filter: blur(8px);
    
    font-size: 11px;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: #4ecdc4;
    
    cursor: pointer;
    transition: all 300ms;
    
    pointer-events: auto;
}

.floating-show-btn--left {
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    
    border-right: 1.5px solid rgba(78, 205, 196, 0.4);
    border-top-right-radius: 12px;
    border-bottom-right-radius: 12px;
    box-shadow: 4px 0 20px rgba(0, 0, 0, 0.5);
}

.floating-show-btn--right {
    right: 0;
    top: 50%;
    transform: translateY(-50%);
    
    border-left: 1.5px solid rgba(78, 205, 196, 0.4);
    border-top-left-radius: 12px;
    border-bottom-left-radius: 12px;
    box-shadow: -4px 0 20px rgba(0, 0, 0, 0.5);
}

.floating-show-btn--bottom {
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    
    border-top: 1.5px solid rgba(78, 205, 196, 0.4);
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.5);
}
```

---

## 🖼️ Background Layer Pattern

### For Interactive Backgrounds (Like Simulation Canvas)

```tsx
// Background Canvas - NEVER resizes when panels open/close
<div 
    className="fixed inset-0 z-0"
    style={{ top: LAYOUT.topNav.height }}
>
    <Canvas />
    <OverlayHUD />
</div>
```

### Key Rules

1. **position: fixed** - Not affected by parent containers
2. **inset: 0** - Fills entire viewport
3. **z-index: 0** - Lowest layer
4. **pointer-events: auto** - Receives mouse events

---

## 📋 Page-Specific Layouts

### Home Page (Portal)

```
┌─────────────────────────────────────────────────────────────────┐
│                         TOP NAV (z:50)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                     ┌───────────────────┐                       │
│                     │    HERO CARD      │                       │
│                     │   (Bento Grid)    │                       │
│                     └───────────────────┘                       │
│                                                                 │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│   │  QUICK  │  │  QUICK  │  │  QUICK  │  │  QUICK  │           │
│   │  START  │  │  START  │  │  START  │  │  START  │           │
│   └─────────┘  └─────────┘  └─────────┘  └─────────┘           │
│                                                                 │
│                       SYSTEM TICKER                             │
└─────────────────────────────────────────────────────────────────┘
```

### Gallery Page (Browser)

```
┌─────────────────────────────────────────────────────────────────┐
│                         TOP NAV (z:50)                          │
├─────────────────────────────────────────────────────────────────┤
│         FILTER BAR (Search, Categories, Tags)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐   │
│   │  PROJECT  │  │  PROJECT  │  │  PROJECT  │  │  PROJECT  │   │
│   │   CARD    │  │   CARD    │  │   CARD    │  │   CARD    │   │
│   └───────────┘  └───────────┘  └───────────┘  └───────────┘   │
│                                                                 │
│   ┌───────────┐  ┌───────────┐  ┌───────────┐                  │
│   │  PROJECT  │  │  PROJECT  │  │  PROJECT  │                  │
│   │   CARD    │  │   CARD    │  │   CARD    │                  │
│   └───────────┘  └───────────┘  └───────────┘                  │
│                                                                 │
│                       SYSTEM TICKER                             │
└─────────────────────────────────────────────────────────────────┘
```

### Lab Page (Workspace)

```
┌─────────────────────────────────────────────────────────────────┐
│                         TOP NAV (z:50)                          │
├─────────────────────────────────────────────────────────────────┤
│ ┌─────────┐                                        ┌─────────┐  │
│ │  LEFT   │    SIMULATION CANVAS (z:0, FIXED)      │  RIGHT  │  │
│ │  PANEL  │                                        │  PANEL  │  │
│ │ (z:10)  │         ┌───────────────┐              │ (z:10)  │  │
│ │ overlay │         │      HUD      │              │ overlay │  │
│ │         │         │    (z:30)     │              │         │  │
│ │         │         └───────────────┘              │         │  │
│ └─────────┘                                        └─────────┘  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │                 BOTTOM DOCK (z:20, overlay)                 │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✅ Implementation Checklist

### For Every New Page

- [ ] Use `TopNav` component (48px height, z-50)
- [ ] Define page-specific content area
- [ ] Set proper z-index hierarchy
- [ ] Add pointer-events handling

### For Workspace Pages (With Panels)

- [ ] Fixed background canvas (z-0)
- [ ] Overlay panels with transform animations
- [ ] Panel headers with HIDE buttons (shrink-0)
- [ ] Floating SHOW buttons (z-150)
- [ ] LayoutContext for state management

### Testing Checklist

- [ ] Panel open/close doesn't resize canvas
- [ ] Buttons always visible (no overflow)
- [ ] Animations are smooth (60fps)
- [ ] Z-index hierarchy is correct
- [ ] Responsive at all breakpoints

---

## 🎨 CSS Tokens Reference

```css
:root {
    /* Layout Dimensions */
    --layout-topnav-height: 48px;
    --layout-panel-width: 300px;
    --layout-dock-height: 240px;
    
    /* Z-Index */
    --z-background: 0;
    --z-panel: 10;
    --z-dock: 20;
    --z-hud: 30;
    --z-topnav: 50;
    --z-modal: 100;
    --z-floating-btn: 150;
    
    /* Glass Effect */
    --glass-bg: rgba(10, 10, 14, 0.98);
    --glass-blur: blur(16px);
    --glass-border: rgba(78, 205, 196, 0.3);
    
    /* Animation */
    --animation-slide-in: 300ms cubic-bezier(0.4, 0, 0.2, 1);
    --animation-slide-out: 200ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

---

**Last Updated:** 2024-12-24
**Version:** 1.0
**Author:** UET Design System Team
