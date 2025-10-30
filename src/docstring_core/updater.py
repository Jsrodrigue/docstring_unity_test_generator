# src/docstring_core/updater.py
import ast
from pathlib import Path
from typing import List
from src.docstring_core.docstring_models import DocstringOutput

def update_docstring(file_path: Path, item: DocstringOutput):
    """
    Update a single docstring in a Python file.
    """
    lines = file_path.read_text(encoding="utf-8").splitlines()
    tree = ast.parse("\n".join(lines))

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == item.name:
            docstring_exists = ast.get_docstring(node, clean=False) is not None
            indent_str = " " * (len(lines[node.body[0].lineno - 1]) - len(lines[node.body[0].lineno - 1].lstrip()) if node.body else 4)
            doc_lines = item.docstring.strip().split("\n")
            new_doc_block = [indent_str + '"""'] + [indent_str + line for line in doc_lines] + [indent_str + '"""']

            if docstring_exists:
                doc_node = node.body[0]
                start_idx = doc_node.lineno - 1
                end_idx = getattr(doc_node.value, "end_lineno", start_idx)
                lines[start_idx:end_idx] = new_doc_block
            else:
                insert_idx = node.body[0].lineno - 1 if node.body else node.lineno
                lines[insert_idx:insert_idx] = new_doc_block

    file_path.write_text("\n".join(lines), encoding="utf-8")

def update_docstrings(file_path: Path, items: List[DocstringOutput]):
    """
    Update multiple docstrings in a Python file.
    """
    for item in items:
        update_docstring(file_path, item)
