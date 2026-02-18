#!/usr/bin/env python3
"""
Reset 0.30 Mega Flora Biotech Logs

Topic-specific reset script for 0.30_Mega_Flora_Biotech topic.
This topic has minimal logs (3 items).
"""

import sys
from pathlib import Path

# Add parent directory to path to import the core reset system
sys.path.insert(0, str(Path(__file__).parent.parent))

from reset_topic_logs import LogResetter


def main():
    """Reset logs for 0.30_Mega_Flora_Biotech topic."""
    print("=" * 80)
    print("RESET LOGS: 0.30_Mega_Flora_Biotech")
    print("=" * 80)
    print()
    print("This topic has 3 log files.")
    print()

    # Create resetter
    resetter = LogResetter(dry_run=False, verbose=True)

    # Reset logs, keeping all (minimal logs)
    print("Keeping all logs (minimal count)...")
    resetter.reset_topic("0.30_Mega_Flora_Biotech", keep_recent=10, force=True)

    # Generate report
    resetter.generate_report()


if __name__ == "__main__":
    main()
