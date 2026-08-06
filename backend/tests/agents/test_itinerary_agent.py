"""Tests for the Itinerary Agent."""

from app.agents.itinerary_agent import ItineraryAgent
from tests.fakes.fake_chat_model import FakeStructuredChatModel


def _state() -> dict:
    return {
        "destination": "Japan",
        "duration": 2,
        "preferences": ["culture"],
        "strategy": {"description": "Cultural trip"},
    }


async def test_generates_day_structure():
    agent = ItineraryAgent(
        llm=FakeStructuredChatModel(
            [
                {
                    "days": [
                        {
                            "day": 1,
                            "title": "Tokyo",
                            "activities": [
                                {
                                    "time": "09:00",
                                    "name": "Visit Tokyo Tower",
                                    "description": "",
                                    "category": "sightseeing",
                                    "estimated_cost": 10,
                                }
                            ],
                            "notes": "",
                        },
                        {
                            "day": 2,
                            "title": "Kyoto",
                            "activities": [],
                            "notes": "Travel day",
                        },
                    ],
                    "summary": "A two day cultural tour",
                }
            ]
        )
    )

    update = await agent.execute(_state())

    assert len(update["itinerary"]["days"]) == 2
    first_activity = update["itinerary"]["days"][0]["activities"][0]
    assert first_activity["name"] == "Visit Tokyo Tower"
    assert update["itinerary"]["destination"] == "Japan"
    assert update["itinerary"]["summary"] == "A two day cultural tour"


async def test_returns_failed_status_on_invalid_output():
    agent = ItineraryAgent(llm=FakeStructuredChatModel([{"days": [{"day": "one"}]}]))

    update = await agent.execute(_state())

    assert update["status"] == "failed"
    assert "error" in update
