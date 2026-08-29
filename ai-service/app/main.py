from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.investigation import router as investigation_router
from app.core.handlers import register_exception_handlers
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(
    title="DevPilot AI Service",
    version="0.1.0",
    description="Internal structured AI capability for DevPilot.",
)


register_exception_handlers(app)
app.include_router(health_router)
app.include_router(investigation_router)