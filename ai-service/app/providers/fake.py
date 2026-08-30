from app.models.investigation import (
    InvestigationRequest,
    InvestigationResponse,
    InvestigationStep,
    PossibleCause,
    SuggestedTest,
)
from app.providers.base import InvestigationProvider


class FakeInvestigationProvider(InvestigationProvider):
    async def investigate(
        self,
        request: InvestigationRequest,
    ) -> InvestigationResponse:
        return InvestigationResponse(
            summary="Test Response",
            assumptions=["Assumptions: The application is running on a Linux server."],
            possible_causes=[
                PossibleCause(
                    title="example configuration issue",
                    explanation=(
                        f"The issue '{request.issue.title}' may be caused "
                        "by an incorrect application configuration."
                    ),
                    confidence=0.75,
                )
            ],
            investigation_steps=[
                InvestigationStep(
                    order=1,
                    description=(
                        f"Perform the following steps to investigate the issue '{request.issue.title}':"
                    ),
                )
            ],
            suggested_tests=[
                SuggestedTest(
                    name="Configuration Validation",
                    description="Verify that the application configuration is correct.",
                )
            ],
        )
