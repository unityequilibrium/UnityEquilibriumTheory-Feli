import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "research_uet/topics"


def batch_migrate():
    print(f"🤖 Starting Batch Migration Robot on: {ROOT}")
    count = 0
    fixed = 0
    skipped = 0

    # Regex Patterns
    # 1. Detect Manual Path Construction (Risk)
    # Pattern: path = ...parents[X] / "Result" ...
    # We want to replace it with:
    # from research_uet.core.uet_glass_box import UETPathManager
    # output_dir = UETPathManager.get_result_dir(topic="TOPIC_ID", name="Script_Name", pillar="03_Research")

    for topic_dir in ROOT.iterdir():
        if not topic_dir.is_dir() or topic_dir.name.startswith("__"):
            continue

        topic_name = topic_dir.name

        # Target only 03_Research (leaving Engine for manual if complex)
        # Actually user said ALL. Let's do Research first as it's the bulk.
        search_dirs = [
            topic_dir / "Code" / "03_Research",
            topic_dir / "Code" / "01_Engine",
        ]

        for search_dir in search_dirs:
            if not search_dir.exists():
                continue

            for script_path in search_dir.glob("*.py"):
                if script_path.name == "__init__.py":
                    continue

                count += 1
                try:
                    with open(script_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    original_content = content

                    # Criteria:
                    # 1. Has Manual Path Logic?
                    # 2. Does NOT have UETBaseSolver (if it has BaseSolver it's already compliant or handled by parent)
                    # 3. Does NOT have UETPathManager already

                    if "UETBaseSolver" in content:
                        continue  # Skip Engine/Compliant classes

                    if "UETPathManager" in content:
                        continue  # Already fixed

                    # Very specific pattern seen in audit:
                    # result_dir = repo_root / "Result" ....
                    # OR Path(__file__).parents[...] / "Result"

                    if '"Result"' not in content and "'Result'" not in content:
                        continue  # No explicit result folder reference? Skip.

                    print(f"🔧 Fixing: {script_path.name}")

                    # 1. Inject Import
                    import_stmt = (
                        "from research_uet.core.uet_glass_box import UETPathManager\n"
                    )
                    # Add after "import sys" or at top
                    if "import sys" in content:
                        content = content.replace(
                            "import sys", "import sys\n" + import_stmt, 1
                        )
                    else:
                        content = import_stmt + content

                    # 2. Replace Path Logic
                    # We can't regex every variation safely.
                    # Strategy: Comment out old path logic, insert new logic at start of `run()` or global?
                    # Most scripts are linear.
                    # Let's simple INSERT the manager path at the top of the main block and hope the script uses variables we can overwrite?
                    # No, that's dangerous (Variable Shadowing).

                    # Better Strategy:
                    # Create a standard variable `output_dir` at the top.
                    # And Replace usage of `... / "Result" ...` with `output_dir`.

                    # Given the risk of breaking logic, I will do a safer 'Injection Only'.
                    # I will add the import and print a TODO.
                    # Wait, user wants it FIXED.

                    # Let's try to find the specific "root / 'Result'" pattern.
                    # Pattern: result_dir = ... / "Result"

                    # Regex replacement:
                    # Capture variable name:  (\w+)\s*=\s*.*?\/\s*["']Result["']
                    # Replace with: \1 = UETPathManager.get_result_dir(topic="{topic_name}", name="{script_path.stem}", pillar="{search_dir.parent.name}")

                    pattern = re.compile(
                        r'(\w+)\s*=\s*(?:[\w\(\)\.\[\]]+)\s*/\s*["\']Result["\']'
                    )

                    # Determine Pillar from path
                    pillar_code = script_path.parent.name  # 03_Research or 01_Engine

                    def replacer(match):
                        var_name = match.group(1)
                        # Construct replacement line
                        return f'{var_name} = UETPathManager.get_result_dir(topic="{topic_name}", name="{script_path.stem}", pillar="{pillar_code}")'

                    new_content = pattern.sub(replacer, content)

                    # Also handle: Path(...) / "Result" / "Outcome"
                    # This is harder.

                    if new_content != original_content:
                        with open(script_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        fixed += 1
                    else:
                        print(f"  ⚠️ Could not match path pattern in {script_path.name}")
                        skipped += 1

                except Exception as e:
                    print(f"  ❌ Error fixing {script_path.name}: {e}")

    print(f"\n📊 Batch Result: Scanned {count}. Fixed {fixed}. Skipped {skipped}.")


if __name__ == "__main__":
    batch_migrate()
