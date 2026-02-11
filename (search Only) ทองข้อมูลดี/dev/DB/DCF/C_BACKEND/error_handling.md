# Error Handling
## Layer C — Error Responses

---

## 🚨 Error Format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {}
  }
}
```

---

## 📋 Error Codes

| Code | HTTP | Description |
|------|------|-------------|
| NOT_FOUND | 404 | Resource not found |
| VALIDATION_ERROR | 400 | Invalid input |
| INTERNAL_ERROR | 500 | Server error |
| UNAUTHORIZED | 401 | Auth required |
| FORBIDDEN | 403 | Access denied |

---

## 🎯 By Endpoint

### /api/runs

| Scenario | Code | Message |
|----------|------|---------|
| Run not found | NOT_FOUND | "Run with ID xxx not found" |
| Invalid worldState | VALIDATION_ERROR | "Invalid worldState format" |

### /api/projects

| Scenario | Code | Message |
|----------|------|---------|
| Project not found | NOT_FOUND | "Project not found" |
| Name required | VALIDATION_ERROR | "Project name is required" |

---

**Layer:** C — Backend Contract
