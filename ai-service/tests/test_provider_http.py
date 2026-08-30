import httpx
import pytest
from httpx import ConnectError

from app.core.exceptions import ProviderResponseError, ProviderTimeoutError, ProviderConnectionError
from app.providers.http import get_json


@pytest.mark.asyncio
async def test_get_json_returns_json_for_success_response()->None:
    def handler(request:httpx.Request)->httpx.Response:
        return httpx.Response(200, json={"status": "ok"})

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        result=await get_json(client,"https://test.test")

    assert result == {"status": "ok"}

@pytest.mark.asyncio
async def test_get_json_returns_error_for_failure_response()->None:
    def handler(request:httpx.Request)->httpx.Response:
        return httpx.Response(500,json={"error": "provider failed"},request=request)

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(ProviderResponseError) as result:
            await get_json(client,"https://test.test")

    assert result.value.status_code == 500

@pytest.mark.asyncio
async def test_get_json_raises_timeout_error_for_timeout()->None:
    def handler(request:httpx.Request)->httpx.Response:
        raise httpx.ReadTimeout(
            "timeout",
            request=request,
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(ProviderTimeoutError) as result:
            await get_json(client,"https://test.test")

    assert str(result.value)=="Provider request timed out"

@pytest.mark.asyncio
async def test_get_json_raises_connection_error_for_request_failure()->None:
    def handler(request:httpx.Request)-> httpx.Response:
        raise httpx.ConnectError(
            "connection failed",
            request=request,
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(ProviderConnectionError) as result:
            await get_json(client,"https://test.test")

    assert str(result.value) == "Provider request failed"