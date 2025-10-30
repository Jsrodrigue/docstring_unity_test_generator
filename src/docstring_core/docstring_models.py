from typing import List
from pathlib import Path
from pydantic import BaseModel
from src.utils.code_extractor import CodeItem

###########################################
# Pydantic docstring output models
###########################################
class DocstringOutput(BaseModel):
    """
    Represents a single generated docstring entry from the LLM.

    Attributes:
        name (str): The name of the function or class.
        type (str): The type of code entity: "function" or "class".
        docstring (str): The generated docstring content.
        original (str): The original docstring, if any.
        source (str): Code snippet associated with this entry.
        file_path (str | Path): Path to the source file.
    """
    name: str
    type: str = "function"  # or "class"
    docstring: str = ""
    original: str = ""
    source: str = ""
    file_path: str | Path = ""

class DocstringList(BaseModel):
    """
    Container for multiple docstring outputs from LLM.

    Attributes:
        items (List[DocstringOutput]): List of docstring entries generated.
    """
    items: List[DocstringOutput]

# Converter from DocstringOutput to CodeItem
def docstring_to_codeitem(doc_out: DocstringOutput) -> CodeItem:
    return CodeItem(
        name=doc_out.name,
        type=doc_out.type,
        source=doc_out.source,
        docstring=doc_out.docstring,
        file_path=Path(doc_out.file_path)
    )
