# agents/code_extractor.py
import ast
from pathlib import Path
from typing import List, Optional

class CodeItem:
    """
    Represents a code entity (function or class) extracted from a Python file.
    """
    def __init__(self, name: str, type: str, source: str, docstring: str, file_path: Path, imports: Optional[List[str]] = None):
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
    Can be used by Orchestrator or any agent that needs structured code.
    """
    def __init__(self, base_path: Path):
        self.base_path = base_path.resolve()

    def _process_node(self, node: ast.AST, source_lines: List[str], file_path: Path) -> CodeItem:
        start = node.lineno - 1
        end = getattr(node, "end_lineno", start+1)
        code_text = "\n".join(source_lines[start:end])
        node_type = "class" if isinstance(node, ast.ClassDef) else "function"
        docstring = ast.get_docstring(node) or ""
        return CodeItem(
            name=node.name,
            type=node_type,
            source=code_text,
            docstring=docstring,
            file_path=file_path,
            imports=[]  # por ahora vacío, luego podemos extraer los imports relevantes
        )

    def extract_from_file(self, file_path: Path) -> List[CodeItem]:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
        tree = ast.parse(source_code)
        source_lines = source_code.splitlines()
        items = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                items.append(self._process_node(node, source_lines, file_path))

        return items

    def extract_from_path(self) -> List[CodeItem]:
        """
        Extract all code items from Python files under base_path (recursively).
        """
        py_files = list(self.base_path.rglob("*.py"))
        all_items = []
        for file in py_files:
            all_items.extend(self.extract_from_file(file))
        return all_items
