from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import UnsupportedProviderError


async def unsupported_provider_handler(
    request: Request,
    exc: UnsupportedProviderError,
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "error": "unsupported_provider",
            "message": str(exc),
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UnsupportedProviderError)
    async def handle_unsupported_provider(
        request: Request,
        exc: UnsupportedProviderError,
    ) -> JSONResponse:
        return await unsupported_provider_handler(request, exc)