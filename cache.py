# engine/cache.py

"""
Cache Management
----------------
Stores scraped product data locally in JSON form.

Benefits:
 - Resume scraping safely without starting over
 - If program stops/crashes, progress is preserved
 - Cached data feeds into PDF generation
"""

import json
import os

CACHE_FILE = "cache.json"


def load_cache():
    """Load cache from disk, or return empty dict if missing/corrupted."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_cache(data):
    """Write cache to disk with indentation for readability."""
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[WARN] Could not save cache: {e}")
