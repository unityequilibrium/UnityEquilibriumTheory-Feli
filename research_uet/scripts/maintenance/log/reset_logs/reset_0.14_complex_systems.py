#!/usr/bin/env python3
"""
Reset 0.14 Complex Systems Logs

Topic-specific reset script for 0.14_Complex_Systems topic.
This topic has excessive logs (1080+ items) and needs periodic cleanup.
"""

import sys
from pathlib import Path

# Add parent directory to path to import the core reset system
sys.path.insert(0, str(Path(__file__).parent.parent))

from reset_topic_logs import LogResetter


def main():
    """Reset logs for 0.14_Complex_Systems topic."""
    print("=" * 80)
    print("RESET LOGS: 0.14_Complex_Systems")
    print("=" * 80)
    print()
    print("This topic has 1080+ log files and needs periodic cleanup.")
    print()

    # Create resetter
    resetter = LogResetter(dry_run=False, verbose=True)

    # Reset logs, keeping 10 most recent
    print("Keeping 10 most recent timestamp folders...")
    resetter.reset_topic("0.14_Complex_Systems", keep_recent=10, force=False)

    # Generate report
    resetter.generate_report()


if __name__ == "__main__":
    main()
