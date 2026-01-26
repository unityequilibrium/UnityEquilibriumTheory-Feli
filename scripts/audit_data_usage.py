import os

TOPICS = [
    "0.15_Cluster_Dynamics",
    "0.2_Black_Hole_Physics",
    "0.3_Cosmology_Hubble_Tension",
    "0.5_Nuclear_Binding_Hadrons",
    "0.6_Electroweak_Physics",
    "0.7_Neutrino_Physics",
    "0.8_Muon_g2_Anomaly",
    "0.9_Quantum_Nonlocality",
]

BASE_DIR = r"C:\Users\santa\Desktop\lad\Lab_uet_harness_v0.8.7\research_uet\topics"

print(f"{'Topic':<35} | {'Real Baseline?':<15} | {'Data/Ref Status':<30}")
print("-" * 90)

for t in TOPICS:
    path = os.path.join(BASE_DIR, t, "Code", "baseline")
    if not os.path.exists(path):
        print(f"{t:<35} | {'MISSING':<15} | {'N/A':<30}")
        continue

    # Check for Standard Physics code (Real Baseline)
    has_std = False
    has_data = False
    ref_count = 0

    for f in os.listdir(path):
        if f.endswith(".py"):
            with open(os.path.join(path, f), "r", encoding="utf-8") as file:
                content = file.read()
                if "Standard Model" in content or "LCDM" in content:
                    has_std = True
                if "json.load" in content or "_load_data" in content:
                    has_data = True
                if "Ref:" in content or "DOI:" in content:
                    ref_count += 1

    baseline_status = "YES" if has_std else "NO (UET Only)"
    data_status = f"Data: {'YES' if has_data else 'NO'}, Refs: {ref_count}"

    print(f"{t[:35]:<35} | {baseline_status:<15} | {data_status:<30}")
