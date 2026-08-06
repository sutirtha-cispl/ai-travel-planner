"""Generic validation and serialization helpers."""

import json
from datetime import date
from typing import Any


def validate_date_range(start_date: date | None, end_date: date | None) -> None:
    if start_date and end_date and end_date < start_date:
        raise ValueError("end_date must not be before start_date")


def to_json(data: Any) -> str:
    """Serialize arbitrary state to a JSON string safe for prompts."""
    return json.dumps(data, default=str, ensure_ascii=False)
