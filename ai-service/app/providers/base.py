from abc import ABC, abstractmethod

from app.models.investigation import (
    InvestigationRequest,
    InvestigationResponse,
)


class InvestigationProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str: ...

    @property
    @abstractmethod
    def model_name(self) -> str: ...

    @abstractmethod
    async def investigate(
        self,
        request: InvestigationRequest,
    ) -> InvestigationResponse:
        pass
