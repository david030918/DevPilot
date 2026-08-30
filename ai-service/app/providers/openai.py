from app.models.investigation import (
    InvestigationRequest,
    InvestigationResponse,
)
from app.providers.base import InvestigationProvider


class OpenAIInvestigationProvider(InvestigationProvider):
    async def investigate(
        self,
        request: InvestigationRequest,
    ) -> InvestigationResponse:
        raise NotImplementedError
