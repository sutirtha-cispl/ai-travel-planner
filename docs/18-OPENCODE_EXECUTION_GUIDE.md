# AI Travel Planner - Opencode AI Execution Guide

Version: 1.0.0

---

# Purpose

This document defines the development workflow for using Opencode AI as an AI coding assistant for the AI Travel Planner project.

The objective is to ensure:

- Consistent architecture.
- Controlled implementation.
- High-quality code.
- Proper documentation.
- Incremental development.

Opencode AI must treat this repository documentation as the source of truth.

---

# Core Development Principle

Do not build everything at once.

Follow:

```
Understand

↓

Plan

↓

Implement

↓

Test

↓

Review

↓

Document
```

---

# Project Knowledge Loading Order

Before making any changes, Opencode AI must read:

```
AGENTS.md

README.md
```

Then read relevant documentation.

---

# Documentation Selection Rules

## Backend Changes

Read:

```
docs/02-ARCHITECTURE.md

docs/03-PROJECT_STRUCTURE.md

docs/04-CODING_STANDARDS.md

docs/06-API_SPEC.md

docs/07-DATABASE.md
```

---

## Agent Changes

Read:

```
docs/08-GRAPH_DESIGN.md

docs/09-AGENTS_DESIGN.md

docs/11-PROMPTS.md
```

---

## Tool Integration Changes

Read:

```
docs/10-TOOLS.md
```

---

## Testing Changes

Read:

```
docs/12-TESTING.md
```

---

## Sprint Execution

Read:

```
docs/<CURRENT_SPRINT>.md
```

Example:

```
docs/14-SPRINT_1_FOUNDATION.md
```

---

# Opencode Working Rules

## Rule 1: Never Code Without Understanding

Before writing code:

Explain:

1. What needs to be implemented.
2. Which files will change.
3. Which architecture components are affected.
4. How testing will be performed.

---

# Rule 2: Always Create an Implementation Plan

Before coding provide:

```
Implementation Plan

1. File changes

2. New components

3. Dependencies

4. Testing approach

5. Risks
```

---

# Rule 3: Follow Existing Architecture

Do not create:

```
random folders

duplicate services

unused abstractions

unnecessary frameworks
```

---

Always follow:

```
Existing Project Structure

↓

Existing Patterns

↓

Existing Coding Standards
```

---

# Rule 4: Keep Business Logic Outside Controllers

Bad:

```
API Route

    |
    |
    Business Logic

    |
    |
    Database
```

---

Good:

```
API Route

    |

Service Layer

    |

Repository Layer

    |

Database
```

---

# Rule 5: Agent Development Rules

When creating an AI agent:

Always define:

```
Agent Name

Purpose

Input

Output

Tools

State Changes

Failure Handling
```

---

Example:

```
Planner Agent

Purpose:

Create travel strategy


Input:

Travel requirements


Output:

Planning strategy


Tools:

None


State:

Updates strategy field
```

---

# Rule 6: LangGraph Rules

Every graph change must define:

## State

What information flows between nodes.

---

## Nodes

What each node does.

---

## Edges

How routing happens.

---

## Failure Paths

What happens when execution fails.

---

# Rule 7: Prompt Engineering Rules

Never place prompts inside Python files.

Bad:

```python
prompt="You are a travel planner..."
```

---

Good:

```
prompts/

    agents/

        planner_prompt.py
```

---

Every prompt must define:

```
Role

Objective

Context

Rules

Output Format
```

---

# Rule 8: Tool Development Rules

Every tool must define:

```
Name

Purpose

Input Schema

Output Schema

Error Handling

Authentication Requirements
```

---

Tools must never:

- Contain business logic.
- Modify agent state directly.
- Hide failures.

---

# Rule 9: Database Rules

Before modifying database:

Check:

```
docs/07-DATABASE.md
```

---

Always create:

- Migration.
- Model update.
- Schema update.
- Tests.

---

# Rule 10: API Development Rules

Every API endpoint requires:

```
Request Schema

Response Schema

Validation

Error Handling

Tests
```

---

# Opencode Sprint Execution Process

Follow this workflow for every sprint.

---

# Step 1: Load Sprint Context

Example:

Sprint 1:

Read:

```
docs/14-SPRINT_1_FOUNDATION.md
```

---

# Step 2: Create Task Breakdown

Convert sprint tasks into smaller tasks.

Example:

Sprint task:

```
Create backend foundation
```

Break into:

```
Create FastAPI app

Create folder structure

Configure settings

Create health endpoint

Add tests
```

---

# Step 3: Implement Small Changes

Never modify:

```
20 files at once
```

Prefer:

```
Small commits

Small features

Small reviews
```

---

# Step 4: Run Validation

After every feature:

Run:

```
Tests

Lint

Type checking

Application startup
```

---

# Step 5: Update Documentation

After implementation:

Update:

```
README.md

Relevant docs
```

---

# Git Workflow With Opencode

Each task should create:

```
One logical commit
```

---

Commit format:

```
type(scope): description
```

---

Examples:

```
feat(agent): add requirement agent

feat(api): create chat endpoint

fix(graph): handle missing state

docs: update sprint guide
```

---

# Feature Development Template

Use this format when requesting Opencode implementation.

```
Feature:

[Feature Name]


Reference Documents:

[List docs]


Goal:

[What should be achieved]


Implementation Requirements:

[List requirements]


Files Expected:

[List files]


Testing Requirements:

[List tests]


Constraints:

[List restrictions]
```

---

# Example Opencode Prompt

```
Implement Sprint 1 Task 8.

Read:

docs/14-SPRINT_1_FOUNDATION.md

Related:

docs/06-API_SPEC.md

Requirements:

Create health API endpoint.

Follow existing architecture.

Create tests.

Do not modify unrelated files.

Before coding explain implementation plan.
```

---

# Code Review Checklist

Before accepting AI-generated code:

---

## Architecture

Check:

☐ Correct folder

☐ Correct layer

☐ No duplicated logic


---

## Code Quality

Check:

☐ Readable

☐ Typed

☐ Documented

☐ Tested


---

## AI Components

Check:

☐ Agent responsibility is clear

☐ Prompt separated

☐ State changes documented


---

## Security

Check:

☐ No secrets

☐ Input validation

☐ Safe API handling


---

# Avoid AI Over Engineering

Opencode must avoid adding:

Without requirement:

```
Microservices

Kubernetes

Event buses

Complex abstractions

Multiple databases

Extra frameworks
```

---

Prefer:

```
Simple

Maintainable

Testable

Expandable
```

---

# Debugging Workflow

When an error occurs:

Follow:

```
Understand Error

↓

Identify Root Cause

↓

Check Documentation

↓

Apply Small Fix

↓

Add Test

↓

Document Learning
```

---

# AI Decision Making Rules

When multiple approaches exist:

Prefer:

1. Existing project pattern.

2. Simpler solution.

3. Easier maintenance.

4. Better testing capability.

---

# Sprint Completion Process

Before moving to next sprint:

Verify:

```
All tasks completed

↓

Tests passing

↓

Documentation updated

↓

Code reviewed

↓

Git history clean
```

---

# Final Development Workflow

The complete workflow:

```
Documentation

↓

Sprint Plan

↓

Opencode Planning

↓

Implementation

↓

Testing

↓

Review

↓

Commit

↓

Next Task
```

---

# Final Goal

Use Opencode AI as:

```
AI Development Partner

Not

Autonomous Code Generator
```

The human developer remains responsible for:

- Architecture decisions.
- Quality control.
- Security.
- Product direction.

Opencode AI accelerates implementation while maintaining engineering discipline.
