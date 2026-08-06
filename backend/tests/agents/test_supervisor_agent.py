"""Tests for the Supervisor Agent."""

from app.agents.supervisor_agent import SupervisorAgent
from tests.fakes.fake_chat_model import FakeStructuredChatModel


def _state(**overrides) -> dict:
    state = {
        "destination": "Japan",
        "duration": 5,
        "budget": 2000,
        "preferences": ["culture"],
        "missing_fields": [],
        "strategy": {},
        "itinerary": {},
        "status": "running",
    }
    state.update(overrides)
    return state


async def test_routes_to_planner_when_requirements_complete():
    agent = SupervisorAgent(
        llm=FakeStructuredChatModel(
            [{"next_step": "planner", "reason": "requirements complete"}]
        )
    )

    update = await agent.execute(_state())

    assert update["next_agent"] == "planner"
    assert update["reason"] == "requirements complete"


async def test_asks_user_when_destination_missing():
    agent = SupervisorAgent(
        llm=FakeStructuredChatModel(
            [{"next_step": "ask_user", "reason": "destination missing"}]
        )
    )

    update = await agent.execute(_state(destination=None))

    assert update["status"] == "waiting_for_input"
    assert "destination" in update["final_response"]


async def test_failed_output_returns_failed_status():
    agent = SupervisorAgent(llm=FakeStructuredChatModel([{"next_step": 123}]))

    update = await agent.execute(_state())

    assert update["status"] == "failed"
    assert "error" in update
