from typing import List, Optional
from pathlib import Path
from src.core_base.generate.generator_manager import BaseGenerationManager
from src.unit_test_core.unit_test_agent import UnitTestAgent


class UnitTestGenerationManager(BaseGenerationManager):
    """
    Manager for generating unit tests from files or folders using a UnitTestAgent.
    Requires a project_path to mirror the structure of the source code inside /tests.
    """

    agent_class = UnitTestAgent

    def __init__(self, model_name: str = "gpt-4o-mini", project_path: Path = None):
        """
        Initializes the manager with the agent and project indexer.

        Args:
            model_name (str): Model used for generation.
            project_path (Path): Root path of the project to index and mirror.
        """
        if project_path is None:
            raise ValueError("❌ 'project_path' is required for UnitTestGenerationManager.")
        super().__init__(model_name=model_name, project_path=project_path)



async def generate_unit_test_from_path_dict(
    path: str,
    model_name: str = "gpt-4o-mini",
    target_names: Optional[List[str]] = None,
    project_path: Optional[str] = None
) -> List[dict]:
    """
    Wrapper for generating unit tests from a file or folder.

    'project_path' is mandatory to correctly mirror the directory structure in /tests.
    """
    if not project_path:
        raise ValueError("[ERROR] 'project_path' is required to generate mirrored test files.")

    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(f"[ERROR] Path not found: {path}")

    project_path_obj = Path(project_path)
    manager = UnitTestGenerationManager(model_name=model_name, project_path=project_path_obj)
    return await manager.generate_for_path(path, target_names=target_names)
