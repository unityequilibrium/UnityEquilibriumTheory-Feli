# UET v5.0 — Economic Policy Standard

## 1. Vision: Adaptive Economic Policy

UET's economic policy is adaptive and data-driven, automatically adjusting difficulty, issuance, and portfolio to maintain stability and prevent inflation.

---

## 2. Economic Principles

### 2.1 Adaptive Difficulty
- Difficulty adjusts based on work unit completion rates
- Target completion rate: 80%
- Prevents both too-easy and too-hard tasks

### 2.2 Energy-Backed Issuance
- Issuance proportional to energy input
- Clamped to prevent hyperinflation/deflation
- Ensures currency backing

### 2.3 Portfolio Diversity
- No single task family dominates (>50% concentration)
- Automatic rotation based on performance
- Prevents inflation from compromised families

---

## 3. Economic Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `target_completion_rate` | 0.8 | 0.5-0.9 | Target work unit completion rate |
| `difficulty_sensitivity` | 0.1 | 0.05-0.2 | Difficulty adjustment sensitivity |
| `max_difficulty_multiplier` | 10.0 | 5.0-20.0 | Maximum difficulty multiplier |
| `min_difficulty_multiplier` | 0.1 | 0.05-0.5 | Minimum difficulty multiplier |
| `epoch_duration_hours` | 24 | 12-168 | Epoch duration in hours |
| `max_issuance_per_epoch` | 1,000,000 | 100k-10M | Maximum issuance per epoch |
| `min_issuance_per_epoch` | 100,000 | 10k-1M | Minimum issuance per epoch |
| `max_task_family_concentration` | 0.5 | 0.3-0.7 | Maximum task family concentration |
| `min_task_family_weight` | 0.05 | 0.01-0.1 | Minimum task family weight |
| `max_task_family_weight` | 0.5 | 0.3-0.7 | Maximum task family weight |

---

## 4. Difficulty Adjustment

### 4.1 Algorithm

```
if completion_rate > target:
    new_difficulty = current * (1 + sensitivity * (completion_rate - target))
elif completion_rate < target:
    new_difficulty = current * (1 - sensitivity * (target - completion_rate))
else:
    new_difficulty = current
```

### 4.2 Clamping

- **Minimum**: `min_difficulty_multiplier`
- **Maximum**: `max_difficulty_multiplier`

### 4.3 Example

| Completion Rate | Target | Adjustment | Old Difficulty | New Difficulty |
|----------------|--------|------------|----------------|----------------|
| 90% | 80% | +10% | 1.0 | 1.1 |
| 60% | 80% | -20% | 1.0 | 0.8 |
| 80% | 80% | 0% | 1.0 | 1.0 |

---

## 5. Issuance Budget

### 5.1 Algorithm

```
issuance_per_kwh = max_issuance / 1,000,000
calculated_issuance = energy_input_kwh * issuance_per_kwh
clamped_issuance = clamp(calculated, min_issuance, max_issuance)
```

### 5.2 Energy-Based Calculation

- More energy = more issuance (up to max)
- Less energy = less issuance (down to min)
- Ensures currency backing

### 5.3 Example

| Energy Input (kWh) | Calculated Issuance | Clamped Issuance |
|---------------------|---------------------|------------------|
| 100,000 | 100,000 | 100,000 (min) |
| 500,000 | 500,000 | 500,000 |
| 2,000,000 | 2,000,000 | 1,000,000 (max) |

---

## 6. Portfolio Rotation

### 6.1 Addition Criteria

- Portfolio not full (<95% total weight)
- Family not already in portfolio
- Governance approval required

### 6.2 Removal Criteria

- Completion rate <10% (too hard)
- Weight >max_task_family_weight (concentration)

### 6.3 Weight Adjustment

| Completion Rate | Action |
|------------------|--------|
| >90% | Decrease weight (too easy) |
| <50% | Decrease weight (too hard) |
| 50-90% | Maintain weight |

### 6.4 Concentration Limits

- No single family >50% weight
- Total portfolio weight = 1.0

---

## 7. Integration with UET Stack

### 7.1 Governance Integration

- Economic parameters adjustable via governance proposals
- Difficulty adjustments executed via governance
- Portfolio rotation executed via governance

### 7.2 Oracle Integration

- Energy input verified by energy oracles
- Issuance budget calculated after verification
- Prevents fake energy claims

### 7.3 Ledger Integration

- Economic policy changes recorded on `uet_chain`
- Difficulty adjustments recorded on ledger
- Issuance budgets recorded on ledger

---

## 8. Implementation Strategy

### Phase 1: Foundation (Month 1)
- [x] Create `uet_economic` crate
- [x] Implement difficulty adjustment engine
- [x] Implement issuance budget engine
- [x] Implement portfolio rotation engine
- [ ] Add economic dashboard
- [ ] Create economic CLI

### Phase 2: Integration (Month 2)
- [ ] Connect to `uet_governance`
- [ ] Connect to `uet_oracle`
- [ ] Connect to `uet_chain`
- [ ] Implement economic API
- [ ] Add governance handlers

### Phase 3: Deployment (Month 3)
- [ ] Deploy to testnet
- [ ] Run economic simulation
- [ ] Tune parameters
- [ ] Security audit
- [ ] Deploy to mainnet

---

## 9. Risk Mitigation

### 9.1 Economic Risks

| Risk | Mitigation |
|------|------------|
| Hyperinflation | Issuance clamping, concentration limits |
| Deflation | Minimum issuance floor, state reserves |
| Difficulty Oscillation | Sensitivity tuning, clamping |
| Portfolio Collapse | Minimum weight limits, emergency disable |

### 9.2 Implementation Risks

| Risk | Mitigation |
|------|------------|
| Parameter Misconfiguration | Governance approval, simulation |
| Calculation Errors | Unit tests, formal verification |
| Integration Bugs | Integration tests, audits |

---

## 10. Success Metrics

- **Difficulty Stability**: <20% change per epoch
- **Issuance Stability**: Within ±10% of target
- **Portfolio Diversity**: >3 active families
- **Completion Rate**: 70-90% target met
- **Economic Participation**: >100 nodes mining

---

> [!NOTE]
> This spec defines the economic policy for UET. Implementation details are in the `uet_economic` crate.
