"""Tool service.

Coordinates travel tools for agents and the application.

The service owns the "which tool, which arguments" decisions (e.g. building
tool requests from extracted travel requirements) and normalizes every tool
outcome into structured, safe results so agents never see raw exceptions.
"""

import asyncio
import logging
from datetime import date, datetime, timedelta
from typing import Any

from langchain_core.tools import ToolException
from pydantic import ValidationError

from app.config.settings import settings
from app.schemas.tools import (
    CurrencyConversionInput,
    FlightSearchInput,
    HotelSearchInput,
    WeatherSearchInput,
)
from app.tools.currency import CurrencyTool
from app.tools.flights import FlightSearchTool
from app.tools.hotels import HotelSearchTool
from app.tools.mocks import (
    MockCurrencyProvider,
    MockFlightProvider,
    MockHotelProvider,
    MockWeatherProvider,
)
from app.tools.registry import ToolRegistry
from app.tools.weather import WeatherTool

logger = logging.getLogger(__name__)

MAX_FORECAST_DAYS = 14

# Fallback currency per popular destination, used to make budget conversions
# useful during planning. Real providers will replace this mapping later.
DESTINATION_CURRENCIES: dict[str, str] = {
    "japan": "JPY",
    "tokyo": "JPY",
    "osaka": "JPY",
    "india": "INR",
    "kolkata": "INR",
    "mumbai": "INR",
    "delhi": "INR",
    "united states": "USD",
    "usa": "USD",
    "new york": "USD",
    "united kingdom": "GBP",
    "uk": "GBP",
    "london": "GBP",
    "europe": "EUR",
    "france": "EUR",
    "paris": "EUR",
    "germany": "EUR",
    "italy": "EUR",
    "spain": "EUR",
    "thailand": "THB",
    "bangkok": "THB",
    "south korea": "KRW",
    "korea": "KRW",
    "seoul": "KRW",
    "australia": "AUD",
    "sydney": "AUD",
    "singapore": "SGD",
    "china": "CNY",
    "beijing": "CNY",
    "shanghai": "CNY",
    "uae": "AED",
    "dubai": "AED",
    "switzerland": "CHF",
    "canada": "CAD",
    "toronto": "CAD",
    "mexico": "MXN",
    "brazil": "BRL",
    "south africa": "ZAR",
}

_TOOL_NAMES = (
    "search_flights",
    "search_hotels",
    "get_weather_forecast",
    "convert_currency",
)


def build_default_registry(
    provider_name: str | None = None,
    timeout_seconds: float | None = None,
) -> ToolRegistry:
    """Build the default tool registry.

    Only mock providers exist today; requesting any other provider name logs
    a warning and falls back to mocks so the application keeps working offline.
    """
    name = (provider_name or settings.TOOLS_PROVIDER or "mock").lower()
    timeout = (
        timeout_seconds
        if timeout_seconds is not None
        else settings.TOOL_TIMEOUT_SECONDS
    )
    if name != "mock":
        logger.warning(
            "Tool provider '%s' is not implemented; falling back to mock providers.",
            name,
        )
    return ToolRegistry(
        [
            FlightSearchTool(provider=MockFlightProvider(), timeout_seconds=timeout),
            HotelSearchTool(provider=MockHotelProvider(), timeout_seconds=timeout),
            WeatherTool(provider=MockWeatherProvider(), timeout_seconds=timeout),
            CurrencyTool(provider=MockCurrencyProvider(), timeout_seconds=timeout),
        ]
    )


def build_tool_service(registry: ToolRegistry | None = None) -> "ToolService":
    """Build a ToolService with the default (mock) registry."""
    return ToolService(registry=registry or build_default_registry())


def _parse_date(value: Any) -> date | None:
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


def _date_bounds(requirements: dict[str, Any]) -> tuple[date, date]:
    travel_dates = requirements.get("travel_dates") or {}
    start = _parse_date(travel_dates.get("start") or travel_dates.get("check_in"))
    end = _parse_date(travel_dates.get("end") or travel_dates.get("check_out"))
    duration = max(int(requirements.get("duration") or 1), 1)
    if start is None:
        start = date.today()
    if end is None or end < start:
        end = start + timedelta(days=duration)
    return start, end


def _destination_currency(destination: str) -> str:
    return DESTINATION_CURRENCIES.get(destination.strip().lower(), "USD")


