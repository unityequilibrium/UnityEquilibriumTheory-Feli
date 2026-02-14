# Canvas View Toggle - UI Specification
## Layer A - UX/UI Intent

**Version:** 1.0  
**Last Updated:** 2025-12-25  
**Layer:** A (UX/UI)

---

## 1. Purpose

Toggle button ให้ user สลับมุมมองระหว่าง:
- **Normal View**: ดูผลลัพธ์ (3D, charts, metrics)
- **Canvas View**: ดูโครงสร้าง (nodes, edges, data flow)

---

## 2. UI Component

```
┌─────────────────────────────────────┐
│  ▶  ⏭  [🔄 Normal View ⌄]  ↻  ●   │
└─────────────────────────────────────┘
              ↑
        Toggle Button
```

---

## 3. Action Map

| action_id | Trigger | Expected Effect | Owner Layer |
|-----------|---------|-----------------|-------------|
| `view_toggle_normal` | Click toggle when in Canvas | Switch to Normal View | B |
| `view_toggle_canvas` | Click toggle when in Normal | Switch to Canvas View | B |

---

## 4. States

| State | Label | Icon | Background |
|-------|-------|------|------------|
| Normal View | "Normal View" | 🔄 | default |
| Canvas View | "Canvas View" | 📊 | highlighted |

---

## 5. Behavior Rules

1. **Single Toggle**: ปุ่มเดียว สลับไปมา
2. **Preserve State**: เมื่อ toggle กลับ ต้องเห็น state เดิม
3. **No Route Change**: ไม่เปลี่ยน URL, อยู่ใน `/lab` เสมอ
4. **action_id Required**: ทุกการ click ต้อง log action_id

---

## 6. Traceability

| This Doc | Links To |
|----------|----------|
| action_id | B_FRONTEND/button_action_ids.md |
| Toggle behavior | D_FLOW_ENGINE/node_canvas_architecture.md §7 |
| LabShell state | B_FRONTEND/smart_system.md |

---

**Status:** ✅ SPEC LOCKED
