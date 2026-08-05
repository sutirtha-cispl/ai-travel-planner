# ============================================
# AI Travel Planner - Development Commands
# ============================================

.PHONY: help install backend-install frontend-install dev backend frontend test backend-test frontend-test lint migrate db-up db-down

help:
	@echo "AI Travel Planner - available commands:"
	@echo "  make install           Install backend and frontend dependencies"
	@echo "  make backend-install   Install backend dependencies"
	@echo "  make frontend-install  Install frontend dependencies"
	@echo "  make dev               Run backend + frontend dev servers"
	@echo "  make backend           Run backend dev server"
	@echo "  make frontend          Run frontend dev server"
	@echo "  make test              Run all tests"
	@echo "  make backend-test      Run backend tests"
	@echo "  make frontend-test     Run frontend tests"
	@echo "  make lint              Lint backend and frontend"
	@echo "  make migrate           Apply database migrations"
	@echo "  make db-up             Start PostgreSQL via Docker Compose"
	@echo "  make db-down           Stop Docker Compose services"

install: backend-install frontend-install

backend-install:
	python -m venv backend/.venv
	backend/.venv/bin/pip install -r backend/requirements.txt

frontend-install:
	cd frontend && npm install

dev:
	docker compose up --build

backend:
	cd backend && .venv/bin/uvicorn app.main:app --reload

frontend:
	cd frontend && npm run dev

test: backend-test frontend-test

backend-test:
	cd backend && .venv/bin/pytest

frontend-test:
	cd frontend && npm test

lint:
	cd backend && .venv/bin/ruff check app tests
	cd frontend && npm run lint

migrate:
	cd backend && .venv/bin/alembic upgrade head

db-up:
	docker compose up -d db

db-down:
	docker compose down
