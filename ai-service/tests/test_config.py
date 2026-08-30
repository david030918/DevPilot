from app.core.config import Settings


def test_settings_use_default_values() -> None:
    settings = Settings()

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
