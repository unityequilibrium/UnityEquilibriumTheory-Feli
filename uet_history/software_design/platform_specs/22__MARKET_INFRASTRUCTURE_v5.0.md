# UET v5.0 — Market Infrastructure Standard

## 1. Vision: Decentralized Trading

UET Market provides decentralized trading infrastructure for UET Coin, enabling liquidity provision and price discovery without centralized exchanges.

---

## 2. Market Principles

### 2.1 Automated Market Making
- Constant product formula for price determination
- No order books required
- Always liquid (if reserves exist)

### 2.2 Liquidity Provision
- Users provide liquidity to pools
- Receive LP tokens representing share
- Earn trading fees proportional to share

### 2.3 Price Discovery
- Spot price from pool reserves
- TWAP for smooth price tracking
- 24h metrics for market analysis

---

## 3. Market Architecture

### 3.1 Components

| Component | Description |
|-----------|-------------|
| `AMM` | Automated market maker with constant product formula |
| `LiquidityPool` | Pool with base/quote reserves and LP tokens |
| `PriceDiscoveryEngine` | Price tracking and metrics |
| `MarketEngine` | High-level market operations |

### 3.2 Trading Flow

```
User → MarketEngine → AMM → LiquidityPool → TradeResult
                      ↓
                PriceDiscoveryEngine
```

---

## 4. AMM Formula

### 4.1 Constant Product Formula

```
x * y = k

output = (input * reserve_out) / (reserve_in + input)
```

Where:
- `x`: Base reserve (e.g., UET)
- `y`: Quote reserve (e.g., USD)
- `k`: Constant product
- `input`: Amount to swap
- `output`: Amount received

### 4.2 Example

| Input | Reserve In | Reserve Out | Output |
|-------|------------|-------------|--------|
| 100 UET | 10,000 UET | 50,000 USD | ~494 USD |

---

## 5. Liquidity Pools

### 5.1 Pool Structure

```rust
LiquidityPool {
    base_reserve: Decimal,      // e.g., 10,000 UET
    quote_reserve: Decimal,     // e.g., 50,000 USD
    lp_token_supply: Decimal,   // e.g., 10,000 LP tokens
    fee_rate: Decimal,          // e.g., 0.003 (0.3%)
}
```

### 5.2 Spot Price

```
spot_price = quote_reserve / base_reserve
```

Example: 50,000 USD / 10,000 UET = 5 USD/UET

### 5.3 Liquidity Depth

```
liquidity_depth = base_reserve * spot_price
```

Example: 10,000 UET * 5 USD/UET = 50,000 USD

---

## 6. Price Discovery

### 6.1 Metrics

| Metric | Description | Calculation |
|--------|-------------|-------------|
| Spot Price | Current market price | quote_reserve / base_reserve |
| TWAP Price | Time-weighted average | Σ(price * weight) / Σ(weight) |
| Volume 24h | Trading volume | Σ(trade_amount) over 24h |
| High 24h | Highest price | max(price) over 24h |
| Low 24h | Lowest price | min(price) over 24h |

### 6.2 Price Update Flow

```
Trade executed → Update spot price → Update TWAP → Update 24h metrics
```

---

## 7. Slippage Protection

### 7.1 Price Impact

```
price_impact = input / (reserve_in + input)
```

Example: 100 / (10,000 + 100) = 0.0099 (~1%)

### 7.2 Minimum Output

```
min_output = output * (1 - slippage_tolerance)
```

Example: 494 USD * (1 - 0.01) = 489 USD (with 1% slippage)

### 7.3 Slippage Check

```
if output < min_output:
    reject trade
```

---

## 8. Fee Structure

### 8.1 Trading Fee

- **Default**: 0.3% (0.003)
- **Adjustable**: Via governance
- **Distribution**: LP token holders

### 8.2 Fee Calculation

```
fee = input_amount * fee_rate
```

Example: 100 UET * 0.003 = 0.3 UET fee

---

## 9. Integration with UET Stack

### 9.1 Governance Integration

- Fee rate adjustments via governance proposals
- Pool creation/removal via governance
- Emergency pause via governance veto

### 9.2 Ledger Integration

- All trades recorded on `uet_chain`
- LP token transfers recorded
- Pool creation/removal recorded

### 9.3 Economic Integration

- Spot price used for economic calculations
- Volume used for liquidity metrics
- High/low used for volatility analysis

---

## 10. Implementation Strategy

### Phase 1: Foundation (Month 1)
- [x] Create `uet_market` crate
- [x] Implement AMM with constant product formula
- [x] Implement liquidity pools
- [x] Implement price discovery
- [ ] Add market dashboard
- [ ] Create market CLI

### Phase 2: Integration (Month 2)
- [ ] Connect to `uet_governance`
- [ ] Connect to `uet_chain`
- [ ] Connect to `uet_economic`
- [ ] Implement market API
- [ ] Add governance handlers

### Phase 3: Deployment (Month 3)
- [ ] Deploy to testnet
- [ ] Seed initial liquidity
- [ ] Run market simulation
- [ ] Security audit
- [ ] Deploy to mainnet

---

## 11. Risk Mitigation

### 11.1 Market Risks

| Risk | Mitigation |
|------|------------|
| Impermanent Loss | Education, LP token incentives |
| Low Liquidity | Minimum reserve requirements |
| Price Manipulation | TWAP smoothing, 24h metrics |
| Front-running | Time-weighted execution |

### 11.2 Implementation Risks

| Risk | Mitigation |
|------|------------|
| Calculation Errors | Unit tests, formal verification |
| Integration Bugs | Integration tests, audits |
| Smart Contract Bugs | Audits, bug bounties |

---

## 12. Success Metrics

- **Liquidity Depth**: >1M UET Coin in pools
- **Trading Volume**: >100k UET Coin daily
- **Price Stability**: <5% daily volatility
- **Liquidity Providers**: >100 active LPs
- **Slippage**: <1% for typical trades

---

> [!NOTE]
> This spec defines the market infrastructure for UET. Implementation details are in the `uet_market` crate.
