"""Tests for the Requirement Agent."""

from app.agents.requirement_agent import RequirementAgent
from app.utils.validators import to_json
from tests.fakes.fake_chat_model import FakeStructuredChatModel


def _state() -> dict:
    return {
        "user_message": (
            "I want a 7 day Japan trip under $2000, I like food and culture"
        ),
        "requirements": {},
        "missing_fields": [],
    }


async def test_extracts_destination_duration_and_budget():
    agent = RequirementAgent(
        llm=FakeStructuredChatModel(
            [
                {
                    "destination": "Japan",
                    "travel_dates": None,
                    "duration": 7,
                    "travelers": None,
                    "budget": 2000,
                    "preferences": ["food", "culture"],
                    "missing_fields": [],
                }
            ]
        )
    )

    update = await agent.execute(_state())

    assert update["destination"] == "Japan"
    assert update["duration"] == 7
    assert update["budget"] == 2000
    assert update["preferences"] == ["food", "culture"]
    assert update["requirements"]["destination"] == "Japan"


async def test_reports_missing_fields():
    agent = RequirementAgent(
        llm=FakeStructuredChatModel(
            [
                {
                    "destination": "Japan",
                    "travel_dates": None,
                    "duration": None,
                    "travelers": None,
                    "budget": None,
                    "preferences": [],
                    "missing_fields": ["duration", "budget"],
                }
            ]
        )
    )

    update = await agent.execute(_state())

    assert update["duration"] is None
    assert update["missing_fields"] == ["duration", "budget"]


async def test_returns_failed_status_on_invalid_output():
    agent = RequirementAgent(
        llm=FakeStructuredChatModel(
            [{"destination": "Japan", "duration": "not-a-number", "preferences": []}]
        )
    )

    update = await agent.execute(_state())

    assert update["status"] == "failed"
    assert "error" in update


def test_prompt_input_serializes_existing_requirements():
    agent = RequirementAgent(llm=FakeStructuredChatModel([{}]))

    prompt_input = agent._prompt_input(
        {"user_message": "hi", "requirements": {"destination": "Japan"}}
    )

    assert prompt_input["user_message"] == "hi"
    assert prompt_input["existing_requirements"] == to_json(
        {"destination": "Japan"}
    )
