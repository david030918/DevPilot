class DevPilotError(Exception):
    """Base exception for DevPilot AI service."""


class UnsupportedProviderError(DevPilotError):
    def __init__(self, provider: str):
        self.provider = provider
        super().__init__(f"Unsupported AI provider: {provider}")