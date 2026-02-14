# 🔘 Button Specification & Interaction Report

> **Version:** 1.0
> **Last Updated:** 2025-12-23
> **Status:** Active Design Document

---

## 📋 Overview

เอกสารนี้รวบรวมปุ่มทั้งหมดในระบบ UET Lab พร้อมรายละเอียดการทำงาน สถานะ และการเชื่อมต่อกับฟังก์ชัน

---

## 🎮 Lab Page Buttons

### 1. Simulation HUD (Top Center)

| ID | ปุ่ม | Icon | Function | Store Action | State Change |
|----|------|------|----------|--------------|--------------|
| `btn_play` | Play | ⏵ | เริ่ม simulation | `useSimStoreV4.play()` | `status: 'running'` |
| `btn_pause` | Pause | ⏸ | หยุด simulation | `useSimStoreV4.pause()` | `status: 'paused'` |
| `btn_step` | Step | ⏭ | ก้าว 1 frame | `simCoreV4.step()` | `step++, t += dt` |
| `btn_reset` | Reset | ⟲ | Reset sim | `useSimStoreV4.reset()` | `t=0, step=0` |

#### Play/Pause Toggle Logic
```typescript
const handlePlayPause = () => {
    if (telemetry.run.status === 'running') {
        pause();  // ⏸ เปลี่ยนเป็น paused
    } else {
        play();   // ⏵ เปลี่ยนเป็น running
    }
};
```

#### Disabled States
| ปุ่ม | Disabled เมื่อ | เหตุผล |
|------|---------------|--------|
| Step ⏭ | `status === 'running'` | Single-step ใช้ได้ตอน paused เท่านั้น |

---

### 2. Top Navigation

| ID | ปุ่ม | Location | Action | Navigation |
|----|------|----------|--------|------------|
| `nav_home` | Home | Left | Navigate | `→ /` |
| `nav_gallery` | Gallery | Left | Navigate | `→ /gallery` |
| `nav_lab` | Lab | Left | Active tab | `/lab` |
| `nav_diag` | Diagnostics | Left | Navigate | `→ /test-lab` |
| `nav_settings` | ⚙ Settings | Right | Opens modal | Settings Modal |
| `nav_back` | ⎋ Back | Right | Navigate back | `history.back()` |

---

### 3. Panel Controls

| ปุ่ม | Location | Action | State |
|------|----------|--------|-------|
| ▶ | Left edge | Show left panel | `leftOpen = true` |
| ◀ | Right edge | Show right panel | `rightOpen = true` |
| Toggle (Dock) | Dock header | Expand/Collapse | `dockOpen = !dockOpen` |

---

### 4. Left Panel (Output)

| ID | ปุ่ม | Function | API Call |
|----|------|----------|----------|
| `btn_save` | 🔽 Save to Gallery | บันทึก run ปัจจุบัน | `POST /api/projects` |
| `btn_export` | 📤 Export | Download telemetry | Local download |

#### Save Button Implementation
```typescript
const handleSave = async () => {
    const res = await fetch('/api/projects', {
        method: 'POST',
        body: JSON.stringify({
            name: `Run ${new Date().toLocaleTimeString()}`,
            config: { room: room.room_id, telemetry }
        })
    });
    if (res.ok) showToast('Saved!');
};
```

---

### 5. Right Panel (Studio/Params)

| Control Type | Control | Function | Connected Action |
|--------------|---------|----------|------------------|
| Input | Time Step (dt) | ปรับ timestep | `setDt(value)` |
| Slider | Speed | ปรับความเร็ว | `setSpeed(value)` |
| Dropdown | Preset | เลือก preset | `setPreset(id)` |
| Sliders | Equation Params | ปรับค่า params | `setEquationParams(id, params)` |

#### Preset Change Flow
```
User selects preset
    ↓
setPreset('galaxy')
    ↓
simCoreV4.setPreset('galaxy')
    ↓
├── Reset all bodies
├── Reset dt, speed
├── Reset equation params
└── Store notify UI
    ↓
UI re-renders with new values
```

