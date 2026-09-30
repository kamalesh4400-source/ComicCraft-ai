from google import genai
from google.genai import types

from app.config import settings
from app.models import ComicOutline


class GeminiFlashService:
    """Generate a structured five-panel comic outline with Gemini."""

    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to .env.")
        self.client = genai.Client(api_key=settings.gemini_api_key)

    def generate_outline(
        self,
        story_prompt: str,
        character_name: str,
        setting: str,
        tone: str,
        art_style: str,
    ) -> ComicOutline:
        prompt = f"""
Create a five-panel comic story outline.

Story idea: {story_prompt}
Main character: {character_name or 'Create an appropriate protagonist'}
Setting: {setting or 'Choose a setting that fits the story'}
Tone: {tone}
Art style: {art_style}

Requirements:
- Return exactly five panels, numbered 1 through 5.
- Each panel must have a short title.
- Each panel must have a visual scene description.
- Each panel must have a detailed image-generation prompt.
- Maintain character and setting continuity across all panels.
- Make the sequence have a clear beginning, development, turning point, and conclusion.
- Do not add extra panels.
"""
        response = self.client.models.generate_content(
            model=settings.gemini_outline_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.8,
                response_mime_type="application/json",
                response_schema=ComicOutline,
            ),
        )
        if not response.parsed:
            raise RuntimeError("Gemini returned no valid structured outline.")
        return response.parsed


def generate_outline(story_prompt: str, character_name: str, setting: str, tone: str, art_style: str) -> ComicOutline:
    return GeminiFlashService().generate_outline(story_prompt, character_name, setting, tone, art_style)
