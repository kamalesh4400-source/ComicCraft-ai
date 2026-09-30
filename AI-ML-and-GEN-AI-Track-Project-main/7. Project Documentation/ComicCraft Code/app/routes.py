from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.models import ImageTestRequest, PromptRequest
from app.services.comic_service import comic_service
from app.services.image_generator import generate_image

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.project_root / "templates"))


def render_form(request: Request, error: str | None = None, form_data: dict | None = None):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "error": error,
        "form_data": form_data or {},
        "demo_mode": settings.demo_mode,
    })


@router.get("/")
def home(request: Request):
    return render_form(request)


@router.post("/generate")
def generate_form(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(""),
    setting: str = Form(""),
    tone: str = Form("adventure"),
    art_style: str = Form("comic book"),
):
    form_data = {
        "story_prompt": story_prompt,
        "character_name": character_name,
        "setting": setting,
        "tone": tone,
        "art_style": art_style,
    }
    try:
        data = PromptRequest(**form_data)
        layout, pdf_path = comic_service.generate(**data.model_dump())
        return templates.TemplateResponse("comic_preview.html", {
            "request": request,
            "layout": layout,
            "pdf_url": f"/{pdf_path.lstrip('/')}",
        })
    except Exception as exc:
        return render_form(request, str(exc), form_data)


@router.post("/generate-comic/json")
def generate_json(payload: PromptRequest):
    try:
        layout, pdf_path = comic_service.generate(**payload.model_dump())
        return JSONResponse({"success": True, "layout": layout, "pdf_url": f"/{pdf_path.lstrip('/')}"})
    except Exception as exc:
        return JSONResponse({"success": False, "error": str(exc)}, status_code=500)


@router.post("/test-image")
def test_image(payload: ImageTestRequest):
    try:
        image_path = generate_image(payload.prompt, 1)
        return {"success": True, "image_url": f"/{image_path.lstrip('/')}"}
    except Exception as exc:
        return JSONResponse({"success": False, "error": str(exc)}, status_code=500)


@router.get("/export-success")
def export_success(request: Request):
    return templates.TemplateResponse("export_success.html", {"request": request})


@router.get("/health")
def health():
    return {"status": "ok", "demo_mode": settings.demo_mode, "image_provider": settings.image_provider}


@router.get("/download/{filename}")
def download_pdf(filename: str):
    safe_name = Path(filename).name
    file_path = settings.export_path / safe_name
    if not file_path.exists():
        return JSONResponse({"error": "PDF not found"}, status_code=404)
    return FileResponse(file_path, media_type="application/pdf", filename=safe_name)
