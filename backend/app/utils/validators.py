"""Generic validation helpers."""

from datetime import date


def validate_date_range(start_date: date | None, end_date: date | None) -> None:
    if start_date and end_date and end_date < start_date:
        raise ValueError("end_date must not be before start_date")
