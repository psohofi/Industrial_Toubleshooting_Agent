from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import duckdb
import pandas as pd

from .constants import EXPECTED_COLUMNS
from .failures import get_failure, load_failures


@dataclass(frozen=True)
class DatasetSummary:
    row_count: int
    min_timestamp: str
    max_timestamp: str
    median_seconds_between_rows: float | None
    p95_seconds_between_rows: float | None


class MetroPTRepository:
    """Read-only analytical repository over the prepared MetroPT-3 Parquet file."""

    def __init__(self, parquet_path: str | Path):
        self.parquet_path = Path(parquet_path)
        if not self.parquet_path.exists():
            raise FileNotFoundError(f"Parquet dataset not found: {self.parquet_path}")

    def _connect(self) -> duckdb.DuckDBPyConnection:
        return duckdb.connect(database=":memory:")

    def _relation(self, con: duckdb.DuckDBPyConnection) -> str:
        escaped = str(self.parquet_path).replace("'", "''")
        return f"read_parquet('{escaped}')"

    def summary(self) -> DatasetSummary:
        con = self._connect()
        try:
            relation = self._relation(con)
            row = con.execute(
                f"""
                SELECT
                    COUNT(*) AS row_count,
                    MIN(timestamp) AS min_timestamp,
                    MAX(timestamp) AS max_timestamp
                FROM {relation}
                """
            ).fetchone()

            gaps = con.execute(
                f"""
                WITH ordered AS (
                    SELECT timestamp,
                           LEAD(timestamp) OVER (ORDER BY timestamp) AS next_timestamp
                    FROM {relation}
                ),
                diffs AS (
                    SELECT EXTRACT(EPOCH FROM (next_timestamp - timestamp)) AS seconds
                    FROM ordered
                    WHERE next_timestamp IS NOT NULL
                )
                SELECT
                    MEDIAN(seconds),
                    QUANTILE_CONT(seconds, 0.95)
                FROM diffs
                WHERE seconds >= 0
                """
            ).fetchone()

            return DatasetSummary(
                row_count=int(row[0]),
                min_timestamp=str(row[1]),
                max_timestamp=str(row[2]),
                median_seconds_between_rows=(float(gaps[0]) if gaps[0] is not None else None),
                p95_seconds_between_rows=(float(gaps[1]) if gaps[1] is not None else None),
            )
        finally:
            con.close()

    def get_sensor_window(
        self,
        start_time: str,
        end_time: str,
        sensors: Sequence[str] | None = None,
        limit: int | None = None,
    ) -> pd.DataFrame:
        sensors = list(sensors or [c for c in EXPECTED_COLUMNS if c != "timestamp"])
        invalid = sorted(set(sensors) - set(EXPECTED_COLUMNS))
        if invalid:
            raise ValueError(f"Unknown sensor columns: {invalid}")

        projection = ", ".join(["timestamp"] + [f'"{s}"' for s in sensors])
        limit_sql = f"LIMIT {int(limit)}" if limit is not None else ""

        con = self._connect()
        try:
            relation = self._relation(con)
            return con.execute(
                f"""
                SELECT {projection}
                FROM {relation}
                WHERE timestamp >= ? AND timestamp <= ?
                ORDER BY timestamp
                {limit_sql}
                """,
                [pd.Timestamp(start_time).to_pydatetime(), pd.Timestamp(end_time).to_pydatetime()],
            ).df()
        finally:
            con.close()

    def sensor_statistics(
        self,
        sensor: str,
        start_time: str,
        end_time: str,
    ) -> dict:
        if sensor not in EXPECTED_COLUMNS or sensor == "timestamp":
            raise ValueError(f"Unknown sensor: {sensor}")

        con = self._connect()
        try:
            relation = self._relation(con)
            row = con.execute(
                f"""
                SELECT
                    COUNT(*) AS count,
                    AVG("{sensor}") AS mean,
                    MIN("{sensor}") AS min,
                    MAX("{sensor}") AS max,
                    STDDEV_SAMP("{sensor}") AS stddev
                FROM {relation}
                WHERE timestamp >= ? AND timestamp <= ?
                """,
                [pd.Timestamp(start_time).to_pydatetime(), pd.Timestamp(end_time).to_pydatetime()],
            ).fetchone()
            return {
                "sensor": sensor,
                "start_time": start_time,
                "end_time": end_time,
                "count": int(row[0]),
                "mean": float(row[1]) if row[1] is not None else None,
                "min": float(row[2]) if row[2] is not None else None,
                "max": float(row[3]) if row[3] is not None else None,
                "stddev": float(row[4]) if row[4] is not None else None,
            }
        finally:
            con.close()

    def get_failure(self, failure_id: int) -> dict:
        return get_failure(failure_id)

    def list_failures(self) -> list[dict]:
        return load_failures()

    def compare_sensor_windows(
        self,
        sensor: str,
        baseline_start: str,
        baseline_end: str,
        target_start: str,
        target_end: str,
    ) -> dict:
        baseline = self.sensor_statistics(sensor, baseline_start, baseline_end)
        target = self.sensor_statistics(sensor, target_start, target_end)

        b = baseline["mean"]
        t = target["mean"]
        pct_change = None if b in (None, 0) or t is None else ((t - b) / abs(b)) * 100.0

        return {
            "sensor": sensor,
            "baseline": baseline,
            "target": target,
            "mean_change_percent": pct_change,
        }
