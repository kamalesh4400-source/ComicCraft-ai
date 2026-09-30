from app.config import settings
from app.models import ComicOutline, ComicStory
from app.services.exporters import save_pdf
from app.services.image_generator import generate_image
from app.services.layout_builder import build_layout


class DemoFlashService:
    def generate_outline(self, story_prompt, character_name, setting, tone, art_style):
        character = character_name or "Alex"
        place = setting or "a mysterious forest"
        titles = ["The Beginning", "Into the Unknown", "The Turning Point", "A Brave Choice", "A New Dawn"]
        return ComicOutline.model_validate({"panels": [
            {"panel_number": i + 1, "title": title,
             "scene_description": f"{character} faces the next stage of the adventure in {place}.",
             "image_prompt": f"{art_style}, {character} in {place}, panel {i + 1}, {tone}, cinematic comic composition"}
            for i, title in enumerate(titles)
        ]})


class DemoProService:
    def generate_story(self, outline):
        panels = []
        for panel in outline.panels:
            panels.append({
                **panel.model_dump(),
                "caption": f"Panel {panel.panel_number}: The adventure continues.",
                "narration": "The moment feels important, and the hero gathers courage for what comes next.",
                "dialogue": '"We can do this!"',
            })
        return ComicStory.model_validate({"panels": panels})


class ComicService:
    def generate(self, story_prompt, character_name, setting, tone, art_style):
        if settings.demo_mode:
            outline = DemoFlashService().generate_outline(story_prompt, character_name, setting, tone, art_style)
            story = DemoProService().generate_story(outline)
        else:
            from app.services.gemini_flash import GeminiFlashService
            from app.services.gemini_pro import GeminiProService
            outline = GeminiFlashService().generate_outline(story_prompt, character_name, setting, tone, art_style)
            story = GeminiProService().generate_story(outline)

        if len(outline.panels) != settings.max_panels or len(story.panels) != settings.max_panels:
            raise RuntimeError("AI output must contain exactly five panels.")

        image_paths = [generate_image(panel.image_prompt, panel.panel_number) for panel in story.panels]
        layout = build_layout(story, image_paths)
        pdf_path = save_pdf(layout)
        return layout, pdf_path


comic_service = ComicService()
