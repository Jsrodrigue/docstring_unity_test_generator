from pydantic import BaseModel

class DocstringOutput(BaseModel):
    """
    Output from the LLM for Python functions and classes.
    Includes the name, suggested docstring, and file path for uniqueness.
    """
    name: str
    docstring: str
    file_path: str