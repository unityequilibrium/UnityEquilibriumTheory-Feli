from pathlib import Path

topics = [
    "0.9_Quantum_Nonlocality",
    "0.12_Vacuum_Energy_Casimir",
    "0.18_Neutrino_Mixing",
]
root = Path(r"c:\Users\santa\Desktop\lad\Lab_uet_harness_v0.9.0\research_uet\topics")

for topic in topics:
    print(f"--- {topic} ---")
    topic_path = root / topic
    if topic_path.exists():
        for p in topic_path.rglob("*.py"):
            print(p)
