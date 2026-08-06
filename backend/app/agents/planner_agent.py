"""Planner Agent.

Creates the high-level travel strategy from collected requirements.
Owns the strategy key in the travel state.
"""

from typing import Any

from app.agents.base_agent import BaseAgent
from app.prompts.agents.planner_prompt import planner_prompt_template
from app.schemas.agent_outputs import PlannerOutput
from app.utils.validators import to_json


class PlannerAgent(BaseAgent):
    name = "planner"
    output_schema = PlannerOutput

    @property
    def prompt_template(self):
        return planner_prompt_template

    def _prompt_input(self, state: dict[str, Any]) -> dict[str, Any]:
        return {"requirements": to_json(state.get("requirements", {}))}

    def _state_update(
        self,
        state: dict[str, Any],
        output: PlannerOutput,
    ) -> dict[str, Any]:
        return {
            "strategy": {
                "description": output.strategy,
                "focus_areas": output.focus_areas,
                "estimated_budget": output.estimated_budget,
            }
        }
