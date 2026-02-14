# Determinism Rules
## Layer D — Reproducibility Contract

**Last Updated:** 2024-12-24  
**Layer:** D (Flow/Engine)  
**Status:** 🔒 LOCKED

---

## 🎯 Core Guarantee

> **Same input + Same seed = Same output**  
> ทุกครั้ง ไม่มีข้อยกเว้น

---

## 🌱 Seed Management

### R1: Seed Generation

```typescript
// Generate on run creation
function generateSeed(): number {
  return Math.floor(Math.random() * 2147483647);
}

// Use seeded RNG everywhere
class SeededRandom {
  private seed: number;
  
  constructor(seed: number) {
    this.seed = seed;
  }
  
  next(): number {
    this.seed = (this.seed * 16807) % 2147483647;
    return this.seed / 2147483647;
  }
}
```

### R2: Seed Persistence

| Event | Action |
|-------|--------|
| Create run | Generate seed, store in state |
| Save run | Save seed to DB (runs.seed) |
| Load run | Restore seed from DB |
| Replay | Use original seed |

### R3: Seed Usage

```typescript
// ❌ FORBIDDEN
const random = Math.random();  // Non-deterministic!
const time = Date.now();        // Non-deterministic!

// ✅ REQUIRED
const rng = new SeededRandom(run.seed);
const random = rng.next();
```

---

## 🔒 Locked Rules

### D1: No Unseeded Random

```
❌ Math.random() without seed
❌ crypto.getRandomValues()
❌ Any external randomness
```

### D2: No Time-based Calculations

```
❌ Date.now() in physics
❌ performance.now() in physics
❌ requestAnimationFrame timing in calculations
```

### D3: No External Dependencies

```
❌ Network calls during simulation loop
❌ User input affecting physics calculations
❌ Environment-dependent values
```

### D4: No Order Dependencies

```
❌ Relying on object key iteration order
❌ Relying on array.sort() without comparator
❌ Parallel operations with race conditions
```

---

## 🔄 Replay Verification

### Required Data for Replay

| Data | Required | Purpose |
|------|----------|---------|
| seed | ✅ | RNG state |
| particles (t=0) | ✅ | Initial conditions |
| equations config | ✅ | Force calculations |
| dt | ✅ | Integration step |

### Verification Process

```
1. Load saved run
2. Initialize with original seed
3. Initialize with original particles
4. Run N steps
5. Compare final state with saved state
6. If match → Determinism verified
7. If no match → BUG DETECTED
```

### Tolerance

```typescript
const DETERMINISM_TOLERANCE = 1e-10;

function isMatch(actual: number, expected: number): boolean {
  return Math.abs(actual - expected) < DETERMINISM_TOLERANCE;
}
```

---

## 📋 Implementation Checklist

```
✅ SeededRandom class implemented
✅ Seed generated on run create
✅ Seed saved to DB (runs.seed BigInt)
✅ Seed loaded on restore
✅ InitialStateGenerator.galaxy() uses SeededRandom (2025-12-25)
⚠️ Replay verification (partial - run_gates.ts covers G0)
⚠️ GraphCompiler seed propagation (uses fallback, not graph seed)
□ Non-determinism detection implemented
□ CI gate for determinism
```

---

## ⚠️ Known Exceptions

| Exception | Reason | Mitigation |
|-----------|--------|------------|
| Frame timing | Display only | Don't use in calcs |
| User camera | UI only | Not saved |
| Panel states | UI only | Not saved |

---

**Layer:** D — Flow/Engine Logic  
**Status:** 🔒 Rules locked, partial implementation  
**Last Updated:** 2025-12-25

