# AI Travel Planner Tools Design

Version: 1.0.0

---

# Purpose

This document defines the tool architecture for the AI Travel Planner.

Tools provide external capabilities to AI agents.

Examples:

- Flight search
- Hotel search
- Weather information
- Maps
- Currency conversion
- Attractions discovery

---

# Tool Architecture

The tool execution flow:

```
Agent

↓

LangChain Tool

↓

Service Layer

↓

External API

↓

Tool Response

↓

Agent Reasoning

↓

LangGraph State
```

---

# Tool Design Principles

Every tool must:

- Have one responsibility
- Have clear input schema
- Have clear output schema
- Validate inputs
- Handle failures
- Return structured data
- Be independently testable

---

# Tool Location

All tools should exist inside:

```
backend/app/tools/
```

Structure:

```
tools/

├── flight_tool.py

├── hotel_tool.py

├── weather_tool.py

├── currency_tool.py

├── maps_tool.py

├── attraction_tool.py

├── restaurant_tool.py

└── base.py
```

---

# Base Tool Interface

All tools should follow a common pattern.

Example:

```python
class TravelTool:

    name: str

    description: str


    async def execute():

        pass
```

---

# Tool Naming Convention

Use descriptive names.

Good:

```
search_flights

get_weather_forecast

calculate_currency_conversion
```

Avoid:

```
tool1

helper

api_call
```

---

# Tool Input Rules

Inputs should always be validated.

Use:

```
Pydantic schemas
```

Example:

```python
class FlightSearchInput(BaseModel):

    departure: str

    destination: str

    date: str
```

---

# Tool Output Rules

Tools should return structured responses.

Example:

```json
{
    "success":true,
    "results":[]
}
```

---

# Tool Error Handling

Never return raw exceptions.

Bad:

```
ConnectionError
```

---

Good:

```json
{
    "success":false,
    "error":"Flight service unavailable"
}
```

---

# Tool Categories

---

# 1. Flight Search Tool

## Purpose

Provides flight information.

Used by:

```
Flight Agent
```

---

## File

```
flight_tool.py
```

---

## Input

```json
{
    "departure":"Kolkata",
    "destination":"Tokyo",
    "date":"2026-04-01"
}
```

---

## Output

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

## Future APIs

Possible integrations:

- Amadeus API
- Skyscanner API
- Travelport API

---

# 2. Hotel Search Tool

## Purpose

Find accommodation.

Used by:

```
Hotel Agent
```

---

## Input

```json
{
    "location":"Tokyo",
    "check_in":"2026-04-01",
    "check_out":"2026-04-07"
}
```

---

## Output

```json
{
    "hotels":[
        {
            "name":"Hotel Example",
            "rating":4.5,
            "price":120
        }
    ]
}
```

---

# 3. Weather Tool

## Purpose

Provides weather information.

Used by:

```
Weather Agent
```

---

## Input

```json
{
    "location":"Tokyo",
    "date":"2026-04-01"
}
```

---

## Output

```json
{
    "temperature":"20C",
    "condition":"Sunny"
}
```

---

# 4. Currency Conversion Tool

## Purpose

Convert currencies.

Used by:

```
Budget Agent
```

---

## Input

```json
{
    "from":"USD",
    "to":"JPY",
    "amount":1000
}
```

---

## Output

```json
{
    "converted_amount":150000
}
```

---

# 5. Maps / Distance Tool

## Purpose

Calculate:

- Distance
- Travel time
- Routes

---

## Input

```json
{
    "from":"Tokyo Station",
    "to":"Mount Fuji"
}
```

---

## Output

```json
{
    "distance":"120km",
    "duration":"2 hours"
}
```

---

# 6. Attraction Search Tool

## Purpose

Find tourist activities.

Used by:

```
Activity Agent
```

---

## Input

```json
{
    "location":"Tokyo",
    "category":"culture"
}
```

---

## Output

```json
{
    "places":[]
}
```

---

# 7. Restaurant Search Tool

## Purpose

Recommend food experiences.

---

## Input

```json
{
    "location":"Tokyo",
    "cuisine":"Japanese"
}
```

---

## Output

```json
{
    "restaurants":[]
}
```

---

# Tool Development Strategy

Tools should be developed in stages.

---

# Phase 1: Mock Tools

Purpose:

Build agent workflows without external dependencies.

Example:

```python
mock_flight_tool()
```

Returns:

```json
{
"price":500
}
```

---

# Phase 2: API Integration

Replace mock implementation.

Example:

```
Mock Flight Tool

↓

Amadeus API
```

Agent code remains unchanged.

---

# Phase 3: Production Tools

Add:

- Authentication
- Rate limiting
- Caching
- Monitoring
- Retry strategy

---

# Tool Retry Strategy

External services fail.

Implement:

```
Attempt 1

↓

Retry

↓

Retry

↓

Fallback
```

Recommended:

Maximum retries:

```
3
```

---

# Tool Timeout

Every external tool requires timeout.

Example:

```
Flight API timeout:

10 seconds
```

---

# Tool Caching

Cache expensive requests.

Examples:

Weather:

```
5 minutes
```

Currency:

```
15 minutes
```

Attractions:

```
24 hours
```

---

# Tool Security

Never expose:

- API keys
- Tokens
- Internal URLs

Use:

```
.env
```

---

# Tool Observability

Track:

- Tool name
- Execution time
- Success/failure
- API response
- Error rate

Example:

```
FlightTool

Execution:

2.4 seconds

Status:

Success
```

---

# Tool Testing

Every tool requires:

## Unit Test

Example:

```
Input validation works.
```

---

## Integration Test

Example:

```
External API response parsed correctly.
```

---

## Failure Test

Example:

```
API unavailable handled correctly.
```

---

# LangChain Tool Registration

Agents should receive tools explicitly.

Example concept:

```
Flight Agent

Tools:

[
 FlightSearchTool
]
```

Avoid:

```
Give all tools to every agent
```

---

# Tool Permissions

Example:

```
Flight Agent

Allowed:

Flight Tool


Hotel Agent

Allowed:

Hotel Tool


Budget Agent

Allowed:

Currency Tool
```

---

# Future Advanced Tools

Possible additions:

---

## Booking Tool

Purpose:

Actual reservation.

Requires:

Human approval.

---

## Document Tool

Purpose:

Generate:

- PDF itinerary
- Travel documents

---

## Memory Tool

Purpose:

Retrieve:

- User preferences
- Previous trips

---

## Search Tool

Purpose:

General travel research.

---

# Final Tool Architecture

```
                 Agent

                   |

                   v

            LangChain Tool

                   |

        ----------------------

        |          |         |

       API     Database    Service


                   |

                   v

              Structured Result
```

---

# Design Goal

Tools should make the AI system capable without making agents complex.

Agents decide.

Tools execute.

LangGraph coordinates.

Services control business logic.

```
