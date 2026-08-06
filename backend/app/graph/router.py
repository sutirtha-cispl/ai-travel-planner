"""Workflow routing logic.

Translates the supervisor's decision into the next graph node.
Acts as a safety net: unknown or missing decisions terminate the workflow.
"""

from typing import Any

from langgraph.graph import END

ROUTE_PATH_MAP: dict[str, str] = {
    "planner": "planner",
    "itinerary": "itinerary",
    "review": "review",
    "ask_user": END,
    "end": END,
}


def route_workflow(state: dict[str, Any]) -> str:
    """Return the graph destination for the current state.

    The supervisor writes ``state["next_agent"]``; the router maps it to a
    concrete node. Anything unrecognized defaults to ``end`` so the graph
    always terminates.
    """
    next_agent = state.get("next_agent", "end")
    if next_agent not in ROUTE_PATH_MAP:
        return "end"
    return next_agent
