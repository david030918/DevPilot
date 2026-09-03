import asyncio
import json
from http import HTTPStatus

import httpx
import pytest

from app.core.exceptions import (
    ProviderConnectionError,
    ProviderOutputError,
    ProviderResponseError,
    ProviderTimeoutError,
)
from app.models.investigation import (
    InvestigationRequest,
    IssueContext,
    RepositoryContext,
)
from app.providers.ollama import OllamaInvestigationProvider


@pytest.fixture
def investigation_request() -> InvestigationRequest:
    return InvestigationRequest(
        repository=RepositoryContext(
            owner="test",
            name="test",
        ),
        issue=IssueContext(
            number=1,
            title="test",
        ),
    )


@pytest.mark.asyncio
async def test_ollama_get_json_returns_json_for_success_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        json_response = {
            "summary": "Test summary",
            "possible_causes": [
                {
                    "title": "Configuration issue",
                    "explanation": "Configuration may be incorrect.",
                    "confidence": 0.8,
                }
            ],
            "investigation_steps": [
                {
                    "order": 1,
                    "description": "Check configuration.",
                }
            ],
            "assumptions": ["The application is running."],
            "suggested_tests": [
                {
                    "name": "Configuration test",
                    "description": "Verify configuration.",
                }
            ],
        }
        return httpx.Response(
            status_code=200,
            json={
                "message": {"role": "assistant", "content": json.dumps(json_response)}
            },
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        provider = OllamaInvestigationProvider(
            client=client,
            base_url="http://test",
            model_name="ollama",
        )
        request = InvestigationRequest(
            repository={
                "owner": "test",
                "name": "test",
            },
            issue={
                "number": 1,
                "title": "test",
            },
        )
        result = await provider.investigate(request)
    assert result.summary == "Test summary"
    assert result.possible_causes[0].confidence == 0.8
    assert result.investigation_steps[0].order == 1


@pytest.mark.asyncio
async def test_ollama_provider_raises_timeout_error(
    investigation_request: InvestigationRequest,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timeout", request=request)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        provider = OllamaInvestigationProvider(
            client=client,
            base_url="http://test",
            model_name="ollama",
        )

        request = investigation_request
        with pytest.raises(ProviderTimeoutError):
            await provider.investigate(request)


@pytest.mark.asyncio
async def test_ollama_provider_raises_response_error_for_http_500(
    investigation_request: InvestigationRequest,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "Internal Server Error"})

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        provider = OllamaInvestigationProvider(
            client=client,
            base_url="http://test",
            model_name="ollama",
        )

        request = investigation_request

        with pytest.raises(ProviderResponseError) as result:
            await provider.investigate(request)
        assert result.value.status_code == 500


@pytest.mark.asyncio
async def test_ollama_provider_raises_connection_error(
    investigation_request: InvestigationRequest,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("Connection error", request=request)

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        provider = OllamaInvestigationProvider(
            client=client,
            base_url="http://test",
            model_name="ollama",
        )

        with pytest.raises(ProviderConnectionError) as result:
            await provider.investigate(investigation_request)
        assert isinstance(result.value.__cause__, httpx.ConnectError)


@pytest.mark.asyncio
async def test_ollama_provider_raises_validation_error(
    investigation_request: InvestigationRequest,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        invalid_content = {
            "summary": "Test summary",
            "possible_causes": [
                {
                    "title": "Bad confidence",
                    "explanation": "Invalid confidence value.",
                    "confidence": 5.0,
                }
            ],
            "investigation_steps": [],
            "assumptions": [],
            "suggested_tests": [],
        }
        return httpx.Response(
            HTTPStatus.OK,
            json={
                "message": {"role": "assistant", "content": json.dumps(invalid_content)}
            },
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        provider = OllamaInvestigationProvider(
            client=client,
            base_url="http://test",
            model_name="ollama",
        )

        with pytest.raises(ProviderOutputError) as result:
            await provider.investigate(investigation_request)
        assert str(result.value).startswith("Ollama response validation failed:")


@pytest.mark.asyncio
async def test_ollama_provider_raises_output_error_for_invalid_json(
    investigation_request: InvestigationRequest,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            HTTPStatus.OK,
            json={
                "message": {
                    "role": "assistant",
                    "content": "json.dumps(invalid_content)",
                }
            },
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        provider = OllamaInvestigationProvider(
            client=client,
            base_url="http://test",
            model_name="ollama",
        )

        with pytest.raises(ProviderOutputError) as result:
            await provider.investigate(investigation_request)
        assert str(result.value).startswith("Ollama response validation failed:")


@pytest.mark.asyncio
async def test_ollama_provider_retries_after_timeout_then_succeeds(
    investigation_request: InvestigationRequest,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    attempts = 0
    sleep_calls: list[float] = []

    async def fake_sleep(delay: float) -> None:
        sleep_calls.append(delay)

    monkeypatch.setattr(
        asyncio,
        "sleep",
        fake_sleep,
    )

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1

        raise httpx.ReadTimeout(
            "timeout",
            request=request,
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        provider = OllamaInvestigationProvider(
            client=client,
            base_url="http://test",
            model_name="ollama",
        )
        with pytest.raises(ProviderTimeoutError) as result:
            await provider.investigate(investigation_request)

    assert attempts == 2
    assert sleep_calls == [0.5]
    assert str(result.value) == "Ollama timed out"


@pytest.mark.asyncio
async def test_ollama_provider_raises_timeout_after_retries_exhausted(
    investigation_request: InvestigationRequest,
) -> None:
    attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1

        raise httpx.ReadTimeout(
            "timeout",
            request=request,
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        provider = OllamaInvestigationProvider(
            client=client,
            base_url="http://test",
            model_name="ollama",
        )

        with pytest.raises(ProviderTimeoutError) as result:
            await provider.investigate(investigation_request)

    assert attempts == 2
    assert isinstance(
        result.value.__cause__,
        httpx.ReadTimeout,
    )


@pytest.mark.asyncio
async def test_ollama_provider_retries_after_connection_error_then_succeeds(
    investigation_request: InvestigationRequest,
) -> None:
    attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1

        if attempts == 1:
            raise httpx.ConnectError(
                "connectErr",
                request=request,
            )
        valid_content = {
            "summary": "Test summary",
            "possible_causes": [],
            "investigation_steps": [],
            "assumptions": [],
            "suggested_tests": [],
        }

        return httpx.Response(
            HTTPStatus.OK,
            json={
                "message": {
                    "role": "assistant",
                    "content": json.dumps(valid_content),
                }
            },
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        provider = OllamaInvestigationProvider(
            client=client,
            base_url="http://test",
            model_name="ollama",
        )

        result = await provider.investigate(investigation_request)

    assert attempts == 2
    assert result.summary == "Test summary"


@pytest.mark.asyncio
async def test_ollama_provider_raises_connection_error_after_retries_exhausted(
    investigation_request: InvestigationRequest,
) -> None:
    attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1

        raise httpx.ConnectError(
            "connectErr",
            request=request,
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        provider = OllamaInvestigationProvider(
            client=client,
            base_url="http://test",
            model_name="ollama",
        )

        with pytest.raises(ProviderConnectionError) as result:
            await provider.investigate(investigation_request)

    assert attempts == 2
    assert isinstance(result.value.__cause__, httpx.ConnectError)
