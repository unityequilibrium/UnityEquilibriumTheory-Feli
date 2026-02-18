# UET v5.0 — Quantum-Resistant Security Standard

This standard defines cryptographic policy for UET nodes, ledger objects, and inter-node transport with crypto-agility for future algorithm migration.

## 1. Security Objectives
- Resist quantum-era attacks on signatures and key exchange.
- Prevent harvest-now-decrypt-later exposure for long-lived traffic.
- Support safe migration when cryptographic assumptions change.

## 2. Signature Policy
### 2.1 Primary Profile
- Primary: Dilithium-class PQ signatures for block/tx/proof signing.

### 2.2 Conservative Profile (Optional)
- Dual-sign for critical transitions (e.g., Dilithium + SPHINCS+).

### 2.3 Identity Binding
All signed artifacts must include:
- `schema_version`
- `sig_alg`
- `hash_alg`
- `key_id`

## 3. Hashing Policy
- Preferred hash functions: SHA3 family or BLAKE3.
- Use 256-bit digests as baseline; 512-bit profiles for long-retention commitments.

## 4. Transport Security Policy
- Node-to-node sessions should use hybrid KEX (classical + PQ KEM) when available.
- mTLS or equivalent authenticated channel is required for external node APIs.
- Stdio MCP is trusted only for local process boundaries.

## 5. Key Management
- Keys must support rotation and revocation metadata.
- Minimum metadata:
  - `key_id`
  - algorithm
  - activation time
  - retirement time
- Compromised key response:
  1. revoke key
  2. rotate signer set
  3. publish incident log

## 6. Crypto-Agility Controls
- Algorithm allowlist is policy-driven and versioned.
- Deprecated algorithms can remain verify-only for a grace period.
- Emergency rotation policy must include quorum requirements and audit trail.

## 7. Security Monitoring and Audit
- Signature failures and replay attempts are security events.
- Verification failures above threshold trigger `SECURITY_VIOLATION` event.
- All algorithm/profile changes require governance record and timestamp.

## 8. Implementation Mapping
- `uet_security` provides algorithm enums, hashing adapters, and signing envelope primitives.
- `uet_chain` persists suite metadata in all ledger-critical structures.
