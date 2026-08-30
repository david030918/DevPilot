from app.core.config import get_settings
from app.core.exceptions import UnsupportedProviderError
from app.providers.fake import FakeInvestigationProvider
from app.providers.openai import OpenAIInvestigationProvider
from app.services.investigation import InvestigationService


def get_investigation_service() -> InvestigationService:
    settings = get_settings()
    if settings.ai_provider == "fake":
        provider = FakeInvestigationProvider()
    elif settings.ai_provider == "openai":
        provider = OpenAIInvestigationProvider()
    else:
        raise UnsupportedProviderError(settings.ai_provider)
    return InvestigationService(provider)
