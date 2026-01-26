import zipfile
import os
import shutil

ZIP_PATH = r"c:\Users\santa\Desktop\lad\Lab_uet_harness_v0.8.7\(search Only) ทองข้อมูลดี\v0.8.7+\lab 02.01.2026.zip"
TARGET = (
    "lab 02.01.2026/06_complex_systems/brain/unified_brain_galaxy_economy_pipeline.py"
)
DEST_DIR = r"c:\Users\santa\Desktop\lad\Lab_uet_harness_v0.8.7\research_uet\topics\0.25_Unified_Theory_Of_Everything\Code\legacy"

os.makedirs(DEST_DIR, exist_ok=True)

try:
    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        fname = os.path.basename(TARGET)
        z.extract(TARGET, path="temp_extract")
        src = os.path.join("temp_extract", TARGET)
        dst = os.path.join(DEST_DIR, fname)
        shutil.move(src, dst)
        print(f"✅ Extracted: {fname}")

    shutil.rmtree("temp_extract")
except Exception as e:
    print(f"❌ Error: {e}")
