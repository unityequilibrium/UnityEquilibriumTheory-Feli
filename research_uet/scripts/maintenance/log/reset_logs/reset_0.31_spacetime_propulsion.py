#!/usr/bin/env python3
"""
Reset 0.31 SpaceTime Propulsion Logs

Topic-specific reset script for 0.31_SpaceTime_Propulsion topic.
This topic has minimal logs (3 items).
"""

import sys
from pathlib import Path

# Add parent directory to path to import the core reset system
sys.path.insert(0, str(Path(__file__).parent.parent))

from reset_topic_logs import LogResetter


def main():
    """Reset logs for 0.31_SpaceTime_Propulsion topic."""
    print("=" * 80)
    print("RESET LOGS: 0.31_SpaceTime_Propulsion")
    print("=" * 80)
    print()
    print("This topic has 3 log files.")
    print()

    # Create resetter
    resetter = LogResetter(dry_run=False, verbose=True)

    # Reset logs, keeping all (minimal logs)
    print("Keeping all logs (minimal count)...")
    resetter.reset_topic("0.31_SpaceTime_Propulsion", keep_recent=10, force=True)

    # Generate report
    resetter.generate_report()


if __name__ == "__main__":
    main()
