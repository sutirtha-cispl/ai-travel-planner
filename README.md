# AI Travel Planner

An Agentic AI-powered travel planning assistant built using LangChain, LangGraph, FastAPI, and React.

The system helps users plan trips by:

- Understanding travel requirements.
- Researching travel options.
- Generating personalized itineraries.
- Optimizing budgets.
- Remembering user preferences.

---

# Project Vision

The goal is to evolve from:

```
AI Chat Assistant
```

into:

```
Autonomous Multi-Agent Travel Planning Platform
```

The system uses specialized AI agents that collaborate to complete complex travel planning tasks.

---

# Key Features

## Phase 1 - MVP

Current focus:

- AI travel conversation
- Requirement extraction
- Trip planning workflow
- AI-generated itinerary
- Basic trip storage
- Web interface


---

## Phase 2 - Intelligent Assistant

Planned:

- User accounts
- Travel memory
- Personal preferences
- Real travel APIs
- Better recommendations


---

## Phase 3 - Production Platform

Future:

- Multi-agent supervisor architecture
- Booking workflows
- RAG travel knowledge system
- Human approval workflows
- Production scalability

---

# Architecture Overview

```
                    User

                     |

                     v

              React Frontend

                     |

                     v

              FastAPI Backend

                     |

                     v

              LangGraph Workflow

                     |

        --------------------------------

        |              |               |

        v              v               v


 Requirement     Travel Agents     Tools


        |              |               |

        --------------------------------


                     |

                     v


              Database / APIs
```

---

# Technology Stack

## Backend

| Technology | Purpose |
|-|-|
| Python | Programming language |
| FastAPI | API framework |
| LangChain | LLM framework |
| LangGraph | Agent orchestration |
| SQLAlchemy | ORM |
| Pydantic | Validation |
| Pytest | Testing |

---

## Frontend

| Technology | Purpose |
|-|-|
| React | UI framework |
| TypeScript | Type safety |
| Vite | Build tooling |

---

## Database

Development:

```
SQLite
```

Production:

```
PostgreSQL
```

---

## AI Components

| Component | Purpose |
|-|-|
| LangGraph | Workflow orchestration |
| LangChain | Agent framework |
| LLM Provider | Reasoning engine |
| Vector Database | Memory and RAG |

---

# Repository Structure

```
ai-travel-planner/

├── AGENTS.md
├── README.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Makefile
├── LICENSE
│
├── docs/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── core/
│   │   ├── config/
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── agents/        (reserved)
│   │   ├── graph/         (reserved)
│   │   ├── tools/         (reserved)
│   │   ├── prompts/       (reserved)
│   │   ├── middleware/
│   │   └── utils/
│   ├── tests/
│   ├── migrations/
│   ├── alembic.ini
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── features/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── store/         (reserved)
│   │   ├── types/
│   │   ├── utils/         (reserved)
│   │   └── assets/
│   ├── nginx.conf
│   └── Dockerfile
│
├── tests/        (reserved for E2E)
├── scripts/      (automation helpers)
└── .github/      (CI workflows)
```

---

# Documentation

Detailed project rules are available here:

```
docs/
```

Important documents:

## Architecture

```
docs/02-ARCHITECTURE.md
```

Defines:

- System design
- Component communication


---

## Agent Design

```
docs/09-AGENTS_DESIGN.md
```

Defines:

- AI agents
- Responsibilities
- Collaboration


---

## LangGraph Workflow

```
docs/08-GRAPH_DESIGN.md
```

Defines:

- State
- Nodes
- Routing


---

## Development Rules

```
AGENTS.md
```

Defines:

- AI coding rules
- Engineering standards

---

# Local Development Setup

## Prerequisites

Install:

```
Python 3.12+

Node.js 20.19+ (required by Vite 8)

Git

Docker + Docker Compose (optional, for the PostgreSQL database and full stack)
```

---

# Backend Setup

Navigate:

```bash
cd backend
```

Create environment:

```bash
python -m venv .venv
```

Activate:

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run server:

```bash
uvicorn app.main:app --reload
```

Backend runs:

```
http://localhost:8000
```

---

# Frontend Setup

Navigate:

```bash
cd frontend
```

Install packages:

```bash
npm install
```

