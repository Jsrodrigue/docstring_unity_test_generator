import ast
from pathlib import Path
from src.docstring_core.docstring_class import DocstringOutput

def update_docstring(file_path: Path, item: DocstringOutput):
    lines = file_path.read_text(encoding="utf-8").splitlines()
    tree = ast.parse("\n".join(lines))

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == item.name:
            docstring_exists = ast.get_docstring(node, clean=False) is not None

            # Calcular indentación del cuerpo
            if node.body:
                first_line = lines[node.body[0].lineno - 1]
                body_indent = len(first_line) - len(first_line.lstrip())
                indent_str = " " * body_indent
            else:
                # Función vacía
                body_indent = 4
                indent_str = " " * body_indent
                lines.insert(node.lineno, indent_str + "pass")

            # Construir nuevo docstring
            doc_lines = item.docstring.strip().split("\n")
            new_doc_block = [indent_str + '"""'] + [indent_str + line for line in doc_lines] + [indent_str + '"""']

            if docstring_exists:
                doc_node = node.body[0]
                # end_lineno da la línea final del docstring
                doc_start_idx = doc_node.lineno - 1
                doc_end_idx = getattr(doc_node.value, "end_lineno", doc_start_idx)  # Python 3.8+
                lines[doc_start_idx:doc_end_idx] = new_doc_block
            else:
                insert_idx = node.body[0].lineno - 1 if node.body else node.lineno
                lines[insert_idx:insert_idx] = new_doc_block

    file_path.write_text("\n".join(lines), encoding="utf-8")
