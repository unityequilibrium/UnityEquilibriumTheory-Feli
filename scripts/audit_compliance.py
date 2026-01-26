import os
import ast
from pathlib import Path
from collections import defaultdict

# Root is where this script lives + research_uet location
ROOT = Path(__file__).resolve().parent / "research_uet/topics"


def audit_compliance():
    print(f"🔍 Starting 5x4 Compliance Audit on: {ROOT}")

    stats = {
        "total_scripts": 0,
        "compliant_base_solver": 0,
        "manual_path_violation": 0,
        "unknown": 0,
    }

    report_lines = []
    report_lines.append("# 5x4 Grid Compliance Report 📊\n")
    report_lines.append("| Topic | Script | Status | Reason |")
    report_lines.append("|---|---|---|---|")

    # Walk through all topics
    for topic_dir in ROOT.iterdir():
        if not topic_dir.is_dir() or topic_dir.name.startswith("__"):
            continue

        topic_name = topic_dir.name

        # Check Code/01_Engine and Code/03_Research
        code_dir = topic_dir / "Code"
        target_dirs = [code_dir / "01_Engine", code_dir / "03_Research"]

        for search_dir in target_dirs:
            if not search_dir.exists():
                continue

            for script_path in search_dir.glob("*.py"):
                if script_path.name == "__init__.py":
                    continue

                stats["total_scripts"] += 1
                status = "UNKNOWN"
                reason = "Analysis Failed"

                try:
                    with open(script_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # 1. Check for UETBaseSolver usage
                    has_base_solver = "UETBaseSolver" in content

                    # 2. Check for Manual Path Construction (Risk)
                    # "parents[2]", "parents[3]", "Result" hardcoded
                    has_manual_path = ("parents[" in content) and (
                        '"Result"' in content or "'Result'" in content
                    )

                    if has_base_solver:
                        stats["compliant_base_solver"] += 1
                        status = "✅ PASS"
                        reason = "Inherits/Uses BaseSolver"
                    elif has_manual_path:
                        stats["manual_path_violation"] += 1
                        status = "❌ FAIL"
                        reason = "Manual Path Construction Detected"
                    else:
                        stats["unknown"] += 1
                        status = "⚠️ WARN"
                        reason = "No Standard Pattern Found"

                    report_lines.append(
                        f"| {topic_name} | {script_path.name} | {status} | {reason} |"
                    )

                except Exception as e:
                    report_lines.append(
                        f"| {topic_name} | {script_path.name} | 💥 ERROR | Read Failed: {e} |"
                    )

    # Summary
    print("\n" + "=" * 40)
    print(f"Total Scripts Scanned: {stats['total_scripts']}")
    print(f"✅ Compliant (BaseSolver): {stats['compliant_base_solver']}")
    print(f"❌ Violation (Manual Path): {stats['manual_path_violation']}")
    print(f"⚠️ Unknown/Other:        {stats['unknown']}")
    print("=" * 40)

    compliance_rate = 0
    if stats["total_scripts"] > 0:
        compliance_rate = (
            stats["compliant_base_solver"] / stats["total_scripts"]
        ) * 100

    print(f"Current System Compliance: {compliance_rate:.1f}%")

    # Write full report to Artifact
    output_path = Path(__file__).resolve().parent / "COMPLIANCE_REPORT.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"📄 Detailed Report generated: {output_path}")


if __name__ == "__main__":
    audit_compliance()
