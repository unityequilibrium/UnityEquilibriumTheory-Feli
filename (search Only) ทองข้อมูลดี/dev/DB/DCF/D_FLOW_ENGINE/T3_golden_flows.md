# T3 Golden Flow Test Specifications
## UET Platform - End-to-End Test Flows

**Last Updated:** 2024-12-25  
**Purpose:** Document critical E2E test flows for PTE

---

## Overview

| Flow | Name | Priority | Automation |
|------|------|----------|------------|
| F1 | Gallery→Lab→Save→Reopen | Critical | Manual/Playwright |
| F2 | Lab→Validate→TestGate→Replay | Critical | Manual/Playwright |
| F3 | Notes Create→Persist | High | Manual/Playwright |

---

## F1: Gallery→Lab→Save→Reopen

### Steps

| Step | Action | Expected | Verify |
|------|--------|----------|--------|
| 1.1 | Navigate to /gallery | Gallery page loads | URL = /gallery |
| 1.2 | Click "Solar System" card | ⚠️ Navigates to /lab?room=solarSystem | URL check |
| 1.3 | Wait for simulation | Canvas renders particles | Particle count > 0 |
| 1.4 | Click Play | Simulation runs | time > 0 |
| 1.5 | Click "Save to Gallery" | Save dialog/toast | runId returned |
| 1.6 | Navigate to /gallery | Gallery loads | ✅ |
| 1.7 | Click saved run | ⚠️ Opens in /lab?runId=X | Replay mode |
| 1.8 | Verify replay | Data matches | telemetry restored |

### Pass Criteria
- All 8 steps complete without error
- runId persists in DB
- Telemetry data is restorable

---

## F2: Lab→Validate→TestGate→Replay

### Steps

| Step | Action | Expected | Verify |
|------|--------|----------|--------|
| 2.1 | Navigate to /lab?room=testGates | Test Gates room loads | Room = testGates |
| 2.2 | Select test scenario | Test UI shows | Scenario loaded |
| 2.3 | Click Run Test | Test executes | Status update |
| 2.4 | Wait for completion | Result: PASS/FAIL/WARN | Grade shown |
| 2.5 | Click Save Counterexample | ⚠️ Saves to DB | runId returned |
| 2.6 | Reload page | ⚠️ Replay loads | telemetry shown |

### Pass Criteria
- Test executes deterministically
- Grade matches expected
- Replay shows same data

---

## F3: Notes Create→Persist

### Steps

| Step | Action | Expected | Verify |
|------|--------|----------|--------|
| 3.1 | Navigate to /lab | Lab loads | ✅ |
| 3.2 | Open Notes tab | Notes panel visible | Tab open |
| 3.3 | Type "Test note" | Text entered | Input value |
| 3.4 | Click Save | ⚠️ Note persists | API call success |
| 3.5 | Refresh page | Page reloads | ✅ |
| 3.6 | Open Notes tab | Previous note shown | Text matches |

### Pass Criteria
- Note text persists across refresh
- API /runs/:id/notes works
- No data loss

---

## Automation Spec (Playwright)

```typescript
// F1 Example
test('F1: Gallery→Lab→Save→Reopen', async ({ page }) => {
  await page.goto('/gallery');
  await page.click('[data-card-id="solarSystem"]');
  await expect(page).toHaveURL(/\/lab\?room=solarSystem/);
  
  await page.waitForSelector('[data-testid="particle-canvas"]');
  await page.click('[data-action-id="sim_play"]');
  
  await page.click('[data-action-id="output_save_gallery"]');
  const runId = await page.textContent('[data-testid="run-id"]');
  
  await page.goto('/gallery');
  await page.click(`[data-run-id="${runId}"]`);
  await expect(page).toHaveURL(/\/lab\?runId=/);
});
```

---

## Test Environment

| Requirement | Value |
|-------------|-------|
| Base URL | http://localhost:3000 |
| Database | PostgreSQL (test instance) |
| Seed | Fixed seed for determinism |
| Timeout | 30s per flow |

---

## Status

| Flow | Manual | Automated |
|------|--------|-----------|
| F1 | ⚠️ Pending | ❌ Not yet |
| F2 | ⚠️ Pending | ❌ Not yet |
| F3 | ⚠️ Pending | ❌ Not yet |

---

**Traceable To:** 
- D_FLOW_ENGINE/test_gate_logic.md
- E_DATABASE/persistence_policy.md
- B_FRONTEND/action_map.md
