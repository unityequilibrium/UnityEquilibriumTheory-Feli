# Doc Structure Standard
## UET Platform - Documentary Template v1.0

**Purpose:** โครงเอกสารแบบเดียวทั้งโปรเจกต์

---

## 📁 Required Directory Structure

```
docs/
├── DCF/                           # Documentary Consistency Framework
│   ├── DCF_MASTER.md             # Framework definition
│   ├── DCF_ANALYSIS_REPORT.md    # Analysis results
│   ├── doc_coverage_table.md     # Inventory
│   ├── doc_structure_v1.md       # This file
│   ├── global_rules.md           # Platform rules (immutable)
│   │
│   ├── A_UX_UI/                  # Layer A
│   │   ├── INDEX.md
│   │   ├── intent.md
│   │   ├── page_map.md
│   │   ├── interaction_rules.md
│   │   └── forbidden_actions.md
│   │
│   ├── B_FRONTEND/               # Layer B
│   │   ├── INDEX.md
│   │   ├── component_map.md
│   │   ├── state_model.md
│   │   ├── action_map.md
│   │   └── layout_contract.md
│   │
│   ├── C_BACKEND/                # Layer C
│   │   ├── INDEX.md
│   │   ├── api_contract.md
│   │   ├── validation_rules.md
│   │   └── error_handling.md
│   │
│   ├── D_FLOW_ENGINE/            # Layer D
│   │   ├── INDEX.md
│   │   ├── flow_diagram.md
│   │   ├── runner_logic.md
│   │   ├── test_gate_logic.md
│   │   └── determinism_rules.md
│   │
│   ├── E_DATABASE/               # Layer E
│   │   ├── INDEX.md
│   │   ├── schema.md
│   │   ├── persistence_policy.md
│   │   └── replay_rules.md
│   │
│   ├── TRACEABILITY/             # Cross-layer
│   │   ├── INDEX.md
│   │   ├── a_to_b.md
│   │   ├── b_to_c.md
│   │   ├── c_to_d.md
│   │   ├── d_to_e.md
│   │   └── e_to_a.md
│   │
│   └── REGISTRIES/               # Registry specs
│       ├── room_registry.md
│       ├── metric_registry.md
│       └── test_registry.md
│
└── platform/                      # Platform reference docs
    ├── API_REFERENCE.md
    ├── BACKEND_ARCHITECTURE.md
    ├── DATABASE_SCHEMA.md
    ├── COMPONENT_REGISTRY.md
    ├── BUTTON_ACTION_IDS.md
    ├── SETTINGS_CONTRACT.md
    ├── SMART_*.md                 # Smart system docs
    └── design_system/             # Design specs
```

---

## 📋 Document Template

ทุก doc ต้องมีโครงสร้างนี้:

```markdown
# [Document Title]
## [Subtitle / Layer identifier]

**Last Updated:** YYYY-MM-DD  
**Layer:** A/B/C/D/E  
**Status:** ✅ Complete / ⚠️ Partial / ❌ Missing

---

## 📋 Purpose

[1-2 sentences describing what this doc covers]

---

## 📊 Content

[Main content organized by sections]

---

## 🔗 Related Docs

- [Link to related doc 1](path)
- [Link to related doc 2](path)

---

## ⬅️ Previous Layer
← [Previous Layer](../X_LAYER/INDEX.md)

## ➡️ Next Layer  
→ [Next Layer](../Y_LAYER/INDEX.md)
```

---

## 🏷️ Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| Layer folder | `X_NAME/` | `A_UX_UI/` |
| Index file | `INDEX.md` | `INDEX.md` |
| Content file | `lowercase_underscore.md` | `state_model.md` |
| Registry file | `[thing]_registry.md` | `room_registry.md` |
| Contract file | `[layer]_contract.md` | `api_contract.md` |

---

## ✅ Validation Rules

1. ทุก layer ต้องมี INDEX.md
2. ทุก doc ต้องมี Last Updated date
3. ทุก doc ต้องมี Layer identifier
4. ทุก doc ต้อง link ไป prev/next layer
5. ห้ามมี orphan doc (ต้องอยู่ใน layer ใดลayer หนึ่ง)

---

**Status:** ✅ Template locked
