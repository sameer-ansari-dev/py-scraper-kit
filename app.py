from flask import Flask, request, render_template_string, send_file, flash, url_for, redirect
from pathlib import Path
import tempfile
from scraper.core import HttpClient, export_rows
from scraper.sites import quotes, books

app = Flask(__name__)
app.secret_key = "dev-key"

HTML = """
<h1>py-scraper-kit UI</h1>
<form method="post">
  Site: <select name="site">
    <option value="quotes">quotes</option>
    <option value="books">books</option>
  </select><br>
  Pages: <input name="pages" value="1" type="number"><br>
  Tag (quotes only): <input name="tag"><br>
  Format: <select name="format"><option>csv</option><option>xlsx</option></select><br>
  <button>Scrape</button>
</form>
{% for m in get_flashed_messages() %}
<p>{{m}}</p>
{% endfor %}
{% if link %}
<p><a href="{{link}}">Download result</a></p>
{% endif %}
"""


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        site = request.form["site"]
        pages = int(request.form["pages"])
        tag = request.form.get("tag")
        fmt = request.form["format"]
        suffix = ".xlsx" if fmt == "xlsx" else ".csv"
        tmp = Path(tempfile.gettempdir()) / f"result{suffix}"

        client = HttpClient(delay=1.0)
        data = quotes.scrape(pages, client, tag) if site == "quotes" else books.scrape(pages, client)
        if not data:
            flash("No data found.")
            return render_template_string(HTML)

        export_rows(data, tmp)
        flash(f"Scraped {len(data)} rows.")
        return render_template_string(HTML, link=url_for("download", fname=tmp.name))
    return render_template_string(HTML)


@app.route("/download/<fname>")
def download(fname):
    f = Path(tempfile.gettempdir()) / fname
    if not f.exists():
        flash("File not found.")
        return redirect(url_for("home"))
    return send_file(f, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
