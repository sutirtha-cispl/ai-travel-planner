"""Review Agent.

Validates the generated itinerary before it reaches the user.
Owns the review-related keys in the travel state.
"""

from typing import Any

from app.agents.base_agent import BaseAgent
from app.prompts.agents.review_prompt import review_prompt_template
from app.schemas.agent_outputs import ReviewOutput
from app.utils.validators import to_json


class ReviewAgent(BaseAgent):
    name = "review"
    output_schema = ReviewOutput

    @property
    def prompt_template(self):
        return review_prompt_template

    def _prompt_input(self, state: dict[str, Any]) -> dict[str, Any]:
        return {
            "itinerary": to_json(state.get("itinerary", {})),
            "requirements": to_json(state.get("requirements", {})),
        }

    def _state_update(
        self,
        state: dict[str, Any],
        output: ReviewOutput,
    ) -> dict[str, Any]:
        return {
            "approved": output.approved,
            "issues": output.issues,
            "suggestions": output.suggestions,
            "review_notes": [note.model_dump() for note in output.review_notes],
        }
