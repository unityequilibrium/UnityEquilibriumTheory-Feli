"""
UET Paper Figure Collector
==========================
Harvests validation plots from all Research Topics and consolidates them
into the `paper/Figures` directory for publication (LaTeX).

Logic:
- Scans `topics/*/Result/*.png`
- Copies files to `research_uet/paper/Figures`
- Renames them to `Fig_{Topic}_{Name}.png`
"""

import shutil
from pathlib import Path
import os

# scripts/Reporting -> scripts -> research_uet
current_file = Path(__file__).resolve()
ROOT_UET = current_file.parents[2]
TOPICS_DIR = ROOT_UET / "topics"
PAPER_FIG_DIR = ROOT_UET / "paper" / "Figures"


def collect_figures():
    print("========================================")
    print("📊 UET FIGURE HARVESTER")
    print("========================================")

    if not PAPER_FIG_DIR.exists():
        PAPER_FIG_DIR.mkdir(parents=True)
        print(f"Created {PAPER_FIG_DIR}")

    count = 0

    # 1. Iterate over Topics
    for topic in sorted(TOPICS_DIR.iterdir()):
        if not topic.is_dir() or not topic.name[0].isdigit():
            continue

        topic_num = topic.name.split("_")[0]  # e.g., "0.1"
        result_dir = topic / "Result"

        if not result_dir.exists():
            continue

        # 2. Find PNGs
        for png in result_dir.glob("*.png"):
            # Construct new name: Fig_0.1_galaxy_rotation.png
            clean_name = png.stem.replace(" ", "_").lower()
            new_name = f"Fig_{topic_num}_{clean_name}{png.suffix}"
            dest = PAPER_FIG_DIR / new_name

            # Copy
            try:
                shutil.copy2(png, dest)
                print(f"  [+] Copied: {new_name} (from {topic.name})")
                count += 1
            except Exception as e:
                print(f"  [!] Error copying {png.name}: {e}")

    print("----------------------------------------")
    print(f"✅ Harvest Complete. {count} figures ready in {PAPER_FIG_DIR.name}/")
    print("========================================")


if __name__ == "__main__":
    collect_figures()
