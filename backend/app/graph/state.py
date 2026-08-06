"""Shared LangGraph state for the travel planning workflow.

TravelState is the single source of truth shared by all agents.
Every agent reads the fields it needs and updates only the fields it owns.
"""

from typing import Any, TypedDict


class TravelState(TypedDict, total=False):
    # Conversation context
    conversation_id: str
    messages: list[dict[str, str]]
    user_message: str

    # Requirements (owned by the Requirement Agent)
    destination: str | None
    travel_dates: dict[str, str] | None
    duration: int | None
    travelers: int | None
    budget: int | None
    preferences: list[str]
    requirements: dict[str, Any]
    missing_fields: list[str]

    # Planning artifacts
    strategy: dict[str, Any]
    itinerary: dict[str, Any]

    # Review results (owned by the Review Agent)
    review_notes: list[dict[str, str]]
    approved: bool
    issues: list[str]
    suggestions: list[str]

    # Routing and execution control (owned by the Supervisor Agent)
    next_agent: str
    reason: str

    # Execution status
    status: str
    error: str | None
    final_response: str
