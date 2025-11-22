#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Universal Book/Product Catalog Scraper + PDF Generator
Author: (Your Name)

This tool:
 - Learns product URL patterns from 5 sample links
 - Optionally crawls a menu/category page
 - Scrapes titles, authors, descriptions, covers
 - Resumes scraping automatically from cache
 - Optionally generates AI-based short highlights
 - Exports a clean Academic-style PDF catalog

PDFs are generated ONLY after scraping fully completes.
"""

import json
import sys

from engine.autodetect import detect_url_pattern
from engine.scrape import scrape_site
from engine.pdf_generator import generate_all_pdfs
from engine.cache import load_cache
from engine.llm import ask_llm_usage


def ask_yes_no(prompt: str) -> bool:
    """Quick helper for yes/no questions."""
    ans = input(prompt + " (Y/N): ").strip().lower()
    return ans in ("y", "yes")


def get_user_urls():
    """Ask user to enter 5 URLs with validation."""
    print("👉 Enter 5 sample product URLs (one per line):")
    urls = []

    for i in range(5):
        url = input(f"URL {i+1}: ").strip()
        if not url.startswith("http"):
            print("⚠️  Invalid URL, must start with http/https. Try again.")
            return get_user_urls()
        urls.append(url)

    return urls


def main():
    print("\n📘 Universal Book/Product PDF Catalog Builder\n")

    # -------- USER INPUT ----------
    samples = get_user_urls()

    print("\n🔗 Optional menu/start URL")
    print("   Leave blank if your site does not have a category/menu page.")
    menu_url = input("Menu URL (press Enter to skip): ").strip() or None

    # --------- PATTERN DETECTION ----------
    print("\n🧠 Detecting URL pattern from examples...")
    pattern = detect_url_pattern(samples)
    print(f"✔ Detected product link pattern: `{pattern}`")

    # --------- LLM OPTION ----------
    print()
    use_llm = ask_llm_usage()
    if use_llm:
        print("🤖 AI highlights will be generated after scraping.")
    else:
        print("📝 No AI highlights will be added.")

    # --------- SCRAPING ----------
    print("\n🔍 Starting scraping process...")
    print("💾 Resume-safe: if you stop now, you can restart later.\n")

    cache = load_cache()
    scraped = scrape_site(samples, menu_url, pattern, cache, use_llm)

    if not scraped:
        print("\n❌ No products found. Please check your URLs and try again.")
        sys.exit(0)

    print(f"\n📚 Successfully collected data for {len(scraped)} products.")

    # --------- PDF GENERATION ----------
    print("\n🖨️ Generating PDF catalog(s) (after scraping is complete)...")
    generate_all_pdfs(scraped, use_llm)

    print("\n🎉 DONE!")
    print("📂 Check the `output_pdfs/` folder for your PDF file(s).")
    print("💡 Tip: You can now re-run the tool to update the catalog anytime.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⛔ Interrupted by user. You can resume next time (cache saved).")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
