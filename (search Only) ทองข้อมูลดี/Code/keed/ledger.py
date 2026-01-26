import pandas as pd
import json
from pathlib import Path
from typing import List, Dict, Any


class UETLedger:
    """
    The Global Ledger: Aggregates decentralized run data into a central view.

    Principles:
    1. Local Sovereignty: Each run stores its own truth (summary.json, config.json).
    2. Central Visibility: The Ledger is just a 'View' of the local truths.
    """

    def __init__(self, log_dir: str = "data_logs"):
        self.log_dir = Path(log_dir)
        self.ledger_file = self.log_dir / "ledger.csv"

    def rebuild(self) -> pd.DataFrame:
        """
        Scans all subfolders in log_dir for 'summary.json' and rebuilds ledger.csv.
        This ensures the ledger is always in sync with the actual files.
        """
        rows = []
        if not self.log_dir.exists():
            print(f"Warning: Log directory {self.log_dir} does not exist.")
            return pd.DataFrame()

        print(f"📖 UET Ledger: Scanning {self.log_dir} for runs...")

        # Scan subdirectories
        for run_folder in self.log_dir.iterdir():
            if not run_folder.is_dir():
                continue

            summary_path = run_folder / "summary.json"
            if not summary_path.exists():
                continue

            try:
                with open(summary_path, "r") as f:
                    data = json.load(f)

                # Flatten metadata for CSV friendliness
                row = {
                    "run_id": data.get("run_id", run_folder.name),
                    "simulation": data.get("simulation"),
                    "status": data.get("status"),
                    "duration": data.get("duration_seconds"),
                    "start_time": data.get("timestamp"),
                    "steps": data.get("total_steps"),
                }

                # Add metadata parameters (flattened)
                meta = data.get("metadata", {})
                for k, v in meta.items():
                    if isinstance(v, (int, float, str, bool)):
                        row[f"param_{k}"] = v

                # Add final state metrics
                final_state = data.get("final_state")
                if final_state:
                    row["omega_final"] = final_state.get("omega")
                    row["is_stable"] = final_state.get("is_stable")
                    row["max_density"] = final_state.get("max_density")

                rows.append(row)

            except Exception as e:
                print(f"⚠️ Failed to read {summary_path}: {e}")

        if not rows:
            print("No valid runs found.")
            return pd.DataFrame()

        df = pd.DataFrame(rows)

        # Sort by run_id (timestamp)
        if "run_id" in df.columns:
            df.sort_values("run_id", inplace=True)

        # Save to Central CSV
        df.to_csv(self.ledger_file, index=False)
        print(f"✅ Ledger Rebuilt: {len(df)} runs indexed in {self.ledger_file}")

        return df

    def append_run(self, summary_path: Path):
        """
        Efficiently appends a single run to the ledger without full rebuild.
        (For future optimization)
        """
        # For now, just rebuild to ensure consistency (Safe Default)
        self.rebuild()
