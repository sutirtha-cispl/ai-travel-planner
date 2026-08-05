# AI Travel Planner - Sprint 3 Tools and Integrations

Version: 1.0.0

---

# Sprint Objective

Connect the Agentic AI workflow with external capabilities.

The goal of this sprint is to evolve the system from:

```
AI Reasoning System
```

into:

```
AI Reasoning + Real World Data System
```

using:

- LangChain Tools
- External APIs
- Service integrations
- Tool-based agent execution

---

# Sprint Duration

Recommended:

```
3-4 Weeks
```

---

# Sprint Outcome

At the end of this sprint, the system should:

- Support external tool execution.
- Allow agents to use specialized tools.
- Retrieve real travel information.
- Handle API failures.
- Cache expensive requests.
- Provide better itinerary recommendations.

---

# Reference Documents

Read before implementation:

```
AGENTS.md

docs/09-AGENTS_DESIGN.md

docs/10-TOOLS.md

docs/11-PROMPTS.md

docs/12-TESTING.md
```

---

# Sprint Architecture

After Sprint 3:

```
                         User

                          |

                          v

                   LangGraph Workflow

                          |

                          v

                   Supervisor Agent

                          |

        -------------------------------------

        |              |            |        |

        v              v            v        v


    Flight Agent  Hotel Agent Weather Activity Agent


        |              |            |        |

        -------------------------------------

                          |

                          v

                  LangChain Tools


                          |

        -------------------------------------

        |              |            |        |

      Flight API   Hotel API   Weather API  Maps API

```

---

# Sprint Scope

## Included

- LangChain tool framework.
- External API abstraction.
- Flight tool.
- Hotel tool.
- Weather tool.
- Maps tool.
- Activity tool.
- Tool error handling.
- Tool testing.


## Not Included

- Booking system.
- Payment processing.
- User memory.
- Autonomous booking.

---

# Task 1: Tool Framework Setup

## Goal

Create reusable tool architecture.

---

Create:

```
backend/app/tools/
```

Structure:

```
tools/

├── base.py

├── flight_tool.py

├── hotel_tool.py

├── weather_tool.py

├── maps_tool.py

├── activity_tool.py

└── currency_tool.py
```

---

# Base Tool Interface

Create:

```
tools/base.py
```

---

Responsibilities:

- Common tool behavior.
- Error handling.
- Logging.
- Response formatting.

---

Example:

```python
class BaseTravelTool:

    name:str

    description:str


    async def execute():

        pass
```

---

# Task 2: Tool Configuration

## Goal

Centralize external API settings.

---

Create:

```
config/tools.py
```

---

Store:

- API keys.
- Base URLs.
- Timeout values.
- Retry configuration.

---

Example:

```env
FLIGHT_API_KEY=

HOTEL_API_KEY=

WEATHER_API_KEY=
```

---

# Task 3: Flight Search Tool

## Goal

Provide flight recommendations.

---

Create:

```
tools/flight_tool.py
```

---

Used By:

```
Flight Agent
```

---

Input:

```json
{
"departure":"Kolkata",
"destination":"Tokyo",
"date":"2026-04-01"
}
```

---

Output:

```json
{
"flights":[
 {
  "airline":"Example Airlines",
  "price":500,
  "duration":"8 hours"
 }
]
}
```

---

Implementation Stages:

## Stage 1

Mock response.

---

## Stage 2

External API integration.

Possible providers:

- Amadeus
- Travel APIs

---

# Task 4: Hotel Search Tool

## Goal

Recommend accommodation.

---

Create:

```
tools/hotel_tool.py
```

---

Used By:

```
Hotel Agent
```

---

Input:

```json
{
"location":"Tokyo",
"budget":1000
}
```

---

Output:

```json
{
"hotels":[]
}
```

---

Capabilities:

- Search hotels.
- Compare ratings.
- Compare prices.

---

# Task 5: Weather Tool

## Goal

Provide weather information.

---

Create:

```
tools/weather_tool.py
```

---

Used By:

```
Weather Agent
```

---

Input:

```json
{
"location":"Tokyo",
"date":"2026-04-01"
}
```

---

Output:

```json
{
"temperature":"20C",
"condition":"Sunny"
}
```

---

# Task 6: Maps and Distance Tool

## Goal

Optimize itinerary planning.

---

Create:

```
tools/maps_tool.py
```

---

Capabilities:

- Distance calculation.
- Travel duration.
- Route suggestion.

---

Input:

