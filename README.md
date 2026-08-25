# DevPilot

DevPilot is a developer investigation and change-intelligence platform. The V1 workflow turns a GitHub issue into a structured investigation report and a set of actionable tasks.

This repository currently contains the first project skeleton described in `DevPilot_Project_Plan.docx`:

- `frontend/` — React + TypeScript application shell
- `backend/` — ASP.NET Core public application API
- `ai-service/` — FastAPI internal AI capability
- `docs/` — architecture and implementation notes

## Current scope

The skeleton intentionally uses sample data. It proves the service boundaries and local developer workflow before authentication, PostgreSQL, GitHub integration, or a real LLM provider are added.

## Quick start

### Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

Then open:

- Frontend: http://localhost:5173
- Backend health: http://localhost:8080/health
- AI service health: http://localhost:8000/health
- AI service docs: http://localhost:8000/docs

### Run services directly

```bash
# terminal 1
cd backend && dotnet run

# terminal 2
cd ai-service && python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --reload --port 8000

# terminal 3
cd frontend && npm install && npm run dev
```

## Next milestones

1. V1.1 — add PostgreSQL, migrations, error handling, logging, and API tests.
2. V1.2 — add routing, an API client/query layer, loading/error states, and sign-in UI.
3. V1.3 — add a GitHub adapter and issue retrieval.
4. V1.4 — add versioned investigation schemas and a deterministic mock AI provider.

See [docs/architecture.md](docs/architecture.md) for the service boundaries.

