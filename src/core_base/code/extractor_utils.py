import re
import ast

def extract_symbols_from_import(import_line: str) -> list[str]:
    """
    Extract imported symbol names from an import line.
    Example:
        'from module import A, B' -> ['A', 'B']
        'import x, y' -> ['x', 'y']
    """
    from_match = re.match(r"from\s+[^\s]+\s+import\s+(.+)", import_line)
    if from_match:
        names_part = from_match.group(1)
    else:
        import_match = re.match(r"import\s+(.+)", import_line)
        names_part = import_match.group(1) if import_match else ""
    names = [n.strip().split(" as ")[0] for n in names_part.split(",") if n.strip()]
    return names

def _get_signature_from_node(node: ast.AST) -> str:
    """
    Build a human-readable function or class signature from the AST node.

    Examples:
        def add(a, b)        -> "add(a, b)"
        class MyClass(Base)  -> "class MyClass(Base)"
    """
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        args = []

        # Regular arguments
        for arg in node.args.args:
            args.append(arg.arg)

        # *args
        if node.args.vararg:
            args.append("*" + node.args.vararg.arg)

        # **kwargs
        if node.args.kwarg:
            args.append("**" + node.args.kwarg.arg)

        return f"{node.name}({', '.join(args)})"

    elif isinstance(node, ast.ClassDef):
        bases = [ast.unparse(base) for base in node.bases] if node.bases else []
        return f"class {node.name}({', '.join(bases)})" if bases else f"class {node.name}"

    return node.name
