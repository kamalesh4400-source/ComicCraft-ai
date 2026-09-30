from app.models import PromptRequest, ComicResponse
from app.services.exporters import save_pdf
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout

def generate_comic(request: PromptRequest) -> ComicResponse:
    outlines = generate_outline(request)
    stories = generate_story(request, outlines)
    image_paths = [generate_image(panel.image_prompt, panel.panel_number) for panel in outlines]
    layout = build_comic_layout(outlines, stories, image_paths)
    title = f"{request.character_name}'s Comic Adventure"
    pdf_url = save_pdf(title, layout)
    return ComicResponse(title=title, panels=layout, pdf_url=pdf_url)
