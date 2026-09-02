import httpx
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_http_client_lifecycle() -> None:
    with TestClient(app):
        http_client = app.state.http_client

        assert isinstance(
            http_client,
            httpx.AsyncClient,
        )
        assert not http_client.is_closed

    assert http_client.is_closed
