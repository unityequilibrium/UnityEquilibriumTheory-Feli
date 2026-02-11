# Defensive Coding Rules
## Layer D — Engine Robustness

**Last Updated:** 2024-12-24  
**Status:** 🔒 LOCKED

---

## ⚠️ CRITICAL: All Initialize Methods Must Be Defensive

### Rule D.1: Null/Undefined Input Handling

> **ALL `.initialize()` and `.hydrate()` methods MUST handle undefined inputs gracefully.**
> 
> ❌ NEVER assume data from API/JSON is valid
> ✅ ALWAYS add null checks before accessing `.length` or other properties

**Pattern:**

```typescript
// ❌ WRONG - crashes on undefined
async initialize(): Promise<void> {
    const data = await fetch('/api/registry').then(r => r.json());
    console.log(`Loaded ${data.metrics.length} metrics`); // CRASH!
}

// ✅ CORRECT - defensive
async initialize(): Promise<void> {
    try {
        const data = await fetch('/api/registry').then(r => r.json());
        if (data?.metrics && Array.isArray(data.metrics)) {
            this.registry.metrics = data.metrics;
            console.log(`Loaded ${data.metrics.length} metrics`);
        } else {
            console.warn('[Registry] Invalid data, using defaults');
        }
    } catch (error) {
        console.error('[Registry] Initialization failed:', error);
    }
}
```

---

## Rule D.2: Fallback to Local Data

> When API fails, fallback to local JSON or sensible defaults.

**Pattern:**

```typescript
constructor() {
    // Initialize with local fallback immediately
    this.registry = {
        metrics: localMetricsData?.metrics || [],
        plot_groups: localMetricsData?.plot_groups || {}
    };
}
```

---

## Rule D.3: Never Crash on Hydration

> Hydration failures MUST NOT cause the entire app to crash.
> Log error, use fallback, continue execution.

---

## Affected Services

| Service | Required Fix |
|---------|--------------|
| MetricRegistryService | Add null check in `initialize()` |
| EquationRegistry | Verify `register()` validates input |
| SimCoreV4 | Ensure `init()` handles preset not found |

---

**Layer:** D — Flow Engine  
**Cross-refs:** [flow_control.md](./flow_control.md), [event_bus.md](./event_bus.md)
