from typing import Optional, List
from src.core_base.executor.executor import execute_in_path
from src.unit_test_core.unit_test_generator import generate_unit_test_from_path_dict
from src.unit_test_core.unit_test_writer import UnitTestWriterWithReview

async def _unit_test_writer_wrapper(results: List[dict], project_path: str, **kwargs):
    writer = UnitTestWriterWithReview(model_name=kwargs.get("model_name", "gpt-4o-mini"))
    await writer.write_unit_tests(results, project_path=project_path)

async def execute_unit_test_in_path(
    path: str,
    model_name: str = "gpt-4o-mini",
    project_path: str = "",
    target_names: Optional[List[str]] = None,
):
    if not project_path:
        raise ValueError("Debes proporcionar `project_path` para generar tests.")
    await execute_in_path(
        path=path,
        generate_func=generate_unit_test_from_path_dict,
        write_func=_unit_test_writer_wrapper,
        model_name=model_name,
        item_name="unit tests",
        target_names=target_names,
        project_path=project_path,
    )
