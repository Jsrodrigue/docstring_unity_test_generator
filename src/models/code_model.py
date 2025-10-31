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
        file_path: str | Path, 
        imports: Optional[List[str]] = None
    ):
        self.name = name
        self.type = type  # "function", "method" or "class"
        self.source = source
        self.docstring = docstring
        self.file_path = file_path
        self.imports = imports or []

    def __repr__(self):
      attrs = {
          "name": self.name,
          "type": self.type,
          "source": self.source,
          "docstring": self.docstring,
          "file_path": str(self.file_path),
          "imports": self.imports,
      }
      return f"CodeItem({attrs})"
