# DevPilot

**Developer Investigation & Change Intelligence Platform**

DevPilot is a public, production-oriented Full Stack + AI Engineering
project that helps developers investigate unfamiliar GitHub issues,
connect issues to repository evidence, understand change impact, and
turn investigation results into actionable work.

``` text
V1  GitHub Issue → AI Investigation → Developer Tasks
V2  Repository → Retrieval / RAG → Evidence-grounded Investigation
V3  Pull Request / Diff → Change Impact → Risk + Regression Test Plan
V4  Tool Calling / MCP → Controlled Agent Workflows → Human Approval
```

DevPilot is **not** intended to be a generic chatbot or thin LLM
wrapper. The focus is combining conventional software engineering with
modern AI engineering: service boundaries, persistence, external APIs,
structured AI output, testing, Docker, CI/CD, retrieval, evaluation, and
controlled automation.

> **Current status:** V1.2 Project API is complete. The current
> development focus is the Python-first AI-service phase.

## Why DevPilot?

A common developer problem is receiving an unfamiliar GitHub issue and
not knowing where to start. DevPilot is designed to progressively
answer:

-   What is this issue actually asking for?
-   What are plausible causes?
-   What should I investigate first?
-   Which repository locations are relevant?
-   What could a proposed change affect?
-   What regression tests should be run?
-   Which investigation steps should become developer tasks?

## Architecture

``` text
React + TypeScript
        │
        ▼
ASP.NET Core 10 ───────────────► GitHub API
        │
        ├────────► PostgreSQL
        │
        ▼
Python + FastAPI
        │
        ▼
   LLM Provider
```

**Frontend:** application UI, repository/issue views, investigation
reports and task workflow.

**ASP.NET Core:** stable public API, Projects, GitHub integration,
persistence, validation and orchestration.

**FastAPI AI service:** structured AI contracts, provider abstraction,
prompts, and later retrieval/RAG, evaluation and tools.

**PostgreSQL:** system of record for application data.

## Technology Stack

-   **Frontend:** React, TypeScript, Vite, React Router, TanStack Query,
    React Hook Form, Zod
-   **Backend:** C#, ASP.NET Core 10, Minimal APIs, EF Core, Npgsql,
    PostgreSQL, FluentValidation, OpenAPI
-   **AI Service:** Python, FastAPI, Pydantic, HTTPX, pytest, async I/O,
    LLM SDKs, Structured Output
-   **Testing:** xUnit, WebApplicationFactory, Testcontainers,
    PostgreSQL integration tests
-   **Infrastructure:** Docker, Docker Compose, GitHub Actions (planned
    for V1 release)

## Repository Structure

``` text
DevPilot/
├── frontend/       # React + TypeScript
├── backend/        # ASP.NET Core API
├── ai-service/     # Python + FastAPI AI service
├── tests/          # .NET integration tests
├── docs/           # Architecture and engineering notes
├── .github/
├── compose.yaml
├── .env.example
├── DevPilot.slnx
└── README.md
```

## Current Capabilities

### V1.0 --- Skeleton ✅

-   React application shell
-   ASP.NET Core API shell
-   FastAPI AI-service shell
-   Docker Compose
-   Architecture documentation

### V1.1 --- Backend Foundation ✅

-   PostgreSQL
-   EF Core / Npgsql / AppDbContext
-   Project entity, constraints and migrations
-   Structured logging
-   xUnit / WebApplicationFactory
-   Testcontainers PostgreSQL
-   Integration tests

### V1.2 --- Project API ✅

``` text
POST /api/projects
→ 201 Created
→ 400 Validation Problem
→ 409 Conflict

GET /api/projects
→ 200 OK

GET /api/projects/{id}
→ 200 OK
→ 404 Not Found
```

Also includes FluentValidation, EF Core projection, `AsNoTracking`,
OpenAPI, modular endpoint mapping, repository uniqueness handling, and
PostgreSQL-backed integration tests.

## Current Development Focus --- Python-First AI Service

The next phase intentionally prioritizes Python and AI engineering.

``` text
POST /ai/investigate-issue
        ↓
Pydantic Validation
        ↓
Investigation Service
        ↓
AI Provider Boundary
        ↓
Deterministic Fake Provider
        ↓
Structured InvestigationResponse
```

This phase covers Python typing, async/await, FastAPI, Pydantic, HTTPX,
pytest, fake/real provider boundaries, structured LLM output, timeouts,
retries, and provider-error handling.

Normal CI must remain deterministic and must not depend on paid LLM
calls.

## Quick Start

### Prerequisites

For the Docker workflow: - Docker with Docker Compose - Git

For direct local development: - .NET 10 SDK - Python - Node.js / npm

### Start Everything

``` bash
cp .env.example .env
docker compose up --build
```

Default endpoints:

Service             Address
  ------------------- --------------------------------
Frontend            `http://localhost:5173`
Backend             `http://localhost:8080`
Backend health      `http://localhost:8080/health`
AI service          `http://localhost:8000`
AI service health   `http://localhost:8000/health`
AI service docs     `http://localhost:8000/docs`
PostgreSQL          `localhost:5432`

