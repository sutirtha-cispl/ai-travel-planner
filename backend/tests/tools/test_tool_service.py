"""Tests for the tool service orchestration."""

from app.services.tool_service import ToolService
from app.tools.currency import CurrencyTool
from app.tools.flights import FlightSearchTool
from app.tools.hotels import HotelSearchTool
from app.tools.mocks import (
    MockCurrencyProvider,
    MockFlightProvider,
    MockWeatherProvider,
)
from app.tools.registry import ToolRegistry
from app.tools.weather import WeatherTool
from tests.fakes.fake_providers import BoomProvider

JAPAN_REQUIREMENTS = {
    "destination": "Japan",
    "duration": 7,
    "travelers": 2,
    "budget": 2000,
    "preferences": ["food", "culture"],
    "travel_dates": {"start": "2026-04-01", "end": "2026-04-08"},
}


async def test_list_tools_describes_all_tools():
    service = ToolService()
    tools = service.list_tools()
    assert len(tools) == 4
    assert all("name" in tool and "description" in tool for tool in tools)


async def test_run_success():
    service = ToolService()
    result = await service.run(
        "convert_currency", source="USD", target="JPY", amount=100
    )
    assert result["success"] is True
    assert result["tool"] == "convert_currency"
    assert result["result"]["converted_amount"] == 15100.0


async def test_run_unknown_tool():
    service = ToolService()
    result = await service.run("book_taxi")
    assert result["success"] is False
    assert "Unknown tool" in result["error"]


async def test_run_invalid_input_returns_safe_error():
    service = ToolService()
    result = await service.run(
        "convert_currency", source="usd", target="JPY", amount=100
    )
    assert result["success"] is False
    assert "error" in result


async def test_run_provider_failure_returns_safe_error():
    registry = ToolRegistry(
        [CurrencyTool(provider=BoomProvider(), timeout_seconds=0.5)]
    )
    service = ToolService(registry=registry)
    result = await service.run(
        "convert_currency", source="USD", target="JPY", amount=100
    )
    assert result["success"] is False
    assert "supersecret" not in result["error"]
    assert result["error"]


async def test_collect_for_requirements_runs_all_tools():
    service = ToolService()
    result = await service.collect_for_requirements(JAPAN_REQUIREMENTS)
    assert set(result) == {
        "search_flights",
        "search_hotels",
        "get_weather_forecast",
        "convert_currency",
    }
    for entry in result.values():
        assert entry["status"] == "ok"
        assert "data" in entry


async def test_collect_returns_empty_without_destination():
    service = ToolService()
    assert await service.collect_for_requirements({}) == {}
    assert await service.collect_for_requirements({"duration": 3}) == {}


async def test_collect_builds_currency_request_from_destination():
    service = ToolService()
    result = await service.collect_for_requirements(
        {**JAPAN_REQUIREMENTS, "destination": "Tokyo"}
    )
    currency = result["convert_currency"]["data"]
    assert currency["target"] == "JPY"
    assert currency["amount"] == 2000.0


async def test_collect_records_partial_failures_gracefully():
    registry = ToolRegistry(
        [
            FlightSearchTool(provider=MockFlightProvider()),
            HotelSearchTool(provider=BoomProvider(), timeout_seconds=0.5),
            WeatherTool(provider=MockWeatherProvider()),
            CurrencyTool(provider=MockCurrencyProvider()),
        ]
    )
    service = ToolService(registry=registry)
    result = await service.collect_for_requirements(JAPAN_REQUIREMENTS)
    assert result["search_hotels"]["status"] == "error"
    assert "supersecret" not in result["search_hotels"]["message"]
    assert result["search_flights"]["status"] == "ok"


async def test_collect_never_raises_for_unknown_requirements():
    service = ToolService()
    result = await service.collect_for_requirements(
        {"destination": "Japan", "travel_dates": {"start": "not-a-date"}}
    )
    for entry in result.values():
        assert entry["status"] in ("ok", "error")


async def test_get_tool_returns_tool_instance():
    service = ToolService()
    assert service.get_tool("search_hotels").name == "search_hotels"
    assert service.get_tool("missing") is None
