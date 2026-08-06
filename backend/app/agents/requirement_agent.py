"""Requirement Agent.

Extracts structured travel requirements from the user's message.
Owns the requirements-related keys in the travel state.
"""

from typing import Any

from app.agents.base_agent import BaseAgent
from app.prompts.agents.requirement_prompt import requirement_prompt_template
from app.schemas.agent_outputs import RequirementOutput
from app.utils.validators import to_json


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
        requirements = {
            "destination": output.destination,
            "travel_dates": output.travel_dates,
            "duration": output.duration,
            "travelers": output.travelers,
            "budget": output.budget,
            "preferences": output.preferences,
            "missing_fields": output.missing_fields,
        }
        return {
            "requirements": requirements,
            "destination": output.destination,
            "travel_dates": output.travel_dates,
            "duration": output.duration,
            "travelers": output.travelers,
            "budget": output.budget,
            "preferences": output.preferences,
            "missing_fields": output.missing_fields,
        }
