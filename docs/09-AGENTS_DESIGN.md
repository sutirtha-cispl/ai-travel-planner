# AI Travel Planner Agent Design

Version: 1.0.0

---

# Purpose

This document defines the AI agent architecture for the AI Travel Planner.

Agents are specialized reasoning components responsible for specific travel planning tasks.

Agents should:

- Have one clear responsibility.
- Receive structured inputs.
- Produce structured outputs.
- Use only required tools.
- Communicate through LangGraph state.

---

# Agent Architecture Principles

## Single Responsibility

Each agent solves one specific problem.

Good:

```
Flight Agent

Responsible for flight recommendations.
```

Bad:

```
Travel Agent

Responsible for:

- Flights
- Hotels
- Budget
- Weather
- Restaurants
- Booking
```

---

## Controlled Tool Access

Agents should only access tools they need.

Example:

```
Flight Agent

Allowed:

Flight Search Tool


Not allowed:

Weather Tool
```

---

## Structured Communication

Agents communicate through:

```
LangGraph State
```

Not through:

```
Direct agent calls
```

---

# Agent System Overview

```
                    Supervisor / Planner Agent

                              |

        ------------------------------------------------

        |              |             |                |

        v              v             v                v


 Flight Agent   Hotel Agent   Activity Agent   Budget Agent


        |              |             |                |

        ------------------------------------------------

                              |

                              v


                  Itinerary Generator Agent


                              |

                              v


                     Review Agent
```

---

# Agent Categories

The system contains:

## Planning Agents

Responsible for reasoning and decisions.

Examples:

- Supervisor Agent
- Planner Agent

---

## Data Agents

Responsible for retrieving information.

Examples:

- Flight Agent
- Hotel Agent
- Weather Agent

---

## Optimization Agents

Responsible for improving decisions.

Examples:

- Budget Agent
- Schedule Agent

---

## Output Agents

Responsible for final presentation.

Examples:

- Itinerary Agent
- Report Agent

---

# 1. Supervisor Agent

## Purpose

The supervisor controls the overall travel planning workflow.

It decides:

- Which agents are needed.
- Execution order.
- Whether additional information is required.

---

## Responsibilities

- Analyze user goal.
- Delegate tasks.
- Monitor progress.
- Combine results.

---

## Input

```json
{
    "travel_request": {},
    "preferences": {}
}
```

---

## Output

```json
{
    "required_agents": [
        "flight",
        "hotel",
        "activity"
    ]
}
```

---

## Tools

None.

The supervisor only reasons.

---

# 2. Requirement Collector Agent

## Purpose

Extract travel requirements from conversation.

---

## Responsibilities

Collect:

- Destination
- Dates
- Duration
- Travelers
- Budget
- Preferences

---

## Input

```json
{
    "message":"Plan my Japan trip"
}
```

---

## Output

```json
{
    "destination":"Japan",
    "missing_fields":[
        "budget"
    ]
}
```

---

## Tools

None.

---

# 3. Flight Agent

## Purpose

Find and evaluate flight options.

---

## Responsibilities

- Search flights.
- Compare options.
- Recommend flights.

---

## Input

```json
{
    "departure":"Kolkata",
    "destination":"Tokyo",
    "dates":"2026-04-01"
}
```

---

## Output

```json
{
    "flights":[
        {
            "airline":"Example Airlines",
            "price":500
        }
    ]
}
```

---

## Tools

Allowed:

```
Flight Search Tool
```

---

# 4. Hotel Agent

## Purpose

Recommend accommodations.

---

## Responsibilities

- Search hotels.
- Evaluate ratings.
- Consider budget.

---

## Input

```json
{
    "location":"Tokyo",
    "budget":1000
}
```

---

## Output

```json
{
    "hotels":[]
}
```

---

## Tools

Allowed:

```
Hotel Search Tool
```

---

# 5. Weather Agent

## Purpose

Provide weather intelligence.

---

## Responsibilities

Analyze:

- Forecast.
- Best travel season.
- Weather risks.

---

## Input

```json
{
    "destination":"Japan",
    "dates":"April"
}
```

---

## Output

```json
{
    "weather_summary":"Mild weather"
}
```

