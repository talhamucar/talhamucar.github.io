# Write Post App

A small Gradio app to create new Jekyll blog posts in `_posts`.

## Setup

```bash
cd writePostApp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Then open the printed local URL in your browser. Fill in the title, date,
categories, tags, and paste the post body in Markdown, then click
**Create Post**. The file is saved to `../_posts/<date>-<title-slug>.md`.

## Build a standalone executable

```bash
./build.sh
```

This creates a virtual environment (if needed), installs dependencies, and
runs PyInstaller. The resulting executable is at
`dist/writePostApp/writePostApp`. Run it directly (no Python install
required) and it will serve the app on `http://127.0.0.1:7860`.
