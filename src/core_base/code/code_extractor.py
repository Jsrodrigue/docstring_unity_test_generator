# src/utils/code_extractor.py
import ast
from pathlib import Path
from typing import List, Union, Optional
import sys
from src.core_base.code.code_model import CodeItem


class CodeExtractorTool:
    """
    Tool to extract all functions, methods, and classes from Python files in a path.
    Returns results as CodeItem objects.
    """

    def __init__(self, base_path: Path):
        self.base_path = base_path.resolve()

    def _process_node(
        self, node: ast.AST, source_lines: List[str], file_path: Path, imports: List[str], parent: str | None = None
    ) -> CodeItem:
        """
        Process an abstract syntax tree (AST) node to extract relevant information including its name, type, source code, and docstring.
        
        Args:
          node (ast.AST): The AST node to process.
          source_lines (List[str]): The lines of source code corresponding to the file.
          file_path (Path): The path of the file the node belongs to.
          imports (List[str]): A list of import statements from the file.
          parent (str | None): The name of the parent class if the node is a method; otherwise, None.
        
        Returns:
          CodeItem: An object containing the extracted information from the node.
        """
        start = node.lineno - 1
        end = getattr(node, "end_lineno", start + 1)
        code_text = "\n".join(source_lines[start:end])
        # Detect type
        if isinstance(node, ast.ClassDef):
            node_type = "class"
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and parent:
            node_type = "method"  # method inside a class
        else:
            node_type = "function"
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
        """
        Extract CodeItem objects from a single Python file, including its functions, methods, classes, and import statements.
        
        Args:
          file_path (Path): The path to the Python file from which to extract code items.
        
        Returns:
          List[CodeItem]: A list of CodeItem objects representing the extracted functions, methods, and classes.
        """
        print(f"[INFO]: Extracting info from file {file_path} ...")
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        tree = ast.parse(source_code)
        source_lines = source_code.splitlines()

        # Extract imports from file
        imports: List[str] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(f"import {alias.name}" + (f" as {alias.asname}" if alias.asname else ""))
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    names = ", ".join(
                        [alias.name + (f" as {alias.asname}" if alias.asname else "") for alias in node.names]
                    )
                    level_dots = "." * node.level
                    imports.append(f"from {level_dots}{module} import {names}")

        items: List[CodeItem] = []

        # --- Extract top-level classes and functions ---
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                items.append(self._process_node(node, source_lines, file_path, imports))
                # --- If it's a class, extract methods inside ---
                if isinstance(node, ast.ClassDef):
                    for sub_node in node.body:
                        if isinstance(sub_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            items.append(
                                self._process_node(sub_node, source_lines, file_path, imports, parent=node.name)
                            )
        print(f"Found {len(items)} items in {file_path}")
        return items

    def extract_from_path(self) -> List[CodeItem]:
        """
        Extract all CodeItem objects from all Python files within the base_path directory, recursively searching through subdirectories.
        
        Returns:
          List[CodeItem]: A list of CodeItem objects representing all functions, methods, and classes found in the Python files under the base_path.
        """
        py_files = list(self.base_path.rglob("*.py"))
        all_items: List[CodeItem] = []
        for file_path in py_files:
            all_items.extend(self.extract_from_file(file_path))
        return all_items


def extract_functions_and_classes(path: Union[str, Path]) -> List[CodeItem]:
    """
    Extracts functions, methods, and classes from a Python file or all .py files in a folder.

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

# -----------------------------
# Helper: extract + filter code items
# -----------------------------
def get_filtered_code_items(file_path: Path, target_names: Optional[List[str]] = None) -> List[CodeItem]:
    """
    Extract functions and classes from a Python file and filter by target names if provided.
    
    Args:
        file_path (Path): Path to a Python file.
        target_names (List[str], optional): List of names to filter.
    
    Returns:
        List[CodeItem]: List of filtered CodeItem objects.
    """
    items = extract_functions_and_classes(file_path)
    if target_names:
        items = [i for i in items if i.name in target_names]
    return items


########### FOR DEBUGGING: use in cli python -m src.utils.code_extractor examples/example.py #################
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python src/utils/code_extractor.py <ruta_al_archivo_o_carpeta_python>")
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