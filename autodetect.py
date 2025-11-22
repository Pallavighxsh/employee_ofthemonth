# engine/autodetect.py

"""
URL Pattern Auto-Detection
--------------------------
Given a list of example product URLs, this module extracts the stable prefix
that uniquely identifies product pages on a website.

Example:
    Input URLs:
        https://site.com/books/BookDetail/978123456/
        https://site.com/books/BookDetail/978555555/
    Output:
        /books/BookDetail/

This prefix is later used to detect and follow similar links across the site.
"""

from urllib.parse import urlparse


def common_prefix(strings):
    """Return the longest shared prefix of all strings."""
    if not strings:
        return ""
    s1, s2 = min(strings), max(strings)
    for i, c in enumerate(s1):
        if c != s2[i]:
            return s1[:i]
    return s1


def detect_url_pattern(urls):
    """
    Detect a reusable URL pattern from a list of full product URLs.
    Returns a prefix path without the domain, like /Books/BookDetail

    This allows scraping of ANY site where product pages follow a consistent format.
    """
    parsed_paths = [urlparse(u).path for u in urls]
    prefix = common_prefix(parsed_paths)
    return prefix.rstrip("/")  # clean trailing slash
