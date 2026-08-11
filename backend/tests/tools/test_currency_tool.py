"""Tests for the currency conversion tool execution and failure handling."""

import pytest
from langchain_core.tools import ToolException
from pydantic import ValidationError

from app.tools.currency import CurrencyTool
from app.tools.mocks import MockCurrencyProvider
from tests.fakes.fake_providers import BoomProvider, MalformedProvider, SlowProvider

VALID_ARGS = {"source": "USD", "target": "JPY", "amount": 1000}


async def test_currency_tool_returns_structured_result():
    tool = CurrencyTool(provider=MockCurrencyProvider())
    result = await tool.ainvoke(VALID_ARGS)
    assert set(result) == {
        "source",
        "target",
        "amount",
        "exchange_rate",
        "converted_amount",
        "provider",
    }
    assert result["converted_amount"] == 151000.0


async def test_currency_tool_rejects_invalid_input():
    tool = CurrencyTool(provider=MockCurrencyProvider())
    with pytest.raises(ValidationError):
        await tool.ainvoke({**VALID_ARGS, "source": "usd"})


async def test_currency_tool_handles_provider_failure_gracefully():
    tool = CurrencyTool(provider=BoomProvider())
    with pytest.raises(ToolException) as excinfo:
        await tool.ainvoke(VALID_ARGS)
    message = str(excinfo.value)
    assert "temporarily unavailable" in message
    assert "supersecret" not in message


async def test_currency_tool_handles_timeout():
    tool = CurrencyTool(provider=SlowProvider(delay=0.2), timeout_seconds=0.05)
    with pytest.raises(ToolException) as excinfo:
        await tool.ainvoke(VALID_ARGS)
    assert "timed out" in str(excinfo.value)


async def test_currency_tool_handles_malformed_response():
    tool = CurrencyTool(provider=MalformedProvider())
    with pytest.raises(ToolException) as excinfo:
        await tool.ainvoke(VALID_ARGS)
    assert "malformed" in str(excinfo.value)
