from typing import List
from src.core_base.code.code_model import CodeItem
from src.core_base.agents.base_agents import BaseCodeGenerationAgent

async def generate_outputs_for_items(agent: BaseCodeGenerationAgent, items: List[CodeItem], output_key: str) -> List[dict]:
    """
    Generic helper to generate structured outputs (e.g. docstrings, unit tests) 
    for a list of CodeItem objects using the provided agent.

    Args:
        agent (BaseCodeGenerationAgent): The agent responsible for generating structured output.
        items (List[CodeItem]): List of code items to process.
        output_key (str): The key name for the generated content (e.g., "docstring" or "unittest_code").

    Returns:
        List[dict]: A list of dictionaries containing the generated data and metadata.
    """
    generated = await agent.generate(items)
    results = []

    for item in items:
        match = next((g for g in generated if g.name == item.name), None)
        if match:
            results.append({
                "name": match.name,
                output_key: getattr(match, output_key, None),
                "file_path": str(item.file_path),
                "source": item.source,
                "original": getattr(item, output_key, None),
            })

    return results

