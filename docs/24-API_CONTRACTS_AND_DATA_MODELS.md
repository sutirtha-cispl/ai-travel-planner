# AI Travel Planner - API Contracts and Data Models

Version: 1.0.0

---

# Purpose

This document defines the communication contracts between all major system components.

The objective is to maintain:

- Clear API boundaries.
- Consistent data structures.
- Predictable agent communication.
- Easier frontend/backend development.
- Better AI code generation.

---

# Architecture Communication Model

```
Frontend

   |

   | HTTP / JSON

   v

Backend API

   |

   | Internal Services

   v

Agent Orchestration Layer

   |

   | Structured Data

   v

Agents

   |

   | Tool Calls

   v

External Services
```

---

# API Design Principles

Follow:

```
RESTful APIs

+

Strong Validation

+

Typed Schemas

+

Consistent Responses
```

---

# API Versioning

All APIs must use:

```
/api/v1/
```

Example:

```
GET /api/v1/trips
```

---

# Standard API Response Format

All APIs should return:

```json
{
"success":true,

"data":{},

"message":"",

"error":null
}
```

---

# Error Response Format

Example:

```json
{
"success":false,

"data":null,

"message":"Validation failed",

"error":{
    "code":"INVALID_INPUT"
}
}
```

---

# Authentication Contract

## Login API

Endpoint:

```
POST /api/v1/auth/login
```

---

Request:

```json
{
"email":"user@example.com",

"password":"password"
}
```

---

Response:

```json
{
"access_token":"jwt-token",

"token_type":"bearer",

"user":{
"id":1,

"email":"user@example.com"
}
}
```

---

# User Registration API

Endpoint:

```
POST /api/v1/auth/register
```

---

Request:

```json
{
"name":"John",

"email":"john@example.com",

"password":"password"
}
```

---

Response:

```json
{
"user_id":1,

"message":"Account created"
}
```

---

# User Profile Contract

Entity:

```
UserProfile
```

---

Schema:

```json
{
"user_id":1,

"travel_style":"budget",

"preferred_activities":[
"food",
"culture"
],

"budget_range":"medium",

"favorite_destinations":[
"Japan"
]
}
```

---

# Trip Planning API

Main AI interaction endpoint.

---

Endpoint:

```
POST /api/v1/trips/plan
```

---

# Request

```json
{
"message":
"Plan a 7 day Japan trip",

"preferences":{

"budget":2000,

"style":"culture"

}
}
```

---

# Response

```json
{
"trip_id":"abc123",

"status":"completed",

"itinerary":{}
}
```

---

# Trip Entity Model

Database:

```
trips
```

---

Schema:

```json
{
"id":"uuid",

"user_id":1,

"title":"Japan Trip",

"destination":"Japan",

"start_date":"2026-04-01",

"end_date":"2026-04-07",

"budget":2000,

"status":"completed"
}
```

---

# Itinerary Contract

Entity:

```
Itinerary
```

---

Schema:

```json
{
"destination":"Tokyo",

"days":[

{
"day":1,

"activities":[

{
"title":"Tokyo Tower",

"time":"10:00",

"location":"Tokyo"
}

]

}

]
}
```

---

# Agent State Contract

LangGraph shared state.

---

Location:

```
graph/state.py
```

---

Schema:

```python
class TravelState:

    user_id:str

    messages:list

    destination:str

    travel_dates:dict

    budget:int

    preferences:list

    requirements:dict

    retrieved_memory:list

    retrieved_documents:list

    tool_results:list

    itinerary:dict

    review_notes:list

    status:str
```

---

# Agent Communication Contract

Every agent receives:

```
Current State
```

and returns:

```
Updated State
```

---

# Agent Input Format

Example:

```json
{
"destination":"Japan",

"budget":2000,

"preferences":[
"food"
]
}
```

---

# Agent Output Format

Example:

```json
{
"updated_fields":{

"strategy":"budget cultural trip"

}
}
```

---

# Requirement Agent Contract

Purpose:

Extract user requirements.

---

Input:

```json
{
"message":
"Plan Japan trip"
}
```

---

Output:

```json
{
"destination":"Japan",

"duration":7,

"budget":2000,

"preferences":[
"culture"
]
}
```

---

# Planner Agent Contract

Purpose:

Create travel strategy.

---

Input:

```
Travel Requirements
```

---

Output:

```json
{
"strategy":

"Affordable cultural experience"
}
```

---

# Flight Tool Contract

Endpoint:

Internal Tool

---

Input:

```json
{
"from":"Kolkata",

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
"airline":"Example",

"price":500,

"duration":"8h"
}

]
}
```

---

# Hotel Tool Contract

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

# Weather Tool Contract

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

# Memory Contract

## Store Memory

Input:

```json
{
"user_id":1,

"type":"preference",

"content":

"Likes cultural experiences"
}
```

---

Output:

```json
{
"stored":true
}
```

---

# Retrieve Memory

Input:

```json
{
"user_id":1,

"query":

"Suggest activities"
}
```

---

Output:

```json
{
"memories":[]
}
```

---

# RAG Retrieval Contract

Input:

```json
{
"query":

"Japan visa requirements"
}
```

---

Output:

```json
{
"documents":[

{
"title":"Japan Visa Guide",

"content":"..."
}

]
}
```

---

# Background Job Contract

For long-running AI tasks.

---

Example:

Generate PDF itinerary.

---

Request:

```json
{
"trip_id":"abc123"
}
```

---

Response:

```json
{
"job_id":"xyz",

"status":"processing"
}
```

---

# Status Values

Use consistent statuses:

```
pending

processing

completed

failed
```

---

# Validation Rules

All incoming data requires:

- Type validation.
- Required field validation.
- Format validation.

---

# Date Validation

Example:

Invalid:

```
end_date before start_date
```

---

# Budget Validation

Example:

Invalid:

```
negative budget
```

---

# API Security Rules

All protected endpoints require:

```
Authorization Header
```

---

Example:

```
Bearer JWT_TOKEN
```

---

# Rate Limits

Recommended:

Authentication:

```
10 requests/minute
```

---

AI Planning:

```
30 requests/hour/user
```

---

# API Testing Requirements

Every endpoint requires:

## Unit Tests

Validate:

- Request schema.
- Response schema.

---

## Integration Tests

Validate:

```
Frontend

↓

API

↓

Agent Workflow
```

---

# API Documentation

Generate:

```
OpenAPI Documentation
```

Available at:

```
/docs
```

---

# Version Migration Strategy

When changing contracts:

Create:

```
v2
```

instead of breaking:

```
v1
```

---

# Final Goal

All system communication should be:

```
Predictable

+

Validated

+

Typed

+

Documented
```

Clear contracts allow humans and AI coding assistants to build the system safely.
