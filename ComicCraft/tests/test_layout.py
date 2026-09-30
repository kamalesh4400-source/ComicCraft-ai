from app.models import PanelOutline, PanelStory
from app.services.layout_builder import build_comic_layout

def test_layout_matches_panels():
    outlines = [
        PanelOutline(panel_number=1, title="Start", scene_description="Beginning", image_prompt="hero"),
        PanelOutline(panel_number=2, title="Next", scene_description="Middle", image_prompt="hero running"),
    ]
    stories = [
        PanelStory(panel_number=2, caption="C2", narration="N2", dialogue=["D2"]),
        PanelStory(panel_number=1, caption="C1", narration="N1", dialogue=["D1"]),
    ]
    result = build_comic_layout(outlines, stories, ["/static/a.png", "/static/b.png"])
    assert result[0].panel_number == 1
    assert result[0].caption == "C1"
    assert result[1].panel_number == 2
    assert result[1].dialogue == ["D2"]