### Backend Build & Tests

``` bash
dotnet restore DevPilot.slnx
dotnet build DevPilot.slnx
dotnet test DevPilot.slnx
```

Integration tests use temporary PostgreSQL containers through
Testcontainers instead of the normal development database.

### Start PostgreSQL Only

``` bash
docker compose up -d database
```

## Roadmap

### V1 --- AI Issue Investigation

**Goal:** deliver a complete deployable workflow without prematurely
introducing repository-wide RAG or autonomous agents.

``` text
Repository
   ↓
GitHub Issue
   ↓
AI Investigation
   ↓
Structured Report
   ↓
Developer Tasks
```

Remaining work includes: - Python FastAPI/Pydantic AI contract -
deterministic fake provider and pytest - real LLM structured output -
React Router, TanStack Query, React Hook Form and Zod - GitHub
repository/issue integration - ASP.NET Core → FastAPI orchestration -
Investigation persistence and UI - Task workflow - CI/CD, deployment,
screenshots and release documentation

**Target:** late October / early November 2026.

### V2 --- Repository Intelligence / RAG

**Goal:** move from issue-only context to evidence grounded in the
repository.

``` text
Repository
   ↓
Ingestion
   ↓
Parsing / Chunking
   ↓
Embeddings
   ↓
Vector / Hybrid Retrieval
   ↓
Context Builder
   ↓
LLM
   ↓
Grounded Investigation + Sources
```

Planned capabilities: - repository ingestion and filtering - code-aware
chunking and metadata - embeddings and vector storage - semantic/hybrid
retrieval - issue-to-relevant-code retrieval - Repository Q&A -
source/file/line references - incremental indexing - retrieval and
groundedness evaluation - cost/token controls

**Success criterion:** given an issue, DevPilot retrieves a small set of
genuinely relevant repository locations and explains why they matter.

**Target:** late November / early December 2026.

### V3 --- Change Impact Intelligence

**Goal:** understand the likely blast radius of an issue or code change.

``` text
Issue / PR / Diff
       ↓
Changed Files / Symbols
       ↓
Dependencies
       ↓
Affected Components
       ↓
API / DB / Test Impact
       ↓
Explainable Risk
       ↓
Regression Test Plan
```

Planned capabilities: - PR/diff analysis - dependency relationships -
direct/transitive impact analysis - affected APIs/database
objects/tests - explainable risk classification - relevant existing-test
discovery - missing regression-test suggestions - change-impact report -
GitHub PR integration - evaluation against curated change scenarios

**Success criterion:** DevPilot produces an evidence-backed impact
report a developer can verify against the repository.

**Target:** December 2026 / January 2027.

### V4 --- PR Intelligence, Tool Calling & Controlled Agents

**Goal:** connect investigation and impact intelligence to bounded
tool-using workflows while keeping humans in control.

``` text
Issue / Pull Request
        ↓
Investigation Agent
        ↓
Tool Selection
        ↓
Repository / GitHub / Retrieval Tools
        ↓
Evidence Collection
        ↓
Investigation / Impact Plan
        ↓
Human Review & Approval
```

Planned capabilities: - typed tool abstraction - LLM tool/function
calling - repository/GitHub/retrieval tools - MCP where it provides a
concrete benefit - bounded multi-step investigation - step/time/token
budgets and stop conditions - human approval and audit trail - optional
proposed patches - no autonomous merge - agent/tool evaluation -
least-privilege credentials and tool allowlists - prompt-injection and
sensitive-data controls

**Safety principle:** autonomous actions should be narrow, observable,
auditable, reversible where practical, and explicitly approved for
high-impact operations.

**V4.0 = Portfolio Complete.** After V4.0, DevPilot moves to maintenance
mode.

## Testing Strategy

**ASP.NET Core** - xUnit - WebApplicationFactory - Testcontainers -
API + PostgreSQL integration tests - later GitHub/AI adapter contract
tests

**Python** - pytest - Pydantic/schema tests - FastAPI endpoint tests -
deterministic fake providers - real LLM calls excluded from normal CI

**Frontend** - component tests - loading/error/success states - workflow
tests - later E2E coverage where valuable

**AI / Later Versions** - structured-output validation - retrieval
datasets and Recall@K - groundedness checks - change-impact evaluation -
agent/tool-selection evaluation

## Public Repository Safety

Do not commit: - employer/client source code - private database schemas
or migrations - customer data - internal API responses - proprietary
business rules - credentials, tokens, API keys or secrets

Use `.env.example`, public repositories, synthetic fixtures, and
secret-safe logs.

## Design Philosophy

``` text
Repeated CRUD
→ move quickly

Modern framework/library
→ understand the core concept, then use it

Architecture / async / database / security / testing / AI
→ study deeply

Non-essential complexity
→ defer
```

The objective is not to maximize the number of frameworks. The objective
is a coherent, testable and explainable developer product that
progressively demonstrates modern software engineering and AI
engineering.

## Documentation

Architecture and implementation notes live under `docs/`. The detailed
product/learning roadmap is maintained separately from this README.

## License

See `LICENSE`.
