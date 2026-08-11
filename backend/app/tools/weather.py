"""Weather tool exposed through the LangChain tool interface."""

from abc import ABC

from app.schemas.tools import WeatherSearchInput, WeatherSearchOutput
from app.tools.base import BaseTravelTool, TravelProvider


class WeatherProvider(TravelProvider, ABC):
    """Interface for weather providers (mock or real)."""


class WeatherTool(BaseTravelTool):
    name: str = "get_weather_forecast"
    description: str = (
        "Get a weather forecast for a location on a given date, optionally "
        "for several consecutive days. Use when the user asks about weather, "
        "temperature, rain, or travel conditions."
    )
    args_schema: type[WeatherSearchInput] = WeatherSearchInput
    input_schema_model: type[WeatherSearchInput] = WeatherSearchInput
    output_schema_model: type[WeatherSearchOutput] = WeatherSearchOutput
