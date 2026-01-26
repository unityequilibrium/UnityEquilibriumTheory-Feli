import os
import shutil

TOPICS_DIR = r"C:\Users\santa\Desktop\lad\Lab_uet_harness_v0.8.7\research_uet\topics"

print("↺ Reverting 'section 1' back to 'baseline' (Emergency Undo)...")

for topic in os.listdir(TOPICS_DIR):
    t_path = os.path.join(TOPICS_DIR, topic)
    if not os.path.isdir(t_path):
        continue

    code_dir = os.path.join(t_path, "Code")
    baseline = os.path.join(code_dir, "baseline")
    section1 = os.path.join(code_dir, "section 1")

    # Check if we recently renamed it (section 1 exists, baseline missing)
    if os.path.exists(section1) and not os.path.exists(baseline):
        try:
            shutil.move(section1, baseline)
            print(f"↺ Reverted 'section 1' -> 'baseline' in {topic}")
        except Exception as e:
            print(f"❌ Error reverting {topic}: {e}")

print("🏁 Revert Complete.")
