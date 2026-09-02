import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from starlette import status

from app.api.dependencies import get_investigation_service
from app.core.exceptions import (
    ProviderConnectionError,
    ProviderOutputError,
    ProviderResponseError,
    ProviderTimeoutError,
    UnsupportedProviderError,
)
from app.main import app
from app.models.investigation import (
    InvestigationRequest,
    IssueContext,
    PossibleCause,
    RepositoryContext,
)
from app.providers.fake import FakeInvestigationProvider
from app.services.investigation import InvestigationService


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


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


def test_investigate_issue_returns_structured_response(
    client: TestClient, investigation_request: InvestigationRequest
) -> None:
    def override_service() -> InvestigationService:
        return InvestigationService(FakeInvestigationProvider())

    app.dependency_overrides[get_investigation_service] = override_service
    try:
        response = client.post(
            "/ai/investigate-issue",
            json=investigation_request.model_dump(),
        )

        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "assumptions" in data
        assert "possible_causes" in data
        assert "investigation_steps" in data
        assert "suggested_tests" in data

        assert data["possible_causes"][0]["confidence"] == 0.75
        assert data["summary"] == "Test Response"
        assert data["assumptions"] == [
            "Assumptions: The application is running on a Linux server."
        ]
    finally:
        app.dependency_overrides.clear()


def test_investigate_issue_reject_invalid_request(client: TestClient) -> None:
    response = client.post(
        "/ai/investigate-issue",
        json={"respository": {"owner": "david030918"}},
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_investigate_issue_returns_500_for_unsupported_provider(
    client: TestClient, investigation_request: InvestigationRequest
) -> None:
    def override_service() -> None:
        raise UnsupportedProviderError("invalid-provider")

    app.dependency_overrides[get_investigation_service] = override_service

    try:
        response = client.post(
            "/ai/investigate-issue",
            json=investigation_request.model_dump(),
        )

        assert response.status_code == 500
        assert response.json() == {
            "error": "unsupported_provider",
            "message": "Unsupported AI provider: invalid-provider",
        }
    finally:
        app.dependency_overrides.clear()


def test_possible_cause_rejects_confidence_above_one() -> None:
    with pytest.raises(ValidationError):
        PossibleCause(
            title="Invalid confidence",
            explanation="Confidence should be between zero and one.",
            confidence=1.5,
        )


def test_possible_cause_rejects_confidence_below_zero() -> None:
    with pytest.raises(ValidationError):
        PossibleCause(
            title="Invalid confidence",
            explanation="Confidence should be between zero and one.",
            confidence=-0.1,
        )


def test_investigate_issue_returns_504_for_provider_timeout(
    client: TestClient, investigation_request: InvestigationRequest
) -> None:
    class TimeoutService:
        async def investigate(self, request):
            raise ProviderTimeoutError("Ollama request timed out")

    def override_service():
        return TimeoutService()

    app.dependency_overrides[get_investigation_service] = override_service

    try:
        response = client.post(
            "/ai/investigate-issue",
            json=investigation_request.model_dump(),
        )

        assert response.status_code == 504

        assert response.json() == {
            "error": "provider_timeout",
            "message": "Ollama request timed out",
        }

    finally:
        app.dependency_overrides.clear()


def test_provider_connection_error(
    client: TestClient, investigation_request: InvestigationRequest
) -> None:
    class ConnectionService:
        async def investigate(self, request):
            raise ProviderConnectionError("Ollama Connection Err")

    def override_service():
        return ConnectionService()

    app.dependency_overrides[get_investigation_service] = override_service

    try:
        response = client.post(
            "/ai/investigate-issue",
            json=investigation_request.model_dump(),
        )
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE

        assert response.json() == {
            "error": "provider_connection_error",
            "message": "Ollama Connection Err",
        }
    finally:
        app.dependency_overrides.clear()


def test_provider_response_error(
    client: TestClient, investigation_request: InvestigationRequest
) -> None:
    class ConnectionService:
        async def investigate(self, request):
            raise ProviderResponseError(status_code=status.HTTP_502_BAD_GATEWAY)

    def override_service():
        return ConnectionService()

    app.dependency_overrides[get_investigation_service] = override_service

    try:
        response = client.post(
            "/ai/investigate-issue",
            json=investigation_request.model_dump(),
        )
        assert response.status_code == status.HTTP_502_BAD_GATEWAY

        assert response.json() == {
            "error": "provider_response_error",
            "message": "Provider response error: 502",
        }
    finally:
        app.dependency_overrides.clear()


def test_provider_output_error(
    client: TestClient, investigation_request: InvestigationRequest
) -> None:
    class OutputErrorService:
        async def investigate(self, request):
            raise ProviderOutputError("Ollama returned invalid structured output")

    def override_service():
        return OutputErrorService()

    app.dependency_overrides[get_investigation_service] = override_service

    try:
        response = client.post(
            "/ai/investigate-issue",
            json=investigation_request.model_dump(),
        )
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        assert response.json() == {
            "error": "provider_output_error",
            "message": "Ollama returned invalid structured output",
        }
    finally:
        app.dependency_overrides.clear()
