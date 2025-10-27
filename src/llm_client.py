import json
from src.constants import clients

#############################
# Helper to make the prompt #
#############################

def make_prompt(prompt_template, functions):
  functions_code = "\n\n".join([f['source'] for f in functions])
  prompt = prompt_template.format(functions_code=functions_code)
  return prompt

######################################
# Function to generate docstrings ####
######################################

def generate_docstrings(functions, prompt_template, system_prompt=None, model="openai/gpt-oss-20b"):
    """
    Generate docstrings for multiple functions in a single LLM call.

    Args:
        functions: list of dicts with keys 'name' and 'source'
        model: str, model name to use

    Returns:
        list of dicts with keys 'name' and 'docstring'
    """
    prompt = make_prompt(prompt_template, functions)
    
    if model not in clients:
        raise ValueError(f"Model '{model}' not found in clients dictionary.")
    client = clients[model]

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000, 
        response_format={"type": "text"}
    )

    raw_text = response.choices[0].message.content.strip()

    try:
        # Conviert the json
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        print("Error parsing JSON from model output:", e)
        print("Raw output was:")
        print(response.choices[0].message.content)
        return []
