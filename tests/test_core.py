import pytest
from scraper.core import export_rows, HttpClient

DATA = [{"a": 1, "b": "x"}, {"a": 2, "b": "y"}]


def test_export_csv(tmp_path):
    f = tmp_path / "x.csv"
    export_rows(DATA, f)
    assert f.exists() and f.read_text()


def test_export_xlsx(tmp_path):
    f = tmp_path / "x.xlsx"
    export_rows(DATA, f)
    assert f.exists() and f.stat().st_size > 0


@pytest.mark.network
def test_http_get():
    c = HttpClient(delay=0.1)
    text = c.get("https://quotes.toscrape.com/")
    assert "<html" in text.lower()
