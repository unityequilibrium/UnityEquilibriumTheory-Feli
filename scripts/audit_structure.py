import os

topics = [
    "0.1_Galaxy_Rotation_Problem",
    "0.20_Atomic_Physics",
    "0.23_Condensed_Matter",
    "0.24_Black_Hole_Cosmology",
    "0.25_Unified_Theory_Of_Everything",
]

base = r"C:\Users\santa\Desktop\lad\Lab_uet_harness_v0.8.7\research_uet\topics"

for t in topics:
    path = os.path.join(base, t)
    print(f"\n--- {t} ---")
    if os.path.exists(path):
        # Walk just 3 levels deep
        for root, dirs, files in os.walk(path):
            level = root.replace(path, "").count(os.sep)
            if level > 3:
                continue
            indent = " " * 4 * (level)
            print(f"{indent}{os.path.basename(root)}/")
            for f in files:
                if f.endswith(".py") or f.endswith(".md") or f.endswith(".json"):
                    print(f"{indent}    {f}")
    else:
        print("    (Missing)")
