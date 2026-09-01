import httpx
from openai import AsyncOpenAI

from app.core.config import get_settings
from app.core.exceptions import UnsupportedProviderError
from app.providers.fake import FakeInvestigationProvider
from app.providers.ollama import OllamaInvestigationProvider
from app.providers.openai import OpenAIInvestigationProvider
from app.services.investigation import InvestigationService


def get_investigation_service() -> InvestigationService:
    settings = get_settings()
    if settings.ai_provider == "fake":
        provider = FakeInvestigationProvider()
    elif settings.ai_provider == "openai":
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is required when AI_PROVIDER=openai")
        client = AsyncOpenAI(
            api_key=settings.openai_api_key, timeout=settings.request_timeout_seconds
        )
        provider = OpenAIInvestigationProvider(
            client=client, model_name=settings.model_name
        )
    elif settings.ai_provider == "ollama":
        client = httpx.AsyncClient(timeout=settings.request_timeout_seconds)
        provider = OllamaInvestigationProvider(
            base_url=settings.ollama_base_url,
            client=client,
            model_name=settings.model_name,
        )
    else:
        raise UnsupportedProviderError(settings.ai_provider)
    return InvestigationService(provider)
