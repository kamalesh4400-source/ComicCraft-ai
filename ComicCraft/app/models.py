from typing import List
from pydantic import BaseModel, Field, field_validator

class PromptRequest(BaseModel):
    story_prompt: str = Field(..., min_length=3, max_length=2000)
    character_name: str = Field(..., min_length=1, max_length=80)
    setting: str = Field(..., min_length=1, max_length=120)
    tone: str = Field(..., min_length=1, max_length=80)
    art_style: str = Field(..., min_length=1, max_length=100)

    @field_validator("story_prompt", "character_name", "setting", "tone", "art_style")
    @classmethod
    def strip_values(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be empty.")
        return value

class ImageTestRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=2000)

class PanelOutline(BaseModel):
    panel_number: int = Field(..., ge=1)
    title: str
    scene_description: str
    image_prompt: str

class PanelStory(BaseModel):
    panel_number: int = Field(..., ge=1)
    caption: str = ""
    narration: str = ""
    dialogue: List[str] = Field(default_factory=list)

class ComicPanel(BaseModel):
    panel_number: int
    title: str
    scene_description: str
    image_prompt: str
    image_path: str
    caption: str = ""
    narration: str = ""
    dialogue: List[str] = Field(default_factory=list)

class ComicResponse(BaseModel):
    title: str
    panels: List[ComicPanel]
    pdf_url: str
