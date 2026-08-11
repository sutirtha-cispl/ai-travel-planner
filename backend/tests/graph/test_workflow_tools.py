"""LangGraph workflow tests with tool integration.

Runs the full Sprint 2 workflow end-to-end with real mock providers wired
into the planner, and verifies tool results flow through the shared state.
"""

from app.agents.itinerary_agent import ItineraryAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.requirement_agent import RequirementAgent
from app.agents.review_agent import ReviewAgent
from app.agents.supervisor_agent import SupervisorAgent
from app.graph.workflow import build_initial_state, build_workflow
from tests.fakes.fake_chat_model import FakeStructuredChatModel

REQUIREMENT_RESPONSE = {
    "destination": "Japan",
    "travel_dates": {"start": "2026-04-01", "end": "2026-04-06"},
    "duration": 5,
    "travelers": 1,
    "budget": 2000,
    "preferences": ["culture", "food"],
    "missing_fields": [],
}

PLANNER_RESPONSE = {
    "strategy": "Budget cultural trip",
    "focus_areas": ["temples", "street food"],
    "estimated_budget": 1500,
}

ITINERARY_RESPONSE = {
    "days": [
        {
            "day": 1,
            "title": "Tokyo",
            "activities": [
                {
                    "time": "09:00",
                    "name": "Visit Tokyo Tower",
                    "category": "sightseeing",
                }
            ],
            "notes": "",
        }
    ],
    "summary": "A cultural tour of Japan",
}

REVIEW_RESPONSE = {
    "approved": True,
    "issues": [],
    "suggestions": [],
    "review_notes": [],
}


def _fake_agents() -> dict:
    return {
        "requirement": RequirementAgent(
            llm=FakeStructuredChatModel([REQUIREMENT_RESPONSE])
        ),
        "supervisor": SupervisorAgent(
            llm=FakeStructuredChatModel([{"next_step": "planner", "reason": "ok"}])
        ),
        "planner": PlannerAgent(llm=FakeStructuredChatModel([PLANNER_RESPONSE])),
        "itinerary": ItineraryAgent(llm=FakeStructuredChatModel([ITINERARY_RESPONSE])),
        "review": ReviewAgent(llm=FakeStructuredChatModel([REVIEW_RESPONSE])),
    }


async def test_workflow_collects_tool_results_and_generates_itinerary():
    graph = build_workflow(agents=_fake_agents())
    result = await graph.ainvoke(build_initial_state("Plan a 5 day Japan trip"))

    assert result["destination"] == "Japan"
    assert result["tool_results"]
    assert set(result["tool_results"]) == {
        "search_flights",
        "search_hotels",
        "get_weather_forecast",
        "convert_currency",
    }
    assert result["tool_results"]["search_flights"]["status"] == "ok"
    first_activity = result["itinerary"]["days"][0]["activities"][0]
    assert first_activity["name"] == "Visit Tokyo Tower"
    assert result["approved"] is True


async def test_workflow_tool_results_are_serializable_in_state():
    graph = build_workflow(agents=_fake_agents())
    result = await graph.ainvoke(build_initial_state("Plan a 5 day Japan trip"))

    import json

    json.dumps(result["tool_results"])
