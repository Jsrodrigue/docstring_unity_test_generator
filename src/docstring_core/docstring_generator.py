from pathlib import Path
from typing import List
from src.utils.code_extractor import extract_functions_and_classes, CodeItem
from src.agents.docstring_agent import DocstringAgent  # tu clase agente

async def generate_from_path_dict(path: str, model_name: str = "gpt-4o-mini") -> List[dict]:
    """
    Scan a file or folder for Python files, extract functions and classes from them, and generate minimal docstrings using the specified DocstringAgent model.
    
    Args:
      path (str): The path to a file or directory to be scanned.
      model_name (str, optional): The name of the model to use for generating docstrings, default is 'gpt-4o-mini'.
    
    Returns:
      List[dict]: A list of dictionaries, each containing 'name', 'docstring', 'file_path', and 'source' keys, where 'name' is the function or class name, 'docstring' is the generated docstring, 'file_path' is the path to the code item, and 'source' is the original code of the function or class.
    """
    path_obj = Path(path).resolve()
    if not path_obj.exists():
        return []

    py_files = [path_obj] if path_obj.is_file() and path_obj.suffix == ".py" else list(path_obj.rglob("*.py"))
    if not py_files:
        return []

    agent = DocstringAgent(model_name=model_name)
    results: List[dict] = []

    for file_path in py_files:
        items: List[CodeItem] = extract_functions_and_classes(file_path)
        if not items:
            continue
        
        generated: List = await agent.generate(items)

        # Matcheamos cada docstring generada con su CodeItem original
        for item in items:
            match = next((g for g in generated if g.name == item.name), None)
            if match:
                results.append({
                    "name": match.name,
                    "docstring": match.docstring,
                    "file_path": str(item.file_path),
                    "source": item.source, 
                    "original": item.docstring
                })

    return results