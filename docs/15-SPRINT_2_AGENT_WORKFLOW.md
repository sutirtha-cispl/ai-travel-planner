# AI Travel Planner - Sprint 2 Agent Workflow

Version: 1.0.0

---

# Sprint Objective

Implement the first real Agentic AI workflow.

The goal of this sprint is to move from:

```
Simple LLM Response
```

to:

```
Multi-Step AI Agent Workflow
```

using:

- LangGraph
- LangChain
- Structured Outputs
- Agent State Management

---

# Sprint Duration

Recommended:

```
2-3 Weeks
```

---

# Sprint Outcome

At the end of this sprint, the system should:

- Understand user travel requirements.
- Maintain workflow state.
- Execute multiple AI agents.
- Route tasks using LangGraph.
- Generate structured itinerary responses.
- Validate AI outputs.

---

# Reference Documents

Read before implementation:

```
AGENTS.md

docs/08-GRAPH_DESIGN.md

docs/09-AGENTS_DESIGN.md

docs/11-PROMPTS.md

docs/12-TESTING.md
```

---

# Sprint Architecture

After Sprint 2:

```
                     User

                      |

                      v

               Requirement Agent

                      |

                      v

              Supervisor Agent

                      |

        ----------------------------

        |                          |

        v                          v


  Planning Agent             Review Agent


        |

        v


 Itinerary Generator Agent


        |

        v


     Final Response
```

---

# Sprint Scope

## Included

- Agent architecture
- LangGraph routing
- Shared state
- Agent prompts
- Structured responses
- Agent testing


## Not Included

- Real travel APIs
- Long-term memory
- Vector database
- Booking system

---

# Task 1: Create Agent Framework

## Goal

Create reusable agent architecture.

---

Create:

```
backend/app/agents/

├── base_agent.py

├── requirement_agent.py

├── supervisor_agent.py

├── planner_agent.py

├── itinerary_agent.py

└── review_agent.py
```

---

# Base Agent

Location:

```
agents/base_agent.py
```

---

Responsibilities:

- Initialize LLM.
- Load prompts.
- Execute reasoning.
- Validate output.

---

Example interface:

```python
class BaseAgent:

    async def execute(
        self,
        state
    ):
        pass
```

---

# Task 2: Implement Travel State

## Goal

Create shared state between agents.

---

Location:

```
graph/state.py
```

---

Create:

```
TravelState
```

---

Initial structure:

```python
class TravelState:

    messages:list

    destination:str

    travel_dates:dict

    budget:int

    preferences:list

    requirements:dict

    itinerary:dict

    review_notes:list
```

---

# State Rules

Agents should:

Read:

```
Existing state
```

Update:

```
Only their responsibility fields
```

Never:

```
Overwrite unrelated data
```

---

# Task 3: Requirement Agent

## Purpose

Extract travel requirements from user input.

---

Responsibilities:

Identify:

- Destination
- Dates
- Duration
- Budget
- Number of travelers
- Interests

---

Example Input:

```
I want a 7 day Japan trip under $2000
```

---

Expected Output:

```json
{
"destination":"Japan",
"duration":7,
"budget":2000
}
```

---

# Prompt

Create:

```
prompts/agents/requirement_prompt.py
```

---

Prompt Rules:

The agent must:

- Extract facts.
- Ask for missing information.
- Never invent details.

---

# Task 4: Supervisor Agent

## Purpose

Control workflow decisions.

---

Location:

```
agents/supervisor_agent.py
```

---

Responsibilities:

- Analyze state.
- Decide next agent.
- Control execution order.

---

Example:

If:

```
destination missing
```

Route:

```
Requirement Agent
```

---

If:

```
requirements complete
```

Route:

```
Planner Agent
```

---

# Task 5: Planner Agent

## Purpose

Create travel planning strategy.

---

Responsibilities:

Analyze:

- User preferences.
- Budget.
- Duration.

---

Output:

```json
{
"strategy":"Budget cultural trip"
}
```

---

# Task 6: Itinerary Agent

## Purpose

Generate final travel schedule.

---

Responsibilities:

Create:

- Day-wise activities.
- Suggested timing.
- Travel flow.

---

Example Output:

