# AI Travel Planner Coding Standards

Version: 1.0.0

---

# Purpose

This document defines coding standards and engineering practices for the AI Travel Planner project.

These rules apply to:

- Backend development
- Frontend development
- LangChain implementation
- LangGraph workflows
- Database operations
- API development
- Testing

All AI-generated code must follow these standards.

---

# Core Engineering Principles

The project follows:

- Clean Code principles
- SOLID principles
- DRY principle
- KISS principle
- Separation of Concerns
- Composition over inheritance
- Explicit over implicit behavior

---

# General Rules

## Code should be:

- Easy to read
- Easy to test
- Easy to modify
- Self-documenting
- Modular

---

# Avoid

Never create:

- Giant files
- Giant classes
- Giant functions
- Duplicate logic
- Hidden dependencies
- Magic values
- Hardcoded secrets
- Unused code

---

# Code Organization

Every module should have a clear responsibility.

Good:

```
trip_service.py

Handles trip business logic.
```

Bad:

```
trip_service.py

Handles:

- Database
- API calls
- AI prompts
- Email
- PDF generation
```

---

# Python Standards

---

# Python Version

Required:

```
Python >= 3.12
```

---

# Formatting

Use:

```
Black
```

Recommended line length:

```
88 characters
```

---

# Import Rules

Imports should be grouped:

Example:

```python
# Standard library
import logging
from datetime import datetime

# Third party
from fastapi import FastAPI
from pydantic import BaseModel

# Local
from app.services.trip_service import TripService
```

---

# Type Hints

Type hints are mandatory.

Bad:

```python
def create_trip(data):
    pass
```

Good:

```python
def create_trip(
    request: TripRequest
) -> TripResponse:
    pass
```

---

# Function Rules

Functions should:

- Do one thing
- Have descriptive names
- Be easy to test

Preferred:

```
20-50 lines
```

Avoid:

```
100+ line functions
```

---

# Naming Rules

Variables:

```python
user_preferences
trip_destination
```

Classes:

```python
TripPlannerAgent
```

Functions:

```python
generate_itinerary()
```

Constants:

```python
DEFAULT_TIMEOUT
```

---

# Classes

Classes should represent one responsibility.

Good:

```python
class BudgetCalculator:
    pass
```

Bad:

```python
class TravelManager:
    pass
```

Containing:

- Flights
- Hotels
- Budget
- Users
- Emails

---

# Dependency Injection

Prefer dependency injection.

Example:

Good:

```python
class TripService:

    def __init__(
        self,
        repository: TripRepository
    ):
        self.repository = repository
```

Avoid:

```python
class TripService:

    repository = TripRepository()
```

---

# Error Handling

Never ignore exceptions.

Bad:

```python
try:
    process()
except:
    pass
```

---

Good:

```python
try:
    process()

except ExternalAPIError as error:
    logger.error(
        "API failed",
        exc_info=error
    )
    raise
```

---

# Custom Exceptions

Create meaningful exceptions.

Example:

```
exceptions.py
```

Example:

```python
class TripNotFoundError(Exception):
    pass
```

---

# Logging Standards

Use:

```python
logging
```

Never use:

```python
print()
```

---

# Log:

- Application events
- Errors
- API failures
- Agent execution
- Tool execution
- Performance


---

# Never log:

- Passwords
- API keys
- Tokens
- Private information

---

# Configuration Management

Never hardcode:

Bad:

```python
OPENAI_KEY="abc123"
```

Good:

```python
settings.openai_api_key
```

---

Use:

```
.env
```

with:

```
.env.example
```

---

# FastAPI Standards

---

# Route Responsibility

Routes should only:

- Receive requests
- Validate input
- Call services
- Return responses


Example:

```
Route

↓

Service

↓

Repository
```

---

# Bad Example

```python
@app.get("/trips")
def trips():

    query database

    call AI

    generate PDF

    return response
```

---

# Good Example

