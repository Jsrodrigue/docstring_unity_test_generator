# src/agents/docstring_agent.py
from constants import PROMPT_TEMPLATE_DOCSTRINGS, SYSTEM_PROMPT_DOCSTRINGS
from src.agents.base_agent import BaseCodeAgent
from src.models.docstring_models import DocstringOutput
from src.utils.code_extractor import CodeItem

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
        self.agent.output_type = list[DocstringOutput]

    def _make_prompt(self, items: list[CodeItem]) -> str:
        """Concatenates the base prompt and item sources with imports at the top."""

        # Collect unique imports
        all_imports = set()
        for item in items:
            all_imports.update(getattr(item, "imports", []))
        imports_code = "\n".join(all_imports)

        # Format functions and classes
        formatted_items = [
            f"# File: {item.file_path}\n# {item.type} {item.name}\n{item.source}"
            for item in items
        ]
        items_code = "\n\n".join(formatted_items)

        return PROMPT_TEMPLATE_DOCSTRINGS + "\n" + imports_code + "\n\n" + items_code

    async def generate(self, items: list[CodeItem]) -> list[DocstringOutput]:
        """Generate improved or new docstrings."""
        prompt = self._make_prompt(items)
        result = await self.run(prompt)
        # result is expected to be a list of DocstringOutput objects
        return result
