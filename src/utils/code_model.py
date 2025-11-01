from pathlib import Path
from typing import List, Optional

class CodeItem:
    """
    Represents a code entity (function or class) extracted from a Python file.
    
    Attributes:
      name (str): The name of the code item.
      type (str): The type of the code item; can be 'function', 'method', or 'class'.
      source (str): The source code of the item.
      docstring (str): The documentation string of the code item.
      file_path (Union[str, Path]): The file path where the code item is located.
      imports (Optional[List[str]]): A list of imported modules or functions used by the code item.
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
      """
      Returns a string representation of the CodeItem instance, displaying its attributes in a structured format.
      """
      attrs = {
          "name": self.name,
          "type": self.type,
          "source": self.source,
          "docstring": self.docstring,
          "file_path": str(self.file_path),
          "imports": self.imports,
      }
      return f"CodeItem({attrs})"