---

## 📚 Gallery Page Buttons

### 1. Header Controls

| ID | ปุ่ม | Function | Modal/Action |
|----|------|----------|--------------|
| `btn_add_project` | ＋ Add New Project | เปิด Add Modal | Opens modal |
| `tab_all` | All Projects | Filter: show all | `filter = 'ALL'` |
| `tab_core` | Core Tests | Filter: core only | `filter = 'CORE'` |
| `tab_arch` | Archetypes | Filter: arch only | `filter = 'ARCH'` |
| `tab_phys` | Physics/GR | Filter: physics | `filter = 'PHYS'` |

### 2. Project Card Buttons

| ปุ่ม | Function | Navigation |
|------|----------|------------|
| Load | โหลด project เข้า Lab | `→ /lab?room=${id}&preset=${presetId}` |

---

## 🪟 Modal Buttons

### Add Project Modal

| ปุ่ม | Function | Condition |
|------|----------|-----------|
| ✕ (Close) | ปิด modal | - |
| Cancel | ปิด modal + reset form | - |
| Save Project | POST to API + close | `disabled if !name` |

### Settings Modal (Planned)

| ปุ่ม | Function | Condition |
|------|----------|-----------|
| Reset | Reset to defaults | - |
| Apply | Save settings | - |

---

## 🔗 Button-Function Connection Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        UI Layer                                  │
├─────────────────────────────────────────────────────────────────┤
│  [⏵ Play]  [⏸ Pause]  [⏭ Step]  [⟲ Reset]  [Preset ▼]        │
│      │          │          │         │          │               │
└──────┼──────────┼──────────┼─────────┼──────────┼───────────────┘
       │          │          │         │          │
       ▼          ▼          ▼         ▼          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Zustand Store (simStoreV4)                    │
├─────────────────────────────────────────────────────────────────┤
│  play()     pause()    step()    reset()    setPreset()         │
│      │          │          │         │          │               │
└──────┼──────────┼──────────┼─────────┼──────────┼───────────────┘
       │          │          │         │          │
       ▼          ▼          ▼         ▼          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SimCoreV4 Engine                              │
├─────────────────────────────────────────────────────────────────┤
│  - Manages animation loop                                        │
│  - Updates WorldState                                            │
│  - Calculates Telemetry                                          │
│  - Notifies subscribers                                          │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    State Updates                                 │
├─────────────────────────────────────────────────────────────────┤
│  worldState.t, worldState.step, telemetry.run.status            │
│                      │                                          │
│                      ▼                                          │
│              UI Auto-Updates                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎨 Button Styles

### Primary (Cyan)
```css
.btn-primary {
    background: linear-gradient(to-r, #0e7490, #0891b2);
    border: 1px solid rgba(14, 165, 233, 0.3);
    color: white;
}
.btn-primary:hover {
    background: linear-gradient(to-r, #0891b2, #06b6d4);
}
```

### Secondary (Gray)
```css
.btn-secondary {
    background: linear-gradient(to-r, #3f3f46, #52525b);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
}
```

### Danger (Red)
```css
.btn-danger {
    background: transparent;
}
.btn-danger:hover {
    background: rgba(239, 68, 68, 0.2);
    color: #f87171;
}
```

### Disabled State
```css
.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
}
```

---

## ✅ Implementation Status

| Component | Total Buttons | Implemented | Connected |
|-----------|---------------|-------------|-----------|
| SimulationHUD | 4 | ✅ 4/4 | ✅ 4/4 |
| TopNav | 6 | ✅ 6/6 | ⬜ 4/6 |
| Left Panel | 2 | ✅ 2/2 | ✅ 2/2 |
| Right Panel | 4+ | ✅ 4/4 | ✅ 4/4 |
| Gallery | 6 | ✅ 6/6 | ✅ 6/6 |
| Modals | 3 | ✅ 3/3 | ✅ 3/3 |

**Overall: 25 buttons, 23 fully connected**
