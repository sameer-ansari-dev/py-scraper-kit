"""
Adapter for http://books.toscrape.com
"""
from typing import List, Dict
from scraper.core import HttpClient, soupify, absolute

BASE = "http://books.toscrape.com/"


def build_url(page: int = 1) -> str:
    return BASE if page == 1 else f"{BASE}catalogue/page-{page}.html"


def parse_page(html: str) -> List[Dict]:
    soup = soupify(html)
    books = []
    for el in soup.select("article.product_pod"):
        title = el.select_one("h3 a")["title"]
        price = el.select_one(".price_color").get_text(strip=True)
        availability = el.select_one(".availability").get_text(strip=True)
        link = absolute(BASE, el.select_one("h3 a")["href"])
        books.append({"title": title, "price": price, "availability": availability, "link": link})
    return books


def scrape(pages: int = 1, client: HttpClient = None) -> List[Dict]:
    client = client or HttpClient()
    data = []
    for p in range(1, pages + 1):
        url = build_url(page=p)
        html = client.get(url)
        rows = parse_page(html)
        if not rows:
            break
        data.extend(rows)
    return data
