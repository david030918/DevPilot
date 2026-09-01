import httpx

from app.core.exceptions import (
    ProviderConnectionError,
    ProviderResponseError,
    ProviderTimeoutError,
)
from app.models.investigation import InvestigationRequest, InvestigationResponse
from app.providers.base import InvestigationProvider


class OllamaInvestigationProvider(InvestigationProvider):
    def __init__(
        self, base_url: str, client: httpx.AsyncClient, model_name: str
    ) -> None:
        self.base_url = base_url
        self.model_name = model_name
        self.client = client

    async def investigate(
        self,
        request: InvestigationRequest,
    ) -> InvestigationResponse:
        try:
            response = await self.client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model_name,
                    "stream": False,
                    "format": InvestigationResponse.model_json_schema(),
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are a software engineering "
                                "investigation assistant. "
                                "Analyze the supplied GitHub issue. "
                                "Return a concise summary, plausible causes, "
                                "investigation steps, assumptions, "
                                "and suggested tests. "
                                "Do not present assumptions as established facts."
                            ),
                        },
                        {
                            "role": "user",
                            "content": (
                                f"Repository: "
                                f"{request.repository.owner}/"
                                f"{request.repository.name}\n"
                                f"Default branch: "
                                f"{request.repository.default_branch}\n\n"
                                f"Issue #{request.issue.number}\n"
                                f"Title: {request.issue.title}\n"
                                f"Body:\n{request.issue.body or ''}"
                            ),
                        },
                    ],
                },
            )

            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise ProviderTimeoutError("Ollama timed out") from exc
        except httpx.HTTPStatusError as exc:
            raise ProviderResponseError(exc.response.status_code) from exc
        except httpx.RequestError as exc:
            raise ProviderConnectionError(f"Ollama request failed: {exc}") from exc
        data = response.json()
        return InvestigationResponse.model_validate_json(data["message"]["content"])
