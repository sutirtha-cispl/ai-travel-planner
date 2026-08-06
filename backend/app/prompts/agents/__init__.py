"""Prompt templates for AI agents."""

from app.prompts.agents.itinerary_prompt import itinerary_prompt_template
from app.prompts.agents.planner_prompt import planner_prompt_template
from app.prompts.agents.requirement_prompt import requirement_prompt_template
from app.prompts.agents.review_prompt import review_prompt_template
from app.prompts.agents.supervisor_prompt import supervisor_prompt_template

__all__ = [
    "itinerary_prompt_template",
    "planner_prompt_template",
    "requirement_prompt_template",
    "review_prompt_template",
    "supervisor_prompt_template",
]
