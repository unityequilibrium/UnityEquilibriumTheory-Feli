# UET v5.0 — Oracle Infrastructure Standard

## 1. Vision: Verifiable Real-World Data

UET's economic model requires verification of real-world data (energy, land, assets) to maintain asset backing. Oracle infrastructure provides decentralized, reputation-based verification of this data.

---

## 2. Oracle Principles

### 2.1 Decentralization
- Multiple oracles for each data type
- No single point of failure
- Reputation-based selection

### 2.2 Reliability
- Reputation tracking for accuracy
- Automatic failover to alternative oracles
- Status management (Active, Inactive, Maintenance, Compromised)

### 2.3 Security
- Cryptographic signature verification
- Reputation decay for incorrect reports
- Compromised oracle detection

### 2.4 Efficiency
- Low-latency verification (<1 hour target)
- Batch verification support
- Caching for frequently accessed data

---

## 3. Oracle Architecture

### 3.1 Components

| Component | Description |
|-----------|-------------|
| `OracleRegistry` | Manages all oracles and their status |
| `EnergyVerifier` | Verifies electricity consumption |
| `LandVerifier` | Verifies land registry |
| `AssetVerifier` | Verifies asset holdings |
| `ReputationScore` | Tracks oracle accuracy |

### 3.2 Oracle Lifecycle

```
Register → Active → Inactive/Maintenance/Compromised
              ↓
         Reputation Tracking
              ↓
         Status Updates
```

### 3.3 Reputation System

| Metric | Description |
|--------|-------------|
| Score | 0.0 to 1.0 (percentage of correct reports) |
| Total Reports | Number of verification attempts |
| Correct Reports | Number of successful verifications |
| Threshold | Minimum score required (default: 0.8) |

---

## 4. Oracle Types

### 4.1 Energy Oracle

**Purpose**: Verify electricity consumption by nodes

**Request**:
```json
{
  "node_id": "uuid",
  "period_start": "2026-01-01T00:00:00Z",
  "period_end": "2026-01-02T00:00:00Z",
  "expected_kwh": 1000.0
}
```

**Response**:
```json
{
  "verified": true,
  "actual_kwh": 1050.0,
  "verification_timestamp": "2026-01-02T01:00:00Z",
  "oracle_id": "uuid",
  "signature": "hex"
}
```

**Data Sources**:
- Utility APIs
- Smart meter data
- Grid operator data

### 4.2 Land Oracle

**Purpose**: Verify land registry and ownership

**Request**:
```json
{
  "land_id": "LAND-001",
  "jurisdiction": "US-CA",
  "owner_id": "OWNER-001"
}
```

**Response**:
```json
{
  "verified": true,
  "land_area_sqm": 10000.0,
  "owner_verified": true,
  "verification_timestamp": "2026-01-02T01:00:00Z",
  "oracle_id": "uuid",
  "signature": "hex"
}
```

**Data Sources**:
- Government land registries
- Property databases
- Legal documents

### 4.3 Asset Oracle

**Purpose**: Verify asset holdings (Bitcoin, Gold, Patents)

**Request**:
```json
{
  "asset_type": "bitcoin",
  "asset_id": "btc-address",
  "expected_amount": 10.0
}
```

**Response**:
```json
{
  "verified": true,
  "actual_amount": 10.5,
  "verification_timestamp": "2026-01-02T01:00:00Z",
  "oracle_id": "uuid",
  "signature": "hex"
}
```

**Data Sources**:
- Blockchain explorers
- Commodity markets
- Patent databases

---

## 5. Verification Process

### 5.1 Multi-Oracle Consensus

1. **Select Oracles**: Get all active and reputable oracles for the type
2. **Try Each Oracle**: Attempt verification with each oracle
3. **Update Reputation**: Track success/failure for each oracle
4. **Return Result**: Return first successful response

### 5.2 Reputation Update

```rust
// Correct report
reputation.calculate(true);

// Incorrect report
reputation.calculate(false);
```

### 5.3 Status Management

| Status | Trigger | Action |
|-------|---------|--------|
| Active | Score >= threshold | Oracle available for verification |
| Inactive | Score < threshold | Oracle unavailable |
| Maintenance | Manual | Oracle under maintenance |
| Compromised | Manual detection | Oracle disabled |

---

## 6. Security Mechanisms

### 6.1 Signature Verification

All oracle responses must be cryptographically signed:
- Signature verification using `uet_security`
- Reject unsigned responses
- Reject invalid signatures

### 6.2 Reputation Decay

- Incorrect reports decrease reputation
- Reputation below threshold = inactive
- Reputation recovery requires time

### 6.3 Compromised Oracle Detection

- Manual flagging by governance
- Automatic detection (anomaly detection)
- Immediate status update to Compromised

---

## 7. Integration with UET Stack

### 7.1 Governance Integration

- Oracle configuration updates via governance proposals
- Emergency disable via governance veto
- Reputation threshold adjustments

### 7.2 Security Integration

- Signature verification using `uet_security`
- Oracle identity verification
- Response integrity checks

### 7.3 Ledger Integration

- Verification results recorded on `uet_chain`
- Reputation changes recorded on ledger
- Status changes recorded on ledger

---

## 8. Implementation Strategy

### Phase 1: Foundation (Month 1)
- [x] Create `uet_oracle` crate
- [x] Implement oracle registry
- [x] Implement reputation system
- [x] Implement energy/land/asset verifiers
- [ ] Add signature verification
- [ ] Create oracle dashboard

### Phase 2: Integration (Month 2)
- [ ] Connect to `uet_governance`
- [ ] Connect to `uet_security`
- [ ] Connect to `uet_chain`
- [ ] Implement oracle API
- [ ] Add oracle CLI

### Phase 3: Deployment (Month 3)
- [ ] Deploy to testnet
- [ ] Onboard energy oracles
- [ ] Onboard land oracles
- [ ] Onboard asset oracles
- [ ] Security audit
- [ ] Deploy to mainnet

---

## 9. Risk Mitigation

### 9.1 Oracle Failure Risks

| Risk | Mitigation |
|------|------------|
| Oracle Unavailable | Multi-oracle failover |
| Oracle Compromised | Reputation system, manual disable |
| Oracle Manipulation | Signature verification, reputation decay |
| Oracle Collusion | Multi-oracle consensus, reputation tracking |

### 9.2 Data Accuracy Risks

| Risk | Mitigation |
|------|------------|
| Incorrect Data | Reputation tracking, verification |
| Stale Data | Timestamp verification, freshness checks |
| Inconsistent Data | Multi-oracle consensus, outlier detection |

---

## 10. Success Metrics

- **Oracle Availability**: >95% uptime
- **Verification Accuracy**: >99% accuracy
- **Verification Latency**: <1 hour average
- **Reputation Score**: >0.8 for active oracles
- **Oracle Diversity**: >3 oracles per type

---

> [!NOTE]
> This spec defines the oracle infrastructure for UET. Implementation details are in the `uet_oracle` crate.
