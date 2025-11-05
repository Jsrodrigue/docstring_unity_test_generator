from pathlib import Path
from typing import Callable, List, Dict, Optional, Any

async def execute_in_path(
    path: str,
    generate_func: Callable[..., Any],
    write_func: Callable[..., Any],
    model_name: str = "gpt-4o-mini",
    project_path: Optional[str] = None,
    target_names: Optional[List[str]] = None,
    item_name: str = "items",
):
    """Ejecutor genérico para docstrings o unit tests."""
    path_obj = Path(path).resolve()
    if not path_obj.exists():
        print(f"[WARN] {path} not found.")
        return

    results = await generate_func(str(path_obj), model_name, target_names, project_path)
    if not results:
        print(f"[INFO] {item_name} not generated.")
        return

    grouped: Dict[str, List[dict]] = {}
    for item in results:
        grouped.setdefault(item["file_path"], []).append(item)

    # Detecta tipo de writer según su firma
    for file_path, items in grouped.items():
        try:
            await write_func(Path(file_path), items, model_name=model_name, project_path=project_path)
        except TypeError:
            # Caso: writer que agrupa internamente (como UnitTestWriterWithReview)
            await write_func(results, project_path=project_path, model_name=model_name)
            break  # Ya procesa todo de una vez
        print(f"✅ {item_name.capitalize()} writen in {file_path}")

    print(f"[OK] {item_name.capitalize()} successfuly actualized.")
