# AI Travel Planner - AI Development Instructions

Version: 1.0.0

---

# Purpose

This file defines the rules and operating instructions for AI coding assistants working on this project.

Applicable to:

- OpenCode AI
- Cline
- Cursor
- Other AI development agents

The AI assistant must follow these instructions before making any changes.

---

# Project Overview

AI Travel Planner is an Agentic AI application that helps users:

- Plan trips
- Research destinations
- Compare travel options
- Generate itineraries
- Optimize budgets
- Remember travel preferences


Core technologies:

Backend:

- Python
- FastAPI
- LangChain
- LangGraph
- SQLAlchemy


Frontend:

- React
- TypeScript


Database:

- SQLite (development)
- PostgreSQL (production)


---

# First Step Before Coding

Before implementing any feature:

Read:

```
docs/01-ROADMAP.md

docs/02-ARCHITECTURE.md

docs/03-PROJECT_STRUCTURE.md

docs/04-CODING_STANDARDS.md
```

Then read the documents related to the requested task.

Examples:

Adding Agent:

Read:

```
docs/08-GRAPH_DESIGN.md

docs/09-AGENTS_DESIGN.md
```

Adding Tool:

Read:

```
docs/10-TOOLS.md
```

Adding Prompt:

Read:

```
docs/11-PROMPTS.md
```

Database change:

Read:

```
docs/07-DATABASE.md
```

---

# Development Approach

Always follow this workflow:

```
Understand Requirement

↓

Review Existing Architecture

↓

Create Implementation Plan

↓

Identify Files To Change

↓

Implement

↓

Run Tests

↓

Review Changes

↓

Update Documentation
```

---

# Before Making Changes

Always explain:

1. What you are going to change.
2. Why the change is required.
3. Which files will be modified.
4. Possible risks.

Do not immediately modify files without understanding the impact.

---

# Architecture Rules

The project follows:

```
Clean Architecture

+

Layered Design

+

Agent-Based Architecture
```

---

# Backend Dependency Flow

Always follow:

```
API Layer

↓

Service Layer

↓

Repository Layer

↓

Database Layer
```

---

# AI Dependency Flow

Always follow:

```
Service Layer

↓

LangGraph

↓

Agents

↓

LangChain Tools

↓

External Services
```

---

# Forbidden Dependencies

Never create:

```
API

↓

Database
```

---

Never create:

```
Agent

↓

Database
```

---

Never create:

```
Agent

↓

External API
```

---

All communication must go through proper layers.

---

# File Creation Rules

Before creating a file:

Check:

```
docs/03-PROJECT_STRUCTURE.md
```

Do not create random folders.

---

Example:

Correct:

```
backend/app/agents/weather_agent.py
```

Incorrect:

```
backend/helpers/weather.py
```

---

# Coding Standards

All code must follow:

```
docs/04-CODING_STANDARDS.md
```

---

Required:

- Type hints
- Clear naming
- Error handling
- Logging
- Tests
- Documentation

---

# Python Rules

Always use:

- Python type hints
- Async where appropriate
- Pydantic validation
- Dependency injection

---

Avoid:

- Global variables
- Hardcoded configuration
- Large functions
- Duplicate logic

---

# FastAPI Rules

Routes should only:

- Validate requests
- Call services
- Return responses


Never:

- Add business logic
- Call databases directly
- Call AI models directly

---

# LangGraph Rules

All AI workflows must use:

```
LangGraph
```

---

Agents should communicate through:

```
Shared Graph State
```

Never:

```
Agent A directly calls Agent B
```

---

# Agent Rules

Every agent must:

Have:

- Single responsibility
- Clear input
- Clear output
- Defined tools
- Tests


Example:

Good:

```
FlightAgent

Only handles flights.
```

Bad:

```
TravelAgent

Handles everything.
```

---

# Tool Rules

Tools must:

- Have schemas
- Validate input
- Return structured output
- Handle failures
- Be tested


Never expose:

- API keys
- Secrets
- Tokens

---

# Prompt Rules

Prompts are production assets.

Never write:

```python
prompt = "..."
```

inside agents.

---

Always use:

```
backend/app/prompts/
```

---

Prompt changes require:

- Documentation
- Evaluation examples
- Version tracking

---

# Database Rules

All database access must go through:

```
Repositories
```

---

Never:

```
Service → SQL Query
```

---

Always:

```
Service

↓

Repository

↓

Database
```

---

# Testing Rules

Every feature requires tests.

---

New Agent:

Required:

- Agent tests
- Graph tests

---

New Tool:

Required:

- Unit tests
- Failure tests

---

New API:

Required:

- API tests
- Schema tests

---

New Database Model:

Required:

- Migration
- Repository tests

---

# Git Rules

Use:

Conventional Commits

Format:

```
type(scope): description
```

Examples:

```
feat(agent): add flight agent

fix(api): handle invalid request

docs: update architecture
```

---

# Change Management Rules

Avoid:

- Large unrelated changes
- Unnecessary refactoring
- Dependency changes without approval

---

Prefer:

Small incremental changes.

---

# Debugging Rules

When fixing issues:

Follow:

```
Reproduce

↓

Identify Layer

↓

Find Root Cause

↓

Apply Minimal Fix

↓

Add Regression Test
```

---

# Security Rules

Never commit:

- API keys
- Passwords
- Tokens
- Environment secrets


Use:

```
.env
```

and:

```
.env.example
```

---

# Documentation Rules

If architecture changes:

Update:

```
docs/
```

---

Examples:

New Agent:

Update:

```
09-AGENTS_DESIGN.md
```

New Tool:

Update:

```
10-TOOLS.md
```

New API:

Update:

```
06-API_SPEC.md
```

---

# AI Response Format

Before implementing:

Provide:

```
Implementation Plan

Files To Modify

Reasoning

Expected Result
```

---

After implementing:

Provide:

```
Changed Files

Testing Performed

Potential Follow-ups
```

---

# Production Quality Rule

Do not optimize for speed of generation.

Optimize for:

- Maintainability
- Scalability
- Reliability
- Security
- Clear architecture

---

# Final Rule

Act as a senior software engineer.

Do not behave like an autocomplete tool.

Every generated change should be suitable for a production Agentic AI application.
