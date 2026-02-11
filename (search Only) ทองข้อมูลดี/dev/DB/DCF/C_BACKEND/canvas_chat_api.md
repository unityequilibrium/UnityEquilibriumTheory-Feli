# Canvas Chat API Contract
## Layer C - Backend API Specification

**Version:** 1.0  
**Last Updated:** 2025-12-25  
**Layer:** C (Backend)

---

## 1. Endpoint

```
POST /api/canvas/chat
```

---

## 2. Request

### Headers

```
Content-Type: application/json
X-Trace-Id: <optional>
```

### Body

```typescript
interface ChatRequest {
    message: string;           // User's message
    graphContext?: {           // Optional graph context
        nodeCount: number;
        edgeCount: number;
        nodeTypes: string[];
    };
}
```

---

## 3. Response

### Success (200)

```typescript
interface ChatResponse {
    text: string;              // AI response text
    patch?: GraphPatch;        // Optional graph modification
}

interface GraphPatch {
    type: 'add_node' | 'remove_node' | 'add_edge' | 'remove_edge' | 'update_param';
    payload: unknown;
}
```

### Error

| Code | Error | Cause |
|------|-------|-------|
| 400 | `Message is required` | Empty message |
| 500 | `GEMINI_API_KEY not configured` | Missing .env.local |
| 500 | `Gemini API error: *` | External API failure |

---

## 4. Validation Rules

| Field | Rule | Error |
|-------|------|-------|
| message | required, non-empty | 400 |
| message | max 2000 chars | 400 |
| graphContext | optional | - |

---

## 5. AI Output Restrictions

> **CRITICAL**: AI can ONLY output GraphPatch

| ✅ Allowed | ❌ Forbidden |
|-----------|-------------|
| add_node | create new route |
| remove_node | modify files |
| add_edge | execute code |
| update_param | access DB directly |

---

## 6. Fallback Behavior

```
Try Gemini API
    ↓ success
Return AI response
    ↓ failure  
Return mock response (client-side)
```

---

## 7. Traceability

| This Doc | Links To |
|----------|----------|
| GraphPatch | D_FLOW_ENGINE/node_canvas_architecture.md |
| API route | frontend/src/app/api/canvas/chat/route.ts |
| Error logging | E_DATABASE/error_log_schema.md |

---

**Status:** ✅ SPEC LOCKED