class ToolService:
    """Runs travel tools safely and builds tool requests from requirements."""

    def __init__(self, registry: ToolRegistry | None = None) -> None:
        self._registry = registry or build_default_registry()

    @property
    def registry(self) -> ToolRegistry:
        return self._registry

    def list_tools(self) -> list[dict[str, str]]:
        return [
            {"name": tool.name, "description": tool.description}
            for tool in self._registry.all
        ]

    def get_tool(self, name: str):
        return self._registry.get(name)

    async def run(self, tool_name: str, **kwargs: Any) -> dict[str, Any]:
        """Execute a tool by name and normalize the outcome.

        Returns:
            On success: ``{"success": True, "tool": name, "result": {...}}``.
            On failure: ``{"success": False, "tool": name, "error": "<safe message>"}``.
        """
        tool = self._registry.get(tool_name)
        if tool is None:
            return {
                "success": False,
                "tool": tool_name,
                "error": f"Unknown tool: {tool_name}",
            }
        try:
            result = await tool.ainvoke(kwargs)
            return {"success": True, "tool": tool_name, "result": result}
        except (ToolException, ValidationError) as exc:
            return {"success": False, "tool": tool_name, "error": str(exc)}
        except Exception as exc:
            logger.error(
                "Tool '%s' failed unexpectedly: %s", tool_name, exc, exc_info=True
            )
            return {
                "success": False,
                "tool": tool_name,
                "error": f"{tool_name} failed unexpectedly. Please try again later.",
            }

    async def collect_for_requirements(
        self, requirements: dict[str, Any]
    ) -> dict[str, Any]:
        """Build and run tool requests from extracted travel requirements.

        Returns a dict keyed by tool name. Each entry is
        ``{"status": "ok", "data": {...}}`` or
        ``{"status": "error", "message": "..."}``. Returns an empty dict when
        there is not enough information (no destination) to run any tool.
        """
        destination = (requirements.get("destination") or "").strip()
        if not destination:
            return {}

        start, end = _date_bounds(requirements)
        duration = max(int(requirements.get("duration") or 1), 1)
        travelers = int(requirements.get("travelers") or 1)
        budget = requirements.get("budget")

        request_specs: dict[str, dict[str, Any]] = {
            "search_flights": FlightSearchInput(
                origin=requirements.get("origin") or settings.DEFAULT_ORIGIN,
                destination=destination,
                departure_date=start,
                return_date=end,
                passengers=min(travelers, 9),
                cabin_class="economy",
            ).model_dump(mode="json"),
            "search_hotels": HotelSearchInput(
                destination=destination,
                check_in=start,
                check_out=end,
                guests=min(travelers, 10),
                rooms=1,
                budget_per_night=(int(budget // duration) if budget else None),
            ).model_dump(mode="json"),
            "get_weather_forecast": WeatherSearchInput(
                location=destination,
                date=start,
                days=min(duration, MAX_FORECAST_DAYS),
            ).model_dump(mode="json"),
            "convert_currency": CurrencyConversionInput(
                source="USD",
                target=_destination_currency(destination),
                amount=float(budget) if budget else 1000.0,
            ).model_dump(mode="json"),
        }

        return await _run_entries(self._registry, request_specs)


async def _run_entries(
    registry: ToolRegistry, request_specs: dict[str, dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    """Run multiple tools concurrently and normalize each result."""

    async def run_one(name: str, kwargs: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        tool = registry.get(name)
        if tool is None:
            return name, {"status": "error", "message": f"Unknown tool: {name}"}
        try:
            result = await tool.ainvoke(kwargs)
            return name, {"status": "ok", "data": result}
        except (ToolException, ValidationError) as exc:
            return name, {"status": "error", "message": str(exc)}
        except Exception as exc:
            logger.error(
                "Tool '%s' failed unexpectedly: %s", name, exc, exc_info=True
            )
            return name, {
                "status": "error",
                "message": f"{name} failed unexpectedly. Please try again later.",
            }

    results = await asyncio.gather(
        *(run_one(name, kwargs) for name, kwargs in request_specs.items()),
        return_exceptions=True,
    )
    entries: dict[str, dict[str, Any]] = {}
    for item in results:
        if isinstance(item, BaseException):
            logger.error("Tool execution raised: %s", item)
            continue
        name, entry = item
        entries[name] = entry
    return entries
