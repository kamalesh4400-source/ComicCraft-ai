from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.panels_dir.mkdir(parents=True, exist_ok=True)
    settings.exports_dir.mkdir(parents=True, exist_ok=True)
    yield

app = FastAPI(
    title="ComicCraft API",
    description="AI comic story and illustration generator.",
    version="1.0.0",
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")
app.mount("/exports", StaticFiles(directory=str(settings.exports_dir)), name="exports")
app.include_router(router)
