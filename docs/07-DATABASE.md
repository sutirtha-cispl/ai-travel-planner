# AI Travel Planner Database Design

Version: 1.0.0

---

# Purpose

This document defines the database architecture for the AI Travel Planner.

The database layer is responsible for:

- User management
- Travel history
- Preferences
- Conversations
- Generated itineraries
- Agent execution records
- Tool results
- Application state persistence

---

# Database Strategy

The project will evolve through multiple database stages.

---

# Phase 1

Development Database

Technology:

```
SQLite
```

Purpose:

- Local development
- Testing
- Rapid iteration

---

# Phase 2

Production Database

Technology:

```
PostgreSQL
```

Purpose:

- Multi-user support
- Scalability
- Production workloads

---

# Database Architecture

```
Application

↓

Services

↓

Repositories

↓

ORM Models

↓

Database
```

---

# Database Rules

Agents must never:

- Query database directly
- Execute SQL
- Modify records directly

Allowed flow:

```
Agent

↓

Service

↓

Repository

↓

Database
```

---

# ORM

Technology:

```
SQLAlchemy
```

---

# Migration Tool

Recommended:

```
Alembic
```

---

# Database Folder Structure

```
backend/app/

database/

├── connection.py

├── session.py

├── migrations/


models/

├── user.py

├── trip.py

├── itinerary.py

├── conversation.py


repositories/

├── user_repository.py

├── trip_repository.py

└── conversation_repository.py
```

---

# Entity Relationship Overview

```
User

 |

 |

 +----------------+

 |                |

 v                v


Trips        Preferences


 |

 |

 v


Itinerary


 |

 |

 v


Activities



User

 |

 |

 v


Conversations

 |

 |

 v


Messages
```

---

# Core Entities

---

# 1. User

Purpose:

Stores application users.

Table:

```
users
```

---

Fields:

| Field | Type |
|-|-|
| id | UUID |
| email | String |
| password_hash | String |
| name | String |
| created_at | Timestamp |
| updated_at | Timestamp |


---

Example:

```json
{
"id":"user_001",
"name":"John",
"email":"john@example.com"
}
```

---

# 2. User Preferences

Purpose:

Stores travel preferences.

Table:

```
preferences
```

---

Fields:

| Field | Type |
|-|-|
| id | UUID |
| user_id | UUID |
| travel_style | String |
| food_preference | String |
| hotel_rating | Integer |
| budget_range | String |
| created_at | Timestamp |


---

Example:

```json
{
"travel_style":"adventure",
"food_preference":"vegetarian",
"hotel_rating":4
}
```

---

# 3. Trip

Purpose:

Stores travel plans.

Table:

```
trips
```

---

Fields:

| Field | Type |
|-|-|
| id | UUID |
| user_id | UUID |
| destination | String |
| start_date | Date |
| end_date | Date |
| budget | Decimal |
| travelers | Integer |
| status | String |
| created_at | Timestamp |
| updated_at | Timestamp |


---

Status values:

```
planning

completed

cancelled
```

---

Example:

```json
{
"destination":"Japan",
"budget":2000,
"status":"completed"
}
```

---

# 4. Itinerary

Purpose:

Stores generated travel schedules.

Table:

```
itineraries
```

---

Fields:

| Field | Type |
|-|-|
| id | UUID |
| trip_id | UUID |
| title | String |
| description | Text |
| created_at | Timestamp |


---

# 5. Itinerary Day

Purpose:

Stores daily schedules.

Table:

```
itinerary_days
```

---

Fields:

| Field | Type |
|-|-|
| id | UUID |
| itinerary_id | UUID |
| day_number | Integer |
| date | Date |


---

Example:

```json
{
"day_number":1,
"activities":[]
}
```

---

# 6. Activities

Purpose:

Stores planned activities.

Table:

```
activities
```

---

Fields:

