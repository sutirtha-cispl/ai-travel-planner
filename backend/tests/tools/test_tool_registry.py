"""Tests for the tool registry."""

from app.services.tool_service import build_default_registry
from app.tools.registry import ToolRegistry
from app.tools.weather import WeatherTool
from tests.fakes.fake_providers import BoomProvider


def test_default_registry_exposes_all_tools():
    registry = build_default_registry()
    assert len(registry) == 4
    assert set(registry.names) == {
        "search_flights",
        "search_hotels",
        "get_weather_forecast",
        "convert_currency",
    }


def test_registry_get_returns_tool_by_name():
    registry = build_default_registry()
    assert registry.get("search_flights").name == "search_flights"


def test_registry_get_returns_none_for_unknown_tool():
    registry = build_default_registry()
    assert registry.get("book_taxi") is None


def test_registry_accepts_custom_tools():
    registry = ToolRegistry([WeatherTool(provider=BoomProvider())])
    assert registry.names == ["get_weather_forecast"]
    assert len(registry) == 1
