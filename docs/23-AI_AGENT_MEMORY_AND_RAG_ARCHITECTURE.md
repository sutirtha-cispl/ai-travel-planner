# AI Travel Planner - Agent Memory and RAG Architecture

Version: 1.0.0

---

# Purpose

This document defines the memory and Retrieval Augmented Generation (RAG) architecture for the AI Travel Planner.

The objective is to enable the AI assistant to:

- Remember user preferences.
- Learn from previous interactions.
- Retrieve travel knowledge.
- Provide personalized recommendations.
- Reduce hallucinations.
- Improve decision quality.

---

# Why Memory and RAG?

A basic LLM application:

```
User Input

↓

Prompt

↓

LLM

↓

Response
```

has no persistent understanding.

An Agentic AI system requires:

```
User Input

↓

Memory Retrieval

↓

Knowledge Retrieval

↓

Agent Reasoning

↓

Tool Execution

↓

Response
```

---

# Memory Architecture Overview

The system uses multiple memory layers.

```
                    User

                     |

                     v

              Conversation Layer

                     |

        ----------------------------

        |                          |

        v                          v


 Short Term Memory          Long Term Memory


        |                          |

        v                          v


 LangGraph State          Vector Database


                     |

                     v


              Agent Context
```

---

# Memory Types

The system should implement three memory types.

---

# 1. Short-Term Memory

## Purpose

Maintain context during the current conversation.

---

Example:

User:

```
Plan a Japan trip.
```

Later:

```
Make it cheaper.
```

The AI understands:

```
Japan trip
```

because conversation context exists.

---

# Storage

Recommended:

```
LangGraph State
```

---

# Lifetime

```
Current Session
```

---

# Data Example

```json
{
"current_destination":"Japan",
"budget":2000,
"duration":7
}
```

---

# 2. Long-Term User Memory

## Purpose

Remember information across sessions.

---

Examples:

User prefers:

```
Budget hotels

Cultural activities

Short flights

Vegetarian food
```

---

# Storage

Recommended:

```
Vector Database

+

User Profile Database
```

---

# Lifetime

```
Months / Years
```

---

# 3. Knowledge Memory

## Purpose

Store general travel knowledge.

---

Examples:

```
Visa rules

Destination guides

Travel policies

Local information
```

---

# Storage

```
Vector Database
```

---

# Complete Memory Flow

```
User Request

        |

        v

Memory Retrieval

        |

        v

Relevant Context

        |

        v

Agent Prompt

        |

        v

LLM Reasoning

        |

        v

Response
```

---

# Vector Database Architecture

Recommended options:

```
PostgreSQL + pgvector

ChromaDB

Pinecone

Weaviate
```

---

# Recommended Initial Choice

For MVP:

```
PostgreSQL + pgvector
```

Reason:

- Existing database.
- Lower infrastructure complexity.
- Easier operations.

---

# Vector Storage Model

Example:

```
memory_vectors

----------------------

id

user_id

content

embedding

metadata

created_at
```

---

# Metadata Example

```json
{
"type":"user_preference",

"category":"food",

"source":"conversation"
}
```

---

# Embedding Pipeline

Architecture:

```
Text

↓

Text Splitter

↓

Embedding Model

↓

Vector

↓

Database
```

---

# Embedding Model

Options:

```
OpenAI Embeddings

Sentence Transformers

Open Source Models
```

---

# Document Ingestion Pipeline

Used for travel knowledge.

```
Documents

↓

Loader

↓

Cleaner

↓

Splitter

↓

Embedding Generator

↓

Vector Database
```

---

# Document Sources

Examples:

```
Destination Guides

Travel Rules

Visa Information

Hotel Policies

Local Recommendations
```

---

# Text Splitting Strategy

Avoid storing huge documents.

---

Recommended:

Chunk size:

```
500-1000 tokens
```

Overlap:

```
100-200 tokens
```

---

Example:

Original:

```
Tokyo Travel Guide
500 pages
```

Converted:

```
Chunk 1

Chunk 2

Chunk 3
```

---

# Retrieval Pipeline

When an agent needs information:

```
Agent

↓

Retriever

↓

Similarity Search

↓

Relevant Documents

↓

Prompt Context

↓

LLM
```

