# AI Travel Planner API Specification

Version: 1.0.0

---

# Purpose

This document defines the API contract for the AI Travel Planner application.

The API layer provides communication between:

```
Frontend

↓

FastAPI Backend

↓

Application Services

↓

AI System

↓

Database / External Services
```

---

# API Design Principles

The API follows:

- REST architecture
- JSON communication
- Predictable resource naming
- Versioned endpoints
- Explicit request/response schemas
- Proper HTTP status codes

---

# Base URL

Development:

```
http://localhost:8000/api/v1
```

Production:

```
https://api.example.com/api/v1
```

---

# Authentication

Future implementation:

JWT-based authentication.

Header:

```
Authorization: Bearer <token>
```

---

# Common Headers

Request:

```
Content-Type: application/json
Accept: application/json
```

---

# Common Response Format

Successful response:

```json
{
    "success": true,
    "data": {},
    "message": "Operation completed successfully"
}
```

---

Error response:

```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid request",
        "details": {}
    }
}
```

---

# HTTP Status Codes

## Success

```
200 OK

201 Created

204 No Content
```

---

## Client Errors

```
400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

422 Validation Error
```

---

## Server Errors

```
500 Internal Server Error

503 Service Unavailable
```

---

# Health API

## Check Application Status

```
GET /health
```

---

## Response

```json
{
    "status": "healthy",
    "version": "1.0.0"
}
```

---

# Chat API

The chat API is the primary AI communication endpoint.

---

# Send Chat Message

```
POST /chat
```

---

## Request

```json
{
    "conversation_id": "abc123",
    "message": "Plan a 7 day Japan trip",
    "user_id": "user_001"
}
```

---

## Fields

### conversation_id

Type:

```
string
```

Description:

Unique conversation identifier.

---

### message

Type:

```
string
```

Description:

User input.

---

### user_id

Type:

```
string
```

Description:

Authenticated user identifier.

---

# Response

```json
{
    "success": true,
    "data": {
        "conversation_id": "abc123",
        "message": "I can help plan your Japan trip.",
        "state": {
            "destination": "Japan"
        }
    }
}
```

---

# Streaming Chat Response

Future implementation.

Technology:

Server Sent Events (SSE)

Endpoint:

```
POST /chat/stream
```

---

Response:

```
data: Thinking...

data: Searching flights...

data: Creating itinerary...
```

---

# Conversation APIs

---

# Create Conversation

```
POST /conversations
```

---

Request:

```json
{
    "title": "Japan Trip"
}
```

---

Response:

```json
{
    "conversation_id": "abc123",
    "title": "Japan Trip"
}
```

---

# Get Conversations

```
GET /conversations
```

---

Response:

```json
[
    {
        "id": "abc123",
        "title": "Japan Trip",
        "created_at": "2026-01-01"
    }
]
```

---

# Get Conversation History

```
GET /conversations/{conversation_id}
```

---

Response:

```json
{
    "messages": [
        {
            "role": "user",
            "content": "Plan Japan trip"
        },
        {
            "role": "assistant",
            "content": "Sure"
        }
    ]
}
```

---

# Trip APIs

---

# Create Trip

```
POST /trips
```

---

Request:

```json
{
    "destination": "Japan",
    "start_date": "2026-04-01",
    "end_date": "2026-04-07",
    "budget": 2000,
    "travelers": 2
}
```

---

Response:

```json
{
    "id": "trip_001",
    "status": "planning"
}
```

---

# Get Trip

```
GET /trips/{trip_id}
```

---

Response:

```json
{
    "id": "trip_001",
    "destination": "Japan",
    "status": "completed",
    "itinerary": {}
}
```

---

# Update Trip

```
PUT /trips/{trip_id}
```

---

Request:

```json
{
    "budget": 3000
}
```

---

Response:

```json
{
    "message": "Trip updated"
}
```

---

# Delete Trip

```
DELETE /trips/{trip_id}
```

---

Response:

```
204 No Content
```

---

# Itinerary APIs

---

# Generate Itinerary

```
POST /trips/{trip_id}/itinerary/generate
```

---

Request:

```json
{
    "preferences": [
        "food",
        "culture"
    ]
}
```

---

Response:

```json
{
    "status": "generated",
    "itinerary_id": "itin_001"
}
```

---

# Get Itinerary

```
GET /itineraries/{id}
```

---

Response:

```json
{
    "days": [
        {
            "day":1,
            "activities":[]
        }
    ]
}
```

---

# Modify Itinerary

```
PUT /itineraries/{id}
```

---

Request:

```json
{
    "instruction":
    "Move hiking activity to day 3"
}
```

---

Response:

```json
{
    "status": "updated"
}
```

---

# User APIs

Future milestone.

---

# Register User

```
POST /users/register
```

---

Request:

```json
{
    "email":"user@example.com",
    "password":"password"
}
```

---

# Login

```
POST /users/login
```

---

Response:

```json
{
    "access_token":"jwt-token"
}
```

---

# User Profile

```
GET /users/profile
```

---

Response:

```json
{
    "name":"John",
    "preferences":{}
}
```

---

# Preferences API

---

# Get Preferences

```
GET /preferences
```

---

Response:

```json
{
    "travel_style":"adventure",
    "food":"vegetarian",
    "hotel_rating":4
}
```

---

# Update Preferences

```
PUT /preferences
```

---

Request:

```json
{
    "travel_style":"luxury"
}
```

---

# Tool Execution APIs

Internal only.

Not exposed publicly.

---

# Flight Search

Internal:

```
POST /internal/tools/flights
```

---

# Hotel Search

```
POST /internal/tools/hotels
```

---

# Weather

```
POST /internal/tools/weather
```

---

# Export APIs

---

# Export Trip

```
POST /trips/{id}/export
```

---

Request:

```json
{
    "format":"pdf"
}
```

---

Supported formats:

```
pdf

markdown

json
```

---

Response:

```json
{
    "download_url":"..."
}
```

---

# API Versioning Strategy

Current:

```
/api/v1
```

Future:

```
/api/v2
```

Breaking changes require a new version.

---

# Pagination

For list endpoints:

Example:

```
GET /trips?page=1&limit=20
```

Response:

```json
{
    "items":[],
    "page":1,
    "limit":20,
    "total":100
}
```

---

# Filtering

Example:

```
GET /trips?status=completed
```

---

# API Security Rules

Never expose:

- API keys
- Internal errors
- Database IDs unnecessarily
- Sensitive information

---

# API Development Rules

Every new API must have:

- Request schema
- Response schema
- Validation
- Error handling
- Documentation
- Tests

---

# API Ownership Rules

Routes:

```
api/routes/
```

Services:

```
services/
```

Schemas:

```
schemas/
```

Repositories:

```
repositories/
```

---

# Final API Architecture

```
Frontend

↓

REST API

↓

FastAPI Routes

↓

Services

↓

LangGraph / Database

↓

Response
```

The API should remain stable even when internal AI architecture changes.
