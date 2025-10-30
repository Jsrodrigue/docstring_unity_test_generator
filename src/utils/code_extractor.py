# src/utils/code_extractor.py
import ast
from pathlib import Path
from typing import List, Optional, Union
import sys
from pathlib import Path

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

    def _process_node(self, node: ast.AST, source_lines: List[str], file_path: Path, imports: List[str]) -> CodeItem:
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
            imports=imports,
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
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(f"import {alias.name}" + (f" as {alias.asname}" if alias.asname else ""))
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    names = ", ".join([alias.name + (f" as {alias.asname}" if alias.asname else "") for alias in node.names])
                    level_dots = "." * node.level
                    imports.append(f"from {level_dots}{module} import {names}")

        items: List[CodeItem] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                item = self._process_node(node, source_lines, file_path, imports)
                items.append(item)

        return items

    def extract_from_path(self) -> List[CodeItem]:
        """Extract all CodeItem objects from Python files under base_path recursively."""
        py_files = list(self.base_path.rglob("*.py"))
        all_items: List[CodeItem] = []
        for file_path in py_files:
            all_items.extend(self.extract_from_file(file_path))
        return all_items

def extract_functions_and_classes(path: Union[str, Path]) -> List[CodeItem]:
    """
    Extracts functions and classes from a Python file or all .py files in a folder.

    Args:
        path (str | Path): Path to a Python file or a folder.

    Returns:
        List[CodeItem]: A list of CodeItem objects.
    """
    path = Path(path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"La ruta {path} no existe")

    extractor = CodeExtractorTool(path.parent if path.is_file() else path)

    if path.is_file() and path.suffix == ".py":
        items = extractor.extract_from_file(path)
    else:
        items = extractor.extract_from_path()

    return items

# test_extractor.py


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python test_extractor.py <ruta_al_archivo_o_carpeta_python>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Error: la ruta {path} no existe")
        sys.exit(1)

    items = extract_functions_and_classes(path)
    print(f"[INFO] Se encontraron {len(items)} items en {path}:\n")
    for item in items:
        print(item.__dict__)
        print()
