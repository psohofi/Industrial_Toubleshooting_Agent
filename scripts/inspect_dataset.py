from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.data.repository import MetroPTRepository


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect prepared MetroPT-3 dataset.")
    parser.add_argument(
        "--parquet",
        default="data/processed/metropt3/telemetry.parquet",
    )
    args = parser.parse_args()

    repo = MetroPTRepository(Path(args.parquet))
    summary = repo.summary()

    print("Dataset summary")
    print("---------------")
    print(f"Rows:              {summary.row_count:,}")
    print(f"Minimum timestamp: {summary.min_timestamp}")
    print(f"Maximum timestamp: {summary.max_timestamp}")
    print(f"Median gap (sec):  {summary.median_seconds_between_rows}")
    print(f"P95 gap (sec):     {summary.p95_seconds_between_rows}")
    print()
    print("Official failure windows")
    print("------------------------")
    for failure in repo.list_failures():
        print(
            f"#{failure['failure_id']}: {failure['failure_type']} | "
            f"{failure['start_time']} -> {failure['end_time']} | "
            f"{failure['severity']}"
        )


if __name__ == "__main__":
    main()
