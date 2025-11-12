#!/usr/bin/env python3
"""
CLI entrypoint for py-scraper-kit.
"""
import argparse
import sys
from pathlib import Path
from scraper.core import HttpClient, export_rows
from scraper.sites import quotes, books

ADAPTERS = {"quotes": quotes, "books": books}


def main(argv=None):
    parser = argparse.ArgumentParser(description="py-scraper-kit CLI")
    parser.add_argument("--site", required=True, choices=ADAPTERS.keys())
    parser.add_argument("--pages", type=int, default=1)
    parser.add_argument("--tag", type=str, default=None)
    parser.add_argument("--out", required=True, type=Path)

    args = parser.parse_args(argv)
    out_path = args.out

    if out_path.suffix.lower() not in (".csv", ".xlsx"):
        print("Error: --out must end with .csv or .xlsx", file=sys.stderr)
        sys.exit(2)

    client = HttpClient(delay=1.0)
    adapter = ADAPTERS[args.site]

    print(f"Scraping {args.site} ({args.pages} pages)...")

    if args.site == "quotes":
        rows = adapter.scrape(pages=args.pages, client=client, tag=args.tag)
    else:
        rows = adapter.scrape(pages=args.pages, client=client)

    if not rows:
        print("No data found.")
        sys.exit(0)

    export_rows(rows, out_path)
    print(f"✅ Done! Wrote {len(rows)} rows to {out_path}")


if __name__ == "__main__":
    main()
