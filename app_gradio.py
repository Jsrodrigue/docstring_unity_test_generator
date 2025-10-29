from pathlib import Path
import gradio as gr
from src.constants import models
from src.docstring_core.docstring_scanner import scan_path_for_docstrings
from src.docstring_core.docstring_updater import update_docstring
from src.docstring_core.docstring_class import DocstringOutput

# -----------------------------
# Scan folder and prepare first item for review
# -----------------------------
async def gradio_scan(folder_path, model):
    results: list[DocstringOutput] = await scan_path_for_docstrings(folder_path, model=model)

    if not results:
        return "", "", "", 0, [], "❌ No items to process."

    results = [r for r in results if r.docstring and r.docstring != r.original]
    if not results:
        return "", "", "", 0, [], "❌ No items to process."

    first_item = results[0]
    full_source = f"# Path: {first_item.file_abs}\n{first_item.source}"
    return (
        first_item.original,
        first_item.docstring,
        full_source,
        0,
        results,
        f"Item 1/{len(results)}",
    )

# -----------------------------
# Show next item
# -----------------------------
def next_item(action: str, edited_text: str, results: list[DocstringOutput], index: int):
    if not results:
        return "", "", "", 0, results, "❌ No items to process."

    if action == "Accept":
        item: DocstringOutput = results[index]
        if (item.original or "").strip() != edited_text.strip():
            item.docstring = edited_text
            update_docstring(Path(item.file_abs), item)
            item.original = edited_text

    # Move to next item
    next_index = index + 1
    if next_index >= len(results):
        return "", "", "", next_index, results, "✅ All items processed!"

    next_item_data = results[next_index]
    full_source = f"# Path: {next_item_data.file_abs}\n{next_item_data.source}"
    return (
        next_item_data.original,
        next_item_data.docstring,
        full_source,
        next_index,
        results,
        f"Item {next_index+1}/{len(results)}",
    )

# -----------------------------
# Accept all remaining items
# -----------------------------
def accept_all(edited_text, results: list[DocstringOutput], index: int):
    if not results or index >= len(results):
        return "", "", "", index, results, "❌ No items to process."

    for i in range(index, len(results)):
        item = results[i]
        if (item.original or "").strip() != item.docstring.strip():
            update_docstring(Path(item.file_abs), item)
            item.original = item.docstring

    return "", "", "", len(results), results, "✅ All items accepted!"

# -----------------------------
# Build Gradio interface
# -----------------------------
with gr.Blocks() as app:
    gr.Markdown("## Python Docstring Generator")
    with gr.Row():
        folder_input = gr.Textbox(label="Folder path", placeholder="Enter path to your Python project folder")
        model_selector = gr.Dropdown(label="Select LLM model", choices=models, value=models[0])
    
    scan_btn = gr.Button("Scan")

    with gr.Row():
        original_box = gr.Textbox(label="Original Docstring", lines=5)
        suggested_box = gr.Textbox(label="Suggested Docstring (editable)", lines=5)

    with gr.Row():
        accept_btn = gr.Button("Accept")
        skip_btn = gr.Button("Skip")
        accept_all_btn = gr.Button("Accept All")
    
    status_box = gr.Textbox(label="Status", interactive=False)
    source_box = gr.Code(label="Full Source", lines=10)

    state_results = gr.State()
    state_index = gr.State()

    # -----------------------------
    # Button callbacks
    # -----------------------------
    scan_btn.click(
        fn=gradio_scan,
        inputs=[folder_input, model_selector],
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

# Launch app
if __name__ == "__main__":
    app.launch(inbrowser=True)
