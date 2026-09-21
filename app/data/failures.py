from __future__ import annotations

from pathlib import Path
import json

DEFAULT_FAILURES_PATH = Path(__file__).resolve().parents[2] / "data" / "metadata" / "failure_events.json"


def load_failures(path: str | Path | None = None) -> list[dict]:
    failure_path = Path(path) if path else DEFAULT_FAILURES_PATH
    with failure_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Failure metadata must be a JSON array")
    return data


def get_failure(failure_id: int, path: str | Path | None = None) -> dict:
    for failure in load_failures(path):
        if failure["failure_id"] == failure_id:
            return dict(failure)
    raise KeyError(f"Unknown failure_id: {failure_id}")
