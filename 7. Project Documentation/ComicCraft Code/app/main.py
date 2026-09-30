from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routes import router

settings.ensure_directories()

app = FastAPI(
    title="ComicCraft API",
    description="AI comic story creator using Gemini and Stable Diffusion.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=str(settings.project_root / "static")), name="static")
app.include_router(router)
