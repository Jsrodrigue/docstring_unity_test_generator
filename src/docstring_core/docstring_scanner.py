from pathlib import Path

from constants import PROMPT_TEMPLATE_DOCSTRINGS, SYSTEM_PROMPT_DOCSTRINGS
from src.docstring_core.docstring_generator import generate_docstrings
from src.utils.ast_utils import extract_functions_and_classes
from src.docstring_core.docstring_models import DocstringOutput
from typing import List


###########################################
# 5️⃣ Scan path for Python docstrings
###########################################
async def scan_path_for_docstrings(path: str, model) -> List[DocstringOutput]:
    """
    Scan a directory or file for Python files, extract existing docstrings,
    and generate suggestions for improvements using the specified model.
    
    Args:
        path (str): Path to the file or directory to scan.
        model: Model used for generating docstrings, passed to the agent.
    
    Returns:
        List[DocstringOutput]: A list of items where suggested docstrings differ
        from the original, along with their related information.
    """
    path_obj = Path(path).resolve()
    if not path_obj.exists():
        return []

    py_files = [path_obj] if path_obj.is_file() and path_obj.suffix == ".py" else list(path_obj.rglob("*.py"))
    if not py_files:
        return []

    all_results = []
    for file_path in py_files:
        items = extract_functions_and_classes(file_path)
        generated = await generate_docstrings(
            items=items,
            prompt_base=PROMPT_TEMPLATE_DOCSTRINGS,
            system_prompt=SYSTEM_PROMPT_DOCSTRINGS,
        )

        for item_info in items:
            match = next((g for g in generated if g.name == item_info["name"]), None)
            suggested_docstring = match.docstring if match else ""
            original_docstring = item_info.get("docstring", "") or ""
            if original_docstring.strip() == suggested_docstring.strip():
                continue  # skip unchanged

            all_results.append(
                DocstringOutput(
                    name=item_info["name"],
                    docstring=suggested_docstring,
                    original=original_docstring,
                    source=item_info.get("source", ""),
                    file_abs=str(file_path),
                )
            )

    return all_results