# AI Travel Planner - Database Schema and Migration Plan

Version: 1.0.0

---

# Purpose

This document defines the database architecture, schema design, relationships, and migration strategy for the AI Travel Planner.

The objective is to create a database structure that supports:

- User management.
- Travel planning.
- AI agent workflows.
- Memory persistence.
- RAG knowledge storage.
- Tool execution tracking.
- Analytics.
- Future SaaS scalability.

---

# Database Strategy

The system uses:

```
PostgreSQL
```

as the primary production database.

---

# Development Database

Development:

```
SQLite
```

Production:

```
PostgreSQL + pgvector
```

---

# Why PostgreSQL?

Advantages:

- Strong relational model.
- JSON support.
- Vector extension support.
- Production maturity.
- Excellent ORM compatibility.

---

# Database Architecture

```
                Application Layer


                       |


                       v


                  PostgreSQL


        --------------------------------

        |              |               |

        v              v               v


     Business      AI Memory       System Logs


      Tables        Tables          Tables
```

---

# Database Technology Stack

Recommended:

```
Database:

PostgreSQL 16+


ORM:

SQLAlchemy


Migration:

Alembic


Vector:

pgvector
```

---

# Database Modules

The database is divided into:

```
1. Authentication

2. User Management

3. Travel Planning

4. AI Execution

5. Memory System

6. RAG System

7. Analytics
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


Trips          User Memories


 |

 |

 v


Itineraries


 |

 |

 v


Activities



User

 |

 |

 v


Agent Executions


 |

 |

 v


Tool Executions
```

---

# 1. Users Table

Purpose:

Store application users.

---

Table:

```
users
```

---

Schema:

```sql
CREATE TABLE users (

id UUID PRIMARY KEY,

email VARCHAR(255) UNIQUE NOT NULL,

password_hash TEXT NOT NULL,

name VARCHAR(100),

is_active BOOLEAN DEFAULT TRUE,

created_at TIMESTAMP,

updated_at TIMESTAMP

);
```

---

# Fields

| Field | Purpose |
|-|-|
| id | Unique identifier |
| email | Login email |
| password_hash | Encrypted password |
| name | User display name |
| is_active | Account status |
| created_at | Creation time |

---

# 2. User Profiles Table

Purpose:

Store travel preferences.

---

Table:

```
user_profiles
```

---

Schema:

```sql
CREATE TABLE user_profiles (

id UUID PRIMARY KEY,

user_id UUID REFERENCES users(id),

travel_style VARCHAR(50),

budget_preference VARCHAR(50),

preferred_activities JSONB,

food_preferences JSONB,

created_at TIMESTAMP,

updated_at TIMESTAMP

);
```

---

Example:

```json
{
"travel_style":"budget",

"activities":[
"food",
"culture"
]
}
```

---

# 3. Trips Table

Purpose:

Store user travel requests.

---

Table:

```
trips
```

---

Schema:

```sql
CREATE TABLE trips (

id UUID PRIMARY KEY,

user_id UUID REFERENCES users(id),

title VARCHAR(255),

destination VARCHAR(255),

start_date DATE,

end_date DATE,

budget NUMERIC,

status VARCHAR(50),

created_at TIMESTAMP,

updated_at TIMESTAMP

);
```

---

# Trip Status Values

Allowed:

```
draft

planning

completed

cancelled
```

---

# 4. Trip Requirements Table

Purpose:

Store extracted user requirements.

---

Table:

```
trip_requirements
```

---

Schema:

```sql
CREATE TABLE trip_requirements (

id UUID PRIMARY KEY,

trip_id UUID REFERENCES trips(id),

duration INTEGER,

preferences JSONB,

constraints JSONB,

created_at TIMESTAMP

);
```

---

Example:

```json
{
"preferences":[
"history",
"food"
],

"constraints":[
"avoid night travel"
]
}
```

---

# 5. Itineraries Table

Purpose:

Store generated travel plans.

---

Table:

```
itineraries
```

---

Schema:

```sql
CREATE TABLE itineraries (

id UUID PRIMARY KEY,

trip_id UUID REFERENCES trips(id),

version INTEGER DEFAULT 1,

content JSONB,

approved BOOLEAN DEFAULT FALSE,

created_at TIMESTAMP

);
```

---

# Why JSONB?

Travel plans are dynamic.

Example:

```json
{
"day":1,

"activities":[

{
"name":"Tokyo Tower",

"time":"10:00"

}

]
}
```

---

# 6. Activities Table

Purpose:

Store itinerary activities.

---

Table:

```
activities
```

---

Schema:

```sql
CREATE TABLE activities (

id UUID PRIMARY KEY,

itinerary_id UUID REFERENCES itineraries(id),

day_number INTEGER,

title VARCHAR(255),

location VARCHAR(255),

description TEXT,

estimated_cost NUMERIC

);
```

---

# 7. Agent Executions Table

Purpose:

Track AI agent workflows.

---

Table:

```
agent_executions
```

---

Schema:

```sql
CREATE TABLE agent_executions (

id UUID PRIMARY KEY,

trip_id UUID REFERENCES trips(id),

agent_name VARCHAR(100),

status VARCHAR(50),

input JSONB,

output JSONB,

execution_time FLOAT,

created_at TIMESTAMP

);
```

---

# Example Record

```json
{
"agent":"planner",

"status":"completed",

"time":2.5
}
```

---

# Agent Status

Values:

