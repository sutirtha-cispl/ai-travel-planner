"""Supervisor Agent.

Analyzes the shared state and decides the next step of the workflow.
It never generates trip content; it only routes.
"""

from typing import Any

from app.agents.base_agent import BaseAgent
from app.prompts.agents.supervisor_prompt import supervisor_prompt_template
from app.schemas.agent_outputs import SupervisorDecision
from app.utils.validators import to_json

SUPERVISOR_END_STEP = "end"
SUPERVISOR_ASK_USER_STEP = "ask_user"

_REQUIRED_FIELDS = ("destination", "duration", "budget")


def _clarification_message(state: dict[str, Any], reason: str) -> str:
    missing = [
        field.replace("_", " ")
        for field in _REQUIRED_FIELDS
        if state.get(field) is None
    ]
    if missing:
        return (
            "I need a few more details before I can plan your trip: "
            + ", ".join(missing)
            + "."
        )
    return reason or "Please share a few more details about your trip."


class SupervisorAgent(BaseAgent):
    name = "supervisor"
    output_schema = SupervisorDecision

    @property
    def prompt_template(self):
        return supervisor_prompt_template

    def _prompt_input(self, state: dict[str, Any]) -> dict[str, Any]:
        summary = {
            "destination": state.get("destination"),
            "duration": state.get("duration"),
            "budget": state.get("budget"),
            "preferences": state.get("preferences", []),
            "has_strategy": bool(state.get("strategy")),
            "has_itinerary": bool(state.get("itinerary")),
            "missing_fields": state.get("missing_fields", []),
            "status": state.get("status"),
        }
        return {"state_summary": to_json(summary)}

    def _state_update(
        self,
        state: dict[str, Any],
        output: SupervisorDecision,
    ) -> dict[str, Any]:
        update: dict[str, Any] = {
            "next_agent": output.next_step,
            "reason": output.reason,
        }
        if output.next_step == SUPERVISOR_ASK_USER_STEP:
            update["status"] = "waiting_for_input"
            update["final_response"] = _clarification_message(state, output.reason)
        return update
