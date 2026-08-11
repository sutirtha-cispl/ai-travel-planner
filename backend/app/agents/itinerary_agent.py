"""Itinerary Agent.

Generates the final day-by-day travel schedule.
Owns the itinerary key in the travel state.
"""

from typing import Any

from app.agents.base_agent import BaseAgent
from app.prompts.agents.itinerary_prompt import itinerary_prompt_template
from app.schemas.agent_outputs import ItineraryOutput
from app.utils.validators import to_json


class ItineraryAgent(BaseAgent):
    name = "itinerary"
    output_schema = ItineraryOutput

    @property
    def prompt_template(self):
        return itinerary_prompt_template

    def _prompt_input(self, state: dict[str, Any]) -> dict[str, Any]:
        return {
            "destination": state.get("destination") or "your destination",
            "duration": state.get("duration"),
            "preferences": to_json(state.get("preferences", [])),
            "strategy": to_json(state.get("strategy", {})),
            "tool_results": to_json(state.get("tool_results", {})),
        }

    def _state_update(
        self,
        state: dict[str, Any],
        output: ItineraryOutput,
    ) -> dict[str, Any]:
        return {
            "itinerary": {
                "destination": state.get("destination"),
                "duration": state.get("duration"),
                "days": [day.model_dump() for day in output.days],
                "summary": output.summary,
            }
        }
