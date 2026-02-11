# UX Interaction Rules
## Layer A — Intent & User Experience

**Version:** 1.0  
**Last Updated:** 2025-12-25  
**Layer:** A (UX/Intent)

---

# 1. Graph Lifecycle (User Perspective)

The user interacts with the Node Graph through distinct lifecycle states, ensuring predictability and data safety.

## 1.1 State: Active Editing
- **Context:** User is manipulating nodes/edges in the Canvas View.
- **Intent:** Explore "what-if" scenarios.
- **Actions:**
  - `graph_save`: Explicitly commit the current layout to persistence.
  - `view_toggle`: Switch visualization mode (does not save/reset).

## 1.2 State: Restoration (Loading)
- **Context:** User wants to revert to a known good state or resume work.
- **Intent:** "Undo my mess" or "Continue from yesterday".
- **Actions:**
  - `graph_load_latest`: Quick actions for immediate restoration (Last In, First Out).
  - `graph_browse`: Explore historical versions (Project Gallery).

---

# 2. Control overlay Specification

To support these lifecycles, the Canvas View MUST implement a dedicated overlay.

## 2.1 Visual Hierarchy
1.  **Primary Action:** Toggle View (Mode Switch).
2.  **Secondary Action:** Save Layout (Commit).
3.  **Tertiary Action:** Load/Browse (Restore).

## 2.2 Feedback Rules
- **On Save:** Must show ephemeral success toast ("Graph Saved").
- **On Load:** Must show confirmation toast ("Loaded: [Graph Name]").
- **On Error:** Must show persistent alert ("Failed to save: [Reason]").

---

# 3. Developer Lifecycle (System Debug)

For system verification, we provide a "Raw View" that bypasses all UI Controller overlays.

## 3.1 View: `/dev` (System Graph)
-   **Context:** Developer needs to verify "Everything is a Node" architecture.
-   **Intent:** See the naked graph with all Actors (AI, DB, Terminal) exposed as nodes.
-   **Access:** `http://localhost:3000/dev`
-   **Restrictions:** No Smart Panels, No Safety Rails. Pure Graph interaction.

---

# 4. Keyboard Shortcuts

Essential keyboard shortcuts for power users.

| Shortcut | Action | Context |
|:---------|:-------|:--------|
| `Space` | Play/Pause simulation | Lab Shell |
| `Escape` | Close modal/overlay | Global |
| `Ctrl+S` | Save graph | Canvas View |
| `Ctrl+Z` | Undo (planned) | Canvas View |
| `[` | Toggle left panel | Lab Shell |
| `]` | Toggle right panel | Lab Shell |
| `F` | Fit view to graph | Canvas View |
| `1-4` | Switch dimension mode | Simulation HUD |

---

# 5. Layered Governance

All UX interactions documented here MUST be traceable to their underlying technical implementation.

| UI Action | Primary Layer | Backend Contract | Persistence |
|:----------|:--------------|:-----------------|:------------|
| Graph Save | B (UI) | [C (API)](../C_BACKEND/api_contract.md) | [E (Schema)](../E_DATABASE/schema.md) |
| Sim Control | D (Engine) | [C (API)](../C_BACKEND/api_contract.md) | [E (Policy)](../E_DATABASE/persistence_policy.md) |

For full mapping, see the [TRACEABILITY_MATRIX.md](../TRACEABILITY_MATRIX.md).

---

**Status:** ✅ SPEC LOCKED
