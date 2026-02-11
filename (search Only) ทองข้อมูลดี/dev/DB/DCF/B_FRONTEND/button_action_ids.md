# Button Action IDs - Canvas Module
## Layer B - Frontend Action Map

**Version:** 1.0  
**Last Updated:** 2025-12-25  
**Layer:** B (Frontend)

---

## 1. Canvas View Actions

| action_id | Component | Expected Effect | Layer |
|-----------|-----------|-----------------|-------|
| `view_toggle_normal` | ViewToggle | Switch to Normal View | B |
| `view_toggle_canvas` | ViewToggle | Switch to Canvas View | B |

---

## 2. AI Copilot Actions

| action_id | Component | Expected Effect | Layer |
|-----------|-----------|-----------------|-------|
| `ai_chat_send` | AIChatNode | Send message to AI | B→C |
| `ai_patch_apply` | AIChatNode | Apply GraphPatch to canvas | B |
| `ai_patch_reject` | AIChatNode | Reject pending GraphPatch | B |

---

## 3. Canvas Control Actions

| action_id | Component | Expected Effect | Layer |
|-----------|-----------|-----------------|-------|
| `canvas_zoom_in` | CanvasControls | Zoom in canvas | B |
| `canvas_zoom_out` | CanvasControls | Zoom out canvas | B |
| `canvas_fit_view` | CanvasControls | Fit all nodes in view | B |
| `canvas_lock_toggle` | CanvasControls | Lock/unlock canvas editing | B |

---

## 4. Node Actions

| action_id | Component | Expected Effect | Layer |
|-----------|-----------|-----------------|-------|
| `node_select` | NodeBase | Select node | B |
| `node_drag` | NodeBase | Drag node position | B |
| `node_connect` | Edge | Create connection | B |
| `node_disconnect` | Edge | Remove connection | B |

---

## 5. Implementation Requirements

### R2.1 Compliance (Global Rules)

```tsx
// ❌ WRONG - missing action_id
<button onClick={handleClick}>Send</button>

// ✅ CORRECT - has action_id
<button 
  data-action-id="ai_chat_send"
  onClick={handleClick}
>
  Send
</button>
```

### Logging

```typescript
// ทุก action ต้อง log
actionLogger.log(action_id, { component, timestamp, payload });
```

---

## 6. Traceability

| This Doc | Links To |
|----------|----------|
| action_id format | global_rules.md R2 |
| Canvas actions | A_UX/canvas_view_toggle.md |
| AI actions | D_FLOW_ENGINE/node_canvas_architecture.md |

---

**Status:** ✅ SPEC LOCKED
