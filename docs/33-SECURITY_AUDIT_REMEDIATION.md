# Security Audit Remediation

Version: 1.0.0

---

# Purpose

Tracks the outcome of the security audit performed on 2026-08-11 and the
remediation decisions. Findings marked as *production-only* are documented
here and deliberately NOT applied to the local development environment so
that the developer workflow remains unchanged.

---

# Summary

| ID | Severity | Finding | Status |
|-|-|-|-|
| C1 | Critical | No authentication / authorization | Documented (production-only) |
| C2 | Critical | No rate limiting on `/chat` | Documented (production-only) |
| H1 | High | Base image CVEs (unfixed upstream) | Documented (production-only) |
| H2 | High | Weak default DB credentials, exposed DB port | Documented (production-only) |
| H3 | High | Backend container runs as root | Fixed |
| H4 | High | Missing security headers | Fixed |
| M1 | Medium | Vulnerable pip / pytest | Fixed |
| M2 | Medium | CI lacks security gates | Fixed |
| M3 | Medium | Broad CORS credentials | Documented (production-only) |
| M4 | Medium | Loose unpinned dependencies | Fixed |

---

# Applied Fixes (quick wins)

These were applied because they are safe for both development and production:

- `backend/Dockerfile` — non-root `appuser`, pip upgraded during build.
- `frontend/Dockerfile` — nginx runs as non-root `nginx` user.
- `frontend/nginx.conf` — security headers, `server_tokens off`, non-root port 8080.
- `docker-compose.yml` — frontend internal port 80 → 8080 (host port 5173 unchanged).
- `backend/requirements.txt` — exact version pins; pytest 9.1.1, pytest-asyncio 1.4.0.
- `.github/workflows/test.yml` — gitleaks, bandit, pip-audit, npm audit gates.
- `backend/bandit.yaml` — skips B324 (SHA1 used only for mock seeding, not crypto).

---

# Production-Only Findings (documented, not applied)

These require production configuration that must NOT be copied into the local
development environment. Apply them as part of the Sprint 4 productization /
deployment workstream.

## C1 — Authentication and Authorization

**Problem:** No API requires a JWT; trips have no owner (`Trip.user_id` is
nullable and never set), so any caller can create/read any trip.

**Apply at production time:**

- Require `Authorization: Bearer <JWT>` on `/api/v1/*` (except `/health`).
- Add `user_id` to trip creation and scope repository queries by `user_id`.
- Keep `docs/20-SECURITY_AND_PRODUCTION_GUIDELINES.md` §3 as the reference.

## C2 — Rate Limiting and Cost Protection

**Problem:** `POST /api/v1/chat` invokes the LLM graph with no throttling,
allowing abuse and unbounded LLM cost.

**Apply at production time:**

- Add a rate limiter (e.g. slowapi or an nginx `limit_req` zone) on `/chat`.
- Enforce per-user and per-IP quotas; add token budget limits.

## H1 — Base Image Vulnerabilities

**Problem:** Docker Scout reports CVEs in `python:3.12-slim` (Debian trixie)
including perl CVE-2026-13221, CVE-2026-12087 (Critical) and CVE-2026-48959,
CVE-2026-48962 (High). All are marked "not fixed" upstream as of the audit.

**Apply at production time:**

- Rebuild against the newest `python:3.12-slim` tag (or pin a patched digest)
  once upstream fixes exist.
- Add a `docker scout cves` gate to the CI build job before deploy.

## H2 — Database Credentials and Port Exposure

**Problem:** `docker-compose.yml` defaults to `travel`/`travel` and publishes
PostgreSQL port 5432 to the host.

**Apply at production time:**

- Require strong `POSTGRES_PASSWORD` (fail startup if unset).
- Remove the host port publish for `db`; reach PostgreSQL only over the
  internal Docker network / private subnet.

## M3 — CORS

**Problem:** `allow_credentials=True` with `allow_methods=["*"]`; origins come
from `CORS_ORIGINS` (default `http://localhost:5173`).

**Apply at production time:**

- Set `CORS_ORIGINS` to the exact production frontend origin(s).
- Restrict `allow_methods` to the used set and keep credentials only where
  cookies are genuinely required.
- The development default must remain `http://localhost:5173`.

---

# Deferred / Accepted Risk

- **L1** — Empty `HOTEL_API_KEY=` placeholder in docs triggers gitleaks
  (false positive). Remove or annotate `gitleaks:allow`.
- **L2** — Verbose exception logging (`exc_info=True`) in agents/tools.
- **L3** — `/docs` (Swagger) exposed in all environments.
- **L4** — `hashlib.sha1` in mock seeding (bandit B324, informational only).

---

# Re-run Procedure

After any dependency or infrastructure change:

```bash
# backend
cd backend
.venv/Scripts/python -m pytest
.venv/Scripts/python -m ruff check app tests
.venv/Scripts/python -m bandit -c bandit.yaml -r app
.venv/Scripts/python -m pip_audit
# repository root
gitleaks git --all --exit-code
# frontend
cd frontend && npm audit --audit-level=high
# container
docker scout cves ai-travel-planner-backend:latest
```
