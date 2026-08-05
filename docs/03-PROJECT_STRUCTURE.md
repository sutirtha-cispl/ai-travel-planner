# AI Travel Planner Project Structure

Version: 1.0.0

---

# Purpose

This document defines the standard project structure for the AI Travel Planner.

The purpose is to ensure:

- Consistent file organization
- Clear separation of responsibilities
- Easier maintenance
- Better AI-assisted development
- Scalable architecture

Any new files should follow the rules defined here.

---

# Root Project Structure

```
ai-travel-planner/

│
├── AGENTS.md
├── README.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Makefile
│
├── docs/
│
├── backend/
│
├── frontend/
│
├── tests/
│
├── scripts/
│
└── .github/
```

---

# Root Level Files

---

# AGENTS.md

Purpose:

Contains AI assistant development rules.

Used by:

- OpenCode AI
- Cline
- Cursor
- Other coding agents


Contains:

- Coding rules
- Architecture rules
- Development workflow

---

# README.md

Purpose:

Human-facing project documentation.

Contains:

- Project overview
- Installation
- Running instructions
- Features
- Screenshots

---

# .env.example

Purpose:

Template for environment variables.

Example:

```
OPENAI_API_KEY=

DATABASE_URL=

ENVIRONMENT=

LOG_LEVEL=
```

Never store real secrets.

---

# docker-compose.yml

Purpose:

Local development environment.

Future services:

- Backend
- Frontend
- Database
- Redis
- Vector database

---

# Makefile

Purpose:

Common development commands.

Examples:

```
make install

make test

make run

make lint
```

---

# docs/

Contains all project documentation.

Structure:

```
docs/

├── 01-ROADMAP.md

├── 02-ARCHITECTURE.md

├── 03-PROJECT_STRUCTURE.md

├── 04-CODING_STANDARDS.md

├── 05-DEVELOPMENT_GUIDE.md

├── 06-API_SPEC.md

├── 07-DATABASE.md

├── 08-GRAPH_DESIGN.md

├── 09-AGENTS_DESIGN.md

├── 10-TOOLS.md

├── 11-PROMPTS.md

├── 12-TESTING.md

└── CHANGELOG.md
```

---

# Backend Structure

Location:

```
backend/
```

Purpose:

Contains the FastAPI application and AI system.

Structure:

```
backend/

│
├── app/
│
├── tests/
│
├── requirements.txt
│
└── pyproject.toml
```

---

# Backend Application Structure

```
backend/app/

│
├── main.py
│
├── api/
│
├── core/
│
├── config/
│
├── database/
│
├── models/
│
├── schemas/
│
├── repositories/
│
├── services/
│
├── agents/
│
├── graph/
│
├── tools/
│
├── prompts/
│
├── utils/
│
└── middleware/
```

---

# main.py

Purpose:

Application entry point.

Responsibilities:

- Create FastAPI application
- Register middleware
- Register routes
- Initialize startup events


Should NOT contain:

- Business logic
- AI logic
- Database queries

---

# api/

Purpose:

HTTP API layer.

Structure:

```
api/

├── routes/

│   ├── chat.py

│   ├── trips.py

│   ├── users.py

│   └── preferences.py


└── dependencies.py
```

Responsibilities:

- Receive requests
- Validate inputs
- Call services
- Return responses


Should NOT:

- Call databases directly
- Execute AI workflows directly

---

# core/

Purpose:

Application-wide core functionality.

Example:

```
core/

├── security.py

├── exceptions.py

├── logging.py

└── constants.py
```

Contains:

- Security helpers
- Custom exceptions
- Global constants

---

# config/

Purpose:

Application configuration.

Example:

```
config/

├── settings.py

└── environment.py
```

Handles:

- Environment variables
- Application settings

Example:

```python
OPENAI_API_KEY

DATABASE_URL

DEBUG
```

---

# database/

Purpose:

Database initialization.

Example:

```
database/

├── connection.py

├── session.py

└── migrations/
```

Responsibilities:

- Database connection
- Session management

---

# models/

Purpose:

Database models.

Example:

```
models/

├── user.py

├── trip.py

├── itinerary.py

└── preference.py
```

Contains:

SQLAlchemy models.

---

# schemas/

Purpose:

API and data validation models.

Example:

```
schemas/

├── user.py

├── trip.py

├── chat.py

└── itinerary.py
```

Contains:

Pydantic models.

---

# repositories/

Purpose:

