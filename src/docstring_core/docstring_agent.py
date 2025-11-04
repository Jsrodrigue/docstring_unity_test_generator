from src.docstring_core.docstring_models import DocstringOutput
from src.docstring_core.docstring_prompts import SYSTEM_PROMPT_DOCSTRINGS, PROMPT_TEMPLATE_DOCSTRINGS
from src.core_base.agents.base_agents import BaseCodeGenerationAgent
from pathlib import Path

class DocstringAgent(BaseCodeGenerationAgent):
    SYSTEM_PROMPT = SYSTEM_PROMPT_DOCSTRINGS
    PROMPT_TEMPLATE = PROMPT_TEMPLATE_DOCSTRINGS
    OutputModel = DocstringOutput

    def __init__(self, model_name: str, project_path: Path = None):
        super().__init__(model_name=model_name, project_path=project_path)
