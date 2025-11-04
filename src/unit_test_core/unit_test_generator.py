from typing import List, Optional
from pathlib import Path
from src.core_base.generate.generator_manager import BaseGenerationManager
from src.unit_test_core.unit_test_agent import UnitTestAgent

class UnitTestGenerationManager(BaseGenerationManager):
    """
    Manager for generating unit tests from files or folders using a UnitTestAgent.
    """
    agent_class = UnitTestAgent

    def __init__(self, model_name: str = "gpt-4o-mini", project_path: Optional[Path] = None):
        """
        Initializes the manager with the agent and project indexer.

        Args:
            model_name (str): Name of the model for the agent.
            project_path (Path, optional): Root path of the project to index.
        """
        super().__init__(model_name=model_name, project_path=project_path)


# -----------------------------
# Wrapper function (CLI/Gradio)
# -----------------------------
async def generate_unit_test_from_path_dict(
    path: str,
    model_name: str = "gpt-4o-mini",
    target_names: Optional[List[str]] = None,
    project_path: Optional[str] = None
) -> List[dict]:
    """
    Wrapper function for generating unit tests from a file or folder.

    Args:
        path (str): Path to file or folder.
        model_name (str, optional): Model name to use.
        target_names (List[str], optional): Filter for specific function/class names.
        project_path (str, optional): Root path of the project to index.

    Returns:
        List[dict]: Generated unit tests with metadata.
    """
    project_path_obj = Path(project_path) if project_path else None
    manager = UnitTestGenerationManager(model_name=model_name, project_path=project_path_obj)
    return await manager.generate_for_path(path, target_names=target_names)


# -----------------------------
# Quick test / CLI usage
# -----------------------------
import asyncio

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "examples/"
    project_root = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"🔍 Running unit test generation on: {path}")
    results = asyncio.run(generate_unit_test_from_path_dict(path, project_path=project_root))
    print(f"✅ Generated {len(results)} test(s)")
    for r in results:
        print(f"\nFile: {r['file_path']}")
        print(f"Imports: {r['imports']}")
        print(f"--- Test Output for {r['name']} ---\n{r['test_code']}")
