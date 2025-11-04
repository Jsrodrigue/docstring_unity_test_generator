from pathlib import Path
from typing import List, Optional, Type
from src.core_base.agents.base_agents import BaseCodeGenerationAgent
from src.core_base.indexer.project_indexer import ProjectIndexer
from src.core_base.generate.generate_utils import generate_outputs_for_items
from src.core_base.code.code_extractor import get_filtered_code_items
from src.core_base.code.code_model import CodeItem


class BaseGenerationManager:
    """
    Base manager that handles code scanning and generation tasks using a specific agent.
    Subclasses must define:
        - agent_class: subclass of BaseCodeGenerationAgent
    """

    agent_class: Type[BaseCodeGenerationAgent]

    def __init__(self, model_name: str = "gpt-4o-mini", project_path: Optional[Path] = None):
        """
        Initializes the agent and project indexer (optional).
        """
        self.project_path = project_path
        self.indexer = None

        # Initialize indexer only if project_path is provided
        if project_path:
            self.indexer = ProjectIndexer(project_path)
            self.indexer.load_or_build()

        # Initialize agent
        self.agent = self.agent_class(model_name=model_name, project_path=project_path)

    async def generate_for_path(
        self,
        path: str,
        target_names: Optional[List[str]] = None
    ) -> List[dict]:
        """
        Generates structured outputs for CodeItems in a specific path.

        If no project_path was provided, falls back to scanning the file directly.
        """
        path_obj = Path(path).resolve()
        if not path_obj.exists():
            return []

        # Case 1: Project indexer available
        if self.indexer:
            if target_names:
                items: List[CodeItem] = []
                for name in target_names:
                    items.extend(self.indexer.query_by_name(name))
            else:
                all_items = self.indexer.all_items()
                items = [item for item in all_items if str(path_obj) in str(item.file_path)]

        # Case 2: No project_path, scan file directly
        else:
            print("[INFO] No project_path detected — scanning file directly.")
            items = get_filtered_code_items(path_obj, target_names)

        if not items:
            print("[WARNNG] No code items found in path:", path_obj)
            return []

        # Run generation using the agent
        results = await generate_outputs_for_items(self.agent, items)
        return results
