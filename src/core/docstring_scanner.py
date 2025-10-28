from pathlib import Path

from src.constants import PROMPT_TEMPLATE, SYSTEM_PROMPT
from src.core.docstring_generator import generate_docstrings
from src.utils.ast_utils import extract_functions


def scan_path_for_docstrings(path: str, model):
    """
    Scan a directory or file path for Python files and extract
    existing docstrings. Suggest replacements based on generated
    ones from a specified model.
    
    Args:
        path (str): The file or directory path to scan for Python files.
        model: The model used for generating suggested docstrings.
    
    Returns:
        list: A list of dictionaries containing information about the
               scanned files, including the original and suggested
    docstrings, and any errors encountered during the scan.
    """
    path_obj = Path(path).resolve()
    if not path_obj.exists():
        return [{"file": None, "file_abs": None, "error": f"Path not found: {path}"}]

    py_files = [path_obj] if path_obj.is_file() and path_obj.suffix == ".py" else list(path_obj.rglob("*.py"))
    if not py_files:
        return [{"file": None, "file_abs": None, "error": "No Python files found."}]

    all_results = []
    for file_path in py_files:
        functions = extract_functions(file_path)
        generated = generate_docstrings(functions=functions, prompt_base=PROMPT_TEMPLATE, system_prompt=SYSTEM_PROMPT, model=model)
        for func_info in functions:
            match = next((g for g in generated if g["name"] == func_info["name"]), None)
            suggested_docstring = match["docstring"] if match else ""
            if (func_info["docstring"] or "").strip() == suggested_docstring.strip():
                continue
            all_results.append({
                "file": str(file_path.relative_to(path_obj.parent)) if file_path.is_file() else str(file_path.relative_to(path_obj)),
                "file_abs": str(file_path),
                "name": func_info["name"],
                "source": func_info["source"],
                "original": func_info["docstring"] or "",
                "suggested": suggested_docstring,
            })
    return all_results