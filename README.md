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

## V1.0 — Skeleton ✅

- [x] Repository structure

- [x] React application shell

- [x] ASP.NET Core API shell

- [x] FastAPI AI service shell

- [x] Docker setup

- [x] Architecture documentation

---

## V1.1 — Backend Foundation

- [x] PostgreSQL

- [x] Database connection

- [x] First entity: `Project`

- [x] Database migrations

- [x] Logging

- [x] Integration tests

---

## V1.2 — Project API

- [x] `GET /projects`

- [x] `POST /projects`

- [ ] `GET /projects/{id}`

- [ ] Request validation

- [ ] Error handling

---

## V1.3 — React Application Foundation

- [ ] React Router

- [ ] TanStack Query

- [ ] API client

- [ ] Projects page

- [ ] Project detail page

---

## V1.4 — GitHub Integration

- [ ] GitHub token configuration

- [ ] GitHub API client

- [ ] Retrieve repository metadata

- [ ] Retrieve GitHub issues

- [ ] Rate-limit handling

- [ ] Error handling

---

## V1.5 — Python AI Contract

- [ ] Pydantic request/response models

- [ ] `POST /ai/investigate-issue`

- [ ] Deterministic fake AI provider

- [ ] `pytest` test suite

---

## V1.6 — Investigation Workflow

Implement the complete investigation flow:

```text
GitHub Issue
     ↓
ASP.NET Core
     ↓
FastAPI
     ↓
Structured Investigation
     ↓
React
```
## V1.7 — Tasks
```text
Investigation Step
↓
Create Task
↓
Todo → In Progress → Done
```
* Create task from investigation step
* Store task
* List tasks
* Update task status
* Support Todo
* Support In Progress
* Support Done

## V1.8 — Real LLM Integration
* Integrate OpenAI or another LLM provider
* Provider configuration
* Timeout handling
* Retry handling
* Structured output
* Response validation
* Error handling
* Secure API-key configuration

## V1.9 — Portfolio Release
* GitHub Actions CI
* Backend tests
* Python tests
* Frontend tests
* Screenshots
* Architecture diagram
* Demo workflow
* README improvements
* Setup instructions
* Known limitations
* V2 roadmap
* Create V1 release/tag

See [docs/architecture.md](docs/architecture.md) for the service boundaries.

