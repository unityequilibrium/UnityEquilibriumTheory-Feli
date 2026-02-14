# UET System Inventory: Ruins vs. v5.0 Synthesis

This report provides an audit of all sub-systems identified in the legacy `ruins` directory, cross-referenced with the current **UET v5.0 Platform Specifications**.

## 📊 Status Summary
- **Synthesized (✅)**: Core engines and foundational governance.
- **Partial (🏗️)**: Infrastructure and basic economic rules.
- **Pending (⏳)**: Advanced simulation, analytics dashboards, and social organizational layers.

---

## 🏛️ 1. Core Foundations (Towers)
| System | Ruins Source | v5.0 Status | Note |
|--------|--------------|-------------|------|
| **Agent Engine** | `001 AGENT ENGINE.md`, `11__COMBINED_AGENT_ENGINE.md` | ✅ [03_SPEC](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/uet_history/software_design/platform_specs/03__AGENT_ENGINE_v5.0_SPEC.md) | High-level synthesis complete. |
| **RAG Engine** | `002 RAG ENGINE.md`, `10_COMBINED_RAG_ENGINE.md` | ✅ [04_SPEC](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/uet_history/software_design/platform_specs/04__RAG_ENGINE_v5.0_SPEC.md) | pgvector integration specified. |
| **Knowledge Sync** | `004 KNOWLEDGE SYSTEM`, `09__COMBINED_KS_ENGINE.md` | ✅ [07_SPEC](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/uet_history/software_design/platform_specs/07__KNOWLEDGE_SYNC_v5.0_SPEC.md) | Semantic versioning & Git sync defined. |
| **Flow/Event Bus** | `08__EVENT_BUS SYSTEM`, `14_event_bus.md.md` | ✅ [05_SPEC](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/uet_history/software_design/platform_specs/05__FLOW_AND_EVENT_v5.0_SPINE.md) | Central event bus spine defined. |
| **Model Routing** | `003 MODEL ROUTING`, `13_model_routing.md.md` | ✅ [06_SPEC](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/uet_history/software_design/platform_specs/06__MODEL_ROUTING_v5.0_OPTIMIZER.md) | Multi-model orchestration defined. |

## 🧪 2. Simulation & Math Engines (Missing in v5.0)
| System | Ruins Source | v5.0 Status | Note |
|--------|--------------|-------------|------|
| **Smart Sim Engine** | `SMART_SIMULATION_DESIGN.md` | ⏳ **PENDING** | Missing spec for dynamic equation selection and multi-coupled solvers. |
| **Geosim Canvas** | `geosim_canvas.md`, `geosim_presets.md` | ⏳ **PENDING** | Specialized geographic/spatial simulation logic. |
| **Telemetry Service** | `telemetry_service.md`, `health_events_api.md` | 🏗️ **PARTIAL** | Basic health checks exist in [11_SPEC](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/uet_history/software_design/platform_specs/11__SLA_AND_VERIFICATION_v5.0_STABILITY.md), but no high-frequency service. |

## 📈 3. Analytics & Business Intelligence
| System | Ruins Source | v5.0 Status | Note |
|--------|--------------|-------------|------|
| **KPI Dashboard** | `KPI_DASHBOARD_PLAN.md`, `ANALYTICS_API.md` | ⏳ **PENDING** | The transformation of business metrics into UET parameters (Ω, β) is not yet drafted. |
| **Smart Audit** | `SMART_AUDIT_REPORT.md`, `SMART_INTEGRATION_AUDIT.md` | 🏗️ **PARTIAL** | Mentioned in SLA but needs a dedicated auditing engine spec. |

## 🏘️ 4. Social & Organizational (Rooms)
| System | Ruins Source | v5.0 Status | Note |
|--------|--------------|-------------|------|
| **Room System** | `ROOM_SYSTEM.md`, `ROOM_SCHEMA.md` | ⏳ **PENDING** | Detailed "Phase/Part" model for organizing projects into "Rooms" with internal governance. |
| **Interaction Laws** | `INTERACTION_RULES.md`, `global_rules.md` | ✅ [10_SPEC](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/uet_history/software_design/platform_specs/10__SYSTEM_COORDINATION_v5.0_RULES.md) | Rules for agent/user interaction and negotiation bonuses. |

## 💹 5. Economic & Financial
| System | Ruins Source | v5.0 Status | Note |
|--------|--------------|-------------|------|
| **Asset Ecosystem** | `🏛️ UET Financial Ecosystem Design Document.md` | ✅ [12_SPEC](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/uet_history/software_design/platform_specs/12__MATHNICRY_ECONOMIC_CONSTITUTION.md) | Thermodynamic backing and PoUW are now centralized. |
| **Credit Lifecycle** | `09__FINANCIAL_LIFECYCLE_v5.0_CREDIT.md` | ✅ [09_SPEC](file:///c:/Users/santa/Desktop/lad/Lab_uet_harness_v0.8.7/uet_history/software_design/platform_specs/09__PLATFORM_ENERGY_UNITS.md) | Internal AEU (Energy Units) system defined. |

---

## 🚧 Critical Gaps for Next Steps
1. **Simulation Specification**: Need to bridge the `uet_core` Rust engine with a high-level JS/TS "Smart Simulation" UI spec.
2. **Predictive Dashboard Spec**: Drafting the logic for converting raw data into UET Field parameters.
3. **Room Hierarchy**: Defining how individual projects (like "Lab UET") fit into the broader "Mega-Platform" room structure.