---

## Tools

Allowed:

```
Weather Tool
```

---

# 6. Activity Agent

## Purpose

Recommend experiences.

---

## Responsibilities

Suggest:

- Attractions.
- Restaurants.
- Cultural activities.
- Local experiences.

---

## Input

```json
{
    "destination":"Tokyo",
    "interests":[
        "food",
        "culture"
    ]
}
```

---

## Output

```json
{
    "activities":[]
}
```

---

## Tools

Allowed:

```
Places Search Tool
```

---

# 7. Budget Agent

## Purpose

Optimize trip cost.

---

## Responsibilities

Calculate:

- Total cost.
- Cost distribution.
- Savings opportunities.

---

## Input

```json
{
    "flights":[],
    "hotels":[],
    "activities":[]
}
```

---

## Output

```json
{
    "total_budget":2500,
    "breakdown":{
        "flight":800,
        "hotel":900
    }
}
```

---

## Tools

None initially.

Future:

Currency Tool

---

# 8. Itinerary Generator Agent

## Purpose

Create final travel schedule.

---

## Responsibilities

Generate:

- Day plans.
- Activities.
- Timing.
- Transport.

---

## Input

```json
{
    "destination":"Japan",
    "activities":[],
    "budget":{}
}
```

---

## Output

```json
{
    "days":[
        {
            "day":1,
            "activities":[]
        }
    ]
}
```

---

## Tools

None.

---

# 9. Review Agent

## Purpose

Quality assurance.

---

## Responsibilities

Check:

- Missing information.
- Impossible schedules.
- Budget conflicts.
- User preferences.

---

## Input

Complete itinerary.

---

## Output

```json
{
    "approved":true,
    "suggestions":[]
}
```

---

# Agent Execution Flow

Example:

User:

```
Plan 7 days Japan trip
```

---

Flow:

```
Requirement Agent

↓

Supervisor Agent

↓

Flight Agent

↓

Hotel Agent

↓

Activity Agent

↓

Budget Agent

↓

Itinerary Agent

↓

Review Agent

↓

User
```

---

# Agent State Contract

Agents read/write LangGraph state.

Example:

```
TravelState
```

Contains:

```
destination

dates

budget

preferences

flight_options

hotel_options

activities

itinerary
```

---

# Agent Prompt Architecture

Every agent should have:

```
prompts/
```

Example:

```
prompts/

flight_agent_prompt.py

hotel_agent_prompt.py

planner_prompt.py
```

---

# Prompt Rules

Prompts should define:

- Role.
- Objective.
- Available information.
- Expected output.
- Constraints.

---

Example:

```
You are a Flight Recommendation Agent.

Your responsibility is to recommend flights.

Do not recommend hotels.

Return structured JSON.
```

---

# Agent Error Handling

Agents should handle:

- Missing data.
- Tool failures.
- Invalid outputs.

Example:

```
Flight API Failure

↓

Agent fallback

↓

Continue planning
```

---

# Agent Testing

Every agent requires:

## Unit Tests

Test reasoning behavior.

Example:

```
Budget Agent calculates totals correctly.
```

---

## Tool Tests

Example:

```
Flight Agent correctly calls flight tool.
```

---

## Integration Tests

Example:

```
Multiple agents generate itinerary.
```

---

# Future Multi-Agent Architecture

Production version:

```
                    Supervisor

                        |

        --------------------------------

        |              |               |

    Research       Planning       Optimization


        |              |               |

        --------------------------------

                        |

                 Final Response
```

---

# Future Agent Capabilities

Possible additions:

## Visa Agent

Handles:

- Visa requirements.
- Documentation.

---

## Packing Agent

Generates:

- Packing checklist.

---

## Safety Agent

Provides:

- Travel warnings.
- Safety recommendations.

---

## Booking Agent

Handles:

- Reservations.
- Confirmations.

---

# Final Agent Architecture Goal

The system should evolve from:

```
Single AI assistant
```

into:

```
Collaborative AI Travel Team

Supervisor

+

Specialized Agents

+

Tools

+

Memory

+

Human Approval
```

The architecture should make adding new agents simple without modifying existing agents.
