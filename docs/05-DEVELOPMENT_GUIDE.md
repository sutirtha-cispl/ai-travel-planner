# AI Travel Planner Development Guide

Version: 1.0.0

---

# Purpose

This document defines the development workflow for the AI Travel Planner project.

It explains:

- How developers should work
- How AI coding agents should operate
- How features should be implemented
- How changes should be reviewed
- How milestones should be completed

---

# Development Philosophy

The project follows an incremental development approach.

The goal is not to quickly generate code.

The goal is to build a maintainable production-grade Agentic AI system.

Development priorities:

1. Correct architecture
2. Clean implementation
3. Testing
4. Documentation
5. Speed

---

# Development Lifecycle

Every feature follows this lifecycle:

```
Requirement

↓

Design

↓

Implementation Plan

↓

Development

↓

Testing

↓

Code Review

↓

Documentation Update

↓

Merge
```

---

# Before Starting Development

Before implementing anything:

## Step 1

Read:

```
AGENTS.md
```

---

## Step 2

Read relevant documentation:

```
docs/01-ROADMAP.md

docs/02-ARCHITECTURE.md

docs/03-PROJECT_STRUCTURE.md

docs/04-CODING_STANDARDS.md
```

---

## Step 3

Understand:

- Current milestone
- Existing architecture
- Existing code patterns

---

## Step 4

Explain:

- Implementation approach
- Files affected
- Potential risks

---

# Feature Development Process

Every feature should follow these steps.

---

# Step 1: Requirement Understanding

Identify:

- What problem are we solving?
- Which milestone does it belong to?
- What components are affected?

Example:

Feature:

"Generate daily itinerary"

Affected areas:

```
Agent

↓

Graph

↓

API

↓

Frontend
```

---

# Step 2: Architecture Planning

Before coding answer:

Questions:

- Which layer owns this logic?
- Is a new service required?
- Is a new agent required?
- Is a new tool required?
- Does the database need changes?

---

# Step 3: File Planning

Before creating files:

Check:

```
docs/03-PROJECT_STRUCTURE.md
```

Example:

Correct:

```
backend/app/agents/planner_agent.py
```

Incorrect:

```
backend/app/utils/planner_agent.py
```

---

# Step 4: Implementation

Follow:

```
API

↓

Service

↓

Graph

↓

Agent

↓

Tool

↓

External System
```

depending on the requirement.

---

# Step 5: Testing

Every feature requires tests.

Testing order:

```
Unit Tests

↓

Integration Tests

↓

API Tests

↓

End-to-End Tests
```

---

# Step 6: Documentation

Update relevant documentation.

Examples:

New agent:

Update:

```
docs/09-AGENTS_DESIGN.md
```

New tool:

Update:

```
docs/10-TOOLS.md
```

New API:

Update:

```
docs/06-API_SPEC.md
```

---

# Milestone Execution Workflow

Every milestone follows:

```
Understand milestone

↓

Create implementation plan

↓

Implement smallest working version

↓

Test

↓

Review

↓

Refactor

↓

Complete milestone
```

---

# Definition of Done

A milestone is complete only when:

## Code

- Implementation complete
- No broken features
- Clean architecture followed

---

## Testing

- Tests written
- Tests passing

---

## Documentation

Updated:

- Architecture docs
- API docs
- Agent docs
- Tool docs

---

## Quality

- No unused code
- No TODO placeholders
- No hardcoded secrets

---

# Git Workflow

---

# Branch Strategy

Main branches:

```
main

develop
```

---

Feature branches:

```
feature/<name>
```

Example:

```
feature/langgraph-workflow
```

---

Bug fixes:

```
bugfix/<name>
```

Example:

```
bugfix/chat-timeout
```

---

Documentation:

```
docs/<name>
```

Example:

```
docs/update-agent-flow
```

---

# Commit Convention

Use:

Conventional Commits


Format:

```
type(scope): message
```

---

Examples:

Feature:

```
feat(chat): add streaming response
```

Bug:

