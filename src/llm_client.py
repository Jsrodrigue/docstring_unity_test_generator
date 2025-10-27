from src.constants import clients

##################################
# Function to generate docstring
##################################

def generate_docstring_from_source(
    func_source, 
    model="llama-3.1-8b-instant", 
    backend="openai",
    prompt_template=None,
    system_prompt=None
):
    """
    Generate a Python docstring for a given function source code using an LLM.

    Args:
        func_source: str, the full source code of the function
        model: str, name of the model to use
        backend: str, "openai" or "groq"
        prompt_template: str, base user prompt to prepend before the function code
        system_prompt: str, system prompt to guide the LLM behavior

    Returns:
        str: generated docstring
    """
    if prompt_template is None:
        raise ValueError("prompt_template must be provided")
    if system_prompt is None:
        raise ValueError("system_prompt must be provided")

    prompt = prompt_template + "\nFunction:\n" + func_source

    if backend not in ["openai", "groq"]:
        raise ValueError(f"Unknown backend: {backend}")
    
    if model not in clients:
        raise ValueError(f"Model '{model}' not found in clients dictionary.")
    
    client = clients[model]

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": prompt}],
        max_tokens=200
    )

    return response.choices[0].message.content.strip()
