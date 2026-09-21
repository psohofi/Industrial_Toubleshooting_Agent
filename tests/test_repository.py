from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from app.data.repository import MetroPTRepository


def test_get_failure():
    repo = MetroPTRepository.__new__(MetroPTRepository)
    failure = repo.get_failure(2)
    assert failure["failure_type"] == "Air Leak"
    assert failure["severity"] == "High stress"


def test_unknown_failure():
    repo = MetroPTRepository.__new__(MetroPTRepository)
    with pytest.raises(KeyError):
        repo.get_failure(999)
