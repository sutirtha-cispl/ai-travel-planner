"""Trip schemas."""

import uuid
from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validator


class TripCreate(BaseModel):
    destination: str = Field(..., min_length=1, max_length=255)
    start_date: date | None = None
    end_date: date | None = None

    @model_validator(mode="after")
    def validate_date_range(self) -> "TripCreate":
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date must not be before start_date")
        return self


class TripResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    destination: str
    start_date: date | None
    end_date: date | None
    status: str
