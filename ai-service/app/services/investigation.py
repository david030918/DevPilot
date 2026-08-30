import logging

from app.models.investigation import InvestigationRequest, InvestigationResponse
from app.providers.base import InvestigationProvider

logger = logging.getLogger(__name__)


class InvestigationService:
    def __init__(self, provider: InvestigationProvider):
        self.provider = provider

    async def investigate(self, request: InvestigationRequest) -> InvestigationResponse:
        logger.info(
            "Starting investigation  repository=%s/%s issue=%s",
            request.repository.owner,
            request.repository.name,
            request.issue.number,
        )

        result = await self.provider.investigate(request)

        logger.info(
            "Investigation completed repository=%s/%s issue=%s",
            request.repository.owner,
            request.repository.name,
            request.issue.number,
        )

        return result
