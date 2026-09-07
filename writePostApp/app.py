"""Gradio app for creating Jekyll (chirpy theme) blog posts."""

import re
from datetime import date
from pathlib import Path

import gradio as gr

POSTS_DIR = Path(__file__).resolve().parent.parent / "_posts"


def slugify(title: str) -> str:
    slug = title.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def parse_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def build_front_matter(title: str, post_date: str, categories: str, tags: str) -> str:
    category_list = parse_list(categories)
    tag_list = parse_list(tags)
    categories_str = ", ".join(category_list)
    tags_str = ", ".join(tag.lower() for tag in tag_list)
    return (
        "---\n"
        f"title: {title}\n"
        f"date: {post_date}\n"
        f"categories: [{categories_str}]\n"
        f"tags: [{tags_str}]     # TAG names should always be lowercase\n"
        "---\n"
    )


def create_post(title: str, post_date: str, categories: str, tags: str, content: str):
    if not title.strip():
        return "Error: Title is required.", gr.update()
    if not post_date.strip():
        return "Error: Date is required.", gr.update()

    slug = slugify(title)
    if not slug:
        return "Error: Title must contain at least one letter or number.", gr.update()

    date_part = post_date.strip().split(" ")[0]
    filename = f"{date_part}-{slug}.md"
    filepath = POSTS_DIR / filename

    if filepath.exists():
        return f"Error: File already exists: {filename}", gr.update()

    front_matter = build_front_matter(title.strip(), post_date.strip(), categories, tags)
    file_content = f"{front_matter}\n{content.strip()}\n"

    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    filepath.write_text(file_content, encoding="utf-8")

    return f"Post created: {filepath.relative_to(POSTS_DIR.parent)}", file_content


with gr.Blocks(title="Jekyll Post Creator") as demo:
    gr.Markdown("# Jekyll Post Creator")
    gr.Markdown(f"Posts will be saved to `{POSTS_DIR}`")

    with gr.Row():
        title_input = gr.Textbox(label="Title", placeholder="CERTIFICATIONS")
        date_input = gr.Textbox(label="Date", value=str(date.today()), placeholder="YYYY-MM-DD HH:MM")

    with gr.Row():
        categories_input = gr.Textbox(label="Categories (comma separated)", placeholder="Cybersecurity")
        tags_input = gr.Textbox(label="Tags (comma separated)", placeholder="certificate")

    content_input = gr.Textbox(
        label="Post Content (Markdown)",
        placeholder="Paste your post body in Markdown format here...",
        lines=20,
    )

    create_button = gr.Button("Create Post", variant="primary")

    status_output = gr.Textbox(label="Status", interactive=False)
    preview_output = gr.Textbox(label="File Preview", interactive=False, lines=15)

    create_button.click(
        fn=create_post,
        inputs=[title_input, date_input, categories_input, tags_input, content_input],
        outputs=[status_output, preview_output],
    )

if __name__ == "__main__":
    demo.launch()
