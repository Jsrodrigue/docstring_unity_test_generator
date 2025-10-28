import json

from src.constants import MAX_TOKENS, clients

#############################
# Helper to make the prompt #
#############################


def make_prompt(prompt_base, functions):
    """
    Constructs a prompt by appending function source codes to a base prompt.
    
    Args:
        prompt_base (str): The base prompt string.
        functions (list of dict): List of dictionaries containing function source codes.
    
    Returns:
        str: The constructed prompt string.
    """
    functions_code = "\n\n".join([f["source"] for f in functions])
    prompt = prompt_base + functions_code
    return prompt


######################################
# Function to generate docstrings ####
######################################


def generate_docstrings(
    functions,
    prompt_base,
    system_prompt=None,
    model="meta-llama/llama-4-scout-17b-16e-instruct",
):
    """
    Generate docstrings for multiple functions in a single LLM call.
    
    Args:
        functions (list of dict): List of dicts with keys 'name' and 'source'.
        prompt_base (str): The base prompt string.
        system_prompt (str, optional): The system prompt. Defaults to None.
        model (str, optional): Model name to use. Defaults to 'meta-llama/llama-4-scout-17b-16e-instruct'.
    
    Returns:
        list of dict: List of dicts with keys 'name' and 'docstring'.
    
    Raises:
        ValueError: If the model is not found in clients dictionary.
    """
    prompt = make_prompt(prompt_base, functions)

    if model not in clients:
        raise ValueError(f"Model '{model}' not found in clients dictionary.")
    client = clients[model]

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        max_tokens=MAX_TOKENS,
        response_format={"type": "text"},
    )
    raw_text = response.choices[0].message.content.strip()

    try:
        # Convert to list of dicts
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        print("Error parsing JSON from model output:", e)
        print("Raw output was:")
        print(response.choices[0].message.content)
        return []