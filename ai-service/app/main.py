from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="DevPilot AI Service",
    version="0.1.0",
    description="Internal structured AI capability for DevPilot.",
)


class HealthResponse(BaseModel):
    status: str
    service: str


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="healthy", service="ai-service")

