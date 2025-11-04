from src.unit_test_core.unit_test_models import UnitTestOutput
from src.unit_test_core.unit_test_prompts import SYSTEM_PROMPT_TESTS, PROMPT_TEMPLATE_TESTS
from src.core_base.agents.base_agents import BaseCodeGenerationAgent
from pathlib import Path

class UnitTestAgent(BaseCodeGenerationAgent):
    SYSTEM_PROMPT = SYSTEM_PROMPT_TESTS
    PROMPT_TEMPLATE = PROMPT_TEMPLATE_TESTS
    OutputModel = UnitTestOutput

    def __init__(self, model_name: str, project_path: Path = None):
        super().__init__(model_name=model_name, project_path=project_path)
