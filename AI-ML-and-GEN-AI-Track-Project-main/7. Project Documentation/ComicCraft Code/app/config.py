from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_root: Path = Path(__file__).resolve().parent.parent

    gemini_api_key: str = ""
    gemini_outline_model: str = "gemini-3.8-flash"
    gemini_story_model: str = "gemini-3.1-pro-preview"
    hf_token: str = ""

    app_host: str = "127.0.0.1"
    app_port: int = 8000
    log_level: str = "INFO"

    demo_mode: bool = True
    image_provider: str = "diffusers"
    diffusion_model: str = "runwayml/stable-diffusion-v1-5"
    device: str = "auto"
    image_steps: int = 20
    image_width: int = 512
    image_height: int = 512
    image_guidance_scale: float = 7.0

    panel_dir: str = "static/panels"
    export_dir: str = "static/exports"
    max_panels: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def panel_path(self) -> Path:
        return self.project_root / self.panel_dir

    @property
    def export_path(self) -> Path:
        return self.project_root / self.export_dir

    def ensure_directories(self) -> None:
        self.panel_path.mkdir(parents=True, exist_ok=True)
        self.export_path.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_directories()
