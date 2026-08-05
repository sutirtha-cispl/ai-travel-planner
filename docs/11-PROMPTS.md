# AI Travel Planner Prompt Engineering Guide

Version: 1.0.0

---

# Purpose

This document defines the prompt engineering standards for the AI Travel Planner.

Prompts control:

- Agent behavior
- Reasoning approach
- Output format
- Tool usage
- Decision making
- Safety constraints

---

# Prompt Engineering Principles

Production prompts should be:

- Clear
- Specific
- Testable
- Version controlled
- Task focused
- Output constrained

---

# Prompt Location

All prompts must exist inside:

```
backend/app/prompts/
```

Structure:

```
prompts/

├── base/

│   ├── system_prompt.py

│   └── output_rules.py


├── agents/

│   ├── supervisor_prompt.py

│   ├── requirement_prompt.py

│   ├── flight_prompt.py

│   ├── hotel_prompt.py

│   ├── activity_prompt.py

│   ├── budget_prompt.py

│   ├── itinerary_prompt.py

│   └── review_prompt.py


└── versions/

    ├── v1/

    └── v2/
```

---

# Prompt Management Rules

Never:

```python
prompt = """
You are a travel planner
"""
```

inside:

```
agents/
```

---

Always:

```
prompts/

↓

agent imports prompt
```

---

# Prompt Structure

Every prompt should contain:

```
Role

Objective

Context

Instructions

Constraints

Output Format

Examples
```

---

# Standard Prompt Template

Example:

```text
SYSTEM ROLE:

You are a Flight Recommendation Agent.

OBJECTIVE:

Recommend suitable flights based on user requirements.

CONTEXT:

You receive travel requirements from the planner workflow.

INSTRUCTIONS:

1. Analyze available options.
2. Consider budget.
3. Consider travel duration.

CONSTRAINTS:

- Do not recommend unavailable flights.
- Do not invent prices.

OUTPUT:

Return valid JSON only.
```

---

# Base System Prompt

Every agent inherits common rules.

Example:

```
You are part of an AI Travel Planning System.

Your responsibility is to complete your assigned task.

Rules:

- Use available information.
- Do not fabricate facts.
- Ask for missing information.
- Return structured responses.
- Respect user preferences.
```

---

# Agent Prompt Design

Each agent has a dedicated prompt.

---

# Supervisor Agent Prompt

File:

```
supervisor_prompt.py
```

---

Purpose:

Controls workflow decisions.

---

Responsibilities:

- Understand user objective.
- Select required agents.
- Decide execution order.

---

Example:

```
You are the Supervisor Agent.

Your task is to decide which specialized agents should execute.

Available agents:

- Flight Agent
- Hotel Agent
- Activity Agent
- Budget Agent

Do not perform their tasks yourself.
Delegate.
```

---

# Requirement Collector Prompt

File:

```
requirement_prompt.py
```

---

Purpose:

Extract travel information.

---

Extract:

```
destination

dates

budget

travelers

preferences
```

---

Output:

JSON.

Example:

```json
{
 "destination":"Japan",
 "budget":2000
}
```

---

# Flight Agent Prompt

File:

```
flight_prompt.py
```

---

Role:

```
You are a Flight Recommendation Agent.
```

---

Goal:

Recommend flights.

---

Must consider:

- Price
- Duration
- Airline reliability
- User preference

---

Must not:

- Book flights
- Modify user information

---

Output:

```json
{
 "recommendations":[]
}
```

---

# Hotel Agent Prompt

File:

```
hotel_prompt.py
```

---

Goal:

Recommend accommodation.

Consider:

- Location
- Rating
- Budget
- User preferences

---

Output:

```json
{
 "hotels":[]
}
```

---

# Activity Agent Prompt

File:

```
activity_prompt.py
```

---

Goal:

Recommend experiences.

Consider:

- Interests
- Travel duration
- Location

---

Output:

```json
{
 "activities":[]
}
```

---

# Budget Agent Prompt

File:

```
budget_prompt.py
```

---

Goal:

Optimize travel cost.

Analyze:

- Flights
- Hotels
- Activities

---

Output:

```json
{
 "total_cost":2500,
 "recommendations":[]
}
```

---

# Itinerary Agent Prompt

File:

```
itinerary_prompt.py
```

---

Goal:

Create final travel schedule.

Must consider:

- Distance
- Timing
- User interests
- Budget

---

Output:

```json
{
 "days":[]
}
```

---

# Review Agent Prompt

File:

```
review_prompt.py
```

---

Goal:

Validate final plan.

Check:

- Missing information
- Unrealistic timing
- Budget problems

---

Output:

```json
{
 "approved":true,
 "issues":[]
}
```

---

# Prompt Variables

Prompts should use dynamic variables.

Example:

```text
Destination:

{destination}

Budget:

{budget}
```

---

Never hardcode:

```
Japan

USA

1000 USD
```

---

# Output Formatting Rules

Agent outputs must be structured.

Preferred:

JSON.

---

Example:

Good:

```json
{
 "destination":"Paris",
 "days":5
}
```

Bad:

```
Paris is a great choice.
You should stay five days.
```

---

# Structured Output Enforcement

Use:

- Pydantic models
- LangChain structured output

Example:

```
LLM

↓

Pydantic Schema

↓

Validated Object
```

---

# Prompt Safety Rules

Prompts should prevent:

- Hallucination
- Fake bookings
- Fake prices
- Fake availability

---

Example:

Add:

```
If information is unavailable,
state that clearly.
Do not invent data.
```

---

# Tool Usage Instructions

When agents have tools:

Prompts should define:

```
You may use tools when required.

Do not call tools unnecessarily.

Validate tool results before using them.
```

---

# Prompt Versioning

Prompts evolve.

Version:

```
v1

v2

v3
```

Example:

```
prompts/

versions/

v1/

flight_prompt.py
```

---

# Prompt Change Process

When modifying prompts:

Document:

- Previous behavior
- New behavior
- Expected improvement
- Test cases

---

# Prompt Testing

Prompts require evaluation.

---

# Test Cases

Example:

Input:

```
Plan cheap Japan trip
```

Expected:

```
Budget Agent prioritizes cost.
```

---

# Evaluation Metrics

Track:

## Accuracy

Does output match requirements?

---

## Completeness

Are all required fields present?

---

## Consistency

Does output remain stable?

---

## Safety

Does it avoid hallucination?

---

# Prompt Debugging

When output is wrong:

Check:

```
Input Context

↓

Prompt Instructions

↓

Tool Results

↓

Model Response

↓

Output Parser
```

---

# Prompt Observability

Track:

- Prompt version
- Model version
- Token usage
- Response time
- Errors

---

# Model Configuration

Store model settings separately.

Example:

```
config/

llm_settings.py
```

Contains:

```
model_name

temperature

max_tokens
```

---

# Temperature Guidelines

Reasoning tasks:

```
0.2 - 0.5
```

Creative suggestions:

```
0.6 - 0.8
```

Structured extraction:

```
0
```

---

# Prompt Optimization Workflow

Process:

```
Identify problem

↓

Modify prompt

↓

Run evaluation

↓

Compare results

↓

Release new version
```

---

# Future Prompt Improvements

Possible additions:

- Automated prompt evaluation
- A/B testing
- Prompt analytics
- Agent feedback loops

---

# Final Prompt Architecture

```
Agent

↓

Prompt Template

↓

LLM

↓

Structured Output Parser

↓

LangGraph State

↓

Next Agent
```

---

# Design Goal

Prompts should be managed like software components.

A good prompt should make agents:

- Reliable
- Predictable
- Explainable
- Easy to improve