Database access layer.

Example:

```
repositories/

├── user_repository.py

├── trip_repository.py

└── preference_repository.py
```

Responsibilities:

- Database queries
- CRUD operations


Never place SQL queries inside:

- API routes
- Services
- Agents

---

# services/

Purpose:

Business logic.

Example:

```
services/

├── chat_service.py

├── trip_service.py

├── user_service.py

└── export_service.py
```

Responsibilities:

- Application workflows
- Business rules

Example:

```
API

↓

Service

↓

Repository
```

---

# agents/

Purpose:

AI agent implementations.

Example:

```
agents/

├── planner_agent.py

├── flight_agent.py

├── hotel_agent.py

├── budget_agent.py

└── activity_agent.py
```

Each agent should:

- Have one responsibility
- Use tools
- Return structured output

---

# graph/

Purpose:

LangGraph workflows.

Example:

```
graph/

├── state.py

├── nodes.py

├── edges.py

├── workflow.py

└── router.py
```

Responsibilities:

- Graph state
- Node execution
- Conditional routing

---

# tools/

Purpose:

LangChain tools.

Example:

```
tools/

├── flight_tool.py

├── hotel_tool.py

├── weather_tool.py

├── currency_tool.py

└── attraction_tool.py
```

Each tool should:

- Have schema
- Validate inputs
- Handle errors
- Return structured output

---

# prompts/

Purpose:

Central prompt management.

Example:

```
prompts/

├── planner_prompt.py

├── requirement_prompt.py

├── budget_prompt.py

└── summary_prompt.py
```

Rules:

Never write prompts inside agents.

---

# utils/

Purpose:

Reusable helper functions.

Example:

```
utils/

├── date_utils.py

├── formatting.py

└── validators.py
```

Only generic helpers.

---

# middleware/

Purpose:

FastAPI middleware.

Example:

```
middleware/

├── logging.py

└── rate_limit.py
```

---

# Frontend Structure

Location:

```
frontend/
```

Technology:

- React
- TypeScript
- Vite


Structure:

```
frontend/

src/

│
├── app/

├── components/

├── pages/

├── features/

├── hooks/

├── services/

├── store/

├── types/

├── utils/

└── assets/
```

---

# Frontend Responsibilities

---

# components/

Reusable UI components.

Example:

```
ChatBox.tsx

TripCard.tsx

BudgetChart.tsx
```

---

# features/

Feature-based modules.

Example:

```
features/

├── chat/

├── trips/

└── profile/
```

---

# services/

API communication.

Example:

```
api.ts

chat.service.ts

trip.service.ts
```

---

# hooks/

Reusable React hooks.

Example:

```
useChat.ts

useTrip.ts
```

---

# store/

Application state.

Future:

- Zustand
- Redux Toolkit

---

# tests/

Testing structure.

```
tests/

├── unit/

├── integration/

├── api/

├── agents/

├── graph/

└── tools/
```

---

# scripts/

Automation scripts.

Examples:

```
scripts/

├── seed_database.py

├── migrate.py

└── setup.sh
```

---

# .github/

CI/CD configuration.

Example:

```
.github/

└── workflows/

    ├── test.yml

    └── deploy.yml
```

---

# File Naming Rules

Python:

```
snake_case.py
```

Example:

```
trip_service.py
```

---

Classes:

```
PascalCase
```

Example:

```
TripPlannerAgent
```

---

Functions:

```
snake_case
```

Example:

```
generate_itinerary()
```

---

React Components:

```
PascalCase.tsx
```

Example:

```
TripCard.tsx
```

---

# Dependency Direction

Allowed:

```
API

↓

Services

↓

Repositories

↓

Database
```


AI:

```
Services

↓

Graph

↓

Agents

↓

Tools
```

---

Forbidden:

```
Repository

↓

Service
```

```
Agent

↓

Database
```

```
API

↓

Tool
```

---

# Rules for AI Code Generation

When creating new files:

1. Check this document first.
2. Place files in the correct layer.
3. Avoid creating duplicate folders.
4. Avoid unnecessary abstractions.
5. Follow naming conventions.
6. Keep responsibilities isolated.

---

# Final Structure Goal

The final application should clearly separate:

```
Presentation

↓

API

↓

Business Logic

↓

AI Orchestration

↓

Agents

↓

Tools

↓

External Systems


+

Database

+

Memory
```

The structure should remain understandable even when the project grows into a large production application.
