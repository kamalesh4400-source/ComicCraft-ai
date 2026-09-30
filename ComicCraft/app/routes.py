from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import settings
from app.models import ImageTestRequest, PromptRequest
from app.services.comic_service import generate_comic
from app.services.image_generator import generate_image

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"title": settings.app_name})

@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    form = {
        "story_prompt": story_prompt, "character_name": character_name,
        "setting": setting, "tone": tone, "art_style": art_style,
    }
    try:
        comic = generate_comic(PromptRequest(**form))
        return templates.TemplateResponse(request=request, name="comic_preview.html", context={"comic": comic})
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"title": settings.app_name, "error": str(exc), "form": form},
            status_code=500,
        )

@router.post("/generate-comic/json")
async def generate_comic_json(payload: PromptRequest):
    try:
        return generate_comic(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@router.post("/test-image")
async def test_image(payload: ImageTestRequest):
    try:
        return {"success": True, "image_path": generate_image(payload.prompt, 0)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf_url: str = "/"):
    return templates.TemplateResponse(request=request, name="export_success.html", context={"pdf_url": pdf_url})

@router.get("/health")
async def health():
    return {"status": "ok", "service": settings.app_name, "mock_ai": settings.mock_ai, "image_provider": settings.image_provider}
