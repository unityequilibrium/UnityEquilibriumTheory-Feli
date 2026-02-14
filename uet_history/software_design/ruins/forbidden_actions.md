# Forbidden Actions
## Layer A — Things Users Cannot Do

> **Purpose:** ป้องกันความสับสนและรักษา consistency ของ UX

---

## ❌ Global Forbidden Actions

### Navigation

| Forbidden | Reason |
|-----------|--------|
| Navigate away without save prompt | Data loss risk |
| Open Lab without valid room context | Crash risk |
| Access admin routes without auth | Security |

---

## ❌ Lab Page Forbidden

### Canvas Behavior

| Forbidden | Reason |
|-----------|--------|
| ❌ Resize canvas when panels open/close | Canvas must be fixed background |
| ❌ Overlay anything on HUD | HUD must always be accessible |
| ❌ Block simulation view completely | User needs visual feedback |

### Panel Behavior

| Forbidden | Reason |
|-----------|--------|
| ❌ Open multiple modals at same time | UX confusion |
| ❌ Resize panels beyond max/min | Layout stability |
| ❌ Persist panel states to DB | UI-only settings |

### Simulation Control

| Forbidden | Reason |
|-----------|--------|
| ❌ Run simulation without init | Crash risk |
| ❌ Step faster than frame rate | Performance |
| ❌ Modify equations while running | State corruption |

---

## ❌ Settings Forbidden

### Platform Settings

| Forbidden | Reason |
|-----------|--------|
| ❌ Edit simulation params in Platform Settings | Wrong layer |
| ❌ Save platform settings to DB | Use localStorage only |

### Simulation Settings (Studio Panel)

| Forbidden | Reason |
|-----------|--------|
| ❌ Settings modal can edit sim params | Input via Studio only |
| ❌ Duplicate input locations | Single source of truth |

---

## ❌ Data Persistence Forbidden

| Forbidden | Reason |
|-----------|--------|
| ❌ Save telemetry to localStorage | Too large |
| ❌ Save UI state to DB | Not persistent data |
| ❌ Lose worldState on save | Core data |

---

## ⚠️ Conditional Restrictions

| Condition | Restriction |
|-----------|-------------|
| While simulation running | Cannot change equations |
| While modal open | Cannot interact with background |
| While saving | Cannot navigate away |
| If validation fails | Cannot start simulation |

---

## 🔒 Enforcement

These rules must be enforced via:

1. **Frontend:** Disable buttons, prevent actions
2. **Backend:** Validate requests, reject invalid
3. **Engine:** Guard conditions in SimCore

---

**Layer:** A — UX/UI Intent  
**Status:** 🔄 In Progress
