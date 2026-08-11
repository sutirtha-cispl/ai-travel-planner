"""Agent-to-tool integration tests.

Verifies the Planner Agent can gather travel information through the tool
service and that failures degrade gracefully.
"""

from app.agents.planner_agent import PlannerAgent
from tests.fakes.fake_chat_model import FakeStructuredChatModel

PLANNER_RESPONSE = {
    "strategy": "Budget cultural trip",
    "focus_areas": ["temples", "street food"],
    "estimated_budget": 1500,
}

REQUIREMENTS_STATE = {
    "requirements": {
        "destination": "Tokyo",
        "duration": 5,
        "travelers": 1,
        "budget": 1500,
        "preferences": ["culture"],
        "travel_dates": {"start": "2026-04-01", "end": "2026-04-06"},
    }
}


async def test_planner_agent_collects_tool_results():
    agent = PlannerAgent(llm=FakeStructuredChatModel([PLANNER_RESPONSE]))

    update = await agent.execute(REQUIREMENTS_STATE)

    assert update["strategy"]["description"] == "Budget cultural trip"
    tool_results = update["tool_results"]
    assert set(tool_results) == {
        "search_flights",
        "search_hotels",
        "get_weather_forecast",
        "convert_currency",
    }
    assert all(entry["status"] == "ok" for entry in tool_results.values())
    assert tool_results["convert_currency"]["data"]["target"] == "JPY"


async def test_planner_agent_skips_tools_without_destination():
    agent = PlannerAgent(llm=FakeStructuredChatModel([PLANNER_RESPONSE]))

    update = await agent.execute({"requirements": {"duration": 5}})

    assert update["strategy"]["description"] == "Budget cultural trip"
    assert update["tool_results"] == {}


async def test_planner_agent_degrades_gracefully_on_tool_failure():
    class FailingToolService:
        async def collect_for_requirements(self, requirements):
            raise RuntimeError("boom: internal detail")

    agent = PlannerAgent(
        llm=FakeStructuredChatModel([PLANNER_RESPONSE]),
        tool_service=FailingToolService(),
    )

    update = await agent.execute(REQUIREMENTS_STATE)

    assert update["strategy"]["description"] == "Budget cultural trip"
    assert update["tool_results"] == {"error": "Could not retrieve travel information."}
    assert "internal" not in update["tool_results"]["error"]
