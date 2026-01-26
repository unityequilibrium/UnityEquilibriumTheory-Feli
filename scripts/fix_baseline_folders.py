import os
import shutil

TOPICS_DIR = r"C:\Users\santa\Desktop\lad\Lab_uet_harness_v0.8.7\research_uet\topics"

print("🔍 Scanning for 'baseline' folders to rename...")

for topic in os.listdir(TOPICS_DIR):
    t_path = os.path.join(TOPICS_DIR, topic)
    if not os.path.isdir(t_path):
        continue

    code_dir = os.path.join(t_path, "Code")
    if not os.path.exists(code_dir):
        continue

    baseline = os.path.join(code_dir, "baseline")
    section1 = os.path.join(code_dir, "section 1")

    # CASE A: baseline exists
    if os.path.exists(baseline):
        # CASE B: section 1 also exists (Conflict)
        if os.path.exists(section1):
            print(f"⚠️ Conflict in {topic}: Both 'baseline' and 'section 1' exist.")
            # Move files from baseline to section 1
            for f in os.listdir(baseline):
                src = os.path.join(baseline, f)
                dst = os.path.join(section1, f)
                try:
                    if not os.path.exists(dst):
                        shutil.move(src, dst)
                        print(f"   Moved {f} -> section 1")
                except Exception as e:
                    print(f"   Error moving {f}: {e}")
            # Try to remove empty baseline
            try:
                os.rmdir(baseline)
                print(f"   ✅ Removed empty 'baseline' in {topic} (Merged)")
            except:
                print(f"   ⚠️ Could not remove 'baseline' in {topic} (Not empty?)")

        # CASE C: Only baseline exists (Simple Rename)
        else:
            try:
                shutil.move(baseline, section1)
                print(f"✅ Renamed 'baseline' -> 'section 1' in {topic}")
            except Exception as e:
                print(f"❌ Error renaming {topic}: {e}")

print("🏁 Standardization Complete.")
