import json
from typing import List
from pydantic import BaseModel
from app.config import settings
from app.models import PanelOutline

class OutlineResponse(BaseModel):
    panels: List[PanelOutline]

def _mock_outline(request) -> List[PanelOutline]:
    descriptions = [
        "The hero arrives and discovers the central mystery.",
        "The hero explores the setting and encounters an obstacle.",
        "The hero faces the main challenge and makes a brave choice.",
        "The hero solves the immediate problem with creativity.",
        "The hero reaches a satisfying ending and looks toward a new adventure.",
    ]
    titles = ["The Arrival", "The Discovery", "The Challenge", "The Solution", "A New Beginning"]
    return [
        PanelOutline(
            panel_number=i + 1,
            title=f"Panel {i + 1}: {titles[i]}",
            scene_description=f"{request.character_name} in {request.setting}. {descriptions[i]}",
            image_prompt=(
                f"{request.character_name}, {request.setting}, {request.art_style} comic illustration, "
                f"{request.tone} mood, cinematic composition, expressive character, clean line art"
            ),
        )
        for i in range(5)
    ]

def generate_outline(request) -> List[PanelOutline]:
    if settings.mock_ai:
        return _mock_outline(request)
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured. Set it in .env or use MOCK_AI=true.")

    from google import genai
    client = genai.Client(api_key=settings.gemini_api_key)
    prompt = f"""
Create a cohesive {settings.num_panels}-panel comic outline.

Story prompt: {request.story_prompt}
Main character: {request.character_name}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}

Return exactly {settings.num_panels} panels. Each panel needs:
panel_number, title, scene_description, image_prompt.
Keep the character visually consistent and make the sequence have a clear beginning,
middle, climax and ending. Image prompts should describe action, composition, environment,
lighting and the requested style.
"""
    response = client.models.generate_content(
        model=settings.gemini_outline_model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": OutlineResponse,
        },
    )
    try:
        parsed = response.parsed or OutlineResponse.model_validate(json.loads(response.text))
    except Exception as exc:
        raise RuntimeError("Gemini returned an invalid outline.") from exc

    panels = sorted(parsed.panels, key=lambda p: p.panel_number)
    if len(panels) != settings.num_panels:
        raise RuntimeError(f"Gemini returned {len(panels)} panels; expected {settings.num_panels}.")
    return panels
