"""Hotel search tool exposed through the LangChain tool interface."""

from abc import ABC

from app.schemas.tools import HotelSearchInput, HotelSearchOutput
from app.tools.base import BaseTravelTool, TravelProvider


class HotelProvider(TravelProvider, ABC):
    """Interface for hotel search providers (mock or real)."""


class HotelSearchTool(BaseTravelTool):
    name: str = "search_hotels"
    description: str = (
        "Search available hotel options for a destination and stay dates. "
        "Use when the user asks about accommodation, places to stay, or "
        "hotel prices."
    )
    args_schema: type[HotelSearchInput] = HotelSearchInput
    input_schema_model: type[HotelSearchInput] = HotelSearchInput
    output_schema_model: type[HotelSearchOutput] = HotelSearchOutput
