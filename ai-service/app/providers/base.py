from abc import ABC, abstractmethod

from app.models.investigation import (
    InvestigationRequest,
    InvestigationResponse,
)


class InvestigationProvider(ABC):
    @abstractmethod
    async def investigate(
        self,
        request: InvestigationRequest,
    ) -> InvestigationResponse:
        pass
