# agents/base_agent.py
from agents import Agent, Runner, OpenAIChatCompletionsModel
from constants import clients

class BaseCodeAgent:
    def __init__(self, name: str, system_prompt: str, model_name: str = "gpt-4o-mini"):
        if model_name not in clients:
            raise ValueError(f"Model '{model_name}' not found in clients dictionary.")
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