```json
{
"from":"Tokyo Station",
"to":"Mount Fuji"
}
```

---

Output:

```json
{
"distance":"120km",
"duration":"2 hours"
}
```

---

# Task 7: Activity Search Tool

## Goal

Find attractions and experiences.

---

Create:

```
tools/activity_tool.py
```

---

Used By:

```
Activity Agent
```

---

Input:

```json
{
"location":"Tokyo",
"interest":"food"
}
```

---

Output:

```json
{
"activities":[]
}
```

---

# Task 8: Currency Tool

## Goal

Support international budgeting.

---

Create:

```
tools/currency_tool.py
```

---

Input:

```json
{
"from":"USD",
"to":"JPY",
"amount":1000
}
```

---

Output:

```json
{
"converted":150000
}
```

---

# Task 9: Create Specialized Agents

Add:

```
agents/

├── flight_agent.py

├── hotel_agent.py

├── weather_agent.py

└── activity_agent.py
```

---

# Flight Agent

Responsibilities:

- Call flight tool.
- Analyze options.
- Recommend flights.

---

# Hotel Agent

Responsibilities:

- Call hotel tool.
- Evaluate accommodation.

---

# Weather Agent

Responsibilities:

- Analyze weather conditions.

---

# Activity Agent

Responsibilities:

- Find attractions.
- Match user interests.

---

# Task 10: Update LangGraph Workflow

Current:

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

New:

```
Requirement Agent

↓

Supervisor Agent

        |

--------------------------------

|          |          |          |

Flight   Hotel    Weather   Activity


        |

        v

Planner Agent

        |

        v

Itinerary Agent

        |

        v

Review Agent

        |

        v

END
```

---

# Task 11: Tool Permission Management

Agents should only access required tools.

---

Example:

Flight Agent:

Allowed:

```
Flight Tool
```

---

Hotel Agent:

Allowed:

```
Hotel Tool
```

---

Budget Agent:

Allowed:

```
Currency Tool
```

---

Never:

```
All agents receive all tools
```

---

# Task 12: Tool Error Handling

External services can fail.

Implement:

- Retry.
- Timeout.
- Fallback response.

---

Example:

API failure:

```json
{
"success":false,
"message":"Flight service unavailable"
}
```

---

# Task 13: Tool Caching

Cache expensive operations.

---

Recommended:

Weather:

```
5 minutes
```

Currency:

```
15 minutes
```

Activities:

```
24 hours
```

---

Possible technologies:

- Redis
- Local cache

---

# Task 14: Tool Testing

Create:

```
tests/tools/
```

---

Required tests:

---

## Flight Tool Test

Verify:

Input:

```
Tokyo flight search
```

Returns:

```
flight list
```

---

## Failure Test

Simulate:

```
API unavailable
```

Expected:

Graceful handling.

---

## Validation Test

Invalid input:

Expected:

Validation error.

---

# Task 15: Agent Tool Integration Testing

Test:

```
User Request

↓

Agent

↓

Tool Call

↓

Result

↓

Final Response
```

---

Example:

User:

```
Find flights to Japan
```

Expected:

```
Flight Agent

↓

Flight Tool

↓

Recommendation
```

---

# Task 16: Observability

Track:

- Tool execution time.
- API failures.
- Agent tool calls.
- Token usage.

---

Example:

```
FlightTool

Execution:

1.8 seconds

Status:

Success
```

---

# Sprint Completion Checklist

## Tools

☐ Base tool created

☐ Flight tool created

☐ Hotel tool created

☐ Weather tool created

☐ Maps tool created

☐ Activity tool created

☐ Currency tool created


---

## Agents

☐ Tool-enabled agents created

☐ Agent permissions configured


---

## Workflow

☐ LangGraph updated

☐ Tool routing implemented


---

## Quality

☐ Error handling added

☐ Tool tests created

☐ Integration tests created

---

# Sprint Demo

User:

```
Plan a 7 day Japan trip.

Budget: $2500.

I like food and culture.
```

System:

1. Extracts requirements.

2. Finds flights.

3. Finds hotels.

4. Checks weather.

5. Finds activities.

6. Calculates budget.

7. Generates itinerary.

8. Reviews final plan.

---

# Next Sprint

After completing Sprint 3, proceed to:

```
docs/17-SPRINT_4_PRODUCTIZATION.md
```

Sprint 4 will introduce:

- Authentication
- User profiles
- Memory
- RAG
- Production deployment
- Monitoring
- Security
- Scaling