| Field | Type |
|-|-|
| id | UUID |
| day_id | UUID |
| name | String |
| description | Text |
| location | String |
| duration | Integer |
| estimated_cost | Decimal |


---

# 7. Conversations

Purpose:

Stores AI conversations.

Table:

```
conversations
```

---

Fields:

| Field | Type |
|-|-|
| id | UUID |
| user_id | UUID |
| title | String |
| created_at | Timestamp |


---

# 8. Messages

Purpose:

Stores chat messages.

Table:

```
messages
```

---

Fields:

| Field | Type |
|-|-|
| id | UUID |
| conversation_id | UUID |
| role | String |
| content | Text |
| created_at | Timestamp |


---

Role values:

```
user

assistant

system

tool
```

---

# 9. Agent Execution Logs

Purpose:

Tracks AI workflow execution.

Table:

```
agent_runs
```

---

Fields:

| Field | Type |
|-|-|
| id | UUID |
| conversation_id | UUID |
| agent_name | String |
| status | String |
| started_at | Timestamp |
| completed_at | Timestamp |


---

Example:

```
PlannerAgent

completed

5 seconds
```

---

# 10. Tool Execution Logs

Purpose:

Tracks external tool usage.

Table:

```
tool_runs
```

---

Fields:

| Field | Type |
|-|-|
| id | UUID |
| tool_name | String |
| input | JSON |
| output | JSON |
| status | String |
| created_at | Timestamp |


---

# Relationships

---

## User → Trips

One user:

Many trips

```
User 1:N Trips
```

---

## User → Conversations

```
User 1:N Conversations
```

---

## Trip → Itinerary

```
Trip 1:1 Itinerary
```

---

## Itinerary → Days

```
Itinerary 1:N Days
```

---

## Day → Activities

```
Day 1:N Activities
```

---

## Conversation → Messages

```
Conversation 1:N Messages
```

---

# Indexing Strategy

Important indexes:

---

Users

```
email
```

Reason:

Fast login lookup.

---

Trips

```
user_id

destination

status
```

---

Messages

```
conversation_id

created_at
```

---

Activities

```
day_id
```

---

# Data Retention Strategy

Future consideration:

Conversation data:

Keep permanently for users.

Agent logs:

Keep limited retention.

Tool logs:

Configurable retention.

---

# JSON Storage Strategy

Some AI-generated data is flexible.

Example:

```
Trip metadata

Tool responses

Agent state
```

Use:

SQLite:

```
JSON column
```

PostgreSQL:

```
JSONB
```

---

# LangGraph State Persistence

Future:

Store graph checkpoints.

Example:

```
graph_checkpoints
```

Fields:

```
id

conversation_id

state_json

created_at
```

---

# Migration Strategy

Every schema change requires:

1. Create migration

2. Update model

3. Update repository

4. Update tests

5. Apply migration

---

Example:

```
alembic revision --autogenerate

alembic upgrade head
```

---

# Repository Pattern

Example:

```
TripService

↓

TripRepository

↓

Database
```

---

Repository example responsibilities:

Allowed:

```
create_trip()

get_trip()

update_trip()
```

Not allowed:

```
generate_itinerary()
```

Business logic belongs in services.

---

# Database Security

Never:

- Store plain passwords
- Store API keys
- Store sensitive tokens


Always:

- Hash passwords
- Encrypt sensitive values
- Validate inputs

---

# Future Database Improvements

Possible additions:

## Vector Database

For:

- RAG
- Travel knowledge
- User preference embeddings


Options:

- ChromaDB
- Pinecone
- Weaviate
- PostgreSQL pgvector


---

## Redis

For:

- Session caching
- Rate limiting
- Background jobs

---

# Final Database Architecture

```
Frontend

↓

API

↓

Services

↓

Repositories

↓

SQLAlchemy Models

↓

SQLite/PostgreSQL


+

Vector Database

+

Cache Layer
```

The database should support the evolution from a single-user AI assistant into a scalable multi-user Agentic AI platform.
