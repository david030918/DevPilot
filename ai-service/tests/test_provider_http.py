import httpx
import pytest

from app.core.exceptions import ProviderResponseError
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