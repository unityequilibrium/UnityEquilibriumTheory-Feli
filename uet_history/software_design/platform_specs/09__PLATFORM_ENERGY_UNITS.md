# UET v5.0 — Platform Energy & Service Units (AEU)

## 1. Overview
While UET Coins are global assets, **Axiomatic Energy Units (AEU)** (formerly Credits) are internal platform tokens used specifically to quantify and pay for **Service Intensity**.

## 2. AEUs vs UET Coins
- **UET Coin**: Value storage, asset-backed, tradeable on the global market.
- **AEU**: Internal "Fuel" for the platform. Non-tradeable outside, but exchangeable for Coin at the **Thermodynamic Exchange Rate (TXR)**.

## 3. The Mining-Service Link
Since platform usage *is* mining, every AEU "burned" for service (e.g., a Claude 3.5 query) triggers a corresponding **PoUW Calculation** in the backend. 
- **Effect**: Using services generates global knowledge, which fuels the coin backing.

## 4. MCP & API Services
- **External Tools**: Connecting an MCP server (e.g., `firecrawl`) costs AEUs based on the external API complexity.
- **Resource Weight**:
  - **L0 (Basic API)**: 1 AEU / call.
  - **L1 (Deep Research)**: 50 AEUs / call.
  - **L2 (Extreme Simulation)**: 500 AEUs / call.

## 5. The "Free Service" Threshold
Every citizen's 50% Dividend (from the Economic Constitution) provides a **Monthly Base AEU Allowance**. 
- **Goal**: No human should ever be "Offline" or "Knowledge-Poor" if they contribute responsibly to the system.

## 6. Transaction Tracking
- **Intent**: `SERVICE_REQUEST`
- **Gate**: Flow Control checks AEU balance or Dividend eligibility.
- **Burn**: AEU deducted.
- **Work**: `uet_core` executes post-process mining to verify the economic cycle.
