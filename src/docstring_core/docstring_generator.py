from pathlib import Path
from typing import List, Optional
from src.utils.code_extractor import extract_functions_and_classes, CodeItem
from src.agents.docstring_agent import DocstringAgent

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

# -----------------------------
# Helper: generate docstrings for items
# -----------------------------
async def generate_docstrings_for_items(agent: DocstringAgent, items: List[CodeItem]) -> List[dict]:
    """
    Generate docstrings for a list of CodeItem objects using the provided agent.
    
    Args:
        agent (DocstringAgent): Agent to use for generation.
        items (List[CodeItem]): List of code items to generate docstrings for.
    
    Returns:
        List[dict]: Generated docstrings with metadata.
    """
    generated = await agent.generate(items)
    results = []
    for item in items:
        match = next((g for g in generated if g.name == item.name), None)
        if match:
            results.append({
                "name": match.name,
                "docstring": match.docstring,
                "file_path": str(item.file_path),
                "source": item.source,
                "original": item.docstring,
            })
    return results

# -----------------------------
# Manager: handles docstring generation
# -----------------------------
class DocstringGenerationManager:
    """
    Manager for generating docstrings from files or folders using a DocstringAgent.
    """
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.agent = DocstringAgent(model_name=model_name)

    async def generate_for_path(
        self,
        path: str,
        target_names: Optional[List[str]] = None
    ) -> List[dict]:
        """
        Scan path for Python files, filter items, and generate docstrings.
        
        Args:
            path (str): Path to file or folder.
            target_names (List[str], optional): Names of functions/classes to process.
        
        Returns:
            List[dict]: List of generated docstrings with metadata.
        """
        path_obj = Path(path).resolve()
        if not path_obj.exists():
            return []

        py_files = (
            [path_obj] if path_obj.is_file() and path_obj.suffix == ".py"
            else list(path_obj.rglob("*.py"))
        )
        if not py_files:
            return []

        results: List[dict] = []

        for file_path in py_files:
            items = get_filtered_code_items(file_path, target_names)
            if not items:
                continue

            results.extend(await generate_docstrings_for_items(self.agent, items))

        return results

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
