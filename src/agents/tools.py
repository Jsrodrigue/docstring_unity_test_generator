# tools.py
from openai import function_tool
from typing import List
from agents.docstring_agent import DocstringAgent
from src.agents.unitytest_agent import UnityTestAgent
from src.utils.code_extractor import CodeExtractorTool, CodeItem
from src.models.docstring_models import DocstringOutput

def make_doc_tool(doc_agent: DocstringAgent):
    @function_tool(
        name="generate_docstrings",
        description="Generates or improves Python docstrings for functions and classes."
    )
    async def tool(items: List[CodeItem]) -> List[DocstringOutput]:
        # Convert CodeItem to dict for the DocstringAgent
        items_dicts = [ci.__dict__ for ci in items]
        # Llamada al agente para generar docstrings
        updated_outputs: List[DocstringOutput] = await doc_agent.generate(items_dicts)
        # Actualizamos los CodeItems con la info de DocstringOutput
        return updated_outputs
    return tool

def make_test_tool(test_agent: UnityTestAgent):
    @function_tool(
        name="generate_unity_tests",
        description="Generates unit tests for Python functions/classes."
    )
    async def tool(items: List[CodeItem]) -> List[str]:
        return await test_agent.generate_tests([ci.__dict__ for ci in items])
    return tool

def make_extract_tool(extractor: CodeExtractorTool):
    @function_tool(
        name="extract_code_items",
        description="Extracts all functions and classes from a Python path."
    )
    async def tool() -> List[CodeItem]:
        return extractor.extract_from_path()
    return tool
