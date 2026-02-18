#!/usr/bin/env python3
"""
Clean up temporary log reports
"""

from pathlib import Path

maintenance_dir = Path("research_uet/scripts/maintenance")

# Find all temporary report files
report_files = [
    "log_analysis_report.csv",
    "log_analysis_report.json",
    "log_health_report.json",
    "log_reset_report.json"
]

deleted_count = 0
for filename in report_files:
    file_path = maintenance_dir / filename
    if file_path.exists():
        file_path.unlink()
        print(f"Deleted: {filename}")
        deleted_count += 1

print(f"\nCleaned up {deleted_count} temporary report files")
