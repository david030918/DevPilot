import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.api.dependencies import get_investigation_service
from app.core.exceptions import UnsupportedProviderError
from app.main import app
from app.models.investigation import PossibleCause
from app.providers.fake import FakeInvestigationProvider
from app.services.investigation import InvestigationService


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_investigate_issue_returns_structured_response(client: TestClient) -> None:
    def override_service() -> InvestigationService:
        return InvestigationService(FakeInvestigationProvider())

    app.dependency_overrides[get_investigation_service] = override_service
    try:
        response = client.post(
            "/ai/investigate-issue",
            json={
                "repository": {
                    "owner": "david030918",
                    "name": "DevPilot",
                    "default_branch": "main",
                },
                "issue": {
                    "number": 1,
                    "title": "Login returns 500",
                    "body": "Users cannot sign in.",
                },
            },
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
    client: TestClient,
) -> None:
    def override_service() -> None:
        raise UnsupportedProviderError("invalid-provider")

    app.dependency_overrides[get_investigation_service] = override_service

    try:
        response = client.post(
            "/ai/investigate-issue",
            json={
                "repository": {
                    "owner": "david030918",
                    "name": "DevPilot",
                    "default_branch": "main",
                },
                "issue": {
                    "number": 1,
                    "title": "Login returns 500",
                    "body": "Users cannot sign in.",
                },
            },
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
