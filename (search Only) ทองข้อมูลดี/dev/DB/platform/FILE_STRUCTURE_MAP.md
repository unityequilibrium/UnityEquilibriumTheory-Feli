# File Structure Map - Code to Documentation

> **Complete Reference: Source Files ↔ Documentation**  
> ทุก path เป็น relative จาก `frontend/src/`  
> **Last Updated:** 2024-12-24

---

## 📊 Summary

| Category | Files | Status |
|----------|-------|--------|
| **lib/** | 47 files | ✅ Exists |
| **components/** | 28 files | ✅ Exists |
| **features/** | 16 files | ✅ Exists |
| **Total** | **91 files** | |

---

## 🧠 SMART SYSTEM FILES

### Existing Smart Components ✅

| Source File | Documentation | Status |
|-------------|---------------|--------|
| [units/logic/UnitConverter.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/features/units/logic/UnitConverter.ts) | [SMART_UNIT_COMPONENT.md](design_system/SMART_UNIT_COMPONENT.md) | ✅ |
| [units/logic/ConversionRules.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/features/units/logic/ConversionRules.ts) | [SMART_UNIT_COMPONENT.md](design_system/SMART_UNIT_COMPONENT.md) | ✅ |
| [units/store/useUnitSystem.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/features/units/store/useUnitSystem.ts) | [SMART_SYSTEM_DESIGN.md](design_system/SMART_SYSTEM_DESIGN.md) | ✅ |
| [units/components/SmartMetric.tsx](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/features/units/components/SmartMetric.tsx) | [SMART_UNIT_COMPONENT.md](design_system/SMART_UNIT_COMPONENT.md) | ✅ |
| [units/components/UnitDropdown.tsx](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/features/units/components/UnitDropdown.tsx) | [SMART_UNIT_COMPONENT.md](design_system/SMART_UNIT_COMPONENT.md) | ✅ |
| [units/types.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/features/units/types.ts) | [SMART_DATA_DICTIONARY.md](SMART_DATA_DICTIONARY.md) | ✅ |

---

## 📚 LIB (Core Libraries)

### Registry
| Source File | Documentation | Status |
|-------------|---------------|--------|
| [lib/registry/index.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/registry/index.ts) | [SMART_DATA_DICTIONARY.md](SMART_DATA_DICTIONARY.md) | ✅ |
| [lib/registry/metrics.json](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/registry/metrics.json) | [SMART_DATA_DICTIONARY.md](SMART_DATA_DICTIONARY.md) | ✅ |
| [lib/contracts/metrics.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/contracts/metrics.ts) | [SMART_DATA_DICTIONARY.md](SMART_DATA_DICTIONARY.md) | ✅ |

### Equations
| Source File | Documentation | Status |
|-------------|---------------|--------|
| [lib/equations/registry.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/equations/registry.ts) | [SMART_SIMULATION_DESIGN.md](design_system/SMART_SIMULATION_DESIGN.md) | ✅ |
| [lib/equations/types.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/equations/types.ts) | [EQUATION_SYSTEM_DESIGN.md](design_system/EQUATION_SYSTEM_DESIGN.md) | ✅ |
| [lib/equations/BaseEquation.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/equations/BaseEquation.ts) | [EQUATION_SYSTEM_DESIGN.md](design_system/EQUATION_SYSTEM_DESIGN.md) | ✅ |
| [lib/equations/modules/newton.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/equations/modules/newton.ts) | [SMART_SIMULATION_DESIGN.md](design_system/SMART_SIMULATION_DESIGN.md) | ✅ |
| [lib/equations/modules/einstein.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/equations/modules/einstein.ts) | [SMART_SIMULATION_DESIGN.md](design_system/SMART_SIMULATION_DESIGN.md) | ✅ |
| [lib/equations/modules/uet.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/equations/modules/uet.ts) | [SMART_SIMULATION_DESIGN.md](design_system/SMART_SIMULATION_DESIGN.md) | ✅ |

### Simulation Engine
| Source File | Documentation | Status |
|-------------|---------------|--------|
| [lib/SimCoreV4.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/SimCoreV4.ts) | [SMART_SIMULATION_DESIGN.md](design_system/SMART_SIMULATION_DESIGN.md) | ✅ |
| [lib/simStoreV4.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/simStoreV4.ts) | [SMART_SIMULATION_DESIGN.md](design_system/SMART_SIMULATION_DESIGN.md) | ✅ |
| [lib/FieldCapture.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/FieldCapture.ts) | [VISUALIZATION_CAPABILITIES.md](design_system/VISUALIZATION_CAPABILITIES.md) | ✅ |

### Services
| Source File | Documentation | Status |
|-------------|---------------|--------|
| [lib/services/telemetryService.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/services/telemetryService.ts) | [BACKEND_ARCHITECTURE.md](BACKEND_ARCHITECTURE.md) | ✅ |
| [lib/services/persistenceService.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/services/persistenceService.ts) | [BACKEND_ARCHITECTURE.md](BACKEND_ARCHITECTURE.md) | ✅ |
| [lib/services/notesService.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/services/notesService.ts) | [API_REFERENCE.md](API_REFERENCE.md) | ✅ |

### Oracle (Physics Verification)
| Source File | Documentation | Status |
|-------------|---------------|--------|
| [lib/oracle/invariants.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/oracle/invariants.ts) | [VERIFICATION_SYSTEM.md](VERIFICATION_SYSTEM.md) | ✅ |
| [lib/oracle/kepler.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/oracle/kepler.ts) | [VERIFICATION_SYSTEM.md](VERIFICATION_SYSTEM.md) | ✅ |
| [lib/oracle/scenarios.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/oracle/scenarios.ts) | [VERIFICATION_SYSTEM.md](VERIFICATION_SYSTEM.md) | ✅ |
| [lib/oracle/testRunner.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/oracle/testRunner.ts) | [SMART_VERIFICATION_SYSTEM.md](SMART_VERIFICATION_SYSTEM.md) | ✅ |

### API & Auth
| Source File | Documentation | Status |
|-------------|---------------|--------|
| [lib/api/response.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/api/response.ts) | [API_REFERENCE.md](API_REFERENCE.md) | ✅ |
| [lib/auth/context.tsx](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/auth/context.tsx) | [BACKEND_ARCHITECTURE.md](BACKEND_ARCHITECTURE.md) | ✅ |
| [lib/auth/permissions.ts](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/lib/auth/permissions.ts) | [BACKEND_ARCHITECTURE.md](BACKEND_ARCHITECTURE.md) | ✅ |

---

## 🎨 COMPONENTS (UI)

### Lab Components
| Source File | Documentation | Status |
|-------------|---------------|--------|
| [components/lab/MetricCard.tsx](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/components/lab/MetricCard.tsx) | [SMART_PLOTLY_DESIGN.md](design_system/SMART_PLOTLY_DESIGN.md) | ✅ |
| [components/lab/MetricCardList.tsx](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/components/lab/MetricCardList.tsx) | [LAB_UI_DESIGN_SPEC.md](design_system/LAB_UI_DESIGN_SPEC.md) | ✅ |
| [components/lab/GraphDock.tsx](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/components/lab/GraphDock.tsx) | [SMART_PLOTLY_DESIGN.md](design_system/SMART_PLOTLY_DESIGN.md) | ✅ |
| [components/lab/EquationList.tsx](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/components/lab/EquationList.tsx) | [EQUATION_SYSTEM_DESIGN.md](design_system/EQUATION_SYSTEM_DESIGN.md) | ✅ |
| [components/lab/UnitValueDisplay.tsx](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/components/lab/UnitValueDisplay.tsx) | [SMART_UNIT_COMPONENT.md](design_system/SMART_UNIT_COMPONENT.md) | ✅ |

### Layout Components
| Source File | Documentation | Status |
|-------------|---------------|--------|
| [components/layout/LeftOutputPanel.tsx](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/components/layout/LeftOutputPanel.tsx) | [LAB_UI_DESIGN_SPEC.md](design_system/LAB_UI_DESIGN_SPEC.md) | ✅ |
| [components/layout/RightStudioPanel.tsx](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/components/layout/RightStudioPanel.tsx) | [LAB_UI_DESIGN_SPEC.md](design_system/LAB_UI_DESIGN_SPEC.md) | ✅ |
| [components/layout/TopNav.tsx](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/components/layout/TopNav.tsx) | [UI_BLUEPRINT.md](design_system/UI_BLUEPRINT.md) | ✅ |
| [components/layout/CenterHUD.tsx](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/components/layout/CenterHUD.tsx) | [LAB_UI_DESIGN_SPEC.md](design_system/LAB_UI_DESIGN_SPEC.md) | ✅ |

---

## 🎮 FEATURES (Feature Modules)

### Simulation
| Source File | Documentation | Status |
|-------------|---------------|--------|
| [features/simulation/Sim3DRoom.tsx](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/features/simulation/Sim3DRoom.tsx) | [SMART_SIMULATION_DESIGN.md](design_system/SMART_SIMULATION_DESIGN.md) | ✅ |
| [features/simulation/SimulationHUD.tsx](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/features/simulation/SimulationHUD.tsx) | [LAB_UI_DESIGN_SPEC.md](design_system/LAB_UI_DESIGN_SPEC.md) | ✅ |
| [features/simulation/GraphDock.tsx](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/features/simulation/GraphDock.tsx) | [SMART_PLOTLY_DESIGN.md](design_system/SMART_PLOTLY_DESIGN.md) | ✅ |
| [features/simulation/MetricCards.tsx](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/features/simulation/MetricCards.tsx) | [SMART_PLOTLY_DESIGN.md](design_system/SMART_PLOTLY_DESIGN.md) | ✅ |

### Rooms
| Source File | Documentation | Status |
|-------------|---------------|--------|
| [features/rooms/RoomRouter.tsx](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/features/rooms/RoomRouter.tsx) | [PAGE_WIRING_DIAGRAMS.md](design_system/PAGE_WIRING_DIAGRAMS.md) | ✅ |

### Diagnostics
| Source File | Documentation | Status |
|-------------|---------------|--------|
| [features/diagnostics/DiagnosticsTerminal.tsx](file:///c:/Users/santa/Desktop/lad/uet_harness_v0_1_hangfix_v5_3_dtladderfix/uet_harness_v0_1/frontend/src/features/diagnostics/DiagnosticsTerminal.tsx) | [SMART_VERIFICATION_SYSTEM.md](SMART_VERIFICATION_SYSTEM.md) | ✅ |

---

## 📋 Verification Checklist

### Smart System Files
```
✅ UnitConverter.ts exists
✅ useUnitSystem.ts exists
✅ SmartMetric.tsx exists
✅ UnitDropdown.tsx exists
✅ ConversionRules.ts exists
✅ metrics.json has all metrics
```

### Core Engine Files
```
✅ SimCoreV4.ts exists
✅ simStoreV4.ts exists
✅ EquationRegistry exists
✅ Newton/Einstein/UET modules exist
```

### Documentation Links
```
✅ All Smart files link to SMART_*.md
✅ All API files link to API_REFERENCE.md
✅ All simulation files link to SMART_SIMULATION_DESIGN.md
```

---

## 🔗 Quick Links by Category

| Category | Doc | Key Files |
|----------|-----|-----------|
| **Smart Units** | [SMART_UNIT_COMPONENT](design_system/SMART_UNIT_COMPONENT.md) | UnitConverter, SmartMetric, UnitDropdown |
| **Smart Charts** | [SMART_PLOTLY_DESIGN](design_system/SMART_PLOTLY_DESIGN.md) | GraphDock, MetricCard |
| **Smart Sim** | [SMART_SIMULATION_DESIGN](design_system/SMART_SIMULATION_DESIGN.md) | SimCoreV4, simStoreV4 |
| **Metrics** | [SMART_DATA_DICTIONARY](SMART_DATA_DICTIONARY.md) | metrics.json, registry |
| **API** | [API_REFERENCE](API_REFERENCE.md) | api/response, services |
| **UI** | [LAB_UI_DESIGN_SPEC](design_system/LAB_UI_DESIGN_SPEC.md) | Panels, TopNav, HUD |

---

> **Note:** ใช้เอกสารนี้เพื่อตรวจสอบว่าทุกไฟล์มี documentation ครอบคลุม
> หาก link ไหนหาย ให้แก้ไขทันที
