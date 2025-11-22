# engine/pdf_generator.py

"""
PDF Generator (Academic Style A)
--------------------------------
Generates a clean, single-column academic-style catalog PDF.

- Shows title, author, description, image, and URL
- Respects resume-scraping workflow (only runs after scrape completes)
- Stores PDFs in `output_pdfs/` folder
"""

import os
import requests
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from PIL import Image as PILImage


OUTPUT_DIR = "output_pdfs"
IMG_DIR = "images"


def _download_image(url):
    """Download a product image if not already downloaded."""
    if not url:
        return None

    os.makedirs(IMG_DIR, exist_ok=True)
    fname = os.path.join(IMG_DIR, os.path.basename(url.split("?")[0]))

    try:
        if not os.path.exists(fname):
            with open(fname, "wb") as f:
                f.write(requests.get(url, timeout=10).content)
        return fname
    except Exception:
        return None


def generate_all_pdfs(books, use_llm):
    """
    Create a single academic-style catalog PDF
    containing all product entries.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUTPUT_DIR, "catalog.pdf")

    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "title",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        spaceAfter=12,
    )

    text_style = styles["Normal"]
    url_style = ParagraphStyle(
        "url_style",
        parent=text_style,
        fontSize=8,
    )

    elems = []

    # Catalog heading
    elems.append(Paragraph("Product Catalog", title_style))
    elems.append(Spacer(1, 0.3 * inch))

    for b in books:
        # Title
        elems.append(Paragraph(f"<b>{b.get('title','').strip()}</b>", styles["Heading3"]))

        # Author if found
        if b.get("author"):
            elems.append(Paragraph(b.get("author", ""), text_style))
        elems.append(Spacer(1, 0.05 * inch))

        # Image (small academic styling)
        img_path = _download_image(b.get("image"))
        if img_path:
            try:
                with PILImage.open(img_path) as _:
                    elems.append(Image(img_path, width=1.1 * inch, height=1.5 * inch))
                    elems.append(Spacer(1, 0.05 * inch))
            except Exception:
                pass

        # Description
        desc = b.get("description", "").strip()
        if desc:
            elems.append(Paragraph(desc, text_style))
            elems.append(Spacer(1, 0.05 * inch))

        # URL (small, academic)
        elems.append(Paragraph(f"<font size=8>{b.get('url')}</font>", url_style))
        elems.append(Spacer(1, 0.25 * inch))

    doc.build(elems)

    print(f"📄 PDF created: {pdf_path}")
