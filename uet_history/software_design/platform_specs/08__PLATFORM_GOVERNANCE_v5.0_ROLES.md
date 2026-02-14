# UET v5.0 — Platform Governance & Roles Specification

## 1. Overview
Platform Governance defines the hierarchy of human and agent actors within the Unity Mega-Platform. It ensures the "Architecture of Trust" by strictly enforcing boundaries between research data, personal workspaces, and global infrastructure.

## 2. The 4-Tier Role System

| Role | Description | Core Permission |
| :--- | :--- | :--- |
| **Guest** | Unauthenticated user exploring public theories. | Read PUBLIC data only. |
| **Member** | Registered user with personal and project access. | CRUD inside OWN projects. |
| **Power User** | Advanced researchers/developers with agent access. | Run complex simulations & RAG agents. |
| **Admin** | System governors and infrastructure managers. | System-wide config + G-KB promotion. |

## 3. Permission Matrix

| Action | Guest | Member | Power User | Admin |
| :--- | :---: | :---: | :---: | :---: |
| View Public Theory | ✅ | ✅ | ✅ | ✅ |
| Create Project | ❌ | ✅ | ✅ | ✅ |
| Edit Project (Own) | ❌ | ✅ | ✅ | ✅ |
| Edit Project (Other) | ❌ | ❌ | ❌ | ✅ |
| Upload to P-KB | ❌ | ✅ | ✅ | ✅ |
| Promote P-KB to G-KB | ❌ | ❌ | ❌ | ✅ |
| Run L2 Global Agents | ❌ | ❌ | ✅ | ✅ |
| Manage System Config | ❌ | ❌ | ❌ | ✅ |

## 4. Agent Boundary Enforcement
In UET v5.0, an Agent's permissions are **strictly inherited** from its invoking owner.
- **Rule**: `Agent.Permissions = Owner.Permissions`
- **Constraint**: User-agents cannot elevate privileges to access `uet_core` internal logs or cross-project data unless explicitly shared via the Event Bus with appropriate tokens.

## 5. Knowledge Levels & Isolation
1.  **Personal (L1)**: Sandboxed data, invisible to agents unless specified.
2.  **Project (L2)**: Shared within a research team. Primary context for Research Agents.
3.  **Global (L3)**: Immutable, Axiomatic truth. Visible to all for retrieval, modifiable only by Admin.

## 6. Audit & Accountability
- **System Log**: Every action by a Power User or Admin that modifies the L3 Global state must be signed and logged.
- **Transparency**: Users can view the "Audit Trail" of any piece of knowledge to see its origin and validation history.

## 7. Input/Output Contracts
- **Input**: User Identity Token (JWT), Action Intent, Target Resource ID.
- **Verification**: Flow-Gatekeeper validates token against the Permission Matrix before the Event Bus delivers the message.
