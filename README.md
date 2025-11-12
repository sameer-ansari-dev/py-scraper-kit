# py-scraper-kit

A small, ready-to-run Python web scraper toolkit that includes a CLI, a polite HTTP client, site adapters for demo scraping websites, and an optional Flask web interface.

---

## 🚀 Features
- Command-line scraper (`cli.py`) with:
  - `--site` (`quotes`, `books`)
  - `--pages`
  - `--tag` (for quotes only)
  - `--out` (supports `.csv` or `.xlsx`)
- Polite `HttpClient` (delay + rotating user-agents)
- CSV/Excel export using pandas
- Optional Flask UI for easy scraping
- Unit tests using pytest
- MIT licensed and educationally safe

---

## 🧰 Installation
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