```
fix(api): handle invalid request
```

Documentation:

```
docs(architecture): update graph flow
```

Testing:

```
test(agent): add planner agent tests
```

---

# Code Review Process

Before merging:

Review:

## Architecture

- Does the code belong in the correct layer?
- Are responsibilities separated?

---

## Maintainability

- Is naming clear?
- Is code readable?
- Is duplication avoided?

---

## Security

Check:

- Secrets
- User data
- API keys

---

## Testing

Check:

- Tests exist
- Edge cases covered

---

# Debugging Workflow

When a problem occurs:

Follow:

```
Reproduce issue

↓

Check logs

↓

Identify layer

↓

Find root cause

↓

Fix smallest possible area

↓

Add regression test
```

---

# Debugging Layers

## Frontend Issue

Check:

```
Browser Console

↓

Network Tab

↓

API Response

↓

Backend Logs
```

---

## API Issue

Check:

```
Request

↓

Validation

↓

Service

↓

Database
```

---

## Agent Issue

Check:

```
Graph State

↓

Node Execution

↓

Prompt

↓

Tool Response
```

---

## Tool Issue

Check:

```
Input Schema

↓

External API

↓

Response Parsing

↓

Error Handling
```

---

# Adding New AI Capabilities

When adding a new AI capability:

Follow this decision process.

---

## Does it require reasoning?

Example:

"Create a travel plan"

Create:

Agent

---

## Does it access external information?

Example:

"Find flights"

Create:

Tool

---

## Does it control workflow?

Example:

"Decide whether to ask questions"

Create:

Graph node

---

## Does it store information?

Example:

"Remember preferences"

Create:

Database model + Repository

---

# Adding a New Agent

Steps:

1. Define responsibility.

Example:

```
Budget Agent

Responsible only for budget optimization.
```

---

2. Define input.

Example:

```
Trip requirements

Flight options

Hotel options
```

---

3. Define output.

Example:

```
Budget recommendation
```

---

4. Add:

```
agents/
```

---

5. Add graph integration.

---

6. Add tests.

---

7. Update:

```
docs/09-AGENTS_DESIGN.md
```

---

# Adding a New Tool

Steps:

1. Define purpose.

Example:

```
Weather information
```

---

2. Define schema.

Input:

```
location

date
```

Output:

```
forecast
```

---

3. Implement:

```
tools/
```

---

4. Add error handling.

---

5. Add tests.

---

6. Update:

```
docs/10-TOOLS.md
```

---

# Database Change Workflow

For database changes:

Follow:

```
Create Model

↓

Create Migration

↓

Update Repository

↓

Update Schema

↓

Update Service

↓

Add Tests
```

---

# Environment Setup

Required:

```
Python 3.12+

Node.js 20+

Git

Docker
```

---

# Local Development Flow

Start backend:

```
cd backend

run FastAPI server
```

---

Start frontend:

```
cd frontend

npm run dev
```

---

Run tests:

Backend:

```
pytest
```

Frontend:

```
npm test
```

---

# AI Assistant Workflow

When using OpenCode AI:

Use this sequence:

```
Read AGENTS.md

↓

Read related docs

↓

Explain approach

↓

List files to change

↓

Implement

↓

Run tests

↓

Review
```

---

# AI Assistant Restrictions

The AI should NOT:

- Rewrite large sections unnecessarily
- Change architecture without approval
- Create duplicate implementations
- Add unnecessary dependencies
- Skip tests
- Modify unrelated files

---

# Production Readiness Checklist

Before considering the project production-ready:

## Code

☐ Clean architecture

☐ Type safety

☐ Error handling

☐ Logging


## AI

☐ Agents tested

☐ Graph tested

☐ Tools tested


## Security

☐ Secrets protected

☐ Authentication implemented


## Deployment

☐ Docker

☐ CI/CD

☐ Monitoring


---

# Final Rule

Every change should make the system:

- More reliable
- Easier to understand
- Easier to extend
- Easier to maintain

Build the system like a professional engineering team, not a quick prototype.
