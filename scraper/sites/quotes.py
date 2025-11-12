"""
Adapter for https://quotes.toscrape.com
"""
from typing import List, Dict, Optional
from scraper.core import HttpClient, soupify

BASE = "https://quotes.toscrape.com/"


def build_url(page: int = 1, tag: Optional[str] = None) -> str:
    if tag:
        return f"{BASE}tag/{tag}/page/{page}/" if page > 1 else f"{BASE}tag/{tag}/"
    return f"{BASE}page/{page}/" if page > 1 else BASE


def parse_page(html: str) -> List[Dict]:
    soup = soupify(html)
    data = []
    for q in soup.select(".quote"):
        text = q.select_one(".text").get_text(strip=True)
        author = q.select_one(".author").get_text(strip=True)
        tags = ", ".join([t.get_text(strip=True) for t in q.select(".tag")])
        data.append({"text": text, "author": author, "tags": tags})
    return data


def scrape(pages: int = 1, client: HttpClient = None, tag: Optional[str] = None) -> List[Dict]:
    client = client or HttpClient()
    results = []
    for p in range(1, pages + 1):
        url = build_url(page=p, tag=tag)
        html = client.get(url)
        page_data = parse_page(html)
        if not page_data:
            break
        results.extend(page_data)
    return results
