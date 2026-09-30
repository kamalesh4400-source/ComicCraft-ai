from datetime import datetime
from pathlib import Path
import re

from fpdf import FPDF

from app.config import settings


def _clean_pdf_text(value: str) -> str:
    replacements = {
        "—": "-", "–": "-", "“": '"', "”": '"', "‘": "'", "’": "'", "…": "...", "•": "-",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value.encode("latin-1", "replace").decode("latin-1")


class ComicPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", size=8)
        self.cell(0, 10, f"ComicCraft - Page {self.page_no()}", align="C")


def save_pdf(layout: list[dict]) -> str:
    pdf = ComicPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 20)
        pdf.set_x(15)
        pdf.multi_cell(180, 12, _clean_pdf_text(f"Panel {panel['panel_number']}: {panel['title']}"), align="C")
        pdf.ln(4)

        image_rel = panel["image_path"].replace("\\", "/").lstrip("/")
        image_path = settings.project_root / image_rel
        if not image_path.exists():
            raise FileNotFoundError(f"Panel image not found: {image_path}")
        pdf.image(str(image_path), x=15, w=180)
        pdf.ln(6)

        sections = [
            ("Scene", panel.get("scene_description", "")),
            ("Caption", panel.get("caption", "")),
            ("Narration", panel.get("narration", "")),
            ("Dialogue", panel.get("dialogue", "")),
        ]
        for heading, text in sections:
            pdf.set_x(15)
            if text:
                pdf.set_font("Helvetica", "B", 11)
                pdf.multi_cell(180, 7, _clean_pdf_text(heading))
                pdf.set_font("Helvetica", size=10)
                pdf.multi_cell(180, 6, _clean_pdf_text(text))
                pdf.ln(2)

    filename = datetime.now().strftime("comiccraft_%Y%m%d_%H%M%S_%f.pdf")
    output = settings.export_path / filename
    pdf.output(str(output))
    return f"{settings.export_dir.replace(chr(92), '/')}/{filename}"
