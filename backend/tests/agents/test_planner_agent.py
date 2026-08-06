"""Tests for the Planner Agent."""

from app.agents.planner_agent import PlannerAgent
from tests.fakes.fake_chat_model import FakeStructuredChatModel


def _state() -> dict:
    return {
        "requirements": {
            "destination": "Japan",
            "duration": 7,
            "budget": 2000,
            "preferences": ["food", "culture"],
        }
    }


async def test_creates_budget_strategy():
    agent = PlannerAgent(
        llm=FakeStructuredChatModel(
            [
                {
                    "strategy": "Budget cultural trip focusing on food",
                    "focus_areas": ["street food", "temples"],
                    "estimated_budget": 1500,
                }
            ]
        )
    )

    update = await agent.execute(_state())

    assert update["strategy"]["description"] == "Budget cultural trip focusing on food"
    assert update["strategy"]["focus_areas"] == ["street food", "temples"]
    assert update["strategy"]["estimated_budget"] == 1500


async def test_returns_failed_status_on_invalid_output():
    agent = PlannerAgent(llm=FakeStructuredChatModel([{"strategy": 42}]))

    update = await agent.execute(_state())

    assert update["status"] == "failed"
    assert "error" in update
