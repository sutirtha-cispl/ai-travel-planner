"""Tests for tool input/output Pydantic schemas (validation)."""

import pytest
from pydantic import ValidationError

from app.schemas.tools import (
    CabinClass,
    CurrencyConversionInput,
    FlightOption,
    FlightSearchInput,
    HotelOption,
    HotelSearchInput,
    WeatherForecast,
    WeatherSearchInput,
)


def test_flight_input_valid():
    data = FlightSearchInput(
        origin="Kolkata",
        destination="Tokyo",
        departure_date="2026-04-01",
        return_date="2026-04-08",
        passengers=2,
        cabin_class=CabinClass.business,
    )
    assert data.origin == "Kolkata"
    assert data.passengers == 2
    assert data.cabin_class is CabinClass.business


def test_flight_input_rejects_zero_passengers():
    with pytest.raises(ValidationError):
        FlightSearchInput(
            origin="Kolkata",
            destination="Tokyo",
            departure_date="2026-04-01",
            passengers=0,
        )


def test_flight_input_rejects_missing_required_fields():
    with pytest.raises(ValidationError):
        FlightSearchInput(origin="Kolkata", departure_date="2026-04-01")


def test_flight_input_rejects_unknown_cabin_class():
    with pytest.raises(ValidationError):
        FlightSearchInput(
            origin="Kolkata",
            destination="Tokyo",
            departure_date="2026-04-01",
            cabin_class="supersonic",
        )


def test_flight_option_rejects_non_positive_price():
    with pytest.raises(ValidationError):
        FlightOption(
            airline="Skyline Air",
            flight_number="SK101",
            departure="08:30",
            arrival="13:00",
            duration_minutes=270,
            price=0,
            currency="USD",
        )


def test_hotel_input_rejects_checkout_before_checkin_format_errors():
    with pytest.raises(ValidationError):
        HotelSearchInput(
            destination="Tokyo",
            check_in="not-a-date",
            check_out="2026-04-07",
        )


def test_hotel_option_rating_bounds():
    with pytest.raises(ValidationError):
        HotelOption(
            name="Grand Hotel",
            location="Tokyo",
            rating=5.5,
            room_type="double",
            price_per_night=100,
            currency="USD",
        )


def test_weather_input_rejects_zero_days():
    with pytest.raises(ValidationError):
        WeatherSearchInput(location="Tokyo", date="2026-04-01", days=0)


def test_weather_forecast_rejects_invalid_precipitation():
    with pytest.raises(ValidationError):
        WeatherForecast(
            date="2026-04-01",
            temperature_celsius=20.0,
            condition="Sunny",
            precipitation_probability=120,
            wind_speed_kmh=10.0,
        )


def test_currency_input_rejects_lowercase_codes():
    with pytest.raises(ValidationError):
        CurrencyConversionInput(source="usd", target="JPY", amount=100)


def test_currency_input_rejects_non_positive_amount():
    with pytest.raises(ValidationError):
        CurrencyConversionInput(source="USD", target="JPY", amount=0)
