import os
os.environ["MOCK_AI"] = "true"
os.environ["IMAGE_PROVIDER"] = "placeholder"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "ComicCraft" in response.text

def test_generate_json_mock():
    payload = {
        "story_prompt": "A brave fox explores a magical forest.",
        "character_name": "Lumi",
        "setting": "forest",
        "tone": "funny",
        "art_style": "comic book",
    }
    response = client.post("/generate-comic/json", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["panels"]) == 5
    assert data["pdf_url"].startswith("/exports/")
