"""Planner Agent.

Creates the high-level travel strategy from collected requirements.
Owns the strategy and tool_results keys in the travel state.

Before reasoning, the planner gathers up-to-date travel information (flights,
hotels, weather, currency) through the tool service so the strategy can be
grounded in real (mock) data instead of pure guesses.
"""

import logging
from typing import Any

from app.agents.base_agent import BaseAgent
from app.prompts.agents.planner_prompt import planner_prompt_template
from app.schemas.agent_outputs import PlannerOutput
from app.services.tool_service import build_tool_service
from app.utils.validators import to_json

logger = logging.getLogger(__name__)


class PlannerAgent(BaseAgent):
    name = "planner"
    output_schema = PlannerOutput

    def __init__(self, llm=None, tool_service=None) -> None:
        super().__init__(llm=llm)
        self._tool_service = tool_service or build_tool_service()
        self._tool_results: dict[str, Any] = {}

    @property
    def prompt_template(self):
        return planner_prompt_template

    def _prompt_input(self, state: dict[str, Any]) -> dict[str, Any]:
        requirements = state.get("requirements", {})
        return {
            "requirements": to_json(requirements),
            "tool_results": to_json(self._tool_results or {}),
        }

    async def _prepare_prompt(self, state: dict[str, Any]) -> dict[str, Any]:
        requirements = state.get("requirements", {})
        self._tool_results = await self._collect_tool_results(requirements)
        return self._prompt_input(state)

    async def _collect_tool_results(
        self, requirements: dict[str, Any]
    ) -> dict[str, Any]:
        try:
            return await self._tool_service.collect_for_requirements(requirements)
        except Exception as exc:
            logger.warning(
                "Planner tool collection failed: %s", exc, exc_info=True
            )
            return {"error": "Could not retrieve travel information."}

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
            },
            "tool_results": self._tool_results,
        }
