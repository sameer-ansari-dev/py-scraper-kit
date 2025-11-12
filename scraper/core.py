"""
Core utilities for py-scraper-kit.
"""
import time
import random
from typing import Iterable, Dict, Optional, List
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import pandas as pd

DEFAULT_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36",
]


class HttpClient:
    """Polite HTTP client with delay and rotating user-agents."""
    def __init__(self, delay: float = 1.0, user_agents: Optional[List[str]] = None, timeout: int = 10):
        self.delay = delay
        self.user_agents = user_agents or DEFAULT_USER_AGENTS
        self.timeout = timeout
        self._last_request = 0.0

    def _wait(self):
        elapsed = time.time() - self._last_request
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)

    def get(self, url: str, **kwargs) -> str:
        self._wait()
        headers = kwargs.pop("headers", {})
        headers["User-Agent"] = random.choice(self.user_agents)
        resp = requests.get(url, headers=headers, timeout=self.timeout, **kwargs)
        self._last_request = time.time()
        resp.raise_for_status()
        return resp.text


def soupify(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def export_rows(rows: Iterable[Dict], path):
    df = pd.DataFrame(rows)
    if str(path).endswith(".csv"):
        df.to_csv(path, index=False)
    elif str(path).endswith(".xlsx"):
        df.to_excel(path, index=False, engine="openpyxl")
    else:
        raise ValueError("Output must be .csv or .xlsx")


def absolute(base: str, link: str) -> str:
    return urljoin(base, link)
