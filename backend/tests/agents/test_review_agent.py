"""Tests for the Review Agent."""

from app.agents.review_agent import ReviewAgent
from tests.fakes.fake_chat_model import FakeStructuredChatModel


def _state() -> dict:
    return {
        "itinerary": {
            "destination": "Japan",
            "days": [{"day": 1, "activities": [{"name": "Tokyo Tower"}]}],
        },
        "requirements": {"budget": 2000},
    }


async def test_approves_valid_itinerary():
    agent = ReviewAgent(
        llm=FakeStructuredChatModel(
            [
                {
                    "approved": True,
                    "issues": [],
                    "suggestions": ["Add a rest day"],
                    "review_notes": [],
                }
            ]
        )
    )

    update = await agent.execute(_state())

    assert update["approved"] is True
    assert update["issues"] == []
    assert update["suggestions"] == ["Add a rest day"]


async def test_flags_budget_issues():
    agent = ReviewAgent(
        llm=FakeStructuredChatModel(
            [
                {
                    "approved": False,
                    "issues": ["Estimated costs exceed the stated budget"],
                    "suggestions": [],
                    "review_notes": [
                        {"severity": "error", "message": "Budget exceeded"}
                    ],
                }
            ]
        )
    )

    update = await agent.execute(_state())

    assert update["approved"] is False
    assert update["issues"] == ["Estimated costs exceed the stated budget"]
    assert update["review_notes"][0]["severity"] == "error"


async def test_returns_failed_status_on_invalid_output():
    agent = ReviewAgent(
        llm=FakeStructuredChatModel(
            [{"approved": True, "review_notes": [{"message": "missing severity"}]}]
        )
    )

    update = await agent.execute(_state())

    assert update["status"] == "failed"
    assert "error" in update
