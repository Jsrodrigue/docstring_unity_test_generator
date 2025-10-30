from pathlib import Path
from typing import List
from src.docstring_core.docstring_models import DocstringOutput
from src.utils.code_extractor import extract_functions_and_classes, CodeItem
from constants import PROMPT_TEMPLATE_DOCSTRINGS, SYSTEM_PROMPT_DOCSTRINGS
from src.docstring_core.docstring_generator import generate_docstrings

###########################################
# 5️⃣ Scan path for Python docstrings
###########################################
async def scan_path_for_docstrings(path: str, model) -> List[DocstringOutput]:
    """
    Scan a directory or file for Python files, extract code items (functions/classes),
    and generate suggested docstrings using the specified model.
    
    Args:
        path (str): Path to the file or directory to scan.
        model: Model used for generating docstrings, passed to the agent.
    
    Returns:
        List[DocstringOutput]: Suggested docstrings where different from original.
    """
    path_obj = Path(path).resolve()
    if not path_obj.exists():
        return []

    py_files = [path_obj] if path_obj.is_file() and path_obj.suffix == ".py" else list(path_obj.rglob("*.py"))
    if not py_files:
        return []

    all_results: List[DocstringOutput] = []

    for file_path in py_files:
        # extract_functions_and_classes debe devolver List[CodeItem]
        items: List[CodeItem] = extract_functions_and_classes(file_path)

        # Generar docstrings con el agente/modelo
        generated: List[DocstringOutput] = await generate_docstrings(
            items=[ci.__dict__ for ci in items],
            prompt_base=PROMPT_TEMPLATE_DOCSTRINGS,
            system_prompt=SYSTEM_PROMPT_DOCSTRINGS,
            model=model
        )

        # Comparar sugerencias con los docstrings existentes
        for ci in items:
            match = next((g for g in generated if g.name == ci.name), None)
            suggested_docstring = match.docstring if match else ""
            original_docstring = ci.docstring or ""
            if original_docstring.strip() == suggested_docstring.strip():
                continue  # saltar si no hay cambios

            all_results.append(
                DocstringOutput(
                    name=ci.name,
                    type=ci.type,
                    docstring=suggested_docstring,
                    original=original_docstring,
                    source=ci.source,
                    file_path=ci.file_path
                )
            )

    return all_results
