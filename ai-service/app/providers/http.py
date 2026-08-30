import httpx

from app.core.exceptions import (
    ProviderConnectionError,
    ProviderResponseError,
    ProviderTimeoutError,
)


async def get_json(
    client: httpx.AsyncClient,
    url: str,
) -> dict:
    try:
        response = await client.get(url)
        response.raise_for_status()

        return response.json()

    except httpx.TimeoutException as exc:
        raise ProviderTimeoutError("Provider request timed out") from exc

    except httpx.HTTPStatusError as exc:
        raise ProviderResponseError(exc.response.status_code) from exc

    except httpx.RequestError as exc:
        raise ProviderConnectionError("Provider request failed") from exc
