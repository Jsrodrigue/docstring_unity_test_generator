# agents/orchestrator_agent.py
from pathlib import Path
from agents.base_agent import BaseCodeAgent
from agents.docstring_agent import DocstringAgent
from src.agents.unitytest_agent import UnityTestAgent
from src.utils.code_extractor import CodeExtractorTool
from tools import make_doc_tool, make_test_tool, make_extract_tool
from constants import SYSTEM_PROMPT_ORCHESTRATOR

class OrchestratorAgent(BaseCodeAgent):
    """
    Orchestrator agent that coordinates code analysis, docstring generation,
    and unit test creation. Uses external tools for extraction, docstrings,
    and tests to keep the agent lightweight.
    """
    def __init__(self, base_path: str, model_name="gpt-4o-mini"):
        super().__init__(
            name="Orchestrator",
            system_prompt=SYSTEM_PROMPT_ORCHESTRATOR,
            model_name=model_name
        )

        # Sub-agents
        self.doc_agent = DocstringAgent(model_name)
        # self.test_agent = UnityTestAgent(model_name)  # UNCOMENT FOR UNITY TEST
        self.extractor = CodeExtractorTool(Path(base_path))

        # Tools
        self.tools = [
            make_doc_tool(self.doc_agent),
            # make_test_tool(self.test_agent),  # UNCOMENT FOR UNITY TEST
            make_extract_tool(self.extractor)
        ]