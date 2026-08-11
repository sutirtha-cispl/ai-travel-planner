"""Typed input/output schemas for travel tools.

Every tool accepts a Pydantic input model and returns a Pydantic output
model. This guarantees that agents and the tool layer only ever exchange
validated, structured data instead of arbitrary dictionaries.
"""

from datetime import date
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, Field


class CabinClass(StrEnum):
    economy = "economy"
    premium_economy = "premium_economy"
    business = "business"
    first = "first"


# --- Flight search ---------------------------------------------------------


class FlightSearchInput(BaseModel):
    origin: str = Field(
        ...,
        min_length=1,
        max_length=120,
        description="Departure city or airport code",
    )
    destination: str = Field(
        ...,
        min_length=1,
        max_length=120,
        description="Arrival city or airport code",
    )
    departure_date: Annotated[
        date, Field(description="Departure date (YYYY-MM-DD)")
    ]
    return_date: Annotated[
        date | None,
        Field(default=None, description="Optional return date (YYYY-MM-DD)"),
    ]
    passengers: int = Field(default=1, ge=1, le=9, description="Number of passengers")
    cabin_class: CabinClass = Field(
        default=CabinClass.economy, description="Cabin class"
    )


class FlightOption(BaseModel):
    airline: str
    flight_number: str
    departure: str = Field(..., description="Departure time in HH:MM local time")
    arrival: str = Field(..., description="Arrival time in HH:MM local time")
    duration_minutes: int = Field(
        ..., gt=0, description="Total flight duration in minutes"
    )
    price: float = Field(..., gt=0, description="Price per passenger")
    currency: str = Field(..., min_length=3, max_length=3)


class FlightSearchOutput(BaseModel):
    origin: str
    destination: str
    departure_date: Annotated[date, Field(...)]
    options: list[FlightOption] = Field(default_factory=list)
    provider: str = "mock"


# --- Hotel search ----------------------------------------------------------


class HotelSearchInput(BaseModel):
    destination: str = Field(..., min_length=1, max_length=120)
    check_in: Annotated[date, Field(description="Check-in date (YYYY-MM-DD)")]
    check_out: Annotated[date, Field(description="Check-out date (YYYY-MM-DD)")]
    guests: int = Field(default=1, ge=1, le=10, description="Number of guests")
    rooms: int = Field(default=1, ge=1, le=5, description="Number of rooms")
    budget_per_night: int | None = Field(
        default=None, description="Optional maximum price per night"
    )


class HotelOption(BaseModel):
    name: str
    location: str
    rating: float = Field(..., ge=0, le=5, description="Guest rating from 0 to 5")
    room_type: str
    price_per_night: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    amenities: list[str] = Field(default_factory=list)


class HotelSearchOutput(BaseModel):
    destination: str
    check_in: Annotated[date, Field(...)]
    check_out: Annotated[date, Field(...)]
    options: list[HotelOption] = Field(default_factory=list)
    provider: str = "mock"


# --- Weather forecast ------------------------------------------------------


class WeatherSearchInput(BaseModel):
    location: str = Field(..., min_length=1, max_length=120)
    date: Annotated[date, Field(description="Forecast date (YYYY-MM-DD)")]
    days: int = Field(
        default=1,
        ge=1,
        le=14,
        description="Number of consecutive forecast days (1 = single day)",
    )


class WeatherForecast(BaseModel):
    date: Annotated[date, Field(...)]
    temperature_celsius: float
    condition: str
    precipitation_probability: int = Field(..., ge=0, le=100)
    wind_speed_kmh: float = Field(..., ge=0)
    wind_direction: str = ""


class WeatherSearchOutput(BaseModel):
    location: str
    forecasts: list[WeatherForecast] = Field(default_factory=list)
    provider: str = "mock"


# --- Currency conversion ---------------------------------------------------


class CurrencyConversionInput(BaseModel):
    source: str = Field(
        ...,
        min_length=3,
        max_length=3,
        pattern=r"^[A-Z]{3}$",
        description="Source currency ISO code, e.g. USD",
    )
    target: str = Field(
        ...,
        min_length=3,
        max_length=3,
        pattern=r"^[A-Z]{3}$",
        description="Target currency ISO code, e.g. JPY",
    )
    amount: float = Field(..., gt=0, description="Amount to convert")


class CurrencyConversionOutput(BaseModel):
    source: str
    target: str
    amount: float
    exchange_rate: float = Field(
        ..., gt=0, description="1 source unit expressed in target"
    )
    converted_amount: float = Field(..., gt=0)
    provider: str = "mock"
