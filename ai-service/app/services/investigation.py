import logging

from app.models.investigation import (
    InvestigationMetadata,
    InvestigationRequest,
    InvestigationResult,
)
from app.prompts.investigation import (
    INVESTIGATION_PROMPT_VERSION,
    INVESTIGATION_SCHEMA_VERSION,
)
from app.providers.base import InvestigationProvider

logger = logging.getLogger(__name__)


class InvestigationService:
    def __init__(self, provider: InvestigationProvider):
        self.provider = provider

    async def investigate(self, request: InvestigationRequest) -> InvestigationResult:
        logger.info(
            "Starting investigation  repository=%s/%s issue=%s",
            request.repository.owner,
            request.repository.name,
            request.issue.number,
        )

        investigation = await self.provider.investigate(request)

        logger.info(
            "Investigation completed repository=%s/%s issue=%s",
            request.repository.owner,
            request.repository.name,
            request.issue.number,
        )

        return InvestigationResult(
            investigation=investigation,
            metadata=InvestigationMetadata(
                provider=self.provider.provider_name,
                model=self.provider.model_name,
                prompt_version=INVESTIGATION_PROMPT_VERSION,
                schema_version=INVESTIGATION_SCHEMA_VERSION,
            ),
        )
