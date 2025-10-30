# src/docstring_core/updater.py
import ast
from pathlib import Path
from typing import List
from src.docstring_core.docstring_models import DocstringOutput

def update_docstrings(file_path: Path, items: List[DocstringOutput]):
    """
    Update multiple docstrings in a Python file based on DocstringOutput objects.

    Args:
        file_path (Path): Path to the Python file to update.
        items (List[DocstringOutput]): List of docstring entries to apply.
    """
    lines = file_path.read_text(encoding="utf-8").splitlines()
    tree = ast.parse("\n".join(lines))

    # Crear un diccionario para acceso rápido por nombre
    items_dict = {item.name: item for item in items}

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name in items_dict:
            item = items_dict[node.name]

            # Comprobar si ya hay docstring
            docstring_exists = ast.get_docstring(node, clean=False) is not None

            # Calcular indentación
            if node.body:
                first_line = lines[node.body[0].lineno - 1]
                body_indent = len(first_line) - len(first_line.lstrip())
                indent_str = " " * body_indent
            else:
                # Función vacía
                body_indent = 4
                indent_str = " " * body_indent
                lines.insert(node.lineno, indent_str + "pass")

            # Construir bloque de docstring
            doc_lines = item.docstring.strip().split("\n")
            new_doc_block = [indent_str + '"""'] + [indent_str + line for line in doc_lines] + [indent_str + '"""']

            if docstring_exists:
                doc_node = node.body[0]
                doc_start_idx = doc_node.lineno - 1
                doc_end_idx = getattr(doc_node.value, "end_lineno", doc_start_idx)
                lines[doc_start_idx:doc_end_idx] = new_doc_block
            else:
                insert_idx = node.body[0].lineno - 1 if node.body else node.lineno
                lines[insert_idx:insert_idx] = new_doc_block

    file_path.write_text("\n".join(lines), encoding="utf-8")
