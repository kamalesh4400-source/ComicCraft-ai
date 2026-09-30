from PIL import Image
from app.config import settings
from app.services.exporters import save_pdf


def test_save_pdf(tmp_path, monkeypatch):
    image_dir = tmp_path / "static" / "panels"
    image_dir.mkdir(parents=True)
    image = image_dir / "1.png"
    Image.new("RGB", (100, 100), "white").save(image)
    monkeypatch.setattr(settings, "project_root", tmp_path)
    monkeypatch.setattr(settings, "export_dir", "exports")
    (tmp_path / "exports").mkdir(parents=True)
    layout = [{"panel_number": 1, "title": "Test", "image_path": "static/panels/1.png", "scene_description": "scene", "caption": "caption", "narration": "narration", "dialogue": "dialogue"}]
    output = save_pdf(layout)
    assert output.endswith(".pdf")
    assert (tmp_path / "exports").glob("*.pdf")
