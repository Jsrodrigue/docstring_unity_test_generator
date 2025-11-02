from src.core_base.generate.scanner import scan_folder_and_generate
from src.docstring_core.docstring_manager import generate_docstring_from_path_dict
from src.docstring_core.docstring_writer import write_docstrings

def scan_folder_for_docstrings(path: str, model_name: str = "gpt-4o-mini"):
    """
    Scan a folder (or file) for Python code and automatically generate and update docstrings.

    Args:
        path (str): Path to a Python file or folder to scan.
        model_name (str, optional): Model to use for docstring generation.
    """
    scan_folder_and_generate(
        path=path,
        generate_func=generate_docstring_from_path_dict,
        write_func=write_docstrings,
        model_name=model_name,
        item_name="docstrings"
    )
