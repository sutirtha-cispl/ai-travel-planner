"""Deterministic mock weather provider (offline, no API keys required)."""

from datetime import timedelta

from app.schemas.tools import (
    WeatherForecast,
    WeatherSearchInput,
    WeatherSearchOutput,
)
from app.tools.base import TravelProvider
from app.tools.mocks.base import stable_seed

_CONDITIONS = [
    "Sunny",
    "Clear",
    "Partly cloudy",
    "Cloudy",
    "Light rain",
    "Overcast",
]

_WIND_DIRECTIONS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


class MockWeatherProvider(TravelProvider):
    """Returns stable daily forecasts for the requested location."""

    async def execute(self, request: WeatherSearchInput) -> WeatherSearchOutput:
        seed = stable_seed(f"{request.location}:{request.date}")
        base_temp = round(-5.0 + (seed % 400) / 10, 1)
        base_condition = _CONDITIONS[seed % len(_CONDITIONS)]
        base_wind = float(2 + (seed % 28))

        forecasts = []
        for day_offset in range(request.days):
            day_seed = stable_seed(
                f"{request.location}:{request.date}:{day_offset}"
            )
            forecast_date = request.date + timedelta(days=day_offset)
            forecasts.append(
                WeatherForecast(
                    date=forecast_date,
                    temperature_celsius=round(
                        base_temp + ((day_seed % 60) / 10) - 3, 1
                    ),
                    condition=_CONDITIONS[(seed + day_offset) % len(_CONDITIONS)]
                    if day_offset
                    else base_condition,
                    precipitation_probability=(seed + day_offset * 7) % 100,
                    wind_speed_kmh=round(base_wind + (day_seed % 9), 1),
                    wind_direction=_WIND_DIRECTIONS[
                        (seed + day_offset) % len(_WIND_DIRECTIONS)
                    ],
                )
            )

        return WeatherSearchOutput(
            location=request.location,
            forecasts=forecasts,
        )
