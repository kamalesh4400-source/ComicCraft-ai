import json
from typing import List
from pydantic import BaseModel
from app.config import settings
from app.models import PanelOutline, PanelStory

class StoryResponse(BaseModel):
    panels: List[PanelStory]

def _mock_story(outlines: List[PanelOutline]) -> List[PanelStory]:
    return [
        PanelStory(
            panel_number=p.panel_number,
            caption=f"{p.title}.",
            narration=p.scene_description,
            dialogue=[f"{p.title} - let's keep moving!"],
        )
        for p in outlines
    ]

def generate_story(request, outlines: List[PanelOutline]) -> List[PanelStory]:
    if settings.mock_ai:
        return _mock_story(outlines)
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured. Set it in .env or use MOCK_AI=true.")

    from google import genai
    client = genai.Client(api_key=settings.gemini_api_key)
    outline_json = json.dumps([p.model_dump() for p in outlines], ensure_ascii=False, indent=2)
    prompt = f"""
Expand this comic outline into polished comic writing.

Original story prompt: {request.story_prompt}
Character: {request.character_name}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}

Outline:
{outline_json}

For every panel return panel_number, caption, narration, and dialogue.
Caption should be concise. Narration should be 1–3 sentences. Dialogue should be natural.
Keep continuity and do not introduce unexplained main characters.
"""
    response = client.models.generate_content(
        model=settings.gemini_story_model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": StoryResponse,
        },
    )
    try:
        parsed = response.parsed or StoryResponse.model_validate(json.loads(response.text))
    except Exception as exc:
        raise RuntimeError("Gemini returned invalid story JSON.") from exc

    stories = sorted(parsed.panels, key=lambda p: p.panel_number)
    if len(stories) != len(outlines):
        raise RuntimeError("Story panel count does not match outline panel count.")
    return stories
