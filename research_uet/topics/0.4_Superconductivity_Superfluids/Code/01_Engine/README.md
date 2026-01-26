# Engine 01 (Topic 0.4)

## Why is this folder empty?
Topic 0.4 (Superconductivity) does not require a specialized physics engine (like Galaxy or Cosmology).

It relies directly on the **[Core UET Engine]** (`research_uet/core/uet_master_equation.py`).
The logic for calculation is lightweight enough to reside directly in `03_Research` scripts.

## Engine Reference
*   **Core:** `research_uet.core.uet_master_equation`
*   **Functions Used:** `calculate_value`, `calculate_entropy`
