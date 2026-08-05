# AI Travel Planner - Local Development Setup

Version: 1.0.0

---

# Purpose

This document defines the complete local development setup for the AI Travel Planner project.

The objective is to provide a consistent development environment for:

- Developers.
- AI coding assistants.
- Contributors.
- CI/CD pipelines.

---

# Development Environment Overview

The project consists of:

```
Frontend

React + TypeScript + Vite


Backend

FastAPI + LangChain + LangGraph


Database

SQLite (Development)

PostgreSQL (Production)


AI Layer

LangChain + LangGraph


Infrastructure

Docker + Docker Compose
```

---

# Required Software

Install the following tools.

---

# 1. Git

Required:

```
Git >= 2.40
```

Verify:

```bash
git --version
```

---

# 2. Python

Required:

```
Python 3.11+
```

Verify:

```bash
python --version
```

Recommended:

```
Python 3.12
```

---

# 3. Node.js

Required:

```
Node.js 20+
```

Verify:

```bash
node --version
```

---

# 4. Package Managers

Frontend:

Recommended:

```
npm
```

or:

```
pnpm
```

Verify:

```bash
npm --version
```

---

# 5. Docker

Required for production-like development.

Verify:

```bash
docker --version
```

---

# Repository Setup

Clone repository:

```bash
git clone <repository-url>
```

Navigate:

```bash
cd ai-travel-planner
```

---

# Project Structure

Expected:

```
ai-travel-planner/

├── backend/

├── frontend/

├── docs/

├── tests/

├── docker/

├── .env.example

├── README.md

└── AGENTS.md
```

---

# Backend Setup

Navigate:

```bash
cd backend
```

---

# Create Virtual Environment

Create:

```bash
python -m venv venv
```

---

# Activate Environment

## Windows

```bash
venv\Scripts\activate
```

---

## Linux / Mac

```bash
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Verify Installation

```bash
pip list
```

Expected packages:

```
fastapi

uvicorn

langchain

langgraph

sqlalchemy

pytest
```

---

# Backend Environment Setup

Create:

```
backend/.env
```

Copy:

```
backend/.env.example
```

---

Example:

```env
APP_ENV=development

DATABASE_URL=sqlite:///./travel.db

OPENAI_API_KEY=

MODEL_NAME=gpt-4.1-mini
```

---

# Backend Run

Start development server:

```bash
uvicorn app.main:app --reload
```

Expected:

```
Application startup complete
```

---

Backend URL:

```
http://localhost:8000
```

---

API Documentation:

```
http://localhost:8000/docs
```

---

# Frontend Setup

Navigate:

```bash
cd frontend
```

---

# Install Dependencies

```bash
npm install
```

---

# Environment Setup

Create:

```
frontend/.env
```

Example:

```env
VITE_API_URL=http://localhost:8000
```

---

# Frontend Run

Start:

```bash
npm run dev
```

Expected:

```
Local:

http://localhost:5173
```

---

# Database Setup

Development database:

```
SQLite
```

---

Database file:

```
travel.db
```

---

# Migration Setup

Initialize:

```bash
alembic init migrations
```

---

Create migration:

```bash
alembic revision --autogenerate -m "initial migration"
```

---

Apply migration:

```bash
alembic upgrade head
```

---

# PostgreSQL Setup

Production-like development:

Use:

```
PostgreSQL 16+
```

---

Example:

```env
DATABASE_URL=
postgresql://user:password@localhost:5432/travel_db
```

---

# Docker Development Setup

Docker services:

```
Frontend

Backend

Database

Redis

Vector Database
```

---

# Start Services

From root:

```bash
docker compose up
```

---

# Stop Services

```bash
docker compose down
```

---

# Rebuild Containers

```bash
docker compose up --build
```

---

# Environment Variables

All environments should use:

```
.env
```

---

Required variables:

```env
APP_ENV=

DATABASE_URL=

OPENAI_API_KEY=

MODEL_NAME=

JWT_SECRET=

REDIS_URL=
```

---

# Never Commit

Do not commit:

```
.env

.env.local

API keys

Database passwords
```

---

# Backend Development Commands

## Run Server

```bash
uvicorn app.main:app --reload
```

---

## Run Tests

```bash
pytest
```

---

## Run Specific Test

```bash
pytest tests/test_file.py
```

---

## Format Code

Recommended:

```
black
```

Run:

```bash
black .
```

---

## Lint

Recommended:

```
ruff
```

Run:

```bash
ruff check .
```

---

## Type Checking

Recommended:

```
mypy
```

Run:

```bash
mypy .
```

---

# Frontend Development Commands

## Start Development Server

```bash
npm run dev
```

---

## Build Production

```bash
npm run build
```

---

## Run Tests

```bash
npm test
```

---

## Lint

```bash
npm run lint
```

---

# Debugging Workflow

Follow:

```
Identify Issue

↓

Check Logs

↓

Reproduce Locally

↓

Create Fix

↓

Add Test

↓

Commit
```

---

# Backend Debugging

Check:

```
FastAPI logs

Database logs

Agent execution logs
```

---

# Frontend Debugging

Check:

```
Browser console

Network requests

API responses
```

---

# AI Debugging

For agent issues check:

```
Agent State

Prompt

Tool Calls

LLM Response

Validation Errors
```

---

# Recommended IDE Setup

Recommended:

```
VS Code
```

---

# Recommended Extensions

## Python

```
Python

Pylance

Ruff
```

---

## JavaScript

```
ESLint

Prettier
```

---

## Git

```
GitLens
```

---

## AI Development

```
Opencode AI
```

---

# Development Workflow

Every feature follows:

```
Read Documentation

↓

Create Plan

↓

Implement

↓

Test

↓

Review

↓

Commit
```

---

# Branch Strategy

Use:

```
main

develop

feature/*
```

---

Examples:

```
feature/add-memory-system

feature/create-flight-agent

fix/chat-timeout
```

---

# Commit Convention

Format:

```
type(scope): message
```

Examples:

```
feat(agent): add planner agent

fix(api): handle invalid request

docs: update setup guide
```

---

# Common Issues

---

# Issue: Backend Cannot Start

Check:

```
Virtual environment activated

Dependencies installed

Environment variables available
```

---

# Issue: Database Error

Check:

```
DATABASE_URL

Migration status
```

Run:

```bash
alembic upgrade head
```

---

# Issue: LLM Error

Check:

```
API key

Model name

Provider availability
```

---

# Issue: Frontend Cannot Reach Backend

Check:

```
Backend running

CORS configuration

VITE_API_URL
```

---

# New Developer Checklist

Before coding:

☐ Clone repository

☐ Install dependencies

☐ Configure environment

☐ Run backend

☐ Run frontend

☐ Read AGENTS.md

☐ Read relevant docs

---

# AI Developer Checklist

Before asking Opencode AI to implement:

☐ Provide sprint document

☐ Provide related architecture document

☐ Define expected outcome

☐ Define constraints

☐ Request implementation plan first

---

# Final Goal

Every developer should be able to start working by following:

```
Clone Repository

↓

Install Dependencies

↓

Configure Environment

↓

Run Application

↓

Start Development
```

The development environment should be predictable, repeatable, and production aligned.

