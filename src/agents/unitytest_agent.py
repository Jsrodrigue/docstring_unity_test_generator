# agents/test_agent.py
from src.agents.base_agent import BaseCodeAgent

SYSTEM_PROMPT_TESTS = """
You are an expert Python tester specialized in writing unit tests with pytest.
Given source code, generate clear, minimal, and effective unit tests that
cover edge cases and normal scenarios.
"""

PROMPT_TEMPLATE_TESTS = """
Analyze the following Python code and generate pytest unit tests:
"""

class UnityTestAgent(BaseCodeAgent):
    def __init__(self, model_name="gpt-4o-mini"):
        super().__init__(
            name="Test Agent",
            system_prompt=SYSTEM_PROMPT_TESTS,
            model_name=model_name
        )

    async def generate_tests(self, code_snippets: list[dict]):
        prompt = PROMPT_TEMPLATE_TESTS + "\n\n".join([s["source"] for s in code_snippets])
        return await self.run(prompt)
