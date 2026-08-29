from app.core.config import get_settings
from app.core.exceptions import UnsupportedProviderError
from app.providers.fake import FakeInvestigationProvider
from app.services.investigation import InvestigationService


def get_investigation_service()->InvestigationService:
    settings=get_settings()
    if settings.ai_provider=="fake":
        provider=FakeInvestigationProvider()
    else:
        raise UnsupportedProviderError(settings.ai_provider)
    return InvestigationService(provider)