#!/usr/bin/env python3
"""
Reset 0.9 Quantum Nonlocality Logs

Topic-specific reset script for 0.9_Quantum_Nonlocality topic.
This topic has moderate logs (516 items) and may need periodic cleanup.
"""

import sys
from pathlib import Path

# Add parent directory to path to import the core reset system
sys.path.insert(0, str(Path(__file__).parent.parent))

from reset_topic_logs import LogResetter


def main():
    """Reset logs for 0.9_Quantum_Nonlocality topic."""
    print("=" * 80)
    print("RESET LOGS: 0.9_Quantum_Nonlocality")
    print("=" * 80)
    print()
    print("This topic has 516 log files.")
    print()

    # Create resetter
    resetter = LogResetter(dry_run=False, verbose=True)

    # Reset logs, keeping 10 most recent
    print("Keeping 10 most recent timestamp folders...")
    resetter.reset_topic("0.9_Quantum_Nonlocality", keep_recent=10, force=False)

    # Generate report
    resetter.generate_report()


if __name__ == "__main__":
    main()
