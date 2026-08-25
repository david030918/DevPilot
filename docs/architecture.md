# Architecture

## V1 service boundaries

```text
React frontend
      |
      | public HTTP contract
      v
ASP.NET Core API -----> PostgreSQL (planned for V1.1)
      |
      | internal, versioned AI contract
      v
FastAPI AI service -----> LLM provider (planned for V1.4)
```

## Responsibilities

### Frontend

Owns presentation, navigation, asynchronous UI states, and typed consumption of the application API. It never calls the AI service directly.

### Backend

Owns the public application contract, authentication, projects, issues, tasks, persistence, GitHub integration, permissions, and workflow orchestration.

### AI service

Owns prompt/version management, provider adapters, structured-output validation, retries/timeouts, and later repository retrieval. It remains an internal service so AI implementation details can change without destabilising the frontend.

## Initial request flow

The current dashboard calls `GET /api/overview` on the backend. The backend returns deterministic sample data so the frontend shell can be developed independently of GitHub and database work.

