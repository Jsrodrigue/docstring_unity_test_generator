import ast
from pathlib import Path
from typing import List, Dict

def update_docstrings(file_path: Path, items: List[Dict]):
    """
    Update multiple docstrings in a Python file based on minimal dict entries.

    Handles functions, methods, and classes, including empty bodies.

    Args:
        file_path (Path): Path to the Python file to update.
        items (List[Dict]): List of dicts with keys 'name' and 'docstring'.
    """
    lines = file_path.read_text(encoding="utf-8").splitlines()
    tree = ast.parse("\n".join(lines))

    items_map = {item['name']: item for item in items}

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if node.name not in items_map:
            continue

        item = items_map[node.name]

        # Si la función o clase no tiene cuerpo, agregar un pass temporal
        if not node.body:
            insert_idx = node.lineno
            lines.insert(insert_idx, " " * (node.col_offset + 4) + "pass")
            node.body = [None]  # placeholder

        # Indentación correcta: cuerpo de la función/clase
        body_indent = node.body[0].col_offset if hasattr(node.body[0], "col_offset") else node.col_offset + 4
        indent_str = " " * body_indent

        # Construir docstring con la indentación del cuerpo
        doc_lines = item['docstring'].strip().split("\n")
        new_doc_block = [indent_str + '"""'] + [indent_str + line for line in doc_lines] + [indent_str + '"""']

        docstring_exists = ast.get_docstring(node, clean=False) is not None

        if docstring_exists and node.body:
            doc_node = node.body[0]
            start_idx = doc_node.lineno - 1
            end_idx = getattr(getattr(doc_node, "value", None), "end_lineno", start_idx + 1)
            lines[start_idx:end_idx] = new_doc_block
        else:
            insert_idx = node.body[0].lineno - 1 if node.body else node.lineno
            lines[insert_idx:insert_idx] = new_doc_block

    file_path.write_text("\n".join(lines), encoding="utf-8")
