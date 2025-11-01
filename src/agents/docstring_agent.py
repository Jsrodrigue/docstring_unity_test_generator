from src.docstring_core.docstring_models import DocstringOutput
from src.docstring_core.docstring_prompts import SYSTEM_PROMPT_DOCSTRINGS, PROMPT_TEMPLATE_DOCSTRINGS
from src.agents.base_agents import BaseCodeGenerationAgent

class DocstringAgent(BaseCodeGenerationAgent):
    SYSTEM_PROMPT = SYSTEM_PROMPT_DOCSTRINGS
    PROMPT_TEMPLATE = PROMPT_TEMPLATE_DOCSTRINGS
    OutputModel = DocstringOutput