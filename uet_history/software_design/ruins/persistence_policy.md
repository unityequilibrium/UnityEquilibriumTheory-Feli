# Persistence Policy
## Layer E — What Gets Saved (Complete Contract)

**Last Updated:** 2024-12-24  
**Layer:** E (Database)  
**Status:** 🔒 LOCKED

---

## 📋 Decision Tree

```
Is it simulation data?
├── Yes → MUST save to DB (runs table)
│   ├── worldState (particles, time, step)
│   ├── equations config
│   ├── seed
│   └── parameters (dt, softening)
│
└── No → Is it user preference?
    ├── Yes → Save to localStorage
    │   ├── theme
    │   ├── showFPS
    │   └── defaultUnits
    │
    └── No → Is it session UI state?
        ├── Yes → React state only (no persist)
        │   ├── panel open/close
        │   ├── dimension mode
        │   └── camera position
        │
        └── No → Case-by-case evaluation
```

---

## ✅ MUST Persist (Database)

| Data | Table | Column | Type |
|------|-------|--------|------|
| worldState | snapshots | state_json | jsonb |
| equations | run_equations | config | jsonb |
| seed | runs | seed | bigint |
| notes | notes | content | text |
| telemetry | telemetry_samples | value | decimal |
| node graphs | node_graphs | layout | jsonb |

---

## ❌ MUST NOT Persist

| Data | Reason |
|------|--------|
| Panel open/close | UI-only, session |
| Dimension mode (2D/3D/4D) | UI-only, session |
| Camera position | Optional, not core |
| Animation frame state | Runtime only |
| Theme preference | Use localStorage |

---

## 📍 localStorage Keys

| Key | Type | Default |
|-----|------|---------|
| `uet.theme` | 'dark' \| 'light' | 'dark' |
| `uet.showFPS` | boolean | false |
| `uet.defaultUnits` | 'SI' \| 'cgs' | 'SI' |

---

## 🔒 Rules

1. **Never lose worldState** - Core data must persist
2. **Never persist UI state to DB** - Use React state
3. **Never persist preferences to DB** - Use localStorage
4. **Save before navigate** - Prompt if unsaved

---

**Layer:** E — Database/Persistence

