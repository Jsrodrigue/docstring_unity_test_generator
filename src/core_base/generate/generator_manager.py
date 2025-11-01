from pathlib import Path
from typing import List, Optional, Type
from src.core_base.code.code_extractor import get_filtered_code_items
from src.agents_core.base_agents import BaseCodeGenerationAgent
from src.core_base.generate.generate_utils import generate_outputs_for_items

class BaseGenerationManager:
    """
    Base manager that handles code scanning and generation tasks using a specific agent.
    
    Subclasses must define:
        - agent_class: subclass of BaseCodeGenerationAgent
        - output_key: key for generated content (e.g., "docstring" or "unittest_code")
        - item_generator_fn: the function used to trigger generation (optional override)
    """

    agent_class: Type[BaseCodeGenerationAgent]
    output_key: str

    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.agent = self.agent_class(model_name=model_name)

    async def generate_for_path(
        self,
        path: str,
        target_names: Optional[List[str]] = None
    ) -> List[dict]:
        """
        Scans a path (file or folder) for Python files, extracts CodeItem objects,
        and generates structured outputs using the configured agent.

        Args:
            path (str): Path to file or folder.
            target_names (List[str], optional): Names of specific functions/classes to process.

        Returns:
            List[dict]: Generated outputs with metadata.
        """
        path_obj = Path(path).resolve()
        if not path_obj.exists():
            return []

        py_files = (
            [path_obj] if path_obj.is_file() and path_obj.suffix == ".py"
            else list(path_obj.rglob("*.py"))
        )
        if not py_files:
            return []

        results: List[dict] = []

        for file_path in py_files:
            items = get_filtered_code_items(file_path, target_names)
            if not items:
                continue

            # Usa la función genérica reutilizable
            generated = await generate_outputs_for_items(
                self.agent,
                items,
                output_key=self.output_key,
            )
            results.extend(generated)

        return results
