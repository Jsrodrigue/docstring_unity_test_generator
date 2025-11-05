from pathlib import Path
import asyncio
from typing import Optional, List

from src.core_base.executor.executor import execute_in_path
from src.docstring_core.docstring_generator import generate_docstring_from_path_dict
from src.docstring_core.docstring_writer import write_docstrings

async def _docstring_writer_wrapper(file_path: Path, items: List[dict], **_):
    await write_docstrings(file_path, items)

def execute_docstring_in_path(
    path: str,
    model_name: str = "gpt-4o-mini",
    target_names: Optional[List[str]] = None,
    project_path: Optional[str] = None
):
    asyncio.run(
        execute_in_path(
            path=path,
            generate_func=generate_docstring_from_path_dict,
            write_func=_docstring_writer_wrapper,
            model_name=model_name,
            item_name="docstrings",
            target_names=target_names,
            project_path=project_path
        )
    )
