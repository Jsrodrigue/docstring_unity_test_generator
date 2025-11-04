from typing import List, Optional
from src.core_base.executor.executor import execute_in_path
from src.unit_test_core.unit_test_generator import generate_unit_test_from_path_dict
from src.unit_test_core.unit_test_writer import write_unit_tests

def execute_unit_test_in_path(
    path: str,
    model_name: str = "gpt-4o-mini",
    target_names: Optional[List[str]] = None,
    project_path: Optional[str] = None
):
    """
    Executes unit tests in the specified path using the given model.

    This function calls the `execute_in_path` function, providing it with the necessary parameters
    to generate and write unit tests based on the contents found at the specified path.

    Args:
        path (str): The path to the directory or file containing the code to be tested.
        model_name (str, optional): The name of the model to use for generating unit tests. Defaults to 'gpt-4o-mini'.
        target_names (List[str], optional): Specific functions/classes to filter and generate.
        project_path (str, optional): Root path of the project to index.
    """
    execute_in_path(
        path=path,
        generate_func=generate_unit_test_from_path_dict,
        write_func=write_unit_tests,
        model_name=model_name,
        item_name="unit tests",
        target_names=target_names,
        project_path=project_path,
    )
