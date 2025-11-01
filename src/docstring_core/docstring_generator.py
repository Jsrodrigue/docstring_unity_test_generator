from pathlib import Path
from typing import List, Optional
from src.utils.code_extractor import extract_functions_and_classes, CodeItem
from src.agents.docstring_agent import DocstringAgent

async def generate_from_path_dict(
    path: str,
    model_name: str = "gpt-4o-mini",
    target_names: Optional[List[str]] = None,
) -> List[dict]:
    """
    Scan a file or folder for Python files, extract functions and classes,
    and generate minimal docstrings using the specified model.
    
    If target_names is provided, only those specific items will be processed.
    
    Args:
        path (str): Path to a file or directory.
        model_name (str, optional): Model name for docstring generation.
        target_names (List[str], optional): Names of functions or classes to process.
    
    Returns:
        List[dict]: List of dicts with 'name', 'docstring', 'file_path', 'source', and 'original'.
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

    agent = DocstringAgent(model_name=model_name)
    results: List[dict] = []

    for file_path in py_files:
        items: List[CodeItem] = extract_functions_and_classes(file_path)
        if not items:
            continue

        # Si se especifican nombres, filtramos
        if target_names:
            items = [i for i in items if i.name in target_names]
            if not items:
                continue
        
        generated: List = await agent.generate(items)

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
