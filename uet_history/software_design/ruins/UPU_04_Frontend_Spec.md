# UPU 04 — API SPECIFICATION (ENTERPRISE-GRADE)

**UET Platform — Unified API Contract v1.0**  
Status: Draft (Auto‑Generated from UPU v1 Model Architecture)  
Author: System Architect (ChatGPT)  
Version: 1.0

---

# 🔥 0. PRINCIPLES — API DESIGN RULES (GLOBAL)

These rules apply _universally_ to every endpoint in the system.

### **0.1 Design Philosophy**

- **Stable**, **Predictable**, **Traceable** APIs
    
- Zero ambiguity
    
- Machines can consume; humans can read
    
- Uniform response envelope
    
- Consistent error codes
    
- Versioned endpoints (v1)
    

### **0.2 Base URL**

```
/api/v1
```

### **0.3 Standard Response Contract**

All successful responses must wrap inside:

```json
{
  "success": true,
  "data": { ... },
  "meta": { ... }
}
```

All errors must use **API error envelope**:

```json
{
  "success": false,
  "error": {
    "code": "STRING_CONSTANT",
    "message": "Human readable message",
    "details": { }
  }
}
```

### **0.4 Authentication**

- JWT (server-signed)
    
- OR NextAuth session cookie
    
- All protected routes require `Authorization: Bearer <token>` OR session cookie
    

### **0.5 Pagination Standard**

Query params:

```
?page=1&limit=20
```

Meta response:

```
"meta": {
  "page": 1,
  "limit": 20,
  "total": 134,
  "totalPages": 7
}
```

### **0.6 Error Code Format**

```
AUTH_INVALID_TOKEN
AUTH_REQUIRED
NOT_FOUND
VALIDATION_ERROR
RATE_LIMITED
INTERNAL_ERROR
```

---

# 🔥 1. AUTHENTICATION API

Base path:

```
/api/v1/auth
```

## **1.1 POST /auth/register**

Register a user.

### Request

```json
{
  "email": "string",
  "password": "string",
  "name": "string"
}
```

### Response

```json
{
  "success": true,
  "data": {
    "userId": "string"
  }
}
```

---

## **1.2 POST /auth/login**

Returns JWT + session.

### Request

```json
{
  "email": "string",
  "password": "string"
}
```

### Response

```json
{
  "success": true,
  "data": {
    "token": "jwt-token",
    "user": {
      "id": "string",
      "email": "string",
      "name": "string"
    }
  }
}
```

---

## **1.3 GET /auth/me**

Get current user info.

### Response

```json
{
  "success": true,
  "data": {
    "id": "string",
    "email": "string",
    "name": "string",
    "profile": { }
  }
}
```

---

# 🔥 2. USER PROFILE API

Base path:

```
/api/v1/profile
```

## **2.1 GET /profile**

Retrieve profile.

## **2.2 PATCH /profile**

Update profile settings.

```json
{
  "bio": "string",
  "preferences": {
    "theme": "dark",
    "language": "th"
  }
}
```

---

# 🔥 3. CHAT SESSIONS API

Base path:

```
/api/v1/chat
```

## **3.1 POST /chat/new**

Create a new chat session.

### Request

```json
{
  "model": "gpt-4o-mini",
  "title": "optional title"
}
```

### Response

```json
{
  "success": true,
  "data": {
    "sessionId": "string"
  }
}
```

---

## **3.2 POST /chat/:id/message**

Send message to session.

### Request

```json
{
  "role": "user",
  "content": "string",
  "files": ["sourceFileId"],
  "options": {
    "deepResearch": false,
    "webSearch": false,
    "canvas": false
  }
}
```

### Response

```json
{
  "success": true,
  "data": {
    "messageId": "string",
    "response": "LLM output stream"
  }
}
```

---

## **3.3 GET /chat/:id/messages**

Retrieve messages.

```json
{
  "success": true,
  "data": [ { "id": "string", "role": "assistant", "content": "..." } ]
}
```

---

# 🔥 4. KNOWLEDGE BASE API (CORE OF PLATFORM)

Base path:

```
/api/v1/kb
```

## **4.1 POST /kb/upload**

Upload file into **Knowledge Base**.

### Request (multipart)

```
file: <binary>
source: "kb" | "upload" | "update"
projectId?: string
```

### Response

```json
{
  "success": true,
  "data": {
    "sourceFileId": "string",
    "chunksCreated": 14
  }
}
```

---

## **4.2 GET /kb/files**

List all KB files.

## **4.3 GET /kb/file/:id**

Get file metadata + content.

## **4.4 DELETE /kb/file/:id**

Remove file + its chunks.

---

# 🔥 5. KB CHUNK API (Vector DB)

Base path:

```
/api/v1/chunks
```

## **5.1 GET /chunks/search**

RAG vector search.

### Query params

```
?q=string&topK=8
```

### Response

```json
{
  "success": true,
  "data": [
    {
      "chunkId": "string",
      "text": "string",
      "score": 0.82,
      "sourceFileId": "string"
    }
  ]
}
```

---

# 🔥 6. PROJECT API

Base path:

```
/api/v1/projects
```

## **6.1 POST /projects**

Create project.

## **6.2 GET /projects**

List projects.

## **6.3 GET /projects/:id**

Project detail.

## **6.4 POST /projects/:id/comment**

Add comment.

---

# 🔥 7. THEORY API

```
/api/v1/theory
```

- CRUD operations for theory documents
    
- Each Theory Document is a markdown unit
    

---

# 🔥 8. STUDIO (NOTEBOOK LM) API

Base path:

```
/api/v1/studio
```

## **8.1 POST /studio/notebook**

Create notebook.

## **8.2 GET /studio/notebook/:id**

Retrieve notebook.

## **8.3 PATCH /studio/notebook/:id**

Update notebook content.

## **8.4 POST /studio/notebook/:id/task**

Run an AutoPrompt / Analysis Task

### Request

```json
{
  "type": "analysis | summary | deep_research | python_simulation",
  "input": { }
}
```

### Response

```json
{
  "success": true,
  "data": {
    "taskId": "string",
    "status": "pending"
  }
}
```

---

# 🔥 9. SYSTEM STATUS API

```
/api/v1/system/status
```

Returns DB, Vector DB, RAG, Model Router health.

---

# END OF DOCUMENT

This API Spec will be used for: Backend rewrite, Frontend integration, Agent tasks, and automated testing.