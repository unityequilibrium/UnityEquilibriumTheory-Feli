#!/usr/bin/env python3
"""
Reset 0.7 Neutrino Physics Logs

Topic-specific reset script for 0.7_Neutrino_Physics topic.
This topic has moderate logs (300 items) and may need periodic cleanup.
"""

import sys
from pathlib import Path

# Add parent directory to path to import the core reset system
sys.path.insert(0, str(Path(__file__).parent.parent))

from reset_topic_logs import LogResetter


def main():
    """Reset logs for 0.7_Neutrino_Physics topic."""
    print("=" * 80)
    print("RESET LOGS: 0.7_Neutrino_Physics")
    print("=" * 80)
    print()
    print("This topic has 300 log files.")
    print()

    # Create resetter
    resetter = LogResetter(dry_run=False, verbose=True)

    # Reset logs, keeping 10 most recent
    print("Keeping 10 most recent timestamp folders...")
    resetter.reset_topic("0.7_Neutrino_Physics", keep_recent=10, force=False)

    # Generate report
    resetter.generate_report()


if __name__ == "__main__":
    main()
