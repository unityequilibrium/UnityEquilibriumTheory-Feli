# Validation Rules
## Layer C — Input Validation

---

## ✅ Request Validation

### POST /api/runs

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| scenarioId | string | No | Valid scenario ID if provided |
| equations | JSON | No | Array of equation configs |
| worldState | JSON | No | Valid world state structure |
| runName | string | No | Max 255 chars |

### POST /api/projects

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| name | string | Yes | 1-255 chars |
| description | string | No | Max 1000 chars |
| isPublic | boolean | No | Default false |

### POST /api/notes

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| runId | string | Yes | Must exist in runs table |
| content | string | Yes | 1-10000 chars |

---

## 🔒 Security Validation

1. **No SQL injection** - All queries through Prisma
2. **Input sanitization** - HTML stripped
3. **Size limits** - Max 10MB request body

---

**Layer:** C — Backend Contract
