# AGENTS.md

Website of the **Melzer-Madagaskar-Projekt e.V.**, a small volunteer-run German charity
that supports medical care in southern Madagascar. It is a static site served by GitHub Pages.

## Layout

- `docs/`: the published site. GitHub Pages serves from this folder. The custom domain is set in `docs/CNAME`.
  - `index.html`: a one-page home with these sections: Wer wir sind, `#partner` (slideshow), `#jahresberichte`, `#spenden`, `#kontakt`
  - `jahresberichte/<JAHR>.html`: the annual reports, one page per year
  - `impressum.html`, `datenschutz.html`: legal pages
  - `css/styles.css`: the only stylesheet (CSS variables in `:root`, dark theme)
  - `js/slideshow.js` (partner carousel), `js/clipboard.js` (IBAN copy button)
  - `images/`, with report images in `images/jahresberichte/<JAHR>-<name>.jpg`
- `jahresbericht_template.html`: the template for new annual reports. It is not published.
- `usecases.md`: the content strategy (top 5 use cases and personas)

## Conventions

- No build step, framework or package manager. Write plain HTML, CSS and vanilla JS only.
- All content is in **German** (`lang="de"`).
- Every page has a strict CSP meta tag (`default-src 'self'`). Do not add external fonts, CDNs,
  embeds or trackers. JS goes in files under `docs/js/`, not inline.
- Use relative links. Pages in `jahresberichte/` reference assets through `../`.
- Keep the shared header, nav and footer markup the same on every page.
- The repo stores LF line endings. Windows checkouts may show CRLF (autocrlf). If an edit turns the whole file
  into a diff, normalize the file back to LF. The markup mixes tab and space indentation. Keep the existing style when editing.

## Adding an annual report (Jahresbericht)

1. Copy `jahresbericht_template.html` to `docs/jahresberichte/<JAHR>.html`. Fill in the `[PLACEHOLDERS]`
   and delete the layout variants (A–D) you don't use.
2. Put the images in `docs/images/jahresberichte/` as `<JAHR>-<name>.jpg`, plus a `<JAHR>-teaser.jpg`.
3. Add a `jahresbericht-card` at the top of the grid in `docs/index.html#jahresberichte`.
   Only the 4 newest cards are always visible. Older cards go in the `<details>` block.
4. Update the prev/next links on the neighbouring report. Mark the newest report's "next" link and the oldest report's "prev" link as `disabled`.

## Testing

Serve the site with `python -m http.server -d docs 8765` and open it in a browser. Check the layout on mobile and desktop,
check that the links work, and check the browser console for CSP violations.

For automated checks, use [Playwright](https://playwright.dev/python/) with headless Chromium:

```bash
tools/setup-playwright.sh                        # one-time; safe to re-run. Installs into ~/.venvs/playwright
~/.venvs/playwright/bin/python tools/check_pages.py
```

`check_pages.py` serves `docs/` locally and loads every page. A page fails if it logs a CSP error, leaves the footer
`#year` empty, or requests a local file that 404s. Chrome's warning that `frame-ancestors` is ignored in `<meta>` is
known and harmless, so the check ignores it. Playwright is not a site dependency: never add it to `docs/`.
