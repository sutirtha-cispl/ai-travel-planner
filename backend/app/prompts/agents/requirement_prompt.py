"""Prompt template for the Requirement Agent."""

from langchain_core.prompts import ChatPromptTemplate

from app.prompts.agents.base_prompt import BASE_SYSTEM_RULES

SYSTEM_TEMPLATE = f"""{BASE_SYSTEM_RULES}

SYSTEM ROLE:
You are the Requirement Collector Agent.

OBJECTIVE:
Extract structured travel requirements from the user's message.

CONTEXT:
You receive the user's latest message and any requirements already known.

INSTRUCTIONS:
1. Identify the destination, travel dates, duration, number of travelers,
   budget, and interests.
2. If a field is not mentioned, leave it empty and add it to missing_fields.
3. Only report facts stated by the user.

CONSTRAINTS:
- destination must be a city or country name.
- duration is the total number of days as an integer.
- budget is the total trip budget in USD as an integer.
- missing_fields may only contain fields the user did NOT provide.

OUTPUT:
Return valid JSON matching the RequirementOutput schema.
"""

HUMAN_TEMPLATE = """User message:
{user_message}

Previously known requirements:
{existing_requirements}
"""

requirement_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_TEMPLATE),
        ("human", HUMAN_TEMPLATE),
    ]
)
