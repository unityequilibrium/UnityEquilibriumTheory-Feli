# Dev View Specification
## Layer A — /dev Page UX Contract

**Version:** 1.0  
**Last Updated:** 2025-12-25  
**Layer:** A (UX/Intent)

---

## 1. Purpose

The `/dev` page provides a **Live Audit Trail & Governance Monitor** that visualizes:
- Real-time action logs and user interactions
- Distributed trace IDs for cross-layer auditing
- System health status and connection integrity
- Real-time simulation determinism checks

---

## 2. Target Users

| User | Use Case |
|:-----|:---------|
| Developer | Debug platform issues |
| Architect | Verify system design |
| QA | Trace test failures |

---

## 3. Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  /dev - SYSTEM_AUDIT (Audit Trail)                      [Home]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [GOVERNANCE STATUS]                                             │
│  Traceability: ALIGNED                                           │
│  Determinism:  LOCKED                                            │
│                                                                  │
│  [🕵️ LIVE AUDIT TRAIL]                                          │
│  10:04:22 | ID: room_select_open | Trace: b53f...                │
│  10:04:25 | ID: sim_play_pause   | Trace: b53f...                │
│                                                                  │
│  [Controls]                                                      │
│  [RESCAN_DEPENDENCIES] [CLEAR_AUDIT_LOG]                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. System Node Types

| Node Type | Description | Status Source |
|:----------|:------------|:--------------|
| `system-layer-a` | UX/Intent layer | Static |
| `system-layer-b` | Frontend layer | Static |
| `system-layer-c` | API layer | Health check |
| `system-layer-d` | Engine layer | simStore |
| `system-layer-e` | Database layer | Prisma health |
| `system-auth` | Auth service | Session status |
| `system-api` | API route | Request count |
| `system-store` | Zustand store | Subscriber count |
| `system-db` | Database connection | Connection pool |
| `system-test` | Test runner | Last result |
| `system-gate` | Test gate (G0-G4) | Pass/Fail |

---

## 5. Interactions

| Action ID | Trigger | Effect |
|:----------|:--------|:-------|
| `dev_node_select` | Click node | Show details in panel |
| `dev_refresh` | Click refresh | Reload all status |
| `dev_run_tests` | Click "Run Tests" | Execute test gates |
| `dev_close` | Click close | Navigate to /lab |

---

## 6. Data Flow

```mermaid
graph LR
    A[/dev Page] -->|Load| B[systemNodeRegistry]
    B -->|Get Nodes| C[Platform Graph]
    C -->|Render| D[React Flow]
    
    E[Health Check] -->|Poll| F[Node Status]
    F -->|Update| D
```

---

## 7. Access Control

| Role | Can Access? |
|:-----|:------------|
| Developer | ✅ |
| Admin | ✅ |
| User | ❌ (hidden in nav) |

---

## 8. Implementation Status

| Feature | Status |
|:--------|:-------|
| /dev route | ✅ Implemented |
| Audit Trail Overlay | ✅ Implemented |
| Live Trace Tracking | ✅ Implemented |
| Governance Status | ✅ Implemented |
| Audit Controls | ✅ Implemented |

---

**Layer:** A — UX/Intent  
**Status:** ✅ ALIGNED  
**Next:** Monitor production scaling
