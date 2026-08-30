import httpx

from app.core.config import get_settings


def create_http_client() -> httpx.AsyncClient:
    settings = get_settings()

    return httpx.AsyncClient(
        timeout=httpx.Timeout(settings.request_timeout_seconds),
    )
