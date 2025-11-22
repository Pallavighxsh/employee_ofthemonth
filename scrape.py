# engine/scrape.py

"""
Scraping Logic
--------------
- Uses a detected URL pattern to find product links automatically.
- Fetches product details (title, author, description, image).
- Saves progress to cache so scraping can resume later.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from engine.cache import save_cache
from engine.utils import extract_details


def discover_links(start_url, pattern, session):
    """
    Discover product links from a menu/category page.
    Returns a set of URLs that match the product URL pattern.
    """
    try:
        resp = session.get(start_url, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        print(f"[WARN] Could not fetch menu page {start_url}: {e}")
        return set()

    links = set()
    for a in soup.find_all("a", href=True):
        href = urljoin(start_url, a["href"])
        if pattern in href:
            links.add(href)
    return links


def scrape_site(samples, menu_url, pattern, cache, use_llm):
    """
    Main scraping function:
      - Uses sample URLs + discovered menu links
      - Respects cache (resume scraping)
      - Returns list of product dictionaries
    """
    session = requests.Session()

    # Always include the 5 user-provided URLs
    discovered = set(samples)

    # If user provided a menu URL, discover more links:
    if menu_url:
        print(f"🌐 Scanning menu page for more product links...")
        discovered |= discover_links(menu_url, pattern, session)
        print(f"🔎 Found {len(discovered)} product URLs so far.\n")

    results = []
    visited = set(cache.keys())

    for url in list(discovered):
        if url in visited:
            # Use cached record
            results.append(cache[url])
            continue

        print(f"📘 Scraping: {url}")
        try:
            data = extract_details(url, session, use_llm)
            cache[url] = data
            save_cache(cache)
            results.append(data)
        except Exception as e:
            print(f"[ERROR] Skipping {url}: {e}")

    return results
