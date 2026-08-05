# Root-level tests

Backend unit/integration/API tests live under `backend/tests/` and are run
with pytest from the `backend/` directory:

```bash
cd backend
pytest
```

This directory is reserved for cross-cutting and end-to-end tests
(frontend <-> backend) added in later sprints.
