from app.models import ComicStory
from app.services.layout_builder import build_layout


def test_build_layout():
    story = ComicStory.model_validate({"panels": [{"panel_number": i, "title": f"P{i}", "scene_description": "scene", "image_prompt": "image", "caption": "caption", "narration": "narration", "dialogue": "dialogue"} for i in range(1, 6)]})
    layout = build_layout(story, [f"static/panels/{i}.png" for i in range(1, 6)])
    assert len(layout) == 5
    assert layout[0]["image_path"].endswith("1.png")
