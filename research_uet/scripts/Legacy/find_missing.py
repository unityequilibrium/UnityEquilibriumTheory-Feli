from pathlib import Path
import os

root = Path(r"c:\Users\santa\Desktop\lad\Lab_uet_harness_v0.8.7\research_uet\topics")
for p in root.rglob("*.py"):
    if (
        "Cosmological_Constant" in p.name
        or "Oscillation_4D" in p.name
        or "Quantum_Mechanics" in p.name
    ):
        print(p)
