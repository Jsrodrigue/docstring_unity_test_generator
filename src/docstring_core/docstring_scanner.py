from pathlib import Path
import asyncio
from src.docstring_core.docstring_generator import generate_from_path_dict
from src.docstring_core.docstring_updater import update_docstrings


def scan_folder_for_docstrings(path: str, model_name: str = "gpt-4o-mini"):
    """
    Scan a folder (or file) for Python code and automatically generate and update docstrings.

    Args:
        path (str): Path to a Python file or folder to scan.
        model_name (str, optional): Model to use for docstring generation.
    """
    path_obj = Path(path).resolve()
    if not path_obj.exists():
        print(f"[WARNING] The path '{path}' does not exist.")
        return

    print(f"🔍 Scanning {path_obj} for Python files...")

    # 
    results = asyncio.run(generate_from_path_dict(str(path_obj), model_name=model_name))

    if not results:
        print("[INFO] No docstrings were generated.")
        return

    # Group items per file
    grouped = {}
    for item in results:
        grouped.setdefault(item["file_path"], []).append(item)

    print(f"[INFO] Generating docstrings for {len(grouped)} files...")

    for file_path, items in grouped.items():
        update_docstrings(Path(file_path), items)
        print(f"[INFO] Updated docstrings in {file_path}")

    print("[INFO] All docstrings updated successfully!")
