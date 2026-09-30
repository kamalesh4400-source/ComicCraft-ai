def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "ComicCraft" in response.text


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate_json(client):
    response = client.post("/generate-comic/json", json={"story_prompt": "A hero finds a hidden door", "character_name": "Maya", "setting": "forest", "tone": "adventure", "art_style": "comic book"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["layout"]) == 5
    assert data["pdf_url"].endswith(".pdf")
