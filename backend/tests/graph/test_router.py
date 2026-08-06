"""Tests for the workflow routing logic."""

from app.graph.router import ROUTE_PATH_MAP, route_workflow


def test_routes_to_planner():
    assert route_workflow({"next_agent": "planner"}) == "planner"


def test_routes_to_itinerary():
    assert route_workflow({"next_agent": "itinerary"}) == "itinerary"


def test_routes_to_review():
    assert route_workflow({"next_agent": "review"}) == "review"


def test_routes_ask_user_to_end():
    assert route_workflow({"next_agent": "ask_user"}) == "ask_user"
    assert ROUTE_PATH_MAP["ask_user"] == "__end__"


def test_defaults_to_end_when_decision_missing():
    assert route_workflow({}) == "end"
    assert ROUTE_PATH_MAP["end"] == "__end__"


def test_defaults_to_end_when_decision_unknown():
    assert route_workflow({"next_agent": "flying"}) == "end"
