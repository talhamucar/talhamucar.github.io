#!/usr/bin/env bash
# Builds a standalone writePostApp executable with PyInstaller.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt

pyinstaller --noconfirm --onedir --name writePostApp \
  --collect-all gradio \
  --collect-all gradio_client \
  --collect-all safehttpx \
  --collect-all groovy \
  app.py

echo "Build complete: dist/writePostApp/writePostApp"
