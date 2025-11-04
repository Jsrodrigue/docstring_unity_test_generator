from agents import Agent, Runner, OpenAIChatCompletionsModel
from constants import clients
from typing import Type, List
from pathlib import Path
from src.core_base.code.code_model import CodeItem
from src.core_base.code.json_utils import safe_json_loads
from src.core_base.indexer.project_indexer import ProjectIndexer
from src.core_base.code.extractor_utils import extract_symbols_from_import

###############################
# Base Agent
###############################
class BaseCodeAgent:
    """
    Represents an agent that utilizes a specified model to process input text.
    """

    def __init__(self, name: str, system_prompt: str, model_name: str = "gpt-4o-mini"):
        if model_name not in clients:
            raise ValueError(f"Model '{model_name}' not found in clients dictionary.")

        self.model_name = model_name
        client = clients[model_name]
        model_obj = OpenAIChatCompletionsModel(model=model_name, openai_client=client)
        self.agent = Agent(
            name=name,
            instructions=system_prompt,
            output_type=str,
            model=model_obj,
        )

    async def run(self, input_text: str) -> str:
        result = await Runner.run(self.agent, input_text)
        return result.final_output


###############################
# Base Code Generation Agent
###############################
class BaseCodeGenerationAgent(BaseCodeAgent):
    """
    Base agent for generating structured code outputs such as docstrings, tests, etc.
    """

    OutputModel: Type
    SYSTEM_PROMPT: str
    PROMPT_TEMPLATE: str

    def __init__(self, model_name: str, project_path: Path | None = None):
        super().__init__(
            name=self.__class__.__name__,
            system_prompt=self.SYSTEM_PROMPT,
            model_name=model_name,
        )

        self.agent.output_type = list[self.OutputModel]
        self.project_path = project_path

        # Initialize indexer *only if* project_path is provided
        self.indexer = None
        if project_path:
            self.indexer = ProjectIndexer(project_path)
            self.indexer.load_or_build()

    ##########################################################
    # Helper: Summarize code edges for import context
    ##########################################################
    def _summarize_code_edges(self, source: str, head: int = 10, tail: int = 5) -> str:
        lines = source.strip().splitlines()
        if len(lines) <= head + tail:
            return "\n".join(lines)
        return "\n".join(
            lines[:head]
            + ["# ... (middle omitted for brevity) ..."]
            + lines[-tail:]
        )

    ##########################################################
    # Prompt Construction
    ##########################################################
    def _make_prompt(self, items: List[CodeItem]) -> str:
        """
        Build a complete prompt including:
        - Import statements
        - Optional project import snippets (only edges)
        - Target items (full code)
        """
        # === Gather imports
        all_imports = set()
        for item in items:
            if getattr(item, "imports", None):
                all_imports.update(item.imports)

        imports_code = "\n".join(sorted(all_imports)) if all_imports else "# No imports detected"

        # === Internal context (only if indexer is available)
        own_code_block = "# Context disabled (no project indexer)"
        if self.indexer:
            own_imports_code = []
            for imp in all_imports:
                symbols = extract_symbols_from_import(imp)
                for sym in symbols:
                    matches = self.indexer.query_by_name(sym)
                    for match in matches:
                        if not match:
                            continue
                        snippet = (
                            f"# Context snippet from {match.file_path}, DO NOT generate anything for this item\n"
                            f"# {match.type} {match.name}\n"
                            f"{self._summarize_code_edges(match.source)}"
                        )
                        own_imports_code.append(snippet)
            own_code_block = (
                "\n\n".join(own_imports_code)
                if own_imports_code
                else "# No internal import snippets found"
            )

        # === Target items
        formatted_items = [
            f"# File: {item.file_path}\n# {item.type} {item.name}\n{item.source.strip()}"
            for item in items
        ]
        items_code = "\n\n".join(formatted_items)

        # === Combine prompt
        prompt_parts = [
            self.PROMPT_TEMPLATE,
            "\n# === IMPORT STATEMENTS ===\n",
            imports_code,
            "\n\n# === OWN IMPORT CODE SNIPPETS ===\n",
            own_code_block,
            "\n\n# === TARGET ITEMS ===\n# Generate only for these items\n",
            items_code,
        ]

        prompt = "".join(prompt_parts)
        print(f"--- DEBUG PROMPT ---\n{prompt}\n--- END PROMPT ---")
        return prompt


    ##########################################################
    # Run generation
    ##########################################################
    async def generate(self, items: List[CodeItem]) -> List:
        prompt = self._make_prompt(items)

        try:
            result = await self.run(prompt)
        except Exception as e:
            print(f"⚠️ Error generating {self.__class__.__name__} output — using manual fallback")
            print("Details:", e)
            self.agent.output_type = str
            result_text = await self.run(prompt)
            parsed = safe_json_loads(result_text)
            if not parsed:
                return []
            return [self.OutputModel(**d) for d in parsed]

        if isinstance(result, str):
            parsed = safe_json_loads(result)
            if not parsed:
                return []
            return [self.OutputModel(**d) for d in parsed]

        return result
