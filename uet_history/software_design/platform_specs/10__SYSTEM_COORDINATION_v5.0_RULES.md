# UET v5.0 — System Coordination & Interaction Specification

## 1. Overview
System Coordination defines the "Traffic Rules" for how UI Panels, API Services, and Backend Engines interact. It prevents "State Collision" and ensures Knowledge Integrity across the platform.

## 2. Interaction Principles
- **Predictability**: User action -> Deterministic event -> Verified output.
- **Context Isolation**: Data from Project A cannot leak into Project B's chat context.
- **No Side Effects**: Agents can suggest edits (Studio) but cannot commit them directly to the Global KB without manual Admin approval.

## 3. Component Interaction Matrix

| Initiator | Receiver | Channel | Content Type |
| :--- | :--- | :--- | :--- |
| **Chat Panel** | **RAG Engine** | API / RPC | Query + Project_ID |
| **Studio Panel** | **Agent Engine**| Event Bus | Markdown Content + Script_ID |
| **Source Panel** | **Knowledge Sync**| Event Bus | File_Blob + Chunk_Rules |
| **Flow Control** | **All Modules** | State Spine | Permission_Token + State_Lock |

## 4. Request Lifecycle (The Unified Flow)
1.  **Intent Capture**: User interacts with a Panel (e.g., clicks "Summarize").
2.  **Gatekeeping**: Flow Control validates permissions and budget (AT Balance).
3.  **Event Dispatch**: Event Bus broadcasts `REQUEST.AGENT.SUMMARIZE`.
4.  **Engine Execution**: Appropriate engine (Agent/RAG) processes the request.
5.  **State Update**: DB updates record, then UI updates via Real-time socket.

## 5. Knowledge Leakage Prevention (KLP)
- **Project Sandbox**: Every RAG retrieval must include a `scope_id`. Results outside this scope are filtered at the DB layer (`SQL filter where project_id = current`).
- **Session Purge**: Memory buffers for L1/L2 models are cleared immediately upon session termination to prevent residual data from affecting future unrelated queries.

## 6. Conflict Resolution
- **Version Collisions**: If two users edit the same Studio note, the `Knowledge Sync` engine applies a Last-Write-Wins (LWW) or Prompt-based Merge strategy.
- **Event Jams**: If the Event Bus is saturated, Flow Control enters `THROTTLE` state, prioritizing critical system messages over background agent tasks.

## 7. The Negotiation (Equilibrium) Bonus Logic
To reach global economic balance, the platform incentivizes negotiation over static trade.
1.  **Event**: `MARKET.NEGOTIATION.START`
2.  **Engine**: Agent Engine simulates `Nash Equilibrium` for both parties.
3.  **Bonus**: If a deal is struck at the calculated Equilibrium point, both parties receive a **Negotiation Bonus** (in UET Coin).
4.  **Rationale**: This bonus is minted from the "Scientific Work" reserve, as the negotiation itself is a form of social-interaction mining.

## 8. Interaction Safety (Forbidden Actions)
- **Energy Theft**: Attempting to bypass the `uet_core` post-process mining triggers an immediate `WALLET_LOCK`.
- **Side Attacks**: Any intent to manipulate the Thermodynamic TXR (Exchange Rate) is blocked by the Flow Gatekeeper.
