# Traceability Matrix (A-E)
## UET Platform - Cross-Layer Governance

**Version:** 1.1  
**Status:** ✅ ALIGNED  
**Layer:** All (Governance)

---

## 🏗️ 1. Core Feature Traceability

This matrix ensures that every major feature is documented from User Intent (A) down to Database Persistence (E).

| Feature Component | A (UX Intent) | B (Frontend UI) | C (API/Interface) | D (Flow Engine) | E (Database) |
|:---|:---|:---|:---|:---|:---|
| **Graph Interaction** | [dev_view_spec.md](../DCF/A_UX/dev_view_spec.md) | [CanvasView.tsx](../../frontend/src/components/canvas/CanvasView.tsx) | `/api/graphs` | [node_canvas_architecture.md](../DCF/D_FLOW_ENGINE/node_canvas_architecture.md) | `NodeGraph` |
| **Simulation Runtime** | [intent.md](../DCF/A_UX_UI/intent.md) | [SimulationHUD.tsx](../../frontend/src/components/canvas/SimulationHUD.tsx) | `/api/runs` | [sim_core_v4.md](../DCF/D_FLOW_ENGINE/sim_core_v4.md) | `Run` |
| **Live Telemetry** | [telemetry_spec.md](../platform/telemetry_spec.md) | [MetricNode.tsx](../../frontend/src/components/canvas/CanvasNodes.tsx) | `/api/telemetry` | [telemetry_service.md](../DCF/D_FLOW_ENGINE/telemetry_service.md) | `Sample` |
| **AI Copilot** | [ai_interaction.md](../platform/ai_interaction.md) | [AIChatNode.tsx](../../frontend/src/components/canvas/AIChatNode.tsx) | `/api/ai/chat` | [canvas_chat_api.md](../DCF/C_BACKEND/canvas_chat_api.md) | `EventLog` |
| **Global Audit** | [dev_view_spec.md](../DCF/A_UX/dev_view_spec.md) | [DevPage.tsx](../../frontend/src/app/dev/page.tsx) | `/api/health` | [test_gate_logic.md](../DCF/D_FLOW_ENGINE/test_gate_logic.md) | `AuditLog` |

---

## 🔄 2. Interaction Traceability (Action IDs)

Every `data-action-id` in Layer B MUST result in a traceable state change in C, D, or E.

| Action Category | Trigger (B) | Handler (D/C) | Validation Rule (C) | Persistence (E) |
|:---|:---|:---|:---|:---|
| **Graph Cycles** | `graph_save` | `GraphController.save()` | Schema v1 Check | `NodeGraph` insertion |
| **Sim Cycles** | `hud_play_pause` | `SimRunner.tick()` | Determinism Lock | `Run.step` update |
| **Registry Mod** | `sim_add_equation` | `RegistryManager.add()` | Existence Check | N/A (Registry-only) |

---

## 🔐 3. Layer Constraints

| Layer | Primary Constraint | Violation Consequence |
|:---|:---|:---|
| **A (UX)** | No "Orphan" features | Feature Reversion |
| **B (UI)** | Strict `data-action-id` | UI Rejection |
| **C (API)** | Mandatory `x-trace-id` | Request Rejection (403) |
| **D (Engine)** | Strict Determinism (R4.1) | Calculation Invalidated |
| **E (DB)** | Persistence Policy (R6.1) | State Loss (Critical) |

---

## 📋 4. Readiness Declaration

**Is this platform ready for full architectural AUDIT?**
- [x] All Registries Documented
- [x] All API Endpoints Contracted
- [x] All Action IDs Mapped
- [x] Global Rules Locked

**Ready for AUDIT_PLAN?** 🟢 YES

---

**Last Updated:** 2025-12-25  
**Approver:** System Architect
