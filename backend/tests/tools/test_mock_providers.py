"""Tests for the deterministic mock providers."""

from datetime import date

import pytest

from app.schemas.tools import (
    CabinClass,
    CurrencyConversionInput,
    FlightSearchInput,
    HotelSearchInput,
    WeatherSearchInput,
)
from app.tools.mocks import (
    MockCurrencyProvider,
    MockFlightProvider,
    MockHotelProvider,
    MockWeatherProvider,
)


async def test_flight_mock_is_deterministic():
    provider = MockFlightProvider()
    request = FlightSearchInput(
        origin="Kolkata",
        destination="Tokyo",
        departure_date=date(2026, 4, 1),
    )
    first = await provider.execute(request)
    second = await provider.execute(request)
    assert first == second
    assert len(first.options) >= 3
    assert all(option.price > 0 for option in first.options)
    assert all(option.currency == "USD" for option in first.options)


async def test_flight_mock_price_changes_with_cabin_class():
    provider = MockFlightProvider()
    economy = await provider.execute(
        FlightSearchInput(
            origin="Kolkata",
            destination="Tokyo",
            departure_date=date(2026, 4, 1),
            cabin_class=CabinClass.economy,
        )
    )
    business = await provider.execute(
        FlightSearchInput(
            origin="Kolkata",
            destination="Tokyo",
            departure_date=date(2026, 4, 1),
            cabin_class=CabinClass.business,
        )
    )
    assert business.options[0].price > economy.options[0].price


async def test_flight_mock_returns_empty_results_for_sentinel():
    provider = MockFlightProvider()
    result = await provider.execute(
        FlightSearchInput(
            origin="Kolkata",
            destination="Nowhere",
            departure_date=date(2026, 4, 1),
        )
    )
    assert result.options == []


async def test_hotel_mock_returns_valid_options():
    provider = MockHotelProvider()
    result = await provider.execute(
        HotelSearchInput(
            destination="Tokyo",
            check_in=date(2026, 4, 1),
            check_out=date(2026, 4, 7),
        )
    )
    assert len(result.options) >= 4
    assert all(0 <= option.rating <= 5 for option in result.options)
    assert all(option.price_per_night > 0 for option in result.options)


async def test_hotel_mock_applies_budget_filter():
    provider = MockHotelProvider()
    result = await provider.execute(
        HotelSearchInput(
            destination="Tokyo",
            check_in=date(2026, 4, 1),
            check_out=date(2026, 4, 7),
            budget_per_night=100,
        )
    )
    assert all(option.price_per_night <= 100 for option in result.options)


async def test_weather_mock_returns_requested_number_of_days():
    provider = MockWeatherProvider()
    result = await provider.execute(
        WeatherSearchInput(
            location="Tokyo",
            date=date(2026, 4, 1),
            days=5,
        )
    )
    assert len(result.forecasts) == 5
    dates = [forecast.date for forecast in result.forecasts]
    assert dates == sorted(dates)
    assert all(0 <= f.precipitation_probability <= 100 for f in result.forecasts)


async def test_currency_mock_conversion_is_deterministic():
    provider = MockCurrencyProvider()
    request = CurrencyConversionInput(source="USD", target="JPY", amount=1000)
    first = await provider.execute(request)
    second = await provider.execute(request)
    assert first == second
    assert first.converted_amount == 151000.0
    assert first.exchange_rate == 151.0


async def test_currency_mock_supports_reverse_conversion():
    provider = MockCurrencyProvider()
    result = await provider.execute(
        CurrencyConversionInput(source="JPY", target="USD", amount=151000)
    )
    assert result.converted_amount == pytest.approx(1000.0, abs=0.1)


async def test_currency_mock_falls_back_for_unknown_currency():
    provider = MockCurrencyProvider()
    result = await provider.execute(
        CurrencyConversionInput(source="USD", target="XXX", amount=100)
    )
    assert result.converted_amount == 100.0
