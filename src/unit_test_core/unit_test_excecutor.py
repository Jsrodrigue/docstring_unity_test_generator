from src.core_base.excecutor.excecutor import excecute_in_path
from src.unit_test_core.unit_test_generator import generate_unit_test_from_path_dict
from src.unit_test_core.unit_test_writer import write_unit_tests

def excecute_unit_test_in_path(path: str, model_name: str = "gpt-4o-mini"):
    """
    Scan a folder (or file) for Python code and automatically generate and update docstrings.

    Args:
        path (str): Path to a Python file or folder to scan.
        model_name (str, optional): Model to use for docstring generation.
    """
    excecute_in_path(
        path=path,
        generate_func=generate_unit_test_from_path_dict,
        write_func=write_unit_tests,
        model_name=model_name,
        item_name="docstrings"
    )
