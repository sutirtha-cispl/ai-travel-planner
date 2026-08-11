"""Tests for the hotel search tool execution and failure handling."""

import pytest
from langchain_core.tools import ToolException
from pydantic import ValidationError

from app.tools.hotels import HotelSearchTool
from app.tools.mocks import MockHotelProvider
from tests.fakes.fake_providers import BoomProvider, MalformedProvider, SlowProvider

VALID_ARGS = {
    "destination": "Tokyo",
    "check_in": "2026-04-01",
    "check_out": "2026-04-07",
    "guests": 2,
    "rooms": 1,
}


async def test_hotel_tool_returns_structured_result():
    tool = HotelSearchTool(provider=MockHotelProvider())
    result = await tool.ainvoke(VALID_ARGS)
    assert set(result) == {
        "destination",
        "check_in",
        "check_out",
        "options",
        "provider",
    }
    assert len(result["options"]) >= 4
    option = result["options"][0]
    assert {"name", "rating", "price_per_night", "amenities"}.issubset(option)


async def test_hotel_tool_rejects_invalid_input():
    tool = HotelSearchTool(provider=MockHotelProvider())
    with pytest.raises(ValidationError):
        await tool.ainvoke({**VALID_ARGS, "check_in": "not-a-date"})


async def test_hotel_tool_returns_empty_results_for_sentinel():
    tool = HotelSearchTool(provider=MockHotelProvider())
    result = await tool.ainvoke({**VALID_ARGS, "destination": "Nowhere"})
    assert result["options"] == []


async def test_hotel_tool_handles_provider_failure_gracefully():
    tool = HotelSearchTool(provider=BoomProvider())
    with pytest.raises(ToolException) as excinfo:
        await tool.ainvoke(VALID_ARGS)
    message = str(excinfo.value)
    assert "temporarily unavailable" in message
    assert "supersecret" not in message


async def test_hotel_tool_handles_timeout():
    tool = HotelSearchTool(provider=SlowProvider(delay=0.2), timeout_seconds=0.05)
    with pytest.raises(ToolException) as excinfo:
        await tool.ainvoke(VALID_ARGS)
    assert "timed out" in str(excinfo.value)


async def test_hotel_tool_handles_malformed_response():
    tool = HotelSearchTool(provider=MalformedProvider())
    with pytest.raises(ToolException) as excinfo:
        await tool.ainvoke(VALID_ARGS)
    assert "malformed" in str(excinfo.value)
