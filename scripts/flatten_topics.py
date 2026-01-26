import shutil
import os

topics = [
    "0.20_Atomic_Physics",
    "0.23_Condensed_Matter",
    "0.24_Black_Hole_Cosmology",
    "0.25_Unified_Theory_Of_Everything",
]

base = r"C:\Users\santa\Desktop\lad\Lab_uet_harness_v0.8.7\research_uet\topics"

for t in topics:
    # Path to the bad nested folder: Code/section 1/code
    bad_dir = os.path.join(base, t, "Code", "section 1", "code")
    # Path to the good flattened folder: Code/section 1
    good_dir = os.path.join(base, t, "Code", "section 1")

    if os.path.exists(bad_dir):
        print(f"Fixing {t}...")
        for f in os.listdir(bad_dir):
            src = os.path.join(bad_dir, f)
            dst = os.path.join(good_dir, f)
            try:
                shutil.move(src, dst)
                print(f"  > Moved {f} up one level.")
            except Exception as e:
                print(f"  > Error moving {f}: {e}")

        # Remove empty bad dir
        try:
            os.rmdir(bad_dir)
            print("  > Removed empty 'code' folder.")
        except:
            print("  > Could not remove 'code' folder (not empty?).")
    else:
        print(f"{t}: 'code' subfolder not found (already fixed?).")
