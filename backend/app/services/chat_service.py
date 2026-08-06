"""Chat service.

Executes the LangGraph travel workflow for each user message and formats
the result into a human-readable response. If the LLM is not configured,
it degrades gracefully instead of failing.
"""

import logging
from collections.abc import Callable
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


def format_result(result: dict[str, Any]) -> str:
    """Convert the final graph state into a user-facing message."""
    if result.get("status") == "failed":
        logger.error("Travel workflow failed: %s", result.get("error"))
        return FAILED_RESPONSE

    if result.get("final_response"):
        return result["final_response"]

    itinerary = result.get("itinerary")
    if itinerary:
        lines = [
            "Here is your travel plan for "
            f"{itinerary.get('destination') or 'your trip'}."
        ]
        for day in itinerary.get("days", []):
            activities = ", ".join(
                activity.get("name", "")
                for activity in day.get("activities", [])
                if activity.get("name")
            )
            lines.append(f"Day {day.get('day')}: {activities or 'free time'}")
        if itinerary.get("summary"):
            lines.append(itinerary["summary"])
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
            logger.error("Travel workflow execution failed: %s", exc, exc_info=True)
            return ChatResponse(response=FAILED_RESPONSE)

        return ChatResponse(response=format_result(result))
