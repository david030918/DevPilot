from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status

from app.core.exceptions import (
    ProviderConnectionError,
    ProviderOutputError,
    ProviderResponseError,
    ProviderTimeoutError,
    UnsupportedProviderError,
)


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


async def provider_timeout_handler(
    request: Request,
    exc: ProviderTimeoutError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        content={
            "error": "provider_timeout",
            "message": str(exc),
        },
    )


async def provider_response_handler(
    request: Request,
    exc: ProviderResponseError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={
            "error": "provider_response_error",
            "message": str(exc),
        },
    )


async def provider_connection_handler(
    request: Request,
    exc: ProviderConnectionError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "provider_connection_error",
            "message": str(exc),
        },
    )


async def provider_output_handler(
    request: Request,
    exc: ProviderOutputError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={
            "error": "provider_output_error",
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

    @app.exception_handler(ProviderTimeoutError)
    async def handle_provider_timeout(
        request: Request,
        exc: ProviderTimeoutError,
    ) -> JSONResponse:
        return await provider_timeout_handler(request, exc)

    @app.exception_handler(ProviderConnectionError)
    async def handle_provider_connection(
        request: Request,
        exc: ProviderConnectionError,
    ) -> JSONResponse:
        return await provider_connection_handler(request, exc)

    @app.exception_handler(ProviderResponseError)
    async def handle_provider_response(
        request: Request,
        exc: ProviderResponseError,
    ) -> JSONResponse:
        return await provider_response_handler(request, exc)

    @app.exception_handler(ProviderOutputError)
    async def handle_provider_output(
        request: Request,
        exc: ProviderOutputError,
    ) -> JSONResponse:
        return await provider_output_handler(request, exc)
