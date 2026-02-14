# Flow Control Specification
## Layer D — Sequence Validation

**Last Updated:** 2024-12-24  
**Status:** 📋 SPEC (Ready for Implementation)

---

## 1) Purpose

Flow Control ensures that **actions happen in valid sequences**. It prevents:
- Saving before initialization
- Exporting incomplete runs
- Invalid state transitions

---

## 2) Valid State Transitions

### 2.1 Simulation State Machine

```
┌─────────────┐
│    IDLE     │ ←── Initial state
└──────┬──────┘
       │ init()
       ▼
┌─────────────┐
│ INITIALIZED │
└──────┬──────┘
       │ play()
       ▼
┌─────────────┐  pause()  ┌─────────────┐
│   RUNNING   │ ◄───────► │   PAUSED    │
└──────┬──────┘  play()   └──────┬──────┘
       │                         │
       │ reset()                 │ reset()
       ▼                         ▼
┌─────────────┐
│    IDLE     │
└─────────────┘
```

### 2.2 Valid Transitions Table

| From | To | Action | Allowed |
|------|-----|--------|---------|
| IDLE | INITIALIZED | init() | ✅ |
| INITIALIZED | RUNNING | play() | ✅ |
| RUNNING | PAUSED | pause() | ✅ |
| PAUSED | RUNNING | play() | ✅ |
| RUNNING | IDLE | reset() | ✅ |
| PAUSED | IDLE | reset() | ✅ |
| IDLE | RUNNING | play() | ❌ Must init first |
| IDLE | PAUSED | pause() | ❌ Invalid |

---

## 3) Action Prerequisites

### 3.1 Save Snapshot

```
ALLOWED WHEN:
  - status IN ['PAUSED', 'INITIALIZED']
  - step > 0 OR hasInitialState
  
FORBIDDEN WHEN:
  - status = 'IDLE'
  - status = 'RUNNING' (must pause first)
```

### 3.2 Export Data

```
ALLOWED WHEN:
  - telemetry.history.length > 0
  - status IN ['PAUSED', 'INITIALIZED']
  
FORBIDDEN WHEN:
  - No telemetry data
  - status = 'RUNNING'
```

### 3.3 Adjust Parameters

```
ALLOWED WHEN:
  - status IN ['IDLE', 'INITIALIZED', 'PAUSED']
  
FORBIDDEN WHEN:
  - status = 'RUNNING' (must pause first)
```

---

## 4) Flow Control Interface

```typescript
interface FlowControl {
  // Check if action is allowed
  canPerform(action: ActionType): boolean;
  
  // Validate and execute (throws if invalid)
  validateAndExecute<T>(action: ActionType, fn: () => T): T;
  
  // Get current state
  getCurrentState(): SimulationState;
  
  // Get allowed actions from current state
  getAllowedActions(): ActionType[];
}

type ActionType = 
  | 'INIT' | 'PLAY' | 'PAUSE' | 'RESET' | 'STEP'
  | 'SAVE' | 'EXPORT' | 'ADJUST_PARAMS';
```

---

## 5) Error Handling

When Flow Control rejects an action:

```typescript
class FlowControlError extends Error {
  constructor(
    public action: ActionType,
    public currentState: SimulationState,
    public reason: string
  ) {
    super(`Cannot ${action} in state ${currentState}: ${reason}`);
  }
}
```

---

## 6) UI Integration

Buttons MUST be disabled when action is not allowed:

```tsx
<button
  data-action-id="output_save_snapshot"
  disabled={!flowControl.canPerform('SAVE')}
  onClick={handleSave}
>
  Save
</button>
```

---

## 7) Implementation Checklist

- [ ] Create `FlowControl` class in `lib/FlowControl.ts`
- [ ] Integrate with `simStoreV4` state
- [ ] Add `canPerform` checks to all action handlers
- [ ] Disable buttons based on `canPerform` results
- [ ] Log flow control rejections to ErrorLog

---

## 8) Traceability

| Layer | Responsibility |
|-------|----------------|
| A (UX) | User sees disabled buttons |
| B (Frontend) | FlowControl disables UI |
| C (Backend) | API validates request state |
| D (Engine) | SimCore enforces transitions |
| E (Database) | State changes logged |

---

**Layer:** D — Flow Engine  
**Cross-refs:** [event_bus.md](./event_bus.md), [B_FRONTEND/state_model.md](../B_FRONTEND/state_model.md)
