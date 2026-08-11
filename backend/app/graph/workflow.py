"""LangGraph workflow for the travel planning pipeline.

Flow::

    START -> requirement -> supervisor -> (planner | itinerary | review | end)
    planner -> itinerary -> review -> END

The supervisor only routes. Planning artifacts are produced by the
specialized agents and shared through TravelState.
"""

from typing import Any

from langgraph.graph import END, START, StateGraph

from app.agents.base_agent import BaseAgent
from app.agents.itinerary_agent import ItineraryAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.requirement_agent import RequirementAgent
from app.agents.review_agent import ReviewAgent
from app.agents.supervisor_agent import SupervisorAgent
from app.graph.router import ROUTE_PATH_MAP, route_workflow
from app.graph.state import TravelState


def default_agents() -> dict[str, BaseAgent]:
    """Build the default agent set for the workflow."""
    return {
        "requirement": RequirementAgent(),
        "supervisor": SupervisorAgent(),
        "planner": PlannerAgent(),
        "itinerary": ItineraryAgent(),
        "review": ReviewAgent(),
    }


def build_workflow(agents: dict[str, BaseAgent] | None = None) -> Any:
    """Compile and return the travel planning graph.

    Args:
        agents: Optional agent map for dependency injection (used by tests).
    """
    nodes = agents or default_agents()

    workflow = StateGraph(TravelState)

    workflow.add_node("requirement", nodes["requirement"].execute)
    workflow.add_node("supervisor", nodes["supervisor"].execute)
    workflow.add_node("planner", nodes["planner"].execute)
    workflow.add_node("itinerary", nodes["itinerary"].execute)
    workflow.add_node("review", nodes["review"].execute)

    workflow.add_edge(START, "requirement")
    workflow.add_edge("requirement", "supervisor")
    workflow.add_conditional_edges("supervisor", route_workflow, ROUTE_PATH_MAP)
    workflow.add_edge("planner", "itinerary")
    workflow.add_edge("itinerary", "review")
    workflow.add_edge("review", END)

    return workflow.compile()


def build_initial_state(message: str) -> dict[str, Any]:
    """Create the initial TravelState for a new chat message."""
    return {
        "conversation_id": "",
        "messages": [{"role": "user", "content": message}],
        "user_message": message,
        "destination": None,
        "origin": None,
        "travel_dates": None,
        "duration": None,
        "travelers": None,
        "budget": None,
        "preferences": [],
        "requirements": {},
        "missing_fields": [],
        "strategy": {},
        "itinerary": {},
        "tool_results": {},
        "review_notes": [],
        "approved": False,
        "issues": [],
        "suggestions": [],
        "next_agent": "",
        "reason": "",
        "status": "running",
        "error": None,
        "final_response": "",
    }
