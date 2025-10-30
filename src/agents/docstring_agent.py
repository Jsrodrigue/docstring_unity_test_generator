from src.agents.base_agent import BaseCodeAgent
from constants import SYSTEM_PROMPT_DOCSTRINGS, PROMPT_TEMPLATE_DOCSTRINGS
from src.docstring_core.docstring_models import DocstringList, DocstringOutput


class DocstringAgent(BaseCodeAgent):
    """
    Agent specialized in generating or improving Python docstrings
    for functions and classes using PEP 257 conventions.
    """

    def __init__(self, model_name: str = "gpt-4o-mini"):
        super().__init__(
            name="Docstring Generator Agent",
            system_prompt=SYSTEM_PROMPT_DOCSTRINGS,
            model_name=model_name,
        )
        # Set the output type 
        self.agent.output_type = DocstringList

    def _make_prompt(self, items: list[dict]) -> str:
        """Concatenates the base prompt and item sources."""
        items_code = "\n\n".join([item["source"] for item in items])
        return PROMPT_TEMPLATE_DOCSTRINGS + items_code

    async def generate(self, items: list[dict]) -> list[DocstringOutput]:
        """Generate improved or new docstrings."""
        prompt = self._make_prompt(items)
        result = await self.run(prompt)
        # Runner returns a pydantic DocstringList object
        return result.items
