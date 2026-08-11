"""Tests for the weather tool execution and failure handling."""

import pytest
from langchain_core.tools import ToolException
from pydantic import ValidationError

from app.tools.mocks import MockWeatherProvider
from app.tools.weather import WeatherTool
from tests.fakes.fake_providers import BoomProvider, MalformedProvider, SlowProvider

VALID_ARGS = {
    "location": "Tokyo",
    "date": "2026-04-01",
    "days": 3,
}


async def test_weather_tool_returns_structured_result():
    tool = WeatherTool(provider=MockWeatherProvider())
    result = await tool.ainvoke(VALID_ARGS)
    assert set(result) == {"location", "forecasts", "provider"}
    assert len(result["forecasts"]) == 3
    forecast = result["forecasts"][0]
    assert {
        "date",
        "temperature_celsius",
        "condition",
        "precipitation_probability",
        "wind_speed_kmh",
    }.issubset(forecast)


async def test_weather_tool_rejects_invalid_input():
    tool = WeatherTool(provider=MockWeatherProvider())
    with pytest.raises(ValidationError):
        await tool.ainvoke({**VALID_ARGS, "days": 0})


async def test_weather_tool_supports_single_day():
    tool = WeatherTool(provider=MockWeatherProvider())
    result = await tool.ainvoke({"location": "Tokyo", "date": "2026-04-01"})
    assert len(result["forecasts"]) == 1


async def test_weather_tool_handles_provider_failure_gracefully():
    tool = WeatherTool(provider=BoomProvider())
    with pytest.raises(ToolException) as excinfo:
        await tool.ainvoke(VALID_ARGS)
    message = str(excinfo.value)
    assert "temporarily unavailable" in message
    assert "supersecret" not in message


async def test_weather_tool_handles_timeout():
    tool = WeatherTool(provider=SlowProvider(delay=0.2), timeout_seconds=0.05)
    with pytest.raises(ToolException) as excinfo:
        await tool.ainvoke(VALID_ARGS)
    assert "timed out" in str(excinfo.value)


async def test_weather_tool_handles_malformed_response():
    tool = WeatherTool(provider=MalformedProvider())
    with pytest.raises(ToolException) as excinfo:
        await tool.ainvoke(VALID_ARGS)
    assert "malformed" in str(excinfo.value)
