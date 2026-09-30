from app.models import ComicStory


def build_layout(story: ComicStory, image_paths: list[str]) -> list[dict]:
    if len(story.panels) != 5 or len(image_paths) != 5:
        raise ValueError("ComicCraft requires exactly five panels and five images.")
    return [
        {
            "panel_number": panel.panel_number,
            "title": panel.title,
            "image_path": image_paths[index],
            "scene_description": panel.scene_description,
            "caption": panel.caption,
            "narration": panel.narration,
            "dialogue": panel.dialogue,
            "image_prompt": panel.image_prompt,
        }
        for index, panel in enumerate(story.panels)
    ]
