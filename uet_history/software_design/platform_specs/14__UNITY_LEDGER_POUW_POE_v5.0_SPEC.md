# UET v5.0 — Unity Ledger PoUW/PoE Specification

This document defines the canonical ledger model for Proof of Useful Work (PoUW) and Proof of Equilibrium (PoE), including task formats, proof objects, commit rules, and anti-cheat controls.

## 1. Scope and Goals
- Define a machine-verifiable consensus payload for useful computation.
- Ensure verification is cheaper than proving.
- Provide crypto-agile and quantum-resistant metadata on all signed objects.

## 2. Work Model
### 2.1 Task Families
- `deterministic_simulation`: fixed-seed simulation with deterministic output.
- `optimization_bounded`: optimization proof with verifiable bound/certificate.
- `equilibrium_certificate`: UET equilibrium proof with compact verification artifact.

### 2.2 Task Object (Canonical)
Required fields:
- `task_id`
- `family`
- `input_seed`
- `difficulty`
- `created_at`

## 3. Proof Object (Canonical)
Required fields:
- `task_id`
- `node_id`
- `result_hash_hex`
- `verification_artifact` (kind/hash/verifier_hint)
- `runtime_ms`
- `nonce`
- `suite` (`schema_version`, `sig_alg`, `hash_alg`, `key_id`)
- `signature_hex`

## 4. Block Commit Rules
- Transactions and work proofs are hashed with canonical serialization.
- Merkle roots:
  - `tx_merkle_root_hex`
  - `proof_root_hex`
- Header includes `state_root_hex` and proposer signature.
- A block is valid only if:
  1. Header signature is valid.
  2. All included proofs pass verification policy.
  3. Merkle roots match body content.

## 5. Anti-Cheat Controls
- Replay protection: `task_id + node_id + nonce` uniqueness.
- Anti-precompute (optional): commit/reveal epochs with beacon randomness.
- Result stealing resistance: proof signature bound to `node_id` and `key_id`.
- Fraud proofs: invalid accepted proof can be challenged within policy window.

## 6. Economic Linkage
- Rewarding policy is defined by `12__MATHNICRY_ECONOMIC_CONSTITUTION.md`.
- This spec defines *technical validity*; economics defines *issuance weighting*.

## 7. Governance and Upgrades
- Schema is versioned by `schema_version`.
- New task family onboarding flow:
  1. Testnet trial
  2. Benchmark + adversarial audit
  3. Mainnet activation epoch
- Emergency disable path must be audited and logged.

## 8. Reference Implementation Mapping
- Rust crate `uet_chain`: task/proof/tx/block data model and canonical hashing.
- Rust crate `uet_security`: signature/hash suite, envelope, key identity primitives.
