from pydantic import BaseModel
from pathlib import Path

class UnitTestOutput(BaseModel):
    """
    A model representing the output from the LLM for generating pytest unit tests.

    Attributes:
      function_name (str): The name of the function to be tested.
      test_code (str): The complete pytest code as a string that tests the function.
      file_path (str | Path): The path of the Python file containing the function, for uniqueness.
    """
    function_name: str
    test_code: str
    file_path: str | Path
