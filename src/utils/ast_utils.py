import ast
from pathlib import Path
from typing import List, Dict

def process_node(node, source_lines):
    """
    Processes an AST node representing a function or class and returns a dictionary containing relevant information.
    
    Args:
        node (ast.AST): Node of type FunctionDef, AsyncFunctionDef, or ClassDef.
        source_lines (list[str]): List of source code lines in the Python file.
    
    Returns:
        dict: Dictionary with keys 'name' (str), 'type' (str), 'source' (str), and 'docstring' (str).
    """
    start = node.lineno - 1
    end = getattr(node, "end_lineno", None)
    code_text = "\n".join(source_lines[start:end])

    node_type = "class" if isinstance(node, ast.ClassDef) else "function"
    docstring = ast.get_docstring(node)

    return {
        "name": node.name,
        "type": node_type,
        "source": code_text,
        "docstring": docstring,
    }




def extract_functions_and_classes(file_path: Path) -> List[Dict[str, str]]:
    """
    Extracts functions and classes from a Python file, including their
    existing docstrings and source code.
    
    Args:
        file_path (Path): Path to the Python file to analyze.
    
    Returns:
        List[Dict[str, str]]: A list of dictionaries, where each dictionary
        contains:
            - 'name': The name of the function or class.
            - 'docstring': The existing docstring or an empty string.
            - 'source': The full source code of the function or class.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    tree = ast.parse(source_code)
    results = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            # Extract name
            name = node.name
            # Extract docstring
            docstring = ast.get_docstring(node) or ""
            # Extract source code (approximate)
            try:
                # ast nodes have lineno and end_lineno attributes (Python 3.8+)
                start_line = node.lineno - 1  # line numbers are 1-based
                end_line = node.end_lineno
                source_lines = source_code.splitlines()[start_line:end_line]
                source = "\n".join(source_lines)
            except AttributeError:
                # fallback if end_lineno not available
                source = ""  # could use astunparse if you want full source
            results.append({
                "name": name,
                "docstring": docstring,
                "source": source
            })

    return results