# UET v5.0 — Task Portfolio and Rotation Policy

This policy defines how PoUW/PoE task families are introduced, monitored, rotated, or retired to reduce systemic risk from future mathematical shortcuts or exploit discoveries.

## 1. Why Portfolio Rotation Exists
- A single task family can become vulnerable if a shortcut is discovered.
- Portfolio rotation prevents one mathematical break from collapsing issuance security.

## 2. Task Lifecycle
1. Proposal
2. Testnet activation
3. Adversarial benchmark
4. Mainnet activation
5. Continuous telemetry monitoring
6. Deprecation or retirement

## 3. Minimum Entry Criteria
- Deterministic input/output behavior.
- Verification cost significantly lower than proving cost.
- Clear anti-replay and anti-result-theft semantics.
- Reference verifier implementation and test vectors.

## 4. Runtime Portfolio Rules
- Maintain at least two active task families where practical.
- Apply epoch-based weighting to tune issuance distribution.
- Cap concentration: no single family should dominate issuance beyond policy threshold.

## 5. Emergency Response
- If exploit likelihood is high, governance can mark family as `restricted`.
- Restricted families become verify-only and ineligible for new reward issuance.
- Full retirement requires migration epoch and public incident report.

## 6. Fraud Proof and Slashing Hook
- If accepted proof is later shown invalid, challenger submits fraud proof.
- On successful challenge:
  - reward rollback policy applies
  - malicious producer penalties apply per governance rules

## 7. Governance and Transparency
- Every state transition of a task family is logged.
- Each release must publish changelog of enabled/disabled families.
- Changes must reference benchmark and audit artifacts.
