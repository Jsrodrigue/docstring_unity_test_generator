from typing import List, Optional

from src.core_base.executor.executor import execute_in_path
from src.docstring_core.docstring_generator import generate_docstring_from_path_dict
from src.docstring_core.docstring_writer import write_docstrings

def execute_docstring_in_path(
    path: str,
    model_name: str = "gpt-4o-mini",
    target_names: Optional[List[str]] = None,
    project_path: Optional[str] = None
):
    """
    Executes the generation and writing of docstrings in the specified path.
    
    This function utilizes a provided model to generate docstrings for the target items, and writes them to the appropriate files.
    
    Args:
      path (str): The path to the directory or file where docstrings need to be generated.
      model_name (str, optional): The name of the model to be used for generation, defaults to 'gpt-4o-mini'.
      target_names (Optional[List[str]], optional): A list of specific function or class names to target. If None, all items will be processed.
      project_path (Optional[str], optional): The root path of the project for indexing purposes.
    
    Returns:
      None: This function does not return a value.
    """
    execute_in_path(
        path=path,
        generate_func=generate_docstring_from_path_dict,
        write_func=write_docstrings,
        model_name=model_name,
        item_name="docstrings",
        target_names=target_names,
        project_path=project_path,
    )