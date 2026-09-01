from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.investigation import router as investigation_router
from app.core.config import get_settings
from app.core.handlers import register_exception_handlers
from app.core.logging import configure_logging

configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.http_client = httpx.AsyncClient(timeout=settings.request_timeout_seconds)
    yield
    await app.state.http_client.aclose()


app = FastAPI(
    title="DevPilot AI Service",
    version="0.1.0",
    description="Internal structured AI capability for DevPilot.",
    lifespan=lifespan,
)


register_exception_handlers(app)
app.include_router(health_router)
app.include_router(investigation_router)
