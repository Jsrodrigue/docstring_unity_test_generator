from pathlib import Path
import asyncio
from typing import Callable, List, Dict

# ---------------- Generic folder scanner ----------------
def scan_folder_and_generate(
    path: str,
    generate_func: Callable[[str, str], asyncio.Future],
    write_func: Callable[[Path, List[dict]], None],
    model_name: str = "gpt-4o-mini",
    item_name: str = "items",
):
    """
    Generic function to scan a folder (or file), generate items using a model,
    group them per file, and write them using a provided writer function.

    Args:
        path (str): Path to a Python file or folder to scan.
        generate_func (Callable): Async function with signature (path:str, model_name:str) -> list of dict.
        write_func (Callable): Function with signature (file_path:Path, items:List[dict]) -> None.
        model_name (str, optional): Model to use for generation.
        item_name (str, optional): Friendly name for logging (e.g., 'docstrings', 'unit tests').
    """
    path_obj = Path(path).resolve()
    if not path_obj.exists():
        print(f"[WARNING] The path '{path}' does not exist.")
        return

    print(f"🔍 Scanning {path_obj} for Python files...")

    # Generate items
    results: List[dict] = asyncio.run(generate_func(str(path_obj), model_name))

    if not results:
        print(f"[INFO] No {item_name} were generated.")
        return

    # Group items per file
    grouped: Dict[str, List[dict]] = {}
    for item in results:
        grouped.setdefault(item["file_path"], []).append(item)

    print(f"[INFO] Generating {item_name} for {len(grouped)} files...")

    # Write items
    for file_path, items in grouped.items():
        write_func(Path(file_path), items)
        print(f"[INFO] Updated {item_name} in {file_path}")

    print(f"[INFO] All {item_name} updated successfully!")


