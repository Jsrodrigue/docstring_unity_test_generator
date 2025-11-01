from typing import List, Optional
from src.core_base.generate.generator_manager import BaseGenerationManager
from src.docstring_core.docstring_agent import DocstringAgent

class DocstringGenerationManager(BaseGenerationManager):
    """
    Manager for generating docstrings from files or folders using a DocstringAgent.
    """
    agent_class = DocstringAgent
    output_key = "docstring"


# -----------------------------
# Wrapper function (CLI/Gradio)
# -----------------------------
async def generate_from_path_dict(
    path: str,
    model_name: str = "gpt-4o-mini",
    target_names: Optional[List[str]] = None
) -> List[dict]:
    """
    Wrapper function for generating docstrings from a file or folder.
    
    Args:
        path (str): Path to file or folder.
        model_name (str, optional): Model name to use.
        target_names (List[str], optional): Filter for specific function/class names.
    
    Returns:
        List[dict]: Generated docstrings with metadata.
    """
    manager = DocstringGenerationManager(model_name=model_name)
    return await manager.generate_for_path(path, target_names=target_names)
