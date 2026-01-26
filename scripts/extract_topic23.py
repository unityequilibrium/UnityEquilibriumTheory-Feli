import zipfile
import os
import shutil

ZIP_PATH = r"c:\Users\santa\Desktop\lad\Lab_uet_harness_v0.8.7\(search Only) ทองข้อมูลดี\v0.8.7+\lab 02.01.2026.zip"
TARGET_FILE = (
    "lab 02.01.2026/03_condensed_matter/condensed_matter/test_superfluidity.py"
)
DEST_DIR = r"c:\Users\santa\Desktop\lad\Lab_uet_harness_v0.8.7\research_uet\topics\0.23_Condensed_Matter\Code\legacy"

os.makedirs(DEST_DIR, exist_ok=True)

print(f"Extracting {TARGET_FILE}...")
try:
    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        # Extract to temp
        z.extract(TARGET_FILE, path="temp_extract")

        # Move to destination
        src = os.path.join("temp_extract", TARGET_FILE)
        dst = os.path.join(DEST_DIR, "test_superfluidity_legacy.py")
        shutil.move(src, dst)
        print(f"✅ Extracted to: {dst}")

    # Cleanup
    shutil.rmtree("temp_extract")

except Exception as e:
    print(f"❌ Error: {e}")
