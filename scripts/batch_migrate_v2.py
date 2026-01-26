import os
import re
from pathlib import Path

# Target Root
ROOT = Path(__file__).resolve().parent / "research_uet/topics"


def batch_migrate_v2():
    print(f"🤖 Starting Batch Robot V2 (The Cleanup) on: {ROOT}")
    count = 0
    fixed = 0

    # 1. Patterns to Destroy (Legacy Paths)
    # detecting: repo_root = Path(__file__)...
    # detecting: something = repo_root / "research_uet" ... / "Result" ...

    # We want to replace manual result dirs with Standard UETPathManager

    for topic_dir in ROOT.iterdir():
        if not topic_dir.is_dir() or topic_dir.name.startswith("__"):
            continue

        topic_name = topic_dir.name

        # We target Research folders primarily (as Engines are mostly fixed or manual)
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

                    # Optimization: If it already uses UETPathManager.get_result_dir, skip?
                    # But some might use it AND maintain legacy paths.
                    # Let's check if it still has "manual path smells".

                    has_manual_path = (
                        "parents[" in content
                        or '/ "Result"' in content
                        or "/ 'Result'" in content
                    )

                    if not has_manual_path:
                        continue

                    print(f"🔧 Analyzing: {script_path.name}")

                    # ---------------------------------------------------------
                    # STEP 1: Ensure Import
                    # ---------------------------------------------------------
                    if "UETPathManager" not in content:
                        import_stmt = "from research_uet.core.uet_glass_box import UETPathManager\n"
                        if "import sys" in content:
                            content = content.replace(
                                "import sys", "import sys\n" + import_stmt, 1
                            )
                        else:
                            content = import_stmt + content

                    # ---------------------------------------------------------
                    # STEP 2: The Complex Pattern Replacement
                    # ---------------------------------------------------------

                    # Pattern A: `fig_dir = ... / "Result" / "figures"`
                    # We want to replace the definition of fig_dir with a standard one.
                    # But regex is hard for multi-line path construction.

                    # Strategy: Inject a standard `output_dir` and `fig_dir` at the top of the main execution block
                    # And then search-replace usage of the OLD variables? Too risky.

                    # Strategy: Look for the specific "Result" string and replace the whole line?

                    lines = content.split("\n")
                    new_lines = []
                    pillar_code = search_dir.parent.name  # 03_Research

                    # We will define standard_output explicitly if we find a replacement need
                    injected_standard_output = False
                    standard_def = f'    output_dir = UETPathManager.get_result_dir(topic="{topic_name}", name="{script_path.stem}", pillar="{pillar_code}")'
                    standard_fig_def = f'    fig_dir = output_dir / "figures"\n    fig_dir.mkdir(parents=True, exist_ok=True)'

                    for line in lines:
                        # Detect lines constructing result paths
                        # e.g. fig_dir = repo_root / ... / "Result" / "figures"
                        if (
                            '/ "Result"' in line or "/ 'Result'" in line
                        ) and "=" in line:
                            # It's an assignment like `out_path = ...`
                            # We replace it with our Standard Definition

                            # Extract variable name
                            var_name = line.split("=")[0].strip()
                            indent = line[: len(line) - len(line.lstrip())]

                            print(
                                f"   -> Replacing manual path assignment for '{var_name}'"
                            )

                            # If variable is 'fig_dir' or similar, append / "figures" ?
                            # Or just map it to the standard output_dir

                            if "fig" in var_name:
                                # It's likely a figure directory
                                new_lines.append(
                                    f'{indent}output_dir = UETPathManager.get_result_dir(topic="{topic_name}", name="{script_path.stem}", pillar="{pillar_code}")'
                                )
                                new_lines.append(
                                    f'{indent}{var_name} = output_dir / "figures"'
                                )
                                new_lines.append(
                                    f"{indent}{var_name}.mkdir(parents=True, exist_ok=True)"
                                )
                            else:
                                # Standard output
                                new_lines.append(
                                    f'{indent}{var_name} = UETPathManager.get_result_dir(topic="{topic_name}", name="{script_path.stem}", pillar="{pillar_code}")'
                                )

                            continue

                        # Detect: plt.savefig(...) using manual path JOINing
                        # e.g. plt.savefig(result_dir / "plot.png")
                        # If we fixed the variable 'result_dir' above, this line is fine!

                        # What if they use `repo_root / "..." / "Result"` directly in savefig?
                        # That's rare. Usually assigned to variable.

                        new_lines.append(line)

                    content = "\n".join(new_lines)

                    if content != original_content:
                        with open(script_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        fixed += 1
                        print(f"   ✅ Fixed path logic in {script_path.name}")

                except Exception as e:
                    print(f"   ❌ Error fixing {script_path.name}: {e}")

    print(f"\n📊 Batch V2 Result: Scanned {count}. Fixed {fixed}.")


if __name__ == "__main__":
    batch_migrate_v2()
