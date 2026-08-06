"""End-to-end tests for the LangGraph travel workflow."""

from app.agents.itinerary_agent import ItineraryAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.requirement_agent import RequirementAgent
from app.agents.review_agent import ReviewAgent
from app.agents.supervisor_agent import SupervisorAgent
from app.graph.workflow import build_initial_state, build_workflow
from tests.fakes.fake_chat_model import FakeStructuredChatModel

REQUIREMENT_RESPONSE = {
    "destination": "Japan",
    "travel_dates": None,
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


def _fake_agents(next_step: str = "planner") -> dict:
    return {
        "requirement": RequirementAgent(
            llm=FakeStructuredChatModel([REQUIREMENT_RESPONSE])
        ),
        "supervisor": SupervisorAgent(
            llm=FakeStructuredChatModel([{"next_step": next_step, "reason": "ok"}])
        ),
        "planner": PlannerAgent(llm=FakeStructuredChatModel([PLANNER_RESPONSE])),
        "itinerary": ItineraryAgent(llm=FakeStructuredChatModel([ITINERARY_RESPONSE])),
        "review": ReviewAgent(llm=FakeStructuredChatModel([REVIEW_RESPONSE])),
    }


async def test_workflow_runs_requirement_to_review():
    graph = build_workflow(agents=_fake_agents())
    result = await graph.ainvoke(build_initial_state("Plan a 5 day Japan trip"))

    assert result["destination"] == "Japan"
    assert result["duration"] == 5
    assert result["budget"] == 2000
    assert result["strategy"]["description"] == "Budget cultural trip"
    first_activity = result["itinerary"]["days"][0]["activities"][0]
    assert first_activity["name"] == "Visit Tokyo Tower"
    assert result["approved"] is True
    assert result["status"] == "running"


async def test_workflow_asks_user_when_data_missing():
    graph = build_workflow(agents=_fake_agents(next_step="ask_user"))
    result = await graph.ainvoke(build_initial_state("I want to go somewhere"))

    assert result["next_agent"] == "ask_user"
    assert result["status"] == "waiting_for_input"
    assert result["final_response"]
    assert not result.get("itinerary")


async def test_workflow_terminates_when_supervisor_fails():
    agents = _fake_agents()
    agents["supervisor"] = SupervisorAgent(
        llm=FakeStructuredChatModel([{"next_step": 123}])
    )

    graph = build_workflow(agents=agents)
    result = await graph.ainvoke(build_initial_state("Plan a trip"))

    assert result["status"] == "failed"
    assert "error" in result
