from google import genai
from google.genai import types

from app.config import settings
from app.models import ComicOutline, ComicStory


class GeminiProService:
    """Expand the outline into narration, captions, dialogue, and image prompts."""

    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to .env.")
        self.client = genai.Client(api_key=settings.gemini_api_key)

    def generate_story(self, outline: ComicOutline) -> ComicStory:
        outline_json = outline.model_dump_json(indent=2)
        prompt = f"""
Expand this five-panel comic outline into a polished comic script.

OUTLINE:
{outline_json}

Requirements:
- Return exactly five panels in the same order.
- Preserve each panel number, title, scene description, and image prompt.
- Add a concise caption where useful.
- Add engaging narration describing action, emotion, or context.
- Add natural character dialogue where appropriate.
- Keep dialogue short enough for a comic panel.
- Maintain continuity between panels.
- Make the final panel feel like a satisfying conclusion.
"""
        response = self.client.models.generate_content(
            model=settings.gemini_story_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.85,
                response_mime_type="application/json",
                response_schema=ComicStory,
            ),
        )
        if not response.parsed:
            raise RuntimeError("Gemini returned no valid comic story.")
        return response.parsed


def generate_story(outline: ComicOutline) -> ComicStory:
    return GeminiProService().generate_story(outline)
