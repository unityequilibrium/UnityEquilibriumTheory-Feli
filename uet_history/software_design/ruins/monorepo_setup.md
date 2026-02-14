# Monorepo Setup Specification
## Layer E — Database/Persistence

**Version:** 2.0 (Prisma 7)  
**Last Updated:** 2025-12-25  
**Layer:** E (Database)

---

## 1. Overview

UET Platform ใช้ **Bun** (replacing npm) สำหรับ monorepo management
และ runtime performance.

```bash
uet_harness_v0_1/
├── package.json       ← workspaces config
├── frontend/          ← Next.js 16 app
├── database/          ← Prisma 7 + exports
│   ├── prisma.config.ts   ← NEW: Connection config
│   └── prisma/schema.prisma
```

---

## 2. Package Structure

### Root (package.json)

```json
{
  "name": "uet-platform",
  "private": true,
  "workspaces": ["frontend", "database"]
}
```

### Database (@uet/database) — Prisma 7

```json
{
  "name": "@uet/database",
  "main": "index.ts",
  "exports": {
    ".": "./index.ts",
    "./client": "./node_modules/.prisma/client"
  },
  "dependencies": {
    "@prisma/client": "^7.2.0"
  },
  "devDependencies": {
    "prisma": "^7.2.0"
  }
}
```

---

## 3. Rules

| Rule | Description |
|------|-------------|
| **Single Schema** | Prisma schema อยู่ใน database/ เท่านั้น |
| **All Bun** | ใช้ `bun` command เท่านั้น |
| **No Duplicate** | ห้ามมี prisma/ ใน frontend |
| **Version Lock** | Prisma version ต้องตรงกันทุก package |

---

## 4. Frontend Import

```typescript
// frontend/src/lib/prisma.ts
import { PrismaClient } from '@uet/database/client';
// หรือ
import { prisma } from '@uet/database';
```

---

## 5. Commands

| Command | Where | Purpose |
|---------|-------|---------|
| `bun install` | root | Install all |
| `bun run dev --filter frontend` | root | Run frontend |
| `bun run studio` | database | Prisma Studio |
| `bunx prisma generate` | database | Update Client |

---

## 6. Traceability

| This Doc | Links To |
|----------|----------|
| Package structure | global_rules.md R1 |
| Prisma config | schema.md |
| Setup commands | LOCALHOST_SERVICES.md |

---

---

## 7. Troubleshooting (Windows)

### 7.1 Prisma Generic "EPERM" Error

**Symptom:** `Error: EPERM: operation not permitted, rename ...\query_engine-windows.dll.node`

**Cause:** VSCode or running Bun/Node process holds a file lock on the binary.

**Fix:**
1. **Stop Dev Server:** Ctrl+C in all terminals running `bun run dev`.
2. **Clear Lock:** Wait 5-10 seconds.
3. **Generate:** Run `bunx prisma generate --schema ./database/prisma/schema.prisma` manually.
4. **Restart:** `bun run dev --filter frontend`.

---

**Status:** ✅ SPEC LOCKED
