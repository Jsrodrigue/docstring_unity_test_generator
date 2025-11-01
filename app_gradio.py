from pathlib import Path
import gradio as gr
from constants import models
from src.docstring_core.docstring_generator import generate_from_path_dict
from src.docstring_core.docstring_updater import update_docstrings

# -----------------------------
# Scan folder and prepare first item for review
# -----------------------------
async def gradio_scan(folder_path, model, names=""):
    target_names = [n.strip() for n in names.split(",")] if names else None

    results: list[dict] = await generate_from_path_dict(
        folder_path,
        model_name=model,
        target_names=target_names
    )
    
    if not results:
        return "", "", "", 0, [], "❌ No items to process."

    # Solo items con docstring generado
    results = [r for r in results if r["docstring"].strip()]
    if not results:
        return "", "", "", 0, [], "❌ No items to process."

    first_item = results[0]

    return (
        first_item.get("original", ""),
        first_item["docstring"],
        first_item["source"],
        0,
        results,
        f"Item 1/{len(results)}",
    )

# -----------------------------
# Show next item
# -----------------------------
def next_item(action: str, edited_text: str, results: list[dict], index: int):
    if not results or index >= len(results):
        return "", "", "", index, results, "❌ No items to process."

    if action == "Accept":
        item = results[index]
        update_docstrings(Path(item["file_path"]), [item])
        item["docstring"] = edited_text

    next_index = index + 1
    if next_index >= len(results):
        return "", "", "", next_index, results, "✅ All items processed!"

    next_item_data = results[next_index]
    with open(next_item_data["file_path"], "r", encoding="utf-8") as f:
        source_code = next_item_data.get("source", f.read())
    full_source = f"# Path: {next_item_data['file_path']}\n{source_code}"

    return (
        next_item_data.get("original", ""),
        next_item_data["docstring"],
        full_source,
        next_index,
        results,
        f"Item {next_index+1}/{len(results)}",
    )

# -----------------------------
# Accept all remaining items
# -----------------------------
def accept_all(_, results: list[dict], index: int):
    if not results or index >= len(results):
        return "", "", "", index, results, "❌ No items to process."

    for i in range(index, len(results)):
        item = results[i]
        update_docstrings(Path(item["file_path"]), [{"name": item["name"], "docstring": item["docstring"]}])

    return "", "", "", len(results), results, "✅ All items accepted!"

# -----------------------------
# Build Gradio interface
# -----------------------------
with gr.Blocks() as app:
    gr.Markdown("## Python Docstring Generator")
    
    # Inputs
    with gr.Row():
        folder_input = gr.Textbox(label="Folder path", placeholder="Enter path to your Python project folder")
        model_selector = gr.Dropdown(label="Select LLM model", choices=models, value=models[0])
        names_input = gr.Textbox(label="Function/Class names (comma-separated)", placeholder="e.g. foo,bar,BazClass")

    scan_btn = gr.Button("Scan")

    # Docstring preview/edit
    with gr.Row():
        original_box = gr.Textbox(label="Original Docstring", lines=5)
        suggested_box = gr.Textbox(label="Suggested Docstring (editable)", lines=5)

    # Action buttons
    with gr.Row():
        accept_btn = gr.Button("Accept")
        skip_btn = gr.Button("Skip")
        accept_all_btn = gr.Button("Accept All")

    # Status & source
    status_box = gr.Textbox(label="Status", interactive=False)
    source_box = gr.Code(label="Function/Class Source", lines=10)

    # Internal state
    state_results = gr.State()
    state_index = gr.State()

    # -----------------------------
    # Button callbacks
    # -----------------------------
    scan_btn.click(
        fn=gradio_scan,
        inputs=[folder_input, model_selector, names_input],
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

if __name__ == "__main__":
    app.launch(inbrowser=True)
