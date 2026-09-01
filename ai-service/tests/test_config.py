from app.core.config import Settings, get_settings


def test_settings_use_default_values() -> None:
    settings = Settings(_env_file=None)

    assert settings.ai_provider == "fake"
    assert settings.request_timeout_seconds == 30.0


def test_settings_read_environment_variables(
    monkeypatch,
) -> None:
    monkeypatch.setenv(
        "AI_PROVIDER",
        "test-provider",
    )

    settings = Settings()

    assert settings.ai_provider == "test-provider"


def test_setting_read_open_api_key(monkeypatch) -> None:
    monkeypatch.setenv(
        "OPENAI_API_KEY",
        "test-key",
    )

    settings = Settings()

    assert settings.openai_api_key == "test-key"


def OpenAIInvestigationProvider(monkeypatch) -> None:
    settings = Settings()
    assert settings.ai_provider == "fake"

    get_settings.cash_clear()
    monkeypatch.setenv(
        "AI_PROVIDER",
        "openai",
    )
    settings = Settings()
    assert settings.ai_provider != "fake"
