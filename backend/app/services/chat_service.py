"""Chat service.

Executes the LangGraph travel workflow for each user message and formats
the result into a human-readable response. If the LLM is not configured,
it degrades gracefully instead of failing.
"""

import logging
from collections.abc import Callable
from datetime import datetime
from typing import Any
from uuid import uuid4

from app.config.settings import settings
from app.graph.workflow import build_initial_state, build_workflow
from app.schemas.chat import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

NOT_CONFIGURED_RESPONSE = (
    "AI travel planning is not configured yet. "
    "Set OPENAI_API_KEY and restart the backend to enable it."
)
FAILED_RESPONSE = "I could not complete the travel plan. Please try again."
RATE_LIMITED_RESPONSE = (
    "The AI service is temporarily rate-limited because the daily token quota "
    "was exceeded. Please try again later, or upgrade the plan at your "
    "provider console."
)

# Substrings that identify provider rate-limit errors across backends.
_RATE_LIMIT_MARKERS = (
    "rate_limit_exceeded",
    "rate limit",
    "code: 429",
)


def _is_rate_limit_error(message: str) -> bool:
    lowered = message.lower()
    return any(marker in lowered for marker in _RATE_LIMIT_MARKERS)

# Emoji used when an activity category cannot be matched.
_DEFAULT_ACTIVITY_EMOJI = "📍"

# Keyword -> emoji mapping for activity categories. Categories are free-form
# strings produced by the LLM, so matching is intentionally permissive.
_CATEGORY_EMOJIS: list[tuple[str, str]] = [
    ("museum", "🏛️"),
    ("gallery", "🖼️"),
    ("art", "🎨"),
    ("temple", "🛕"),
    ("church", "⛪"),
    ("history", "🏛️"),
    ("culture", "🎭"),
    ("sight", "📷"),
    ("landmark", "🗼"),
    ("beach", "🏖️"),
    ("snorkel", "🤿"),
    ("dive", "🤿"),
    ("swim", "🏊"),
    ("surf", "🏄"),
    ("water", "🌊"),
    ("boat", "🚤"),
    ("cruise", "🚢"),
    ("cooking", "👨‍🍳"),
    ("food", "🍽️"),
    ("restaurant", "🍴"),
    ("cuisine", "🥘"),
    ("wine", "🍷"),
    ("shopping", "🛍️"),
    ("market", "🛒"),
    ("adventure", "🧗"),
    ("hiking", "🥾"),
    ("trek", "🥾"),
    ("sport", "⚽"),
    ("yoga", "🧘"),
    ("spa", "💆"),
    ("massage", "💆"),
    ("relax", "🌴"),
    ("nature", "🌿"),
    ("wildlife", "🦜"),
    ("park", "🌳"),
    ("night", "🌙"),
    ("flight", "✈️"),
    ("transport", "🚗"),
    ("depart", "🛫"),
]


def _format_budget(budget: int | None) -> str:
    if budget is None:
        return ""
    return f"${budget:,}"


def _format_date(value: str) -> str:
    for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(value, fmt).strftime("%b %d, %Y")
        except ValueError:
            continue
    return value


def _activity_emoji(category: str) -> str:
    lowered = category.lower()
    for keyword, emoji in _CATEGORY_EMOJIS:
        if keyword in lowered:
            return emoji
    return _DEFAULT_ACTIVITY_EMOJI


def _format_activity(activity: dict[str, Any]) -> str:
    name = activity.get("name", "")
    emoji = _activity_emoji(activity.get("category", ""))
    time = activity.get("time")
    line = f"- 🕘 {time} · {emoji} **{name}**" if time else f"- {emoji} **{name}**"
    description = activity.get("description")
    if description:
        line += f" — {description}"
    cost = activity.get("estimated_cost")
    if cost:
        line += f" (💵 {_format_budget(cost)})"
    return line


def _format_day(day: dict[str, Any]) -> list[str]:
    lines = [f"### 📅 Day {day.get('day', '')}".rstrip()]
    title = day.get("title")
    if title:
        lines[0] += f" — {title}"
    activities = [
        activity for activity in day.get("activities", []) if activity.get("name")
    ]
    if activities:
        lines.extend(_format_activity(activity) for activity in activities)
    else:
        lines.append("- Free time")
    notes = day.get("notes")
    if notes:
        lines.append(f"📝 *{notes}*")
    return lines


def _format_trip_header(result: dict[str, Any]) -> str:
    destination = result.get("destination") or result.get("itinerary", {}).get(
        "destination"
    )
    title = f"## 🗺️ Your Trip to {destination}" if destination else "## 🗺️ Your Trip"

    origin = result.get("origin")
    travel_dates = result.get("travel_dates") or {}
    travelers = result.get("travelers")
    budget = result.get("budget")

    details: list[str] = []
    if origin and destination:
        details.append(f"📍 **From:** {origin} → {destination}")
    elif origin:
        details.append(f"📍 **From:** {origin}")
    start = travel_dates.get("start") or travel_dates.get("check_in")
    end = travel_dates.get("end") or travel_dates.get("check_out")
    if start:
        date_label = f"**{_format_date(start)}**"
        if end:
            date_label += f" – **{_format_date(end)}**"
        details.append(f"📅 **Dates:** {date_label}")
    if travelers:
        label = "adult" if travelers == 1 else "adults"
        details.append(f"👥 **Travelers:** {travelers} {label}")
    if budget:
        details.append(f"💰 **Budget:** {_format_budget(budget)}")

    lines = [title]
    if details:
        lines.append("\n" + "  |  ".join(details))
    return "\n".join(lines)


def format_result(result: dict[str, Any]) -> str:
    """Convert the final graph state into a user-facing message."""
    if result.get("status") == "failed":
        error = str(result.get("error") or "")
        logger.error("Travel workflow failed: %s", error)
        if _is_rate_limit_error(error):
            return RATE_LIMITED_RESPONSE
        return FAILED_RESPONSE

    if result.get("final_response"):
        return result["final_response"]

    itinerary = result.get("itinerary")
    if itinerary:
        lines = [_format_trip_header(result)]
        for day in itinerary.get("days", []):
            lines.extend(_format_day(day))
        if itinerary.get("summary"):
            lines.extend(["", "### ✨ Summary", itinerary["summary"]])
        return "\n".join(lines)

    return "I don't have enough information to create a plan yet."


class ChatService:
    def __init__(
        self,
        workflow_factory: Callable[[], Any] | None = None,
    ) -> None:
        self._workflow_factory = workflow_factory or build_workflow

    def _initial_state(self, request: ChatRequest) -> dict[str, Any]:
        state = build_initial_state(request.message)
        state["conversation_id"] = uuid4().hex
        return state

    async def send_message(self, request: ChatRequest) -> ChatResponse:
        if not settings.OPENAI_API_KEY:
            return ChatResponse(response=NOT_CONFIGURED_RESPONSE)

        try:
            result = await self._workflow_factory().ainvoke(
                self._initial_state(request)
            )
        except Exception as exc:
            logger.error(
                "Travel workflow execution failed: %s", exc, exc_info=True
            )
            if _is_rate_limit_error(str(exc)):
                return ChatResponse(response=RATE_LIMITED_RESPONSE)
            return ChatResponse(response=FAILED_RESPONSE)

        return ChatResponse(response=format_result(result))
