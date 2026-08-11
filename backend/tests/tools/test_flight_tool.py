"""Tests for the flight search tool execution and failure handling."""

import pytest
from langchain_core.tools import ToolException
from pydantic import ValidationError

from app.tools.flights import FlightSearchTool
from app.tools.mocks import MockFlightProvider
from tests.fakes.fake_providers import BoomProvider, MalformedProvider, SlowProvider

VALID_ARGS = {
    "origin": "Kolkata",
    "destination": "Tokyo",
    "departure_date": "2026-04-01",
    "return_date": "2026-04-08",
    "passengers": 2,
    "cabin_class": "business",
}


async def test_flight_tool_returns_structured_result():
    tool = FlightSearchTool(provider=MockFlightProvider())
    result = await tool.ainvoke(VALID_ARGS)
    assert set(result) == {
        "origin",
        "destination",
        "departure_date",
        "options",
        "provider",
    }
    assert len(result["options"]) >= 3
    assert result["provider"] == "mock"
    option = result["options"][0]
    assert {"airline", "flight_number", "price", "currency"}.issubset(option)


async def test_flight_tool_rejects_invalid_input():
    tool = FlightSearchTool(provider=MockFlightProvider())
    with pytest.raises(ValidationError):
        await tool.ainvoke({**VALID_ARGS, "passengers": 0})


async def test_flight_tool_returns_empty_results_for_sentinel():
    tool = FlightSearchTool(provider=MockFlightProvider())
    result = await tool.ainvoke({**VALID_ARGS, "destination": "Nowhere"})
    assert result["options"] == []


async def test_flight_tool_handles_provider_failure_gracefully():
    tool = FlightSearchTool(provider=BoomProvider())
    with pytest.raises(ToolException) as excinfo:
        await tool.ainvoke(VALID_ARGS)
    message = str(excinfo.value)
    assert "temporarily unavailable" in message
    assert "supersecret" not in message
    assert "boom" not in message


async def test_flight_tool_handles_timeout():
    tool = FlightSearchTool(provider=SlowProvider(delay=0.2), timeout_seconds=0.05)
    with pytest.raises(ToolException) as excinfo:
        await tool.ainvoke(VALID_ARGS)
    assert "timed out" in str(excinfo.value)


async def test_flight_tool_handles_malformed_response():
    tool = FlightSearchTool(provider=MalformedProvider())
    with pytest.raises(ToolException) as excinfo:
        await tool.ainvoke(VALID_ARGS)
    assert "malformed" in str(excinfo.value)
