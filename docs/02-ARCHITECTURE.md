# AI Travel Planner Architecture

Version: 1.0.0

---

# Purpose

This document defines the high-level architecture of the AI Travel Planner.

The architecture is designed to support:

- Agentic AI workflows
- LangChain integrations
- LangGraph orchestration
- Multiple specialized agents
- External tool integrations
- Persistent user data
- Future SaaS scalability

The architecture should evolve gradually while maintaining clean separation of responsibilities.

---

# Architecture Principles

The system follows these principles:

## Separation of Concerns

Each layer has a clearly defined responsibility.

Examples:

API layer

Handles HTTP communication.

Service layer

Handles business logic.

Agent layer

Handles AI reasoning.

Tool layer

Handles external capabilities.

Repository layer

Handles data persistence.

---

## Modular Design

Each component should be replaceable.

Examples:

The OpenAI model can be replaced.

The database can be replaced.

Mock tools can be replaced with real APIs.

The frontend can be replaced.

---

## AI First Architecture

AI capabilities are isolated from the application logic.

The application should not depend directly on a specific LLM provider.

---

# High-Level Architecture

```
                    User

                     |
                     |
                     v

              React Frontend

                     |

                     |

              FastAPI Backend

                     |

        ----------------------------

        |                          |

        v                          v


 Application Layer          Authentication


        |

        |

        v


       AI Orchestration Layer

       (LangGraph)

        |

        |

        +--------------------+

        |                    |

        v                    v


   Agents                Tools


        |                    |

        |                    |

        v                    v


   LangChain          External APIs


        |

        |

        v


    Data Layer


        |

        |

        v


 Database / Storage
```

---

# System Components

The application consists of the following major components:

---

# 1. Frontend Layer

Technology:

- React
- TypeScript
- TailwindCSS
- shadcn/ui


## Responsibilities

The frontend handles:

- User interaction
- Chat interface
- Trip visualization
- Itinerary display
- User preferences
- Authentication UI


## Frontend should NOT:

- Call LLM APIs directly
- Contain business logic
- Handle AI decisions

All AI communication goes through the backend.

---

# 2. API Layer

Technology:

- FastAPI


Location:

```
backend/api/
```


## Responsibilities

The API layer handles:

- HTTP requests
- Request validation
- Response formatting
- Authentication checks


Examples:

```
POST /api/chat

POST /api/trips

GET /api/trips/{id}

PUT /api/preferences
```


## API Layer should NOT:

- Execute AI logic
- Call LangChain directly
- Query database directly

---

# 3. Application Service Layer

Location:

```
backend/services/
```


## Responsibilities

Contains business logic.

Examples:

- Trip service
- User service
- Preference service
- Export service


Example flow:

```
API

↓

Service

↓

Repository

↓

Database
```

---

# 4. AI Orchestration Layer

Technology:

- LangGraph


Location:

```
backend/graph/
```


## Responsibilities

Controls AI execution flow.


Example:

```
START

↓

Understand User Request

↓

Collect Information

↓

Validate

↓

Plan Trip

↓

Call Tools

↓

Generate Response

↓

END
```


The graph controls:

- State
- Routing
- Agent execution
- Tool usage

---

# 5. Agent Layer

Location:

```
backend/agents/
```


## Responsibilities

Contains specialized AI agents.


Examples:

## Planner Agent

Responsible for:

- Overall trip planning
- Decision making


## Flight Agent

Responsible for:

- Flight recommendations


## Hotel Agent

Responsible for:

- Accommodation


## Budget Agent

Responsible for:

- Cost optimization


## Activity Agent

Responsible for:

- Attractions and experiences


Each agent should have one responsibility.

---

# 6. Tool Layer

Location:

```
backend/tools/
```


## Responsibilities

Provides external capabilities.


Examples:

```
FlightSearchTool

HotelSearchTool

WeatherTool

CurrencyTool

MapTool
```


Tools are controlled by agents.

---

# Tool Architecture

```
Agent

 |

 |

 v

LangChain Tool

 |

 |

 v

Service

 |

 |

 v

External API
```

---

# 7. Data Layer

The data layer manages persistence.


Components:

```
database/

models/

repositories/
```


---

# Database Responsibilities

Stores:

Users

Trips

Itineraries

Preferences

Conversations

Tool results

---

# Repository Layer

Location:

```
backend/repositories/
```


Responsibilities:

- Database queries
- Data access abstraction


Example:

```
TripRepository

UserRepository

PreferenceRepository
```

---

# AI Execution Flow

Example user request:

```
Plan a 7 day Japan trip
```

---

## Step 1

Frontend sends request.


```
React

↓

POST /chat
```

---

## Step 2

FastAPI receives request.


```
API Controller

↓

Chat Service
```

---

## Step 3

Service invokes LangGraph.


```
Chat Service

↓

Travel Graph
```

---

## Step 4

Graph analyzes request.


```
Requirement Agent
```

---

## Step 5

Missing information check.


Example:

```
Need budget?

Need travel dates?
```

---

## Step 6

Agents execute.


```
Planner Agent

↓

Flight Agent

↓

Hotel Agent

↓

Activity Agent
```

---

## Step 7

Tools are called.


```
Agent

↓

Tool

↓

External Service
```

---

## Step 8

Final response generated.


```
Graph

↓

API

↓

Frontend
```

---

# LangGraph Architecture

The graph represents the AI workflow.


Example:

```
              START

                |

                v

        Requirement Agent

                |

                v

        Validation Node

                |

        ----------------

        |              |

        v              v

   Missing Data      Complete


        |              |

        v              v


    User Input     Planner Agent


                       |

                       v


                  Tool Agents


                       |

                       v


              Final Response


                       |

                       v


                      END
```

---

# State Management

The graph maintains shared state.

Example:

```
TravelState

{

destination,

dates,

budget,

preferences,

flight_options,

hotel_options,

itinerary,

final_response

}
```

State should be:

- Explicit
- Typed
- Validated

---

# Prompt Architecture

Prompts are separated from code.

Location:

```
backend/prompts/
```


Example:

```
planner_prompt.py

hotel_prompt.py

budget_prompt.py
```


Benefits:

- Easier testing
- Easier updates
- Version control

---

# Configuration Architecture

Location:

```
backend/config/
```


Handles:

- Environment variables
- API keys
- Application settings


Example:

```
OPENAI_API_KEY

DATABASE_URL

ENVIRONMENT
```

---

# Error Handling Architecture

Errors should flow through layers.


Example:

```
External API Failure

↓

Tool Exception

↓

Agent Error Handler

↓

Graph Recovery

↓

User Friendly Message
```

---

# Logging Architecture

Track:

- API requests
- Agent execution
- Tool execution
- Graph transitions
- Errors
- Performance


Never log:

- API keys
- Passwords
- Private user information

---

# Future Scalability Design

The architecture supports:

## Multiple LLM Providers

Example:

```
OpenAI

↓

LangChain Interface

↓

Application
```

Can later support:

- Anthropic
- Gemini
- Local models

---

## Multiple Databases

Current:

SQLite

Future:

PostgreSQL

---

## Multiple Frontends

Possible clients:

- Web
- Mobile
- Voice assistant

---

## Distributed Agents

Future:

```text
Planner Service

Flight Service

Hotel Service

Budget Service
```

---

# Deployment Architecture

Future production deployment:

```text
                CDN

                 |

                 |

          React Application

                 |

                 |

          API Gateway

                 |

        -----------------

        |               |

        v               v


    FastAPI        Background Workers


        |

        |

     LangGraph


        |

        |

    PostgreSQL


        |

        |

 External Services
```

---

# Architectural Rules

Always:

- Keep AI logic separate.
- Keep business logic separate.
- Use services.
- Use repositories.
- Use typed models.
- Keep agents focused.
- Keep tools independent.

Never:

- Put AI logic inside API routes.
- Put database code inside agents.
- Hardcode prompts.
- Mix frontend and backend logic.
- Create a single giant agent.

---

# Final Architecture Goal

The final system should look like:

```
Frontend

↓

API Layer

↓

Application Services

↓

LangGraph Orchestrator

↓

Specialized Agents

↓

LangChain Tools

↓

External APIs


+

Database

+

Memory System
```

The architecture should allow the project to grow from a learning project into a production-grade Agentic AI SaaS platform.
