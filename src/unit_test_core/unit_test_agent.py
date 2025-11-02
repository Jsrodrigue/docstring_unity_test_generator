from src.unit_test_core.unit_test_models import UnitTestOutput
from src.core_base.agents.base_agents import BaseCodeGenerationAgent
from src.unit_test_core.unit_test_prompts import SYSTEM_PROMPT_TESTS, PROMPT_TEMPLATE_TESTS

class UnitTestAgent(BaseCodeGenerationAgent):
    """
    A class that extends the BaseCodeGenerationAgent to facilitate the generation of unit tests.
    
    This class utilizes a predefined system prompt and prompt template specific to unity testing.
    
    Attributes:
      SYSTEM_PROMPT (str): The system prompt to be used for generating tests.
      PROMPT_TEMPLATE (str): The template prompt used during the code generation process.
      OutputModel: Model that structures the output of the generated tests.
    """
    SYSTEM_PROMPT = SYSTEM_PROMPT_TESTS
    PROMPT_TEMPLATE = PROMPT_TEMPLATE_TESTS
    OutputModel = UnitTestOutput