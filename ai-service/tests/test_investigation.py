from fastapi.testclient import TestClient

from app.api.dependencies import get_investigation_service
from app.core.exceptions import UnsupportedProviderError
from app.main import app


client = TestClient(app)


def test_investigate_issue_returns_structured_response() -> None:
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
    assert "possible_causes" in data
    assert "investigation_steps" in data
    assert "suggested_tests" in data

    assert data["possible_causes"][0]["confidence"] == 0.75

def test_investigate_issue_reject_invalid_request()->None:
    response=client.post(
        "/ai/investigate-issue",
        json={
            "respository": {
                "owner":"david030918"
            }
        },
    )
    assert response.status_code == 422
    data=response.json()
    assert "detail" in data
    print(data["detail"])

def test_investigate_issue_returns_500_for_unsupported_provider() -> None:
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
