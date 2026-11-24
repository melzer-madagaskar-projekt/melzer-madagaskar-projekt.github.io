"""Smoke test for the static site: serves docs/ locally and checks every page in headless Chromium.

Fails if a page logs a Content Security Policy error, has an empty footer year, or loads a local asset that 404s.
Setup: tools/setup-playwright.sh  -  Run: ~/.venvs/playwright/bin/python tools/check_pages.py
"""
import functools
import http.server
import pathlib
import sys
import threading

from playwright.sync_api import sync_playwright

DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"
IGNORED = ("'frame-ancestors' is ignored when delivered via a <meta> element",)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main() -> int:
    handler = functools.partial(QuietHandler, directory=str(DOCS))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}/"

    pages = sorted(p.relative_to(DOCS).as_posix() for p in DOCS.rglob("*.html"))
    failures = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for path in pages:
            page = browser.new_page()
            errors = []
            page.on("console", lambda m: "Content Security Policy" in m.text
                    and not any(i in m.text for i in IGNORED) and errors.append(f"CSP: {m.text[:200]}"))
            page.on("response", lambda r: r.url.startswith(base) and r.status >= 400
                    and errors.append(f"{r.status}: {r.url[len(base):]}"))
            page.goto(base + path, wait_until="load")
            year = page.locator("#year")
            if year.count() and not (year.text_content() or "").strip():
                errors.append("footer #year is empty")
            status = "FAIL" if errors else "ok"
            print(f"{status:4} {path}")
            for e in errors:
                print(f"     {e}")
            failures += bool(errors)
            page.close()
        browser.close()
    server.shutdown()
    print(f"\n{len(pages) - failures}/{len(pages)} pages ok")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
