import ast
from pathlib import Path


def compare_and_confirm(func_info, suggested_docstring):
    """
    Displays the original and suggested docstrings for a function and asks for confirmation.
    
    Args:
        func_info (dict): Dictionary containing function information.
        suggested_docstring (str): The suggested docstring.
    
    Returns:
        bool: True if the suggested docstring is accepted, False otherwise.
    """
    print(f"\nFunction: {func_info['name']}")
    print("ORIGINAL DOCSTRING:")
    print(func_info["docstring"] or "(None)")
    print("\nSUGGESTED DOCSTRING:")
    print(suggested_docstring)

    respuesta = input("\nAccept suggested docstring? (y/n): ")
    return respuesta.lower() == "y"


def update_docstring(file_path, func_data):
    """
    Updates or inserts a docstring for a specific function in a Python file.
    
    Args:
        file_path (str | Path): Path to the Python file.
        func_data (dict): Dictionary with function name and new docstring.
    
        func_data:
            - name (str): Function name.
            - docstring (str): New docstring with \n for line breaks.
    """
    file_path = Path(file_path)
    lines = file_path.read_text(encoding="utf-8").splitlines()
    tree = ast.parse("\n".join(lines))

    for node in ast.walk(tree):
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == func_data["name"]
        ):
            if not node.body:
                continue  # skip empty functions

            # --- Compute indentation ---
            func_indent = len(lines[node.lineno - 1]) - len(
                lines[node.lineno - 1].lstrip()
            )
            body_indent = " " * (func_indent + 4)

            # --- Prepare new docstring block ---
            doc_lines = func_data["docstring"].split("\n")
            new_doc_block = (
                [body_indent + '"""']
                + [body_indent + line for line in doc_lines]
                + [body_indent + '"""']
            )

            # --- Replace existing docstring if found ---
            if (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(getattr(node.body[0], "value", None), ast.Constant)
                and isinstance(node.body[0].value.value, str)
            ):
                doc_start_idx = node.body[0].lineno - 1
                doc_end_idx = doc_start_idx + 1
                open_quote = lines[doc_start_idx].strip()[:3]

                while doc_end_idx < len(lines):
                    if lines[doc_end_idx].strip().endswith(open_quote):
                        doc_end_idx += 1
                        break
                    doc_end_idx += 1

                lines[doc_start_idx:doc_end_idx] = new_doc_block

            else:
                # --- Insert docstring at the start of the body ---
                insert_idx = node.body[0].lineno - 1
                lines[insert_idx:insert_idx] = new_doc_block

    # --- Write back to file ---
    file_path.write_text("\n".join(lines), encoding="utf-8")