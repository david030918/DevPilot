from openai import AsyncOpenAI

from app.models.investigation import (
    InvestigationRequest,
    InvestigationResponse,
)
from app.providers.base import InvestigationProvider


class OpenAIInvestigationProvider(InvestigationProvider):
    def __init__(
        self,
        client: AsyncOpenAI,
        model_name: str,
    ) -> None:
        self.client = client
        self.model_name = model_name

    async def investigate(
        self,
        request: InvestigationRequest,
    ) -> InvestigationResponse:

        raise NotImplementedError
