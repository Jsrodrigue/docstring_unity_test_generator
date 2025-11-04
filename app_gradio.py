from pathlib import Path
from typing import List, Optional
import gradio as gr
import asyncio

# ============================================================
# 🧩 Imports from your project
# ============================================================
from constants import models
from src.docstring_core.docstring_generator import generate_docstring_from_path_dict
from src.docstring_core.docstring_writer import write_docstrings
from src.unit_test_core.unit_test_generator import generate_unit_test_from_path_dict
from src.unit_test_core.unit_test_writer import write_unit_tests


# ============================================================
# 🧠 Docstring Generation Core
# ============================================================

async def gradio_scan_and_generate(folder_path, model, names="", project_path=None):
    """Scan folder and generate docstrings."""
    target_names = [n.strip() for n in names.split(",")] if names else None

    results: list[dict] = await generate_docstring_from_path_dict(
        folder_path,
        model_name=model,
        target_names=target_names,
        project_path=project_path,
    )

    if not results:
        return "", "", "", 0, [], "❌ No items to process."

    results = [r for r in results if r["docstring"].strip()]
    if not results:
        return "", "", "", 0, [], "❌ No docstrings generated."

    first_item = results[0]
    return (
        first_item.get("original_docstring", ""),
        first_item["docstring"],
        first_item["source"],
        0,
        results,
        f"Item 1/{len(results)}",
    )


def next_item(action: str, edited_text: str, results: list[dict], index: int):
    """Handle Accept / Skip actions and navigate to the next item."""
    if not results or index >= len(results):
        return "", "", "", index, results, "❌ No items to process."

    if action == "Accept":
        item = results[index]
        item["docstring"] = edited_text
        write_docstrings(Path(item["file_path"]), [item])

    next_index = index + 1
    if next_index >= len(results):
        return "", "", "", next_index, results, "✅ All items processed!"

    next_item_data = results[next_index]
    with open(next_item_data["file_path"], "r", encoding="utf-8") as f:
        source_code = next_item_data.get("source", f.read())

    full_source = f"# Path: {next_item_data['file_path']}\n{source_code}"
    return (
        next_item_data.get("original_docstring", ""),
        next_item_data["docstring"],
        full_source,
        next_index,
        results,
        f"Item {next_index + 1}/{len(results)}",
    )


def accept_all(_, results: list[dict], index: int):
    """Accept all remaining docstrings."""
    if not results or index >= len(results):
        return "", "", "", index, results, "❌ No items to process."

    for i in range(index, len(results)):
        item = results[i]
        write_docstrings(Path(item["file_path"]), [item])

    return "", "", "", len(results), results, "✅ All items accepted!"


# ============================================================
# 🧪 Unit Test Generation Core
# ============================================================


async def gradio_generate_unit_tests(folder_path, model, names, project_path):
    """Gradio handler for test generation."""
    if not project_path:
        return "❌ Please provide the project root path (required)."

    target_names = [n.strip() for n in names.split(",")] if names else None

    results = await generate_unit_test_from_path_dict(
        path=folder_path,
        model_name=model,
        target_names=target_names,
        project_path=project_path,
    )

    if not results:
        return "❌ No test cases generated."

    write_unit_tests(results, project_path)
    return f"✅ Generated and wrote {len(results)} test(s) to 'tests/' folder."


# ============================================================
#  UI Tab: Docstring Generator
# ============================================================

def build_docstring_tab():
    """Create the full UI for docstring generation."""
    with gr.Tab(" Docstring Generator"):
        gr.Markdown("### Generate and review Python docstrings")

        with gr.Group():
            with gr.Row():
                folder_input = gr.Textbox(label="Folder path", placeholder="Path to your Python folder")
                project_input = gr.Textbox(label="Project root path", placeholder="Root path (required for tests mirror)")
            with gr.Row():
                model_selector = gr.Dropdown(label="Model", choices=models, value=models[0])
                names_input = gr.Textbox(label="Names (comma-separated)", placeholder="e.g. foo,bar,BazClass")

        scan_btn = gr.Button("🔍 Scan & Generate")

        # Docstring preview/edit
        with gr.Row():
            original_box = gr.Textbox(label="Original Docstring", lines=5)
            suggested_box = gr.Textbox(label="Suggested Docstring (editable)", lines=5)

        # Action buttons
        with gr.Row():
            accept_btn = gr.Button("✅ Accept")
            skip_btn = gr.Button("➡️ Skip")
            accept_all_btn = gr.Button("🚀 Accept All")

        # Status & source
        status_box = gr.Textbox(label="Status", interactive=False)
        source_box = gr.Code(label="Function/Class Source", lines=10)

        # Internal state
        state_results = gr.State()
        state_index = gr.State()

        # Button callbacks
        scan_btn.click(
            fn=gradio_scan_and_generate,
            inputs=[folder_input, model_selector, names_input, project_input],
            outputs=[original_box, suggested_box, source_box, state_index, state_results, status_box],
        )

        accept_btn.click(
            fn=lambda edited, results, idx: next_item("Accept", edited, results, idx),
            inputs=[suggested_box, state_results, state_index],
            outputs=[original_box, suggested_box, source_box, state_index, state_results, status_box],
        )

        skip_btn.click(
            fn=lambda edited, results, idx: next_item("Skip", edited, results, idx),
            inputs=[suggested_box, state_results, state_index],
            outputs=[original_box, suggested_box, source_box, state_index, state_results, status_box],
        )

        accept_all_btn.click(
            fn=accept_all,
            inputs=[suggested_box, state_results, state_index],
            outputs=[original_box, suggested_box, source_box, state_index, state_results, status_box],
        )


# ============================================================
#  UI Tab: Unit Test Generator
# ============================================================

def build_tests_tab():
    """Create the UI for unit test generation."""
    with gr.Tab("Unit Test Generator"):
        gr.Markdown("### Generate pytest-style unit tests from your project")

        with gr.Group():
            with gr.Row():
                folder_input = gr.Textbox(label="Folder path", placeholder="Path to the file or folder to test")
                project_input = gr.Textbox(label="Project root path (required)", placeholder="Root path of your project")
            with gr.Row():
                model_selector = gr.Dropdown(label="Model", choices=models, value=models[3]) # Model recomended
                names_input = gr.Textbox(label="Function/Class names (optional)", placeholder="e.g. foo,bar,BazClass")

        generate_btn = gr.Button("🧪 Generate Tests")
        status_box = gr.Textbox(label="Status", interactive=False, lines=5)

        generate_btn.click(
            fn=lambda folder, model, names, project: asyncio.run(
                gradio_generate_unit_tests(folder, model, names, project)
            ),
            inputs=[folder_input, model_selector, names_input, project_input],
            outputs=status_box,
        )


# ============================================================
# 🚀 Launch Gradio App
# ============================================================

with gr.Blocks() as app:
    gr.Markdown("# 🧠 AI Code Assistant")
    build_docstring_tab()
    build_tests_tab()

if __name__ == "__main__":
    app.launch(inbrowser=True)
