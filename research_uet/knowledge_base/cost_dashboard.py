"""
UET Cost Dashboard
==================
CLI tool to monitor API costs per agent, per model, per day.

Reads cost_log.jsonl written by CostTracker in api_client.py.

Usage:
    python -m research_uet.knowledge_base.cost_dashboard
    python -m research_uet.knowledge_base.cost_dashboard --days 7
    python -m research_uet.knowledge_base.cost_dashboard --agent orchestrator

Rust Compatibility:
    - Reads standard JSONL format (serde-compatible)
    - Pure text output (no Python-only UI libraries)
"""

import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


# =============================================================================
# DASHBOARD
# =============================================================================


class CostDashboard:
    """API cost dashboard — reads cost_log.jsonl and produces reports."""

    def __init__(self, log_file: str | Path):
        self.log_file = Path(log_file)

    def load_entries(self, days: Optional[int] = None) -> list[dict]:
        """Load entries from JSONL, optionally filtered by date range."""
        if not self.log_file.exists():
            return []

        entries = []
        cutoff = None
        if days:
            cutoff = (datetime.now() - timedelta(days=days)).isoformat()[:10]

        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if cutoff and entry.get("date", "") < cutoff:
                        continue
                    entries.append(entry)
                except json.JSONDecodeError:
                    continue

        return entries

    def report(
        self,
        days: Optional[int] = None,
        agent_filter: Optional[str] = None,
    ) -> str:
        """
        Generate a formatted cost report.

        Args:
            days: Filter to last N days
            agent_filter: Show only this agent
        """
        entries = self.load_entries(days=days)

        if agent_filter:
            entries = [e for e in entries if e.get("agent_id") == agent_filter]

        if not entries:
            return self._empty_report(days, agent_filter)

        # Aggregate by agent
        by_agent: dict[str, dict] = defaultdict(
            lambda: {
                "model": "",
                "calls": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "cost_usd": 0.0,
                "errors": 0,
            }
        )

        # Daily totals
        by_date: dict[str, float] = defaultdict(float)

        for entry in entries:
            agent = entry.get("agent_id", "unknown")
            agg = by_agent[agent]
            agg["model"] = entry.get("model", "?")
            agg["calls"] += 1
            agg["input_tokens"] += entry.get("input_tokens", 0)
            agg["output_tokens"] += entry.get("output_tokens", 0)
            agg["cost_usd"] += entry.get("cost_usd", 0.0)
            if not entry.get("success", True):
                agg["errors"] += 1

            date = entry.get("date", "unknown")
            by_date[date] += entry.get("cost_usd", 0.0)

        # Build report
        total_cost = sum(a["cost_usd"] for a in by_agent.values())
        total_calls = sum(a["calls"] for a in by_agent.values())
        total_input = sum(a["input_tokens"] for a in by_agent.values())
        total_output = sum(a["output_tokens"] for a in by_agent.values())

        # Date range
        dates = sorted(by_date.keys())
        date_range = f"{dates[0]} → {dates[-1]}" if dates else "?"

        # Header
        lines = [
            "",
            "╔══════════════════════════════════════════════════════════════╗",
            f"║         API Cost Report — {date_range:>30s}   ║",
            "╠══════════════════════════════════════════════════════════════╣",
            "║ Agent           │ Model                │ Calls │ Cost USD  ║",
            "║─────────────────┼──────────────────────┼───────┼───────────║",
        ]

        # Agent rows (sorted by cost descending)
        for agent, agg in sorted(by_agent.items(), key=lambda x: -x[1]["cost_usd"]):
            model = agg["model"]
            # Truncate model name
            if "/" in model:
                model = model.split("/")[-1]
            model = model[:20]

            err_flag = f" ⚠{agg['errors']}" if agg["errors"] else ""
            lines.append(
                f"║ {agent:<15s} │ {model:<20s} │ {agg['calls']:>5d} │ "
                f"${agg['cost_usd']:>7.4f}  ║{err_flag}"
            )

        # Totals
        lines.extend(
            [
                "║─────────────────┼──────────────────────┼───────┼───────────║",
                f"║ TOTAL           │ {len(by_agent)} agents{' ' * 14}│ {total_calls:>5d} │ "
                f"${total_cost:>7.4f}  ║",
                "╚══════════════════════════════════════════════════════════════╝",
            ]
        )

        # Token summary
        lines.extend(
            [
                "",
                f"  📊 Tokens: {total_input:,} input + {total_output:,} output = "
                f"{total_input + total_output:,} total",
            ]
        )

        # Daily breakdown
        if len(by_date) > 1:
            lines.append("\n  📅 Daily costs:")
            for date in sorted(by_date.keys()):
                bar_len = min(int(by_date[date] * 200), 40)
                bar = "█" * bar_len
                lines.append(f"    {date}: ${by_date[date]:.4f} {bar}")

        return "\n".join(lines)

    def _empty_report(self, days: Optional[int], agent_filter: Optional[str]) -> str:
        """Return empty report message."""
        msg = "  No API calls logged"
        if days:
            msg += f" in the last {days} days"
        if agent_filter:
            msg += f" for agent '{agent_filter}'"
        if not self.log_file.exists():
            msg += f"\n  Log file not found: {self.log_file}"
        return msg

    def agent_summary(self) -> dict[str, dict]:
        """Get per-agent summary as dict (for programmatic use)."""
        entries = self.load_entries()
        summary: dict[str, dict] = {}

        for entry in entries:
            agent = entry.get("agent_id", "unknown")
            if agent not in summary:
                summary[agent] = {
                    "calls": 0,
                    "cost_usd": 0.0,
                    "model": entry.get("model", "?"),
                }
            summary[agent]["calls"] += 1
            summary[agent]["cost_usd"] += entry.get("cost_usd", 0.0)

        return summary


# =============================================================================
# CLI
# =============================================================================


def main():
    """CLI entry point."""
    import argparse

    # Default log path
    default_log = Path(__file__).resolve().parent / "cost_log.jsonl"

    parser = argparse.ArgumentParser(description="UET API Cost Dashboard")
    parser.add_argument("--log", type=str, default=str(default_log), help="Path to cost_log.jsonl")
    parser.add_argument("--days", type=int, help="Show only last N days")
    parser.add_argument("--agent", type=str, help="Filter by agent ID")
    args = parser.parse_args()

    dashboard = CostDashboard(args.log)
    print(dashboard.report(days=args.days, agent_filter=args.agent))


if __name__ == "__main__":
    main()