```json
{
"days":[
 {
  "day":1,
  "activities":[
   "Visit Tokyo Tower"
  ]
 }
]
}
```

---

# Task 7: Review Agent

## Purpose

Validate generated itinerary.

---

Checks:

- Missing information.
- Budget issues.
- Unrealistic schedules.
- Conflicting activities.

---

Output:

```json
{
"approved":true,
"issues":[]
}
```

---

# Task 8: Implement LangGraph Workflow

Create:

```
graph/workflow.py
```

---

Final workflow:

```
START

↓

Requirement Agent

↓

Supervisor Agent

↓

Planner Agent

↓

Itinerary Agent

↓

Review Agent

↓

END
```

---

# Graph Routing Rules

Example:

```
Requirement Agent

        |

        |

Missing Data?

    /       \

 Yes         No

 |            |

Ask User    Planner
```

---

# Task 9: Structured Output

## Goal

Prevent invalid AI responses.

---

Use:

- Pydantic models
- LangChain structured output

---

Create:

```
schemas/agent_outputs.py
```

---

Models:

```
RequirementOutput

PlannerOutput

ItineraryOutput

ReviewOutput
```

---

Example:

```python
class RequirementOutput(BaseModel):

    destination:str

    duration:int
```

---

# Task 10: Agent Prompt Implementation

Create:

```
prompts/agents/
```

Files:

```
requirement_prompt.py

supervisor_prompt.py

planner_prompt.py

itinerary_prompt.py

review_prompt.py
```

---

Each prompt must define:

- Role
- Goal
- Context
- Rules
- Output format

---

# Task 11: Chat API Integration

Update:

```
api/routes/chat.py
```

---

New flow:

```
POST /chat

↓

Create TravelState

↓

Execute LangGraph

↓

Return final response
```

---

Example Request:

```json
{
"message":
"Plan a 5 day Japan trip"
}
```

---

Example Response:

```json
{
"itinerary":{}
}
```

---

# Task 12: Agent Error Handling

Every agent must handle:

- Missing data
- Invalid output
- LLM failure
- Timeout

---

Example:

If itinerary generation fails:

Return:

```json
{
"status":"failed",
"reason":"Unable to generate itinerary"
}
```

---

# Task 13: Agent Testing

Create:

```
tests/agents/
```

---

Required tests:

---

## Requirement Agent Test

Input:

```
Plan Japan trip
```

Expected:

Destination extracted.

---

## Planner Agent Test

Input:

```
Budget trip
```

Expected:

Budget strategy created.

---

## Itinerary Agent Test

Expected:

Day structure generated.

---

# Task 14: Graph Testing

Create:

```
tests/graph/
```

---

Test:

Complete workflow execution.

---

Scenario:

Input:

```
Plan 5 day Japan trip
```

Expected:

```
Requirement

↓

Planner

↓

Itinerary

↓

Review
```

---

# Task 15: Logging

Add agent execution logs.

Track:

- Agent name
- Execution time
- Status
- Errors

---

Example:

```
RequirementAgent

Execution:

1.2 seconds

Status:

Success
```

---

# Sprint Completion Checklist

## Agents

☐ Base agent created

☐ Requirement agent created

☐ Supervisor agent created

☐ Planner agent created

☐ Itinerary agent created

☐ Review agent created


---

## LangGraph

☐ State implemented

☐ Nodes created

☐ Routing implemented

☐ Workflow tested


---

## AI Quality

☐ Structured outputs enabled

☐ Prompts created

☐ Error handling added


---

## Testing

☐ Agent tests created

☐ Graph tests created

☐ API flow tested


---

# Sprint Demo

User enters:

```
Create a 7 day Japan travel plan.
Budget is $2000.
I like culture and food.
```

System should:

1. Extract requirements.

2. Decide workflow.

3. Generate travel strategy.

4. Create itinerary.

5. Review output.

6. Return structured response.

---

# Next Sprint

After completing Sprint 2, proceed to:

```
docs/16-SPRINT_3_TOOLS_AND_INTEGRATIONS.md
```

Sprint 3 will introduce:

- External tools
- Flight search
- Hotel search
- Weather integration
- Maps
- Real-world data
- Tool-based agent reasoning