```
started

processing

completed

failed
```

---

# 8. Tool Executions Table

Purpose:

Track external API usage.

---

Table:

```
tool_executions
```

---

Schema:

```sql
CREATE TABLE tool_executions (

id UUID PRIMARY KEY,

agent_execution_id UUID,

tool_name VARCHAR(100),

request JSONB,

response JSONB,

status VARCHAR(50),

created_at TIMESTAMP

);
```

---

# Example

```json
{
"tool":"flight_search",

"status":"success"
}
```

---

# 9. Conversation History Table

Purpose:

Store chat history.

---

Table:

```
conversations
```

---

Schema:

```sql
CREATE TABLE conversations (

id UUID PRIMARY KEY,

user_id UUID REFERENCES users(id),

trip_id UUID REFERENCES trips(id),

role VARCHAR(20),

message TEXT,

created_at TIMESTAMP

);
```

---

# Roles

Allowed:

```
user

assistant

system

tool
```

---

# 10. User Memory Table

Purpose:

Store long-term AI memory.

---

Table:

```
user_memories
```

---

Schema:

```sql
CREATE TABLE user_memories (

id UUID PRIMARY KEY,

user_id UUID REFERENCES users(id),

memory_type VARCHAR(50),

content TEXT,

confidence FLOAT,

embedding VECTOR,

created_at TIMESTAMP,

updated_at TIMESTAMP

);
```

---

# Memory Types

Examples:

```
preference

interest

restriction

behavior
```

---

# 11. Knowledge Documents Table

Purpose:

Store RAG source documents.

---

Table:

```
knowledge_documents
```

---

Schema:

```sql
CREATE TABLE knowledge_documents (

id UUID PRIMARY KEY,

title VARCHAR(255),

source VARCHAR(255),

content TEXT,

metadata JSONB,

created_at TIMESTAMP

);
```

---

# 12. Document Chunks Table

Purpose:

Store searchable chunks.

---

Table:

```
document_chunks
```

---

Schema:

```sql
CREATE TABLE document_chunks (

id UUID PRIMARY KEY,

document_id UUID REFERENCES knowledge_documents(id),

content TEXT,

embedding VECTOR,

metadata JSONB

);
```

---

# Vector Search

Enable:

```
pgvector extension
```

---

Example:

```sql
CREATE EXTENSION vector;
```

---

# 13. API Request Logs

Purpose:

Monitor application requests.

---

Table:

```
api_logs
```

---

Schema:

```sql
CREATE TABLE api_logs (

id UUID PRIMARY KEY,

user_id UUID,

endpoint VARCHAR(255),

status INTEGER,

response_time FLOAT,

created_at TIMESTAMP

);
```

---

# Database Relationships

Main relationships:

```
User

1

|

|

Many

Trips
```

---

```
Trip

1

|

|

Many

Itineraries
```

---

```
Trip

1

|

|

Many

Agent Executions
```

---

```
User

1

|

|

Many

Memories
```

---

# Index Strategy

Important indexes:

---

Users:

```sql
CREATE INDEX idx_users_email
ON users(email);
```

---

Trips:

```sql
CREATE INDEX idx_trips_user
ON trips(user_id);
```

---

Memories:

```sql
CREATE INDEX idx_memory_user
ON user_memories(user_id);
```

---

# Migration Strategy

Tool:

```
Alembic
```

---

# Migration Flow

```
Schema Change

↓

Create Migration

↓

Review Migration

↓

Apply Migration

↓

Verify Database
```

---

# Migration Commands

Create migration:

```bash
alembic revision \
--autogenerate \
-m "add trips table"
```

---

Apply migration:

```bash
alembic upgrade head
```

---

Rollback:

```bash
alembic downgrade -1
```

---

# Migration Rules

Never:

```
Modify old migrations
```

Always:

```
Create new migration
```

---

# Database Backup Strategy

Production:

Enable:

```
Daily backups

Point-in-time recovery

Backup testing
```

---

# Data Retention Policy

Keep:

```
User accounts

Trips

Important memories
```

Review:

```
Logs

Temporary executions
```

---

# Database Security

Required:

- Encrypted connections.
- Strong passwords.
- Limited database permissions.
- No direct public access.

---

# Performance Optimization

Implement:

## Query Optimization

Use:

```
Indexes

Query analysis
```

---

## Connection Pooling

Use:

```
SQLAlchemy Pool
```

---

## Caching

Use:

```
Redis
```

for frequently accessed data.

---

# Testing Strategy

Database tests should cover:

## Model Tests

Verify:

- Relationships.
- Validation.

---

## Migration Tests

Verify:

- Upgrade works.
- Downgrade works.

---

## Integration Tests

Verify:

```
API

↓

Database

↓

Agent Workflow
```

---

# Initial Migration Order

Recommended sequence:

```
1. Users

2. User Profiles

3. Trips

4. Requirements

5. Itineraries

6. Activities

7. Conversations

8. Agent Logs

9. Tool Logs

10. Memory

11. RAG Documents
```

---

# Future Scaling

Possible improvements:

```
Database partitioning

Read replicas

Dedicated vector database

Analytics warehouse
```

---

# Final Database Goal

The database should support:

```
User Management

+

Travel Planning

+

AI Agent Execution

+

Long-Term Memory

+

Knowledge Retrieval

+

Production Analytics
```

The database is the foundation that allows the AI Travel Planner to evolve from a prototype into a scalable SaaS platform.
