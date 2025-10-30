# src/utils/code_extractor.py
import ast
from pathlib import Path
from typing import List, Optional

class CodeItem:
    """
    Represents a code entity (function or class) extracted from a Python file.
    """
    def __init__(
        self, 
        name: str, 
        type: str, 
        source: str, 
        docstring: str, 
        file_path: Path, 
        imports: Optional[List[str]] = None
    ):
        self.name = name
        self.type = type  # "function" o "class"
        self.source = source
        self.docstring = docstring
        self.file_path = file_path
        self.imports = imports or []

    def __repr__(self):
        return f"<CodeItem {self.type} {self.name} in {self.file_path.name}>"


class CodeExtractorTool:
    """
    Tool to extract all functions and classes from Python files in a path.
    Returns results as CodeItem objects.
    """
    def __init__(self, base_path: Path):
        self.base_path = base_path.resolve()

    def _process_node(self, node: ast.AST, source_lines: List[str], file_path: Path) -> CodeItem:
        start = node.lineno - 1
        end = getattr(node, "end_lineno", start + 1)
        code_text = "\n".join(source_lines[start:end])
        node_type = "class" if isinstance(node, ast.ClassDef) else "function"
        docstring = ast.get_docstring(node) or ""
        return CodeItem(
            name=node.name,
            type=node_type,
            source=code_text,
            docstring=docstring,
            file_path=file_path,
            imports=[],
        )

    def extract_from_file(self, file_path: Path) -> List[CodeItem]:
        """Extract CodeItem objects from a single Python file, including imports."""
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        tree = ast.parse(source_code)
        source_lines = source_code.splitlines()

        # Extraer imports del archivo
        imports: List[str] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                # Reconstruir la línea de importación
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(f"import {alias.name}" + (f" as {alias.asname}" if alias.asname else ""))
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    names = ", ".join([alias.name + (f" as {alias.asname}" if alias.asname else "") for alias in node.names])
                    level_dots = "." * node.level  # para imports relativos
                    imports.append(f"from {level_dots}{module} import {names}")

        items: List[CodeItem] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                item = self._process_node(node, source_lines, file_path)
                item.imports = imports  # asignamos todos los imports del archivo
                items.append(item)

        return items


def extract_functions_and_classes(file_path: Path) -> List[CodeItem]:
    """
    Extracts functions and classes from a Python file as CodeItem objects.

    Args:
        file_path (Path): Path to the Python file to analyze.

    Returns:
        List[CodeItem]: A list of CodeItem objects.
    """
    extractor = CodeExtractorTool(file_path.parent)
    # filtra solo el archivo especificado
    items = extractor.extract_from_file(file_path)
    return items

# test_extractor.py
import sys
from pathlib import Path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python test_extractor.py <ruta_al_archivo_python>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists() or not file_path.suffix == ".py":
        print(f"Error: el archivo {file_path} no existe o no es un .py")
        sys.exit(1)

    items = extract_functions_and_classes(file_path)
    print(f"[INFO] Se encontraron {len(items)} items en {file_path}:\n")
    for item in items:
        print(item.__dict__)
        print()