```python
@app.get("/trips")
async def get_trip():

    return await trip_service.get_trip()
```

---

# API Response Models

Always use Pydantic models.

Bad:

```python
return {
"id":1
}
```

Good:

```python
return TripResponse(...)
```

---

# HTTP Status Codes

Use proper status codes.

Examples:

200

Successful request

201

Created

400

Bad request

401

Unauthorized

404

Not found

500

Server error

---

# Async Programming

Use async for:

- API calls
- Database calls
- External services


Example:

```python
async def fetch_weather():
    pass
```

---

# LangChain Standards

---

# Model Access

Do not call models directly everywhere.

Bad:

```python
OpenAI()
```

inside multiple files.

---

Create:

```
services/llm_service.py
```

or

```
core/llm.py
```

---

# Prompt Management

Never:

```python
prompt = """
You are a travel planner
"""
```

inside agents.

---

Use:

```
prompts/
```

Example:

```
planner_prompt.py
```

---

# Tool Standards

Every tool requires:

- Name
- Description
- Input schema
- Output schema
- Error handling


Example:

```
FlightSearchTool

Input:

departure

destination

date


Output:

flight list
```

---

# LangGraph Standards

---

# Graph State

State must be typed.

Example:

```python
class TravelState(TypedDict):

    destination: str

    budget: float
```

---

# Nodes

Every node:

- Performs one task
- Has clear input
- Has clear output


Good:

```
collect_requirements()

validate_trip()

generate_plan()
```

---

Bad:

```
process_everything()
```

---

# Agents

Each agent has one responsibility.

Example:

Good:

```
FlightAgent

HotelAgent

BudgetAgent
```

Bad:

```
TravelAgent

Does everything.
```

---

# Database Standards

---

# ORM

Use:

SQLAlchemy


---

# Models

Database models:

```
models/
```

---

# Queries

Only repositories can access database.

Allowed:

```
Repository

↓

Database
```

Forbidden:

```
Service

↓

Database
```

---

# Schema Validation

Use Pydantic.

Separate:

Database Models

from

API Schemas

---

# Frontend Standards

---

# TypeScript

Strict mode enabled.

---

# Components

Components should be:

- Small
- Reusable
- Focused

---

Avoid:

```
1000 line component
```

---

# React Rules

Prefer:

- Functional components
- Hooks
- Composition

Avoid:

- Class components
- Global state unnecessarily

---

# API Communication

Frontend communicates through:

```
services/
```

Example:

```
trip.service.ts
```

Never call APIs directly inside components.

---

# Testing Standards

---

# Backend

Use:

```
pytest
```

Test:

- Services
- Tools
- Agents
- Graph nodes
- APIs

---

# Frontend

Test:

- Components
- Hooks
- User interactions

---

# Test Naming

Example:

```python
test_should_generate_itinerary_when_budget_exists()
```

Tests should describe behavior.

---

# Documentation Standards

Every important module should contain:

- Purpose
- Usage
- Dependencies


---

# Git Standards

Use:

Conventional Commits


Examples:

```
feat(chat): add streaming response

fix(api): handle invalid trip request

test(agent): add planner tests

docs: update architecture
```

---

# Code Review Checklist

Before merging:

Check:

- Does it follow architecture?
- Are responsibilities separated?
- Are tests added?
- Are errors handled?
- Is logging present?
- Are secrets protected?
- Is documentation updated?

---

# AI Code Generation Rules

When generating code:

Always:

1. Explain approach.
2. Show affected files.
3. Keep changes minimal.
4. Follow project structure.
5. Add tests.
6. Mention assumptions.


Never:

- Generate unnecessary files.
- Refactor unrelated code.
- Change architecture without approval.
- Skip validation.
- Skip error handling.

---

# Definition of Quality

Code is considered complete only when:

- It works.
- It is readable.
- It is tested.
- It follows architecture.
- It can be maintained by another developer.
