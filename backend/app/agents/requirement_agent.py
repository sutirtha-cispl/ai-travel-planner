"""Requirement Agent.

Extracts structured travel requirements from the user's message.
Owns the requirements-related keys in the travel state.
"""

from typing import Any

from app.agents.base_agent import BaseAgent
from app.prompts.agents.requirement_prompt import requirement_prompt_template
from app.schemas.agent_outputs import RequirementOutput
from app.utils.validators import to_json

# Only these fields block planning. Optional details (e.g. preferences) must
# not be reported as missing so the supervisor does not loop back to ask_user.
CRITICAL_FIELDS = {"destination", "duration", "budget"}


class RequirementAgent(BaseAgent):
    name = "requirement"
    output_schema = RequirementOutput

    @property
    def prompt_template(self):
        return requirement_prompt_template

    def _prompt_input(self, state: dict[str, Any]) -> dict[str, Any]:
        return {
            "user_message": state.get("user_message", ""),
            "existing_requirements": to_json(state.get("requirements", {})),
        }

    def _state_update(
        self,
        state: dict[str, Any],
        output: RequirementOutput,
    ) -> dict[str, Any]:
        missing_fields = [
            field for field in output.missing_fields if field in CRITICAL_FIELDS
        ]
        requirements = {
            "origin": output.origin,
            "destination": output.destination,
            "travel_dates": output.travel_dates,
            "duration": output.duration,
            "travelers": output.travelers,
            "budget": output.budget,
            "preferences": output.preferences,
            "missing_fields": missing_fields,
        }
        return {
            "requirements": requirements,
            "origin": output.origin,
            "destination": output.destination,
            "travel_dates": output.travel_dates,
            "duration": output.duration,
            "travelers": output.travelers,
            "budget": output.budget,
            "preferences": output.preferences,
            "missing_fields": missing_fields,
        }