---

# Retrieval Configuration

Important parameters:

## Top K

Number of documents retrieved.

Example:

```
Top 5
```

---

## Similarity Threshold

Avoid irrelevant information.

Example:

```
0.75
```

---

# Agent Memory Integration

Every intelligent agent can access memory.

---

# Example

Planner Agent:

Before:

```
Create Japan itinerary.
```

---

After:

```
User likes:

- Food experiences
- Museums
- Budget travel

Create Japan itinerary.
```

---

# Memory Retrieval Rules

Agents should retrieve:

Only relevant memory.

---

Avoid:

Sending all user history.

---

Reason:

- Higher token usage.
- Confusing context.
- Privacy concerns.

---

# Memory Service Architecture

Create:

```
backend/app/memory/

├── memory_service.py

├── vector_store.py

├── embeddings.py

└── retriever.py
```

---

# Memory Service Responsibilities

The memory service handles:

- Store memories.
- Retrieve memories.
- Update memories.
- Delete memories.

---

# Memory Extraction Agent

Purpose:

Convert conversations into useful memories.

---

Flow:

```
Conversation

↓

Memory Extractor Agent

↓

Important Facts

↓

Store Memory
```

---

# Example

Conversation:

```
I prefer vegetarian restaurants.
```

Extract:

```json
{
"type":"preference",

"value":"vegetarian food"
}
```

---

# Memory Classification

Before storing:

Classify memory.

---

Types:

```
Preference

Behavior

History

Restriction

Interest
```

---

# Memory Storage Rules

Store:

```
Useful future information
```

Do not store:

```
Temporary requests

Sensitive unnecessary data

Random conversation
```

---

# Memory Update Strategy

Memory can change.

Example:

Old:

```
User likes budget hotels.
```

New:

```
User prefers luxury hotels.
```

---

System should:

```
Update

or

Create new preference
```

---

# Memory Confidence Score

Every memory should have:

```
confidence
```

Example:

```json
{
"memory":"likes hiking",

"confidence":0.85
}
```

---

# Memory Expiration

Some information becomes outdated.

Example:

```
Travel destination interest
```

---

Implement:

```
created_at

last_used_at

expiration
```

---

# RAG + Agent Workflow

Complete architecture:

```
User

↓

Supervisor Agent

↓

Memory Retrieval

↓

Knowledge Retrieval

↓

Specialized Agent

↓

Tools

↓

Final Response
```

---

# Prompt Context Structure

Final prompt:

```
System Instructions

+

User Request

+

User Memory

+

Retrieved Knowledge

+

Tool Results
```

---

# RAG Evaluation

Measure:

## Retrieval Accuracy

Did we retrieve useful documents?

---

## Context Quality

Was retrieved information relevant?

---

## Answer Improvement

Did RAG improve response?

---

# Memory Testing

Required tests:

---

## Store Memory Test

Input:

```
User likes museums
```

Expected:

Memory created.

---

## Retrieval Test

Query:

```
Suggest activities
```

Expected:

Museum preference retrieved.

---

## Privacy Test

Verify:

Sensitive information is not stored.

---

# Performance Optimization

Implement:

## Caching

Cache:

```
Frequently used travel knowledge
```

---

## Async Retrieval

Use:

```
Async database queries
```

---

## Retrieval Limits

Avoid:

```
Huge context injection
```

---

# Security Considerations

Protect:

- User memories.
- Personal preferences.
- Travel history.

---

Rules:

- User can delete memories.
- Users cannot access other users' memories.
- Sensitive data requires additional protection.

---

# Implementation Roadmap

## Phase 1

Basic memory:

```
Conversation State
```

---

## Phase 2

User preferences:

```
Database Storage
```

---

## Phase 3

Vector memory:

```
Embeddings

+

Retrieval
```

---

## Phase 4

Advanced personalization:

```
Adaptive AI Assistant
```

---

# Final Architecture Goal

The AI Travel Planner becomes:

```
A chatbot

        +

Memory System

        +

Knowledge System

        +

Agent Reasoning

        +

Personalized Travel Assistant
```

The goal is not only answering questions.

The goal is understanding users over time.
