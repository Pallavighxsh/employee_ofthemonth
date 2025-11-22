# engine/utils.py

"""
Data Extraction Helpers
-----------------------
Extracts title, author, description, and image from product pages.

These functions use simple heuristics so the scraper works across
different websites without needing custom CSS selectors.
"""

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from engine.llm import summarize_description


def extract_details(url, session, use_llm):
    """
    Fetch a product page and extract core details:
      - title
      - author (if detectable)
      - description
      - image
      - url
      - optional summary (AI highlight if enabled)
    """
    resp = session.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # ----- TITLE -----
    title_el = soup.find("h1") or soup.find("h2") or soup.title
    title = title_el.get_text(strip=True) if title_el else "Untitled"

    # ----- AUTHOR -----
    author = ""
    # naive but works across many academic catalog pages
    for tag in soup.find_all(text=True):
        txt = str(tag).strip()
        if txt.lower().startswith("author") or txt.lower().startswith("by "):
            author = txt
            break

    # ----- DESCRIPTION -----
    paragraphs = soup.find_all("p")
    if paragraphs:
        # choose the longest paragraph as the likely book description
        description = max(paragraphs, key=lambda p: len(p.get_text(strip=True))).get_text(strip=True)
    else:
        description = ""

    # ----- IMAGE -----
    img = soup.find("img")
    image_url = urljoin(url, img["src"]) if img and img.get("src") else None

    # ----- OPTIONAL AI SUMMARY -----
    highlight = summarize_description(description) if use_llm and description else ""

    return {
        "url": url,
        "title": title,
        "author": author,
        "description": description,
        "image": image_url,
        "highlight": highlight,
    }
