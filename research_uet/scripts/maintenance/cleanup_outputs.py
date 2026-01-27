import os
import shutil
from pathlib import Path

# Config
ROOT = Path("research_uet/topics")
VALID_PILLARS = ["01_Engine", "02_Proof", "03_Research", "04_Competitor"]


def cleanup_results():
    print("🧹 STARTING RESULTS CLEANUP...")
    deleted_count = 0

    if not ROOT.exists():
        print("Root not found.")
        return

    # Iterate all topics
    for topic in ROOT.iterdir():
        if not topic.is_dir() or not topic.name.startswith("0."):
            continue

        result_dir = topic / "Result"
        if not result_dir.exists():
            continue

        print(f"Checking {topic.name}/Result...")

        # Check items in Result
        for item in result_dir.iterdir():
            if item.is_dir():
                # If it's NOT a valid pillar "01_Engine" etc. -> DELETE IT
                if item.name not in VALID_PILLARS:
                    # Double check it looks like a run folder (starts with digits usually)
                    # User complained about "17689..." timestamp folders.
                    print(f"  ❌ Deleting SPAM folder: {item.name}")
                    try:
                        shutil.rmtree(item)
                        deleted_count += 1
                    except Exception as e:
                        print(f"     Failed: {e}")
            else:
                # Delete loose files in Result (stats.csv, pngs)?
                # User images showed PNGs and CSVs loose in Research folders (ok) or Result (maybe ok).
                # But 'Result/' root should be clean.
                if item.name != "README.md":
                    print(f"  ❌ Deleting LOOSE file: {item.name}")
                    try:
                        os.remove(item)
                        deleted_count += 1
                    except Exception as e:
                        print(f"     Failed: {e}")

    print(f"✨ Cleanup Complete. Deleted {deleted_count} items.")


if __name__ == "__main__":
    cleanup_results()
