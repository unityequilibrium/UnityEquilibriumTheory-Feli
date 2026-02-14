# Runner Logic
## Layer D — Simulation Runner

---

## ⚡ SimCoreV4 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       SimCoreV4                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│   │    init()    │───▶│    run()     │───▶│   step()     │  │
│   │ Setup state  │    │ Start loop   │    │ Single tick  │  │
│   └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│   │   pause()    │    │   reset()    │    │  destroy()   │  │
│   │ Stop loop    │    │ Restore init │    │ Cleanup      │  │
│   └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Step Function Logic

```typescript
function step() {
  // 1. Get active equations
  const equations = getActiveEquations();
  
  // 2. Calculate forces
  for (each particle) {
    let force = { x: 0, y: 0, z: 0 };
    for (each equation) {
      force += equation.calculateForce(particle);
    }
  }
  
  // 3. Integrate (Verlet)
  for (each particle) {
    particle.velocity += force * dt;
    particle.position += particle.velocity * dt;
  }
  
  // 4. Update telemetry
  updateTelemetry();
  
  // 5. Increment step
  worldState.step += 1;
  worldState.time += dt;
}
```

---

## 🎮 Run Loop

```typescript
function run() {
  status = 'running';
  
  animationFrame = requestAnimationFrame(loop);
  
  function loop() {
    step();
    
    if (status === 'running') {
      animationFrame = requestAnimationFrame(loop);
    }
  }
}
```

---

**Source:** `lib/SimCoreV4.ts`  
**Layer:** D — Flow/Engine Logic
