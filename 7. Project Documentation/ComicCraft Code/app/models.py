from pydantic import BaseModel, Field, field_validator


class PromptRequest(BaseModel):
    story_prompt: str = Field(..., min_length=10, max_length=2000)
    character_name: str = Field(default="", max_length=100)
    setting: str = Field(default="", max_length=200)
    tone: str = Field(default="adventure", max_length=50)
    art_style: str = Field(default="comic book", max_length=100)

    @field_validator("story_prompt", "character_name", "setting", "tone", "art_style")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()


class ImageTestRequest(BaseModel):
    prompt: str = Field(default="A heroic fox exploring a magical forest, comic book illustration", min_length=3, max_length=1000)


class PanelOutline(BaseModel):
    panel_number: int = Field(..., ge=1, le=5)
    title: str = Field(..., min_length=1, max_length=120)
    scene_description: str = Field(..., min_length=1, max_length=1000)
    image_prompt: str = Field(..., min_length=1, max_length=1500)


class ComicOutline(BaseModel):
    panels: list[PanelOutline] = Field(..., min_length=5, max_length=5)


class PanelStory(BaseModel):
    panel_number: int = Field(..., ge=1, le=5)
    title: str = Field(..., min_length=1, max_length=120)
    scene_description: str = Field(..., min_length=1, max_length=1000)
    image_prompt: str = Field(..., min_length=1, max_length=1500)
    caption: str = Field(default="", max_length=500)
    narration: str = Field(default="", max_length=1000)
    dialogue: str = Field(default="", max_length=1000)


class ComicStory(BaseModel):
    panels: list[PanelStory] = Field(..., min_length=5, max_length=5)
