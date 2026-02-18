# UET v5.0 — Decentralized Governance Standard

## 1. Vision: Community-Driven Economic Policy

UET governance enables decentralized decision-making for economic policy changes, ensuring that the community controls the evolution of the economic system while maintaining security and stability.

---

## 2. Governance Principles

### 2.1 Transparency
- All proposals and votes are recorded on the blockchain
- Governance parameters are publicly visible
- Execution results are auditable

### 2.2 Inclusivity
- Multiple voting strategies (1-person-1-vote, token-weighted, node-weighted, quadratic)
- Minimum quorum requirements ensure broad participation
- No single entity can unilaterally change policy

### 2.3 Security
- Emergency veto power for critical situations
- Time lock periods prevent rushed changes
- Quorum and approval thresholds prevent manipulation

### 2.4 Efficiency
- Automated policy execution via handlers
- Deterministic verification of policy changes
- Fast finalization for urgent proposals

---

## 3. Governance Architecture

### 3.1 Components

| Component | Description |
|-----------|-------------|
| `VotingProtocol` | Calculates voting power and checks quorum/approval |
| `ProposalManager` | Manages proposal lifecycle (create, submit, vote, finalize) |
| `PolicyEngine` | Executes passed proposals via registered handlers |
| `GovernanceState` | Stores proposals, voters, and configuration |

### 3.2 Voting Power Strategies

| Strategy | Formula | Use Case |
|----------|---------|----------|
| One Person One Vote | 1 vote per voter | Democratic participation |
| Token Weighted | Proportional to token holdings | Stakeholder influence |
| Node Weighted | Proportional to work units | Contributor influence |
| Quadratic | sqrt(weight) | Anti-whale protection |
| Hybrid | Token weight × w1 + Node weight × w2 | Balanced approach |

### 3.3 Proposal Lifecycle

```
Draft → Voting → Passed/Failed → Executed
         ↓
     Cancelled (by proposer)
     Vetoed (by emergency authority)
```

---

## 4. Proposal Types

### 4.1 Economic Policy Proposals

| Type | Purpose | Handler |
|------|---------|---------|
| `DifficultyAdjustment` | Adjust difficulty for task families | `DifficultyAdjustmentHandler` |
| `IssuanceBudgetAdjustment` | Adjust epoch issuance budget | `IssuanceBudgetHandler` |
| `TaskFamilyAddition` | Add new task family to portfolio | `TaskFamilyAdditionHandler` |
| `TaskFamilyRemoval` | Remove task family from portfolio | `TaskFamilyRemovalHandler` |
| `TaskFamilyWeightAdjustment` | Adjust task family weights | `TaskFamilyWeightHandler` |
| `EmergencyDisable` | Disable compromised task family | `EmergencyDisableHandler` |

### 4.2 Infrastructure Proposals

| Type | Purpose | Handler |
|------|---------|---------|
| `OracleConfigUpdate` | Update oracle configuration | `OracleConfigHandler` |
| `GovernanceParameterUpdate` | Update governance parameters | `GovernanceParamHandler` |
| `MintingPolicyUpdate` | Update minting policies | `MintingPolicyHandler` |

---

## 5. Governance Configuration

### 5.1 Default Parameters

```toml
min_voting_period_hours = 24
max_voting_period_hours = 168  # 7 days
min_quorum_percentage = 30.0
min_approval_percentage = 60.0
time_lock_hours = 24
```

### 5.2 Quorum Requirements

- **Minimum**: 30% of total voting power must participate
- **Calculation**: (Voted Power / Total Power) × 100
- **Failure**: Proposal fails if quorum not met

### 5.3 Approval Thresholds

- **Minimum**: 60% of votes must be approve (excluding abstentions)
- **Calculation**: (Approve Power / (Approve + Reject Power)) × 100
- **Failure**: Proposal fails if approval not met

### 5.4 Time Lock

- **Purpose**: Prevent rushed changes
- **Duration**: 24 hours after proposal passes
- **Execution**: Policy executes after time lock expires

---

## 6. Security Mechanisms

### 6.1 Emergency Veto

- **Authority**: Designated emergency authority (can be null)
- **Power**: Can veto any proposal at any time
- **Use Case**: Critical security issues, bugs, exploits
- **Limitation**: Can be revoked via governance proposal

### 6.2 Proposal Cancellation

- **Who**: Only proposer can cancel
- **When**: Only in Draft status
- **Reason**: Mistake, duplicate, no longer needed

### 6.3 Voter Verification

- **Active Voters Only**: Only active voters can vote
- **Identity Verification**: Voter identity must be verified
- **One Vote Per Voter**: Each voter can only vote once per proposal

---

## 7. Integration with UET Stack

### 7.1 Ledger Integration

- **Proposal Recording**: All proposals recorded on `uet_chain`
- **Vote Recording**: All votes recorded on `uet_chain`
- **Execution Recording**: Execution results recorded on `uet_chain`

### 7.2 Security Integration

- **Proposal Signing**: Proposals signed by proposer's key
- **Vote Signing**: Votes signed by voter's key
- **Verification**: All signatures verified before acceptance

### 7.3 Oracle Integration

- **Policy Verification**: Oracle verification before policy execution
- **Asset Backing**: Energy/land/hard asset verification
- **Reputation System**: Oracle reputation tracking

---

## 8. Implementation Strategy

### Phase 1: Foundation (Month 1)
- [x] Create `uet_governance` crate
- [x] Implement voting protocol
- [x] Implement proposal lifecycle
- [x] Implement policy execution engine
- [ ] Add governance token model
- [ ] Create governance dashboard

### Phase 2: Integration (Month 2)
- [ ] Connect to `uet_chain` ledger
- [ ] Connect to `uet_security` signing
- [ ] Connect to `uet_oracle` verification
- [ ] Implement governance API
- [ ] Add governance CLI

### Phase 3: Deployment (Month 3)
- [ ] Deploy to testnet
- [ ] Bootstrap governance (initial voters, parameters)
- [ ] Run governance simulation
- [ ] Security audit
- [ ] Deploy to mainnet

---

## 9. Risk Mitigation

### 9.1 Governance Attack Risks

| Risk | Mitigation |
|------|------------|
| 51% Attack | Quadratic voting, delegation limits |
| Whale Manipulation | Quadratic voting, time lock |
| Voter Apathy | Minimum quorum, incentives |
| Emergency Abuse | Veto revocation, transparency |

### 9.2 Policy Execution Risks

| Risk | Mitigation |
|------|------------|
| Bug in Handler | Formal verification, audits |
| Incorrect Parameters | Validation, dry-run mode |
| Execution Failure | Rollback mechanism, error handling |

---

## 10. Success Metrics

- **Governance Participation**: >30% of token holders vote
- **Proposal Success Rate**: >70% of proposals pass
- **Execution Success Rate**: >95% of proposals execute successfully
- **Time to Execution**: <48 hours from proposal to execution
- **Voter Satisfaction**: >80% satisfaction rate

---

> [!NOTE]
> This spec defines the governance system for UET. Implementation details are in the `uet_governance` crate.
