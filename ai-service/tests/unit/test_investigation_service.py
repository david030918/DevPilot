import pytest

from app.models.investigation import (
    InvestigationRequest,
    InvestigationResponse,
    IssueContext,
    RepositoryContext,
)
from app.providers.base import InvestigationProvider
from app.services.investigation import InvestigationService


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
async def test_fake_investigation_provider(investigation_request: InvestigationRequest):
    class FakeInvestigationProvider(InvestigationProvider):
        @property
        def provider_name(self) -> str:
            return "fake"

        @property
        def model_name(self) -> str:
            return "fake-model"

        async def investigate(
            self,
            request: InvestigationRequest,
        ) -> InvestigationResponse:
            return InvestigationResponse(
                summary="Test summary",
                possible_causes=[
                    {
                        "title": "Configuration issue",
                        "explanation": "Configuration may be incorrect.",
                        "confidence": 0.8,
                    }
                ],
                investigation_steps=[
                    {
                        "order": 1,
                        "description": "Check configuration.",
                    }
                ],
                assumptions=["The application is running."],
                suggested_tests=[
                    {
                        "name": "Configuration test",
                        "description": "Verify configuration.",
                    }
                ],
            )

    provider = FakeInvestigationProvider()
    service = InvestigationService(provider)
    result = await service.investigate(investigation_request)
    assert result.investigation.summary == "Test summary"
    assert result.metadata.provider == "fake"
    assert result.metadata.model == "fake-model"
    assert result.metadata.prompt_version == "v1"
    assert result.metadata.schema_version == "v1"
