from src.docstring_core.docstring_models import DocstringOutput
from src.docstring_core.docstring_prompts import SYSTEM_PROMPT_DOCSTRINGS, PROMPT_TEMPLATE_DOCSTRINGS
from src.core_base.agents.base_agents import BaseCodeGenerationAgent

class DocstringAgent(BaseCodeGenerationAgent):
    """
    A class that generates docstrings for Python functions and classes based on specified prompts.
    
    This class extends from BaseCodeGenerationAgent and leverages a system prompt and a prompt template to produce structured docstrings.
    
    Attributes:
      SYSTEM_PROMPT (str): The prompt used to guide the docstring generation process.
      PROMPT_TEMPLATE (str): The template format for the docstrings to be generated.
      OutputModel (type): The model used for output, specifically for structured docstring representation.
    """
    SYSTEM_PROMPT = SYSTEM_PROMPT_DOCSTRINGS
    PROMPT_TEMPLATE = PROMPT_TEMPLATE_DOCSTRINGS
    OutputModel = DocstringOutput