"""Currency conversion tool exposed through the LangChain tool interface."""

from abc import ABC

from app.schemas.tools import (
    CurrencyConversionInput,
    CurrencyConversionOutput,
)
from app.tools.base import BaseTravelTool, TravelProvider


class CurrencyProvider(TravelProvider, ABC):
    """Interface for currency conversion providers (mock or real)."""


class CurrencyTool(BaseTravelTool):
    name: str = "convert_currency"
    description: str = (
        "Convert an amount from one currency to another using current "
        "exchange rates. Use when the user asks about budget, prices in "
        "another currency, or cost conversions."
    )
    args_schema: type[CurrencyConversionInput] = CurrencyConversionInput
    input_schema_model: type[CurrencyConversionInput] = CurrencyConversionInput
    output_schema_model: type[CurrencyConversionOutput] = CurrencyConversionOutput
