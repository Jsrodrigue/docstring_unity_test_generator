# src/agents/docstring_agent.py
import json
import re
from constants import PROMPT_TEMPLATE_DOCSTRINGS, SYSTEM_PROMPT_DOCSTRINGS
from src.agents.base_agent import BaseCodeAgent
from src.models.docstring_models import DocstringOutput
from src.utils.code_extractor import CodeItem

def safe_json_loads(text: str):
    """Try to parse JSON correcting common formatting mistakes."""
    cleaned = re.sub(r',(\s*[}\]])', r'\1', text.strip())  # remove trailing commas
    cleaned = cleaned.replace('\r', '').replace('\x00', '')
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print("Error al parsear JSON incluso tras limpieza:", e)
        print("Contenido limpio:")
        print(cleaned)
        return None


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
        self.model_name = model_name
        self.agent.output_type = list[DocstringOutput]

    def _make_prompt(self, items: list[CodeItem]) -> str:
        """Concatenates the base prompt and item sources with imports at the top."""
        all_imports = set()
        for item in items:
            all_imports.update(getattr(item, "imports", []))
        imports_code = "\n".join(all_imports)

        formatted_items = [
            f"# File: {item.file_path}\n# {item.type} {item.name}\n{item.source}"
            for item in items
        ]
        items_code = "\n\n".join(formatted_items)
        return PROMPT_TEMPLATE_DOCSTRINGS + "\n" + imports_code + "\n\n" + items_code

    async def generate(self, items: list[CodeItem]) -> list[DocstringOutput]:
        """Generate improved or new docstrings."""
        prompt = self._make_prompt(items)

        try:
            result = await self.run(prompt)
        except Exception as e:  # capturamos cualquier error de ejecución
            print("⚠️ Error generando docstrings — usando fallback manual")
            print("Detalles:", e)
            # Cambiar a modo texto para parseo manual
            self.agent.output_type = str
            result_text = await self.run(prompt)
            parsed = safe_json_loads(result_text)
            if not parsed:
                print("=== 0 docstrings generados correctamente ===")
                return []
            return [DocstringOutput(**d) for d in parsed]

        print("=== RAW result ===")
        print(result)

        # Fallback manual if result is string
        if isinstance(result, str):
            parsed = safe_json_loads(result)
            if not parsed:
                print("=== 0 docstrings generados correctamente ===")
                return []
            return [DocstringOutput(**d) for d in parsed]

        return result
