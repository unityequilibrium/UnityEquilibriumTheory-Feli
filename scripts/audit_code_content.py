import os

TOPICS_DIR = r"C:\Users\santa\Desktop\lad\Lab_uet_harness_v0.8.7\research_uet\topics"

print(f"{'Topic':<35} | {'Folder':<15} | {'Verdict':<20} | {'Evidence'}")
print("-" * 100)

for topic in sorted(os.listdir(TOPICS_DIR)):
    t_path = os.path.join(TOPICS_DIR, topic)
    if not os.path.isdir(t_path):
        continue

    code_root = os.path.join(t_path, "Code")
    if not os.path.exists(code_root):
        continue

    # Check baseline subfolder specifically
    baseline_path = os.path.join(code_root, "baseline")
    if os.path.exists(baseline_path):
        sub = "baseline"
        py_files = [f for f in os.listdir(baseline_path) if f.endswith(".py")]

        verdict = "UNKNOWN"
        evidence = ""

        if not py_files:
            verdict = "EMPTY"
        else:
            first_file = py_files[0]
            try:
                with open(
                    os.path.join(baseline_path, first_file), "r", encoding="utf-8"
                ) as f:
                    content = f.read()
                    if "UETMasterEquation" in content or "UETBaseSolver" in content:
                        verdict = "RESEARCH (UET)"
                        evidence = "Uses UET Engine"
                    elif (
                        "Standard Model" in content
                        or "LCDM" in content
                        or "classic" in content.lower()
                    ):
                        verdict = "BASELINE (REF)"
                        evidence = "Standard Physics terms"
                    else:
                        verdict = "AMBIGUOUS"
                        evidence = "No clear keywords"
            except:
                verdict = "ERROR"

        print(f"{topic[:35]:<35} | {sub:<15} | {verdict:<20} | {evidence}")
