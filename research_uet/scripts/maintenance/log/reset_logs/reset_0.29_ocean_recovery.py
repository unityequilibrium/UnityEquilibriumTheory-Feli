#!/usr/bin/env python3
"""
Reset 0.29 Ocean Recovery Logs

Topic-specific reset script for 0.29_Ocean_Recovery topic.
This topic has no logs - may indicate a broken log system.
"""

import sys
from pathlib import Path

# Add parent directory to path to import the core reset system
sys.path.insert(0, str(Path(__file__).parent.parent))

from reset_topic_logs import LogResetter


def main():
    """Reset logs for 0.29_Ocean_Recovery topic."""
    print("=" * 80)
    print("RESET LOGS: 0.29_Ocean_Recovery")
    print("=" * 80)
    print()
    print("This topic has no logs - may indicate a broken log system.")
    print("Running reset will not delete anything but will verify the structure.")
    print()

    # Create resetter
    resetter = LogResetter(dry_run=False, verbose=True)

    # Reset logs (will find nothing to delete)
    resetter.reset_topic("0.29_Ocean_Recovery", keep_recent=0, force=True)

    # Generate report
    resetter.generate_report()


if __name__ == "__main__":
    main()
