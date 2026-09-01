class DevPilotError(Exception):
    """Base exception for DevPilot AI service."""


class UnsupportedProviderError(DevPilotError):
    def __init__(self, provider: str):
        self.provider = provider
        super().__init__(f"Unsupported AI provider: {provider}")


class ProviderError(DevPilotError):
    """Base exception for provider errors."""


class ProviderTimeoutError(ProviderError):
    """Base exception for provider timeout errors."""


class ProviderConnectionError(ProviderError):
    """Base exception for provider connection errors."""


class ProviderResponseError(ProviderError):
    def __init__(self, status_code: int):
        self.status_code = status_code
        super().__init__(f"Provider response error: {status_code}")


class ProviderOutputError(Exception):
    """Base exception for provider output errors."""
