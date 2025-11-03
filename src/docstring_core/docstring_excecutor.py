from typing import List, Optional

from src.core_base.executor.executor import execute_in_path

from src.docstring_core.docstring_generator import generate_docstring_from_path_dict
from src.docstring_core.docstring_writer import write_docstrings


def execute_docstring_in_path(
    path: str, model_name: str = "gpt-4o-mini", target_names: Optional[List[str]] = None
):
    """
    Scan a folder (or file) for Python code and automatically generate and update docstrings.

    Args:
        path (str): Path to a Python file or folder to scan.
        model_name (str, optional): Model to use for docstring generation.
    """
    execute_in_path(
        path=path,
        generate_func=generate_docstring_from_path_dict,
        write_func=write_docstrings,
        model_name=model_name,
        item_name="docstrings",
        target_names=target_names,
    )
