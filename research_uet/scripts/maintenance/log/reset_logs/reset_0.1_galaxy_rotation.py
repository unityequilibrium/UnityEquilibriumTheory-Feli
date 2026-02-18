#!/usr/bin/env python3
"""
Reset 0.1 Galaxy Rotation Problem Logs

Topic-specific reset script for 0.1_Galaxy_Rotation_Problem topic.
This topic has moderate logs (371 items) and may need periodic cleanup.
"""

import sys
from pathlib import Path

# Add parent directory to path to import the core reset system
sys.path.insert(0, str(Path(__file__).parent.parent))

from reset_topic_logs import LogResetter


def main():
    """Reset logs for 0.1_Galaxy_Rotation_Problem topic."""
    print("=" * 80)
    print("RESET LOGS: 0.1_Galaxy_Rotation_Problem")
    print("=" * 80)
    print()
    print("This topic has 371 log files.")
    print()

    # Create resetter
    resetter = LogResetter(dry_run=False, verbose=True)

    # Reset logs, keeping 10 most recent
    print("Keeping 10 most recent timestamp folders...")
    resetter.reset_topic("0.1_Galaxy_Rotation_Problem", keep_recent=10, force=False)

    # Generate report
    resetter.generate_report()


if __name__ == "__main__":
    main()
