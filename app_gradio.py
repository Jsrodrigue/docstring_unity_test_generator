from pathlib import Path

import gradio as gr

from src.constants import models
from src.core.docstring_scanner import scan_path_for_docstrings
from src.core.docstring_updater import update_docstring


# -----------------------------
# Scan folder and prepare first function for review
# -----------------------------
def gradio_scan(folder_path, model):
    """
    Scan a folder for Python files and return the first function needing a docstring update.
    
    Args:
        folder_path (str): The path to the folder containing Python files.
        model: The model to use for scanning the files.
    
    Returns:
        tuple: A tuple containing the original function, suggested docstring,
               source code, the count, a list of results,
               and a message about the processing status.
    """
    results = scan_path_for_docstrings(folder_path, model=model)

    if not results or "error" in results[0]:
        return (
            "",
            "",
            "",
            0,
            [{"error": f"Folder not found or no Python files: {folder_path}"}],
            "❌ No functions to process.",
        )

    # --- Filter functions with suggestion ---
    results_with_suggestions = [r for r in results if r.get("suggested", "").strip()]
    if not results_with_suggestions:
        return (
            "",
            "",
            "",
            0,
            [{"error": "No functions need docstring updates."}],
            "✅ No functions need updates.",
        )

    first_item = results_with_suggestions[0]
    return (
        first_item["original"],
        first_item["suggested"],
        first_item.get("source", ""),  # full source code
        0,
        results_with_suggestions,
        f"Function 1/{len(results_with_suggestions)}",
    )


# -----------------------------
# Show next function
# -----------------------------
def next_function(action, edited_text, results, index):
    """
    Handle the action of Accept or Skip on a function, apply updates if accepted,
     and return the next function in the list.
    
    Args:
        action (str): The action to perform, either 'Accept' or 'Skip'.
        edited_text (str): The updated docstring text to apply if accepted.
        results (list): The list of function results to process.
        index (int): The current index of the function being processed.
    
    Returns:
        tuple: A tuple containing the original function, suggested docstring,
               source code, the next index, the results list,
               and a message about the processing status.
    """
    if not results or "error" in results[0]:
        return (
            "",
            "",
            "",
            0,
            results,
            results[0].get("error", "No functions to process."),
        )

    if action == "Accept":
        item = results[index]
        if (item["original"] or "").strip() != edited_text.strip():
            update_docstring(
                Path(item["file_abs"]), {"name": item["name"], "docstring": edited_text}
            )
            item["original"] = edited_text  # update locally

    # Move to next function
    next_index = index + 1
    if next_index >= len(results):
        return "", "", "", next_index, results, "✅ All functions processed!"

    next_item = results[next_index]
    return (
        next_item["original"],
        next_item["suggested"],
        next_item.get("source", ""),
        next_index,
        results,
        f"Function {next_index+1}/{len(results)}",
    )


# -----------------------------
# Build Gradio interface
# -----------------------------
with gr.Blocks() as app:
    gr.Markdown("## Python Docstring Scanner & Copilot-style Updater")

    # Folder input
    folder_input = gr.Textbox(
        label="Folder path", placeholder="Enter path to your Python project folder"
    )

    # Model selector
    model_selector = gr.Dropdown(
        label="Select LLM model", choices=models, value=models[0]
    )

    scan_btn = gr.Button("Scan")

    # Docstring review boxes in columns
    with gr.Row():
        original_box = gr.Textbox(label="Original Docstring", lines=5)
        suggested_box = gr.Textbox(label="Suggested Docstring (editable)", lines=5)
    source_box = gr.Code(
        label="Full Function Source", lines=10
    )  # shows the whole function

    # Action buttons
    with gr.Row():
        accept_btn = gr.Button("Accept")
        skip_btn = gr.Button("Skip")

    # Hidden states
    state_results = gr.State()
    state_index = gr.State()
    status_box = gr.Textbox(label="Status", interactive=False)

    # -----------------------------
    # Scan button click
    # -----------------------------
    scan_btn.click(
        fn=gradio_scan,
        inputs=[folder_input, model_selector],
        outputs=[
            original_box,
            suggested_box,
            source_box,
            state_index,
            state_results,
            status_box,
        ],
    )

    # -----------------------------
    # Accept / Skip buttons
    # -----------------------------
    accept_btn.click(
        fn=lambda edited, results, idx: next_function("Accept", edited, results, idx),
        inputs=[suggested_box, state_results, state_index],
        outputs=[
            original_box,
            suggested_box,
            source_box,
            state_index,
            state_results,
            status_box,
        ],
    )

    skip_btn.click(
        fn=lambda edited, results, idx: next_function("Skip", edited, results, idx),
        inputs=[suggested_box, state_results, state_index],
        outputs=[
            original_box,
            suggested_box,
            source_box,
            state_index,
            state_results,
            status_box,
        ],
    )

# -----------------------------
# Launch app
# -----------------------------
if __name__ == "__main__":
    app.launch()