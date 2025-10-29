from typing import List
from pydantic import BaseModel

###########################################
# Pydantic docstring output models
###########################################
class DocstringOutput(BaseModel):
    """
    Represents a single generated docstring entry.
    
    Attributes:
        name (str): The name of the docstring entry.
        docstring (str): The generated docstring content.
        original (str): The original docstring (if any).
        source (str): A snippet of code associated with the docstring entry.
        file_abs (str): The absolute file path of the source code file.
    """
    name: str
    docstring: str = ""
    original: str = ""    # original docstring
    source: str = ""      # code snippet
    file_abs: str = ""    # absolute file path

class DocstringList(BaseModel):
    """
    Container for multiple docstring outputs.
    
    Attributes:
        items (List[DocstringOutput]): A list of docstring entries generated
        from the analysis process.
    """
    items: List[DocstringOutput]
