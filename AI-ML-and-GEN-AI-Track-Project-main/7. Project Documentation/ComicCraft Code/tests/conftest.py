import pytest
from fastapi.testclient import TestClient
from app.config import settings
from app.main import app


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(settings, "demo_mode", True)
    monkeypatch.setattr(settings, "image_provider", "demo")
    return TestClient(app)