Start development server:

```bash
npm run dev
```

Frontend runs:

```
http://localhost:5173
```

---

# Environment Variables

Copy:

```
.env.example
```

to:

```
.env
```

at the repository root and fill in your values.

Example:

```env
APP_ENV=development
DATABASE_URL=postgresql+psycopg://travel:travel@localhost:5432/travel_db
LLM_PROVIDER=openai
MODEL_NAME=gpt-4.1-mini
OPENAI_API_KEY=
CORS_ORIGINS=http://localhost:5173
```

Never commit:

```
.env
```

Frontend configuration is read from `frontend/.env` (`VITE_API_URL`).

---

# Quick Start with Docker Compose

The full stack (PostgreSQL + backend + frontend) runs with:

```bash
docker compose up --build
```

Services:

| Service | URL |
|-|-|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |

The backend applies Alembic migrations automatically on startup and the
frontend nginx container proxies `/api/*` to the backend.

To run only the database:

```bash
docker compose up -d db
```

---

# PostgreSQL Setup (local development)

Development uses SQLite by default and PostgreSQL in Docker.

To use PostgreSQL outside Docker, set in `.env`:

```env
DATABASE_URL=postgresql+psycopg://travel:travel@localhost:5432/travel_db
```

Then create the database schema:

```bash
cd backend
.venv/Scripts/alembic upgrade head    # Windows
.venv/bin/alembic upgrade head        # Linux/Mac
```

The PostgreSQL connection settings (`POSTGRES_USER`, `POSTGRES_PASSWORD`,
`POSTGRES_DB`, `POSTGRES_PORT`) are defined in `.env.example` and used by
`docker-compose.yml`.

---

# Database Migrations

Migrations live in:

```
backend/migrations/
```

Create a migration after model changes:

```bash
cd backend
.venv/Scripts/alembic revision --autogenerate -m "description"
```

Apply migrations:

```bash
.venv/Scripts/alembic upgrade head
```

---

# Running Tests

Backend:

```bash
pytest
```

Frontend:

```bash
npm test
```

---

# Development Workflow

Follow:

```
Read Documentation

↓

Create Plan

↓

Implement Feature

↓

Write Tests

↓

Review Changes

↓

Update Docs
```

---

# Git Workflow

Branch naming:

```
feature/<name>

fix/<name>

docs/<name>
```

Examples:

```
feature/add-flight-agent

fix/chat-api-error
```

---

# Commit Convention

Use:

```
type(scope): message
```

Examples:

```
feat(agent): add planner agent

fix(api): validate trip request

docs: update architecture
```

---

# AI Development Workflow

When using Opencode AI:

First read:

```
AGENTS.md
```

Then relevant documentation:

Example:

Adding an agent:

```
docs/08-GRAPH_DESIGN.md

docs/09-AGENTS_DESIGN.md
```

Adding a tool:

```
docs/10-TOOLS.md
```

---

# Current Development Status

## Phase

```
Phase 1 - MVP Agentic Travel Planner
```

---

## Completed

- [x] Project architecture
- [x] Documentation
- [x] Backend foundation (FastAPI, config, database, migrations, API routes)
- [x] Frontend foundation (React, TypeScript, Vite, Tailwind, routing)
- [x] Docker + PostgreSQL setup
- [ ] LangGraph workflow
- [ ] Basic agents

---

# Roadmap

## Sprint 1

Foundation:

- Setup backend
- Setup frontend
- Configure database
- Configure LLM integration


## Sprint 2

Agent workflow:

- Requirement Agent
- Planner Agent
- Itinerary Agent


## Sprint 3

Tools:

- Flight mock tool
- Hotel mock tool
- Weather mock tool


## Sprint 4

Product:

- UI improvements
- Testing
- Deployment preparation

---

# Contributing

Before contributing:

1. Read:

```
AGENTS.md
```

2. Follow:

```
docs/CODING_STANDARDS.md
```

3. Add tests.

4. Update documentation.

---

# License

Add project license information here.

---

# Project Goal

Build a reliable Agentic AI travel assistant that combines:

```
Large Language Models

+

Agent Workflows

+

External Tools

+

Memory

+

Human Interaction
```

to create intelligent travel experiences.
