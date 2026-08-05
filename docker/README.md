# Docker / PostgreSQL helpers

This directory holds Docker-related assets.

- The root `docker-compose.yml` defines the local development stack
  (PostgreSQL, backend, frontend).
- PostgreSQL configuration is provided via environment variables
  (see `.env.example` at the repository root).

Additional Docker assets (e.g. `Dockerfile.*`, `nginx.conf`) live inside
`backend/` and `frontend/` next to their respective applications.
