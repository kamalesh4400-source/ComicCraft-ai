from typing import List
from app.models import ComicPanel, PanelOutline, PanelStory

def build_comic_layout(
    outlines: List[PanelOutline],
    stories: List[PanelStory],
    image_paths: List[str],
) -> List[ComicPanel]:
    if len(outlines) != len(image_paths):
        raise ValueError("Every outline panel must have an image.")
    story_by_number = {item.panel_number: item for item in stories}
    layout = []
    for outline, image_path in zip(outlines, image_paths):
        story = story_by_number.get(outline.panel_number)
        if story is None:
            raise ValueError(f"Missing story content for panel {outline.panel_number}.")
        layout.append(ComicPanel(
            panel_number=outline.panel_number,
            title=outline.title,
            scene_description=outline.scene_description,
            image_prompt=outline.image_prompt,
            image_path=image_path,
            caption=story.caption,
            narration=story.narration,
            dialogue=story.dialogue,
        ))
    return layout
