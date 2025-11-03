from typing import List, Optional
from src.core_base.generate.generator_manager import BaseGenerationManager
from src.unit_test_core.unit_test_agent import UnitTestAgent

class UnitTestGenerationManager(BaseGenerationManager):
    """
    Manager for generating docstrings from files or folders using a DocstringAgent.
    """
    agent_class = UnitTestAgent


# -----------------------------
# Wrapper function (CLI/Gradio)
# -----------------------------
async def generate_unit_test_from_path_dict(
    path: str,
    model_name: str = "gpt-4o-mini",
    target_names: Optional[List[str]] = None
) -> List[dict]:
    """
    Wrapper function for generating unit test from a file or folder.
    
    Args:
        path (str): Path to file or folder.
        model_name (str, optional): Model name to use.
        target_names (List[str], optional): Filter for specific function/class names.
    
    Returns:
        List[dict]: Generated unit test with metadata.
    """
    manager = UnitTestGenerationManager(model_name=model_name)
    return await manager.generate_for_path(path, target_names=target_names)


# -----------------------------
# Quick test 
# uv run python -m src.unit_test_core.unit_test_manager src\\docstring_core\\docstring_scanner.py
# -----------------------------
import asyncio

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "examples/"
    print(f"🔍 Running unit test generation on: {path}")
    results = asyncio.run(generate_unit_test_from_path_dict(path))
    print(f"✅ Generated {len(results)} test(s)")
    for r in results:
        print(f"\nFile: {r['file_path']}")
        print(f"\nImports: {r['imports']}")
        print(f"--- Test Output for {r['name']}---\n{r['test_code']}")