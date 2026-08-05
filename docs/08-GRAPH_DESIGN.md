# AI Travel Planner LangGraph Design

Version: 1.0.0

---

# Purpose

This document defines the LangGraph architecture for the AI Travel Planner.

LangGraph is responsible for:

- Managing AI workflow execution
- Maintaining shared state
- Routing decisions
- Coordinating agents
- Handling tool execution
- Managing human interaction
- Supporting future multi-agent architecture

---

# Why LangGraph

A normal chatbot flow:

```
User

↓

LLM

↓

Response
```

is insufficient for a travel planner.

A travel planner requires:

- Multiple reasoning steps
- Data collection
- Validation
- Tool usage
- Planning
- Revisions
- Memory

Therefore the system uses:

```
LangGraph

+

LangChain

+

Specialized Agents
```

---

# High-Level Graph Architecture

```
                    START

                      |

                      v

            Requirement Collector

                      |

                      v

             Requirement Validator

                      |

        ----------------------------

        |                          |

        v                          v


 Missing Information          Complete


        |                          |

        v                          v


 Ask User                 Planning Agent


                                   |

                                   v


                          Tool Decision Node


                                   |

             --------------------------------

             |              |               |

             v              v               v


        Flight Agent   Hotel Agent   Activity Agent


             |

             v


        Budget Agent


             |

             v


      Itinerary Generator


             |

             v


        Review Node


             |

             v


             END
```

---

# Graph Design Principles

Every graph component must:

- Have one responsibility
- Accept structured state
- Return structured updates
- Be independently testable

---

# Graph Location

Implementation:

```
backend/app/graph/
```

Structure:

```
graph/

├── state.py

├── nodes.py

├── edges.py

├── workflow.py

├── router.py

└── checkpoint.py
```

---

# Graph State Design

The graph communicates through shared state.

State should contain all information required by agents.

---

# TravelState

Example:

```python
class TravelState(TypedDict):

    conversation_id: str

    user_id: str

    messages: list

    destination: str | None

    departure_city: str | None

    start_date: str | None

    end_date: str | None

    travelers: int | None

    budget: float | None

    preferences: dict

    flight_options: list

    hotel_options: list

    activities: list

    itinerary: dict

    final_response: str
```

---

# State Rules

State should be:

- Explicit
- Serializable
- Validated
- Minimal

Avoid:

- Storing unnecessary data
- Storing secrets
- Storing large files

---

# Graph Nodes

---

# 1. Requirement Collector Node

Purpose:

Extract travel requirements from user messages.

Input:

```
User message
```

Output:

```
Updated TravelState
```

Responsibilities:

- Understand intent
- Extract information
- Identify missing fields

---

# 2. Requirement Validator Node

Purpose:

Check whether enough information exists.

Example:

Required:

```
Destination

Travel dates

Budget

Travelers
```

Output:

```
complete = true/false
```

---

# 3. Missing Information Router

Purpose:

Decide next action.

Logic:

```
IF information missing

↓

Ask user


ELSE

↓

Continue planning
```

---

# 4. User Interaction Node

Purpose:

Pause workflow and request information.

Example:

```
What is your budget?
```

---

# 5. Planner Node

Purpose:

Create travel strategy.

Responsibilities:

- Analyze requirements
- Decide required agents
- Create planning approach

---

# 6. Tool Decision Node

Purpose:

Determine required tools.

Example:

Need:

Flight information?

↓

Flight Tool

Need:

Weather?

↓

Weather Tool

---

# 7. Flight Agent Node

Responsibilities:

- Search flights
- Compare options
- Return recommendations

Input:

```
destination

dates

budget
```

Output:

```
flight_options
```

---

# 8. Hotel Agent Node

Responsibilities:

- Search accommodation
- Compare hotels

Output:

```
hotel_options
```

---

# 9. Activity Agent Node

Responsibilities:

Generate:

- Attractions
- Experiences
- Restaurants

Output:

```
activities
```

---

# 10. Budget Agent Node

Responsibilities:

Calculate:

- Estimated cost
- Budget risks
- Alternatives

Output:

```
budget_summary
```

---

# 11. Itinerary Generator Node

Purpose:

Create final day-by-day plan.

Input:

```
All collected information
```

Output:

```
itinerary
```

---

# 12. Review Node

Purpose:

Final quality check.

Checks:

- Missing information
- Budget mismatch
- Logical schedule

---

# Graph Routing

Routing happens using conditional edges.

Example:

```
Validator

      |

      |

   Complete?

      |

  YES ------> Planner

  NO -------> User Question
```

---

# Agent Routing Logic

Example:

```
Planner Agent

        |

        |

Need flight?

        |

       YES

        |

Flight Agent
```

---

# Error Handling Flow

Errors should not crash the graph.

Example:

```
Tool Failure

↓

Error Handler Node

↓

Retry

↓

Alternative Source

↓

Continue
```

---

# Retry Strategy

Recommended:

Maximum retries:

```
3
```

Example:

```
Flight API failed

↓

Retry

↓

Fallback response
```

---

# Human-in-the-loop Design

Future capability.

Example:

Expensive operation:

```
Book flight
```

Flow:

```
Agent

↓

Approval Node

↓

User Confirmation

↓

Continue
```

---

# Memory Integration

Future:

Graph loads:

```
User Preferences

+

Previous Trips

+

Conversation History
```

before execution.

Flow:

```
START

↓

Load Memory

↓

Requirement Collector

```

---

# Graph Persistence

Future:

Use LangGraph checkpoints.

Store:

```
conversation_id

graph_state

timestamp
```

Benefits:

- Resume conversations
- Debug workflows
- Recover failures

---

# Multi-Agent Graph Evolution

Current:

Single planner workflow.

Future:

Supervisor architecture.

```
              Supervisor Agent

                     |

     ---------------------------------

     |              |              |

 Flight Agent  Hotel Agent  Budget Agent


                     |

                     |

              Final Planner
```

---

# Agent Communication Rules

Agents should communicate through:

```
Shared State
```

Not:

```
Direct Agent-to-Agent calls
```

---

# Testing Strategy

Every graph component requires tests.

---

# Node Tests

Example:

```
Requirement node extracts destination
```

---

# Router Tests

Example:

```
Missing budget routes to question node
```

---

# Workflow Tests

Example:

```
Complete trip request generates itinerary
```

---

# Debugging Graph Execution

When debugging:

Inspect:

```
Current Node

↓

State Before

↓

State After

↓

Tool Calls

↓

Final Output
```

---

# Graph Observability

Future integration:

- LangSmith
- OpenTelemetry
- Custom logging

Track:

- Execution time
- Token usage
- Agent decisions
- Tool failures

---

# Final LangGraph Architecture

```
User

↓

FastAPI

↓

LangGraph Workflow

↓

State Management

↓

Specialized Agents

↓

LangChain Tools

↓

External Services

↓

Final Response
```

---

# Design Goal

The graph should become the central intelligence layer of the application.

All AI reasoning, routing, and orchestration should happen through LangGraph.

The application should be able to evolve from:

```
Single AI Assistant
```

into:

```
Autonomous Multi-Agent Travel Planning System
```
