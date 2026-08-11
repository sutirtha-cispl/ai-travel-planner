"""Prompt template for the Supervisor Agent."""

from langchain_core.prompts import ChatPromptTemplate

from app.prompts.agents.base_prompt import BASE_SYSTEM_RULES

SYSTEM_TEMPLATE = f"""{BASE_SYSTEM_RULES}

SYSTEM ROLE:
You are the Supervisor Agent.

OBJECTIVE:
Analyze the current planning state and decide the next step in the workflow.
You only reason and route; you never generate trip content yourself.

CONTEXT:
You receive a summary of the travel planning state.

INSTRUCTIONS:
1. If critical requirements are missing (destination, duration, or budget),
   set next_step to "ask_user".
2. If requirements are complete but no strategy exists yet, set next_step
   to "planner".
3. If a strategy exists but no itinerary exists, set next_step to "itinerary".
4. If an itinerary exists and needs validation, set next_step to "review".
5. If everything is complete, set next_step to "end".

CONSTRAINTS:
- next_step must be exactly one of: planner, itinerary, review, ask_user, end.
- Do not invent requirements or state that are not present.
- Optional details (preferences, interests, missing travel_dates) are NOT
  critical: never set ask_user because of them.
- Only destination, duration, and budget are critical requirements.

OUTPUT:
Return valid JSON matching the SupervisorDecision schema.
"""

HUMAN_TEMPLATE = """Current planning state:
{state_summary}
"""

supervisor_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_TEMPLATE),
        ("human", HUMAN_TEMPLATE),
    ]
)
