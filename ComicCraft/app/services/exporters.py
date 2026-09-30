from pathlib import Path
from fpdf import FPDF
from PIL import Image
from app.config import settings
from app.models import ComicPanel
from app.utils.files import safe_filename

def _write(pdf: FPDF, text: str) -> None:
    if text:
        pdf.multi_cell(0, 7, text)

def save_pdf(title: str, panels: list[ComicPanel]) -> str:
    filename = safe_filename(title.replace(" ", "_"), ".pdf")
    output_path = settings.exports_dir / filename
    pdf = FPDF("P", "mm", "A4")
    pdf.set_auto_page_break(True, margin=15)

    for index, panel in enumerate(panels):
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        pdf.multi_cell(0, 10, f"Panel {panel.panel_number}: {panel.title}")

        image_file = Path(settings.static_dir) / panel.image_path.removeprefix("/static/")
        if image_file.exists():
            with Image.open(image_file) as img:
                ratio = img.width / img.height
            w, max_h = 180, 110
            h = w / ratio
            if h > max_h:
                h, w = max_h, max_h * ratio
            pdf.image(str(image_file), x=(210 - w) / 2, y=35, w=w, h=h)
            pdf.set_y(35 + h + 8)

        pdf.set_font("Helvetica", "I", 10)
        _write(pdf, panel.scene_description)

        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 7, "Caption")
        pdf.ln()
        pdf.set_font("Helvetica", "", 10)
        _write(pdf, panel.caption)

        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 7, "Narration")
        pdf.ln()
        pdf.set_font("Helvetica", "", 10)
        _write(pdf, panel.narration)

        if panel.dialogue:
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 7, "Dialogue")
            pdf.ln()
            pdf.set_font("Helvetica", "", 10)
            _write(pdf, "\n".join(f"- {line}" for line in panel.dialogue))

        pdf.set_y(-12)
        pdf.set_font("Helvetica", "I", 8)
        pdf.cell(0, 8, f"ComicCraft - Page {index + 1}", align="C")

    pdf.output(str(output_path))
    return f"/exports/{output_path.name}"
