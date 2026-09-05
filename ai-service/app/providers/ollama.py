import asyncio
import json

import httpx
from pydantic import ValidationError
from starlette import status

from app.core.exceptions import (
    ProviderConnectionError,
    ProviderOutputError,
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
        self.retryable_status_codes = {
            status.HTTP_502_BAD_GATEWAY,
            status.HTTP_503_SERVICE_UNAVAILABLE,
            status.HTTP_504_GATEWAY_TIMEOUT,
        }

    async def _wait_before_retry(self, attempt: int) -> None:
        delay = 0.5 * (2**attempt)
        await asyncio.sleep(delay)

    async def _send_request_with_retry(
        self,
        request: InvestigationRequest,
    ) -> httpx.Response:
        max_attempts = 3

        for attempt in range(max_attempts):
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
                return response

            except httpx.TimeoutException as exc:
                if attempt == max_attempts - 1:
                    raise ProviderTimeoutError("Ollama timed out") from exc
                await self._wait_before_retry(attempt)
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code not in self.retryable_status_codes:
                    raise ProviderResponseError(exc.response.status_code) from exc

                if attempt == max_attempts - 1:
                    raise ProviderResponseError(exc.response.status_code) from exc

                await self._wait_before_retry(attempt)

            except httpx.RequestError as exc:
                if attempt == max_attempts - 1:
                    raise ProviderConnectionError(
                        f"Ollama request failed: {exc}"
                    ) from exc
                await self._wait_before_retry(attempt)

        raise RuntimeError("Unreachable")

    def _parse_response(self, response: httpx.Response) -> InvestigationResponse:
        try:
            data = response.json()
        except json.JSONDecodeError as exc:
            raise ProviderOutputError("Ollama response was not valid JSON") from exc
        # Output Validate

        try:
            return InvestigationResponse.model_validate_json(data["message"]["content"])
        except KeyError as exc:
            raise ProviderOutputError("Malformed Ollama response") from exc
        except ValidationError as exc:
            raise ProviderOutputError(
                f"Ollama response validation failed: {exc}"
            ) from exc

    async def investigate(
        self,
        request: InvestigationRequest,
    ) -> InvestigationResponse:
        reponse = await self._send_request_with_retry(request)
        return self._parse_response(reponse)
