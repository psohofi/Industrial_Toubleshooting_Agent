from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import duckdb
import pandas as pd
EXPECTED_COLUMNS = [
    "index",
    "timestamp",
    "TP2",
    "TP3",
    "H1",
    "DV_pressure",
    "Reservoirs",
    "Motor_current",
    "Oil_temperature",
    "COMP",
    "DV_electric",
    "Towers",
    "MPG",
    "LPS",
    "Pressure_switch",
    "Oil_Level",
    "Caudal_impulse",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare MetroPT-3 CSV into Parquet.")
    parser.add_argument("--input", required=True, help="Path to MetroPT3(AirCompressor).csv")
    parser.add_argument(
        "--output-dir",
        default=str(PROJECT_ROOT / "data" / "processed" / "metropt3"),
        help="Directory for prepared Parquet files",
    )
    return parser.parse_args()


def validate_columns(columns: list[str]) -> None:
    normalized = [c.strip() for c in columns]
    missing = [c for c in EXPECTED_COLUMNS if c not in normalized]
    unexpected = [c for c in normalized if c not in EXPECTED_COLUMNS]
    if missing or unexpected:
        raise ValueError(
            f"Unexpected CSV schema. Missing={missing}; Unexpected={unexpected}; "
            f"Columns={normalized}"
        )


def prepare(input_path: Path, output_dir: Path) -> None:
    if not input_path.exists():
        raise FileNotFoundError(f"Input CSV does not exist: {input_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    parquet_path = output_dir / "telemetry.parquet"
    if parquet_path.exists():
        parquet_path.unlink()

    header = pd.read_csv(input_path, nrows=0)
    validate_columns(header.columns.tolist())

    csv_path = str(input_path.resolve()).replace("'", "''")
    output_path = str(parquet_path.resolve()).replace("'", "''")

    con = duckdb.connect()
    try:
        con.execute(
            f"""
            COPY (
                SELECT
                    TRY_CAST("index" AS BIGINT) AS "index",
                    TRY_CAST(timestamp AS TIMESTAMP) AS timestamp,
                    TP2, TP3, H1, DV_pressure, Reservoirs,
                    Motor_current, Oil_temperature, COMP, DV_electric,
                    Towers, MPG, LPS, Pressure_switch, Oil_Level, Caudal_impulse
                FROM read_csv(
                    '{csv_path}',
                    header=true,
                    auto_detect=true,
                    sample_size=200000,
                    ignore_errors=false
                )
            ) TO '{output_path}' (FORMAT PARQUET, COMPRESSION ZSTD)
            """
        )

        count, null_timestamps, min_ts, max_ts = con.execute(
            f"""
            SELECT
                COUNT(*),
                COUNT(*) FILTER (WHERE timestamp IS NULL),
                MIN(timestamp),
                MAX(timestamp)
            FROM read_parquet('{output_path}')
            """
        ).fetchone()

        if null_timestamps:
            raise ValueError(f"Prepared dataset contains {null_timestamps} null timestamps")

        print(f"Prepared rows: {count:,}")
        print(f"Timestamp range: {min_ts} -> {max_ts}")
        print(f"Output: {parquet_path}")
    finally:
        con.close()


def main() -> int:
    args = parse_args()
    try:
        prepare(Path(args.input), Path(args.output_dir))
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
