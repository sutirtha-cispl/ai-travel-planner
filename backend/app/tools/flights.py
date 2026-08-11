"""Flight search tool exposed through the LangChain tool interface."""

from abc import ABC

from app.schemas.tools import FlightSearchInput, FlightSearchOutput
from app.tools.base import BaseTravelTool, TravelProvider


class FlightProvider(TravelProvider, ABC):
    """Interface for flight search providers (mock or real)."""


class FlightSearchTool(BaseTravelTool):
    name: str = "search_flights"
    description: str = (
        "Search available flight options between an origin and a destination "
        "on a given date. Use when the user asks about flights, airfare, or "
        "how to get to a destination."
    )
    args_schema: type[FlightSearchInput] = FlightSearchInput
    input_schema_model: type[FlightSearchInput] = FlightSearchInput
    output_schema_model: type[FlightSearchOutput] = FlightSearchOutput
