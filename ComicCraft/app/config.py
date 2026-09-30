from pathlib import Path

from pydantic import Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "ComicCraft"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    log_level: str = "INFO"

    gemini_api_key: str = Field(
        default="",
        validation_alias=AliasChoices("GEMINI_API_KEY"),
    )
    gemini_outline_model: str = Field(
        default="gemini-2.5-flash",
        validation_alias=AliasChoices("GEMINI_OUTLINE_MODEL"),
    )
    gemini_story_model: str = Field(
        default="gemini-2.5-pro",
        validation_alias=AliasChoices("GEMINI_STORY_MODEL"),
    )

    hf_api_key: str = Field(
        default="",
        validation_alias=AliasChoices(
            "HF_API_KEY", "HF_TOKEN"
        ),
    )
    diffusion_model_id: str = Field(
        default="stable-diffusion-v1-5/stable-diffusion-v1-5",
        validation_alias=AliasChoices(
            "DIFFUSION_MODEL_ID", "DIFFUSION_MODEL"
        ),
    )
    image_provider: str = "diffusers"
    mock_ai: bool = Field(
        default=False,
        validation_alias=AliasChoices(
            "MOCK_AI", "DEMO_MODE"
        ),
    )

    device: str = "auto"

    num_panels: int = Field(
        default=5,
        validation_alias=AliasChoices(
            "NUM_PANELS", "MAX_PANELS"
        ),
    )
    image_width: int = 512
    image_height: int = 512
    image_steps: int = 20
    image_guidance_scale: float = 7.5

    static_dir: Path = BASE_DIR / "static"
    templates_dir: Path = BASE_DIR / "templates"

    panels_dir: Path = Field(
        default=BASE_DIR / "static" / "panels"
    )
    exports_dir: Path = Field(
        default=BASE_DIR / "exports"
    )

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()

# Resolve relative directories from the project root.
if not settings.panels_dir.is_absolute():
    settings.panels_dir = BASE_DIR / settings.panels_dir

if not settings.exports_dir.is_absolute():
    settings.exports_dir = BASE_DIR / settings.exports_dir

settings.panels_dir.mkdir(parents=True, exist_ok=True)
settings.exports_dir.mkdir(parents=True, exist_ok=True)
