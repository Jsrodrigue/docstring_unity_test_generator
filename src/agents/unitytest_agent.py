from src.unitytest_core.unitytest_models import UnitTestOutput
from src.agents.base_agents import BaseCodeGenerationAgent
from src.unitytest_core.unitytest_prompts import SYSTEM_PROMPT_TESTS, PROMPT_TEMPLATE_TESTS

class UnityTestAgent(BaseCodeGenerationAgent):
    SYSTEM_PROMPT = SYSTEM_PROMPT_TESTS
    PROMPT_TEMPLATE = PROMPT_TEMPLATE_TESTS
    OutputModel = UnitTestOutput