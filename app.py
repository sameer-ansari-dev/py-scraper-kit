"""
Upgraded Flask UI for py-scraper-kit.

Features:
- Uses templates/static assets (Bootstrap + custom CSS)
- Shows a loading overlay while the server performs the scrape
- Writes result to a temp file with a UUID-based filename
- Redirects to a result page with a download link and simple metadata
"""
from __future__ import annotations
import tempfile
from pathlib import Path
import uuid

from flask import Flask, request, render_template, send_file, redirect, url_for, flash

from scraper.core import HttpClient, export_rows
from scraper.sites import quotes, books

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "dev-key-for-local-testing"  # replace for production

def _safe_tmp_path(suffix: str) -> Path:
    """Create a temp file path with a short UUID to avoid collisions."""
    name = f"py-scraper-{uuid.uuid4().hex[:8]}{suffix}"
    return Path(tempfile.gettempdir()) / name

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        site = request.form.get("site", "quotes")
        pages = max(1, int(request.form.get("pages") or 1))
        tag = request.form.get("tag") or None
        fmt = request.form.get("format", "csv")
        suffix = ".xlsx" if fmt == "xlsx" else ".csv"

        client = HttpClient(delay=1.0)
        try:
            if site == "quotes":
                rows = quotes.scrape(pages=pages, client=client, tag=tag)
            else:
                rows = books.scrape(pages=pages, client=client)
        except Exception as exc:
            # Keep user-friendly message and log to console for local debugging
            app.logger.exception("Scrape failed")
            flash(f"Scrape failed: {exc}", "danger")
            return render_template("index.html")

        if not rows:
            flash("No results found for the given parameters.", "warning")
            return render_template("index.html")

        out_path = _safe_tmp_path(suffix)
        export_rows(rows, out_path)

        # Redirect to result page with filename and metadata in query params
        return redirect(url_for("result", fname=out_path.name, rows=len(rows), site=site))

    return render_template("index.html")

@app.route("/result/<path:fname>")
def result(fname):
    rows = int(request.args.get("rows", 0))
    site = request.args.get("site", "quotes")
    tmp = Path(tempfile.gettempdir()) / fname
    if not tmp.exists():
        flash("Result file not found (it may have been removed).", "danger")
        return redirect(url_for("index"))
    return render_template("result.html", download_name=tmp.name, rows=rows, site=site)

@app.route("/download/<path:fname>")
def download(fname):
    tmp = Path(tempfile.gettempdir()) / fname
    if not tmp.exists():
        flash("File not available for download.", "danger")
        return redirect(url_for("index"))
    # Serve file as attachment
    return send_file(tmp, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
