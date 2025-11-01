import ast
from pathlib import Path
from typing import List, Dict

def update_docstrings(file_path: Path, items: List[Dict]):
    """
    Update multiple docstrings in a Python file based on minimal dict entries.
    
    Handles functions, methods, and classes, including nested ones.
    """
    lines = file_path.read_text(encoding="utf-8").splitlines()
    text = "\n".join(lines)
    tree = ast.parse(text)

    items_map = {item["name"]: item for item in items}

    # Ordenamos por línea descendente → evita desplazar índices al insertar
    target_nodes = [
        node for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and node.name in items_map
    ]
    target_nodes.sort(key=lambda n: n.lineno, reverse=True)

    for node in target_nodes:
        item = items_map[node.name]
        docstring = item["docstring"].strip()

        # Indentación correcta (1er nodo del cuerpo o +4 espacios por defecto)
        if node.body:
            first_body_node = node.body[0]
            indent_level = getattr(first_body_node, "col_offset", node.col_offset + 4)
        else:
            indent_level = node.col_offset + 4
            lines.insert(node.lineno, " " * indent_level + "pass")  # garantiza cuerpo

        indent_str = " " * indent_level
        doc_lines = docstring.split("\n")
        new_doc_block = [indent_str + '"""'] + [indent_str + line for line in doc_lines] + [indent_str + '"""']

        existing_doc = ast.get_docstring(node, clean=False)
        if existing_doc:
            # Reemplazar docstring existente
            doc_node = node.body[0]
            start = doc_node.lineno - 1
            end = getattr(getattr(doc_node, "value", None), "end_lineno", start + 1)
            lines[start:end] = new_doc_block
        else:
            # Insertar docstring nuevo después de la definición
            insert_idx = node.body[0].lineno - 1 if node.body else node.lineno
            lines[insert_idx:insert_idx] = new_doc_block

    file_path.write_text("\n".join(lines), encoding="utf-8")
