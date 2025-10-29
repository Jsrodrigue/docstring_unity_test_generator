from agents import Agent, Runner, OpenAIChatCompletionsModel
from src.constants import SYSTEM_PROMPT, PROMPT_TEMPLATE, clients
from src.docstring_core.docstring_class import DocstringList, DocstringOutput

# -----------------------------
# Funciones
# -----------------------------
def make_prompt(prompt_base: str, items: list[dict]) -> str:
    """
    Constructs a prompt by concatenating the base prompt and item sources.
    
    Args:
        prompt_base (str): The base string to prepend to the items.
        items (list[dict]): A list of dictionaries containing item data,
            expected to include a 'source' key in each dictionary.
    
    Returns:
        str: The combined prompt string containing the base prompt and item sources.
    """
    items_code = "\n\n".join([item["source"] for item in items])
    return prompt_base + items_code

async def generate_docstrings(
    items: list[dict],
    model_name: str = "gpt-4o-mini",
    prompt_base: str = PROMPT_TEMPLATE,
    system_prompt: str | None = None,
) -> list[DocstringOutput]:
    """
    Asynchronously generates docstrings for a list of items using the specified model.
    
    Args:
        items (list[dict]): A list of dictionaries representing items for which
            docstrings should be generated.
        model_name (str, optional): The name of the model to use for generation.
            Defaults to 'gpt-4o-mini'.
        prompt_base (str, optional): The base prompt template to use. Defaults to
            the 'PROMPT_TEMPLATE'.
        system_prompt (str | None, optional): An optional system prompt providing
            instructions to the model. Defaults to None.
    
    Returns:
        list[DocstringOutput]: A list of generated docstring outputs.
    
    Raises:
        ValueError: If the specified model name is not found in the clients
            dictionary.
    """
    if model_name not in clients:
        raise ValueError(f"Model '{model_name}' not found in clients dictionary.")

    prompt = make_prompt(prompt_base, items)
    client = clients[model_name]

    # Crear el modelo según el cliente
    model_obj = OpenAIChatCompletionsModel(model=model_name, openai_client=client)

    # Crear el Agent y Runner
    agent = Agent(
        name="Docstring Generator",
        instructions=system_prompt or SYSTEM_PROMPT,
        output_type=DocstringList,
        model=model_obj,
    )
    result = await Runner.run(agent, prompt)
    return result.final_output.items