import ast

def extract_functions(file_path):
    """
    Reads a python file and extract all the functions.

    Args:
    file_path: path of the .py file

    Returns a list of dictionaries with the info in the format:
    {
        'name': name of function,
        'args': list of arguments,
        'docstring': text of docstring or None,
        'source': full source code of the cunction
    }
    """
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    # Parse the code into an Abstract Syntax Tree (AST)
    tree = ast.parse(code)

    funcs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Extract data of each function
            func_info = {
                "name": node.name,
                "args": [arg.arg for arg in node.args.args],
                "docstring": ast.get_docstring(node),
                "source": ast.get_source_segment(code, node)
            }
            funcs.append(func_info)

    return funcs


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: python src/parser.py <archivo.py>")
        sys.exit(1)

    file_path = sys.argv[1]
    functions = extract_functions(file_path)

    if not functions:
        print("⚠️ No functions found in the file.")
    else:
        for func in functions:
            print(f"\n🔹 Function: {func['name']}")
            print(f"   Arguments: {func['args']}")
            print(f"   Docstring: {func['docstring']}")
            print("-" * 50)
