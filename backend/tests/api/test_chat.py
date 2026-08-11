"""Chat endpoint tests."""

from app.agents.itinerary_agent import ItineraryAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.requirement_agent import RequirementAgent
from app.agents.review_agent import ReviewAgent
from app.agents.supervisor_agent import SupervisorAgent
from app.graph.workflow import build_workflow
from tests.fakes.fake_chat_model import FakeStructuredChatModel

CHAT_URL = "/api/v1/chat"


def test_chat_returns_not_configured_message_without_api_key(client, monkeypatch):
    monkeypatch.setattr("app.config.settings.settings.OPENAI_API_KEY", "")

    response = client.post(CHAT_URL, json={"message": "Plan a trip to Japan"})

    assert response.status_code == 200
    assert "response" in response.json()
    assert "not configured" in response.json()["response"].lower()


def test_chat_returns_itinerary_when_workflow_succeeds(client, monkeypatch):
    monkeypatch.setattr("app.config.settings.settings.OPENAI_API_KEY", "test-key")

    fake_agents = {
        "requirement": RequirementAgent(
            llm=FakeStructuredChatModel(
                [
                    {
                        "destination": "Japan",
                        "origin": "Mumbai",
                        "travel_dates": None,
                        "duration": 5,
                        "travelers": 1,
                        "budget": 2000,
                        "preferences": ["culture"],
                        "missing_fields": [],
                    }
                ]
            )
        ),
        "supervisor": SupervisorAgent(
            llm=FakeStructuredChatModel([{"next_step": "planner", "reason": "ok"}])
        ),
        "planner": PlannerAgent(
            llm=FakeStructuredChatModel(
                [
                    {
                        "strategy": "Cultural trip",
                        "focus_areas": [],
                        "estimated_budget": None,
                    }
                ]
            )
        ),
        "itinerary": ItineraryAgent(
            llm=FakeStructuredChatModel(
                [
                    {
                        "days": [
                            {
                                "day": 1,
                                "title": "Tokyo",
                                "activities": [
                                    {"time": "09:00", "name": "Visit Tokyo Tower"}
                                ],
                                "notes": "",
                            }
                        ],
                        "summary": "A cultural tour",
                    }
                ]
            )
        ),
        "review": ReviewAgent(
            llm=FakeStructuredChatModel(
                [
                    {
                        "approved": True,
                        "issues": [],
                        "suggestions": [],
                        "review_notes": [],
                    }
                ]
            )
        ),
    }
    monkeypatch.setattr(
        "app.services.chat_service.build_workflow",
        lambda: build_workflow(agents=fake_agents),
    )

    response = client.post(CHAT_URL, json={"message": "Plan a 5 day Japan trip"})

    assert response.status_code == 200
    assert "Visit Tokyo Tower" in response.json()["response"]


def test_chat_rejects_empty_message(client):
    response = client.post(CHAT_URL, json={"message": ""})

    assert response.status_code == 422
