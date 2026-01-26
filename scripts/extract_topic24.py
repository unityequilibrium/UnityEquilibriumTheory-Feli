import zipfile
import os
import shutil

ZIP_PATH = r"c:\Users\santa\Desktop\lad\Lab_uet_harness_v0.8.7\(search Only) ทองข้อมูลดี\v0.8.7+\lab 02.01.2026.zip"
TARGETS = [
    "lab 02.01.2026/07_utilities/analysis/ccbh_v3.py",
    "lab 02.01.2026/01_particle_physics/neutrinos/analysis/pbh_hawking_neutrino_4d.py",
]
DEST_DIR = r"c:\Users\santa\Desktop\lad\Lab_uet_harness_v0.8.7\research_uet\topics\0.24_Black_Hole_Cosmology\Code\legacy"

os.makedirs(DEST_DIR, exist_ok=True)

try:
    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        for t in TARGETS:
            fname = os.path.basename(t)
            z.extract(t, path="temp_extract")
            src = os.path.join("temp_extract", t)
            dst = os.path.join(DEST_DIR, fname)
            shutil.move(src, dst)
            print(f"✅ Extracted: {fname}")

    shutil.rmtree("temp_extract")
except Exception as e:
    print(f"❌ Error: {e}")
