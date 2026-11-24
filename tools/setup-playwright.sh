#!/usr/bin/env bash
# Sets up Playwright + headless Chromium for tools/check_pages.py.
# Safe to re-run: skips steps that are already done.
# Installs outside the repo: venv in ~/.venvs/playwright, browsers in ~/.cache/ms-playwright.
set -euo pipefail

VENV="${PLAYWRIGHT_VENV:-$HOME/.venvs/playwright}"

# libatomic1 is needed by Playwright's bundled Node driver on Debian slim images.
if ! dpkg -s libatomic1 >/dev/null 2>&1; then
  sudo apt-get update -qq
  sudo apt-get install -y -qq libatomic1
fi

if [ ! -x "$VENV/bin/python" ]; then
  uv venv -q "$VENV"
fi
if ! "$VENV/bin/python" -c "import playwright" 2>/dev/null; then
  uv pip install -q -p "$VENV/bin/python" playwright
fi

# --with-deps installs Chromium's system libraries via apt (needs sudo).
"$VENV/bin/python" -m playwright install --with-deps chromium

echo "Playwright ready: $VENV/bin/python tools/check_pages.py"
