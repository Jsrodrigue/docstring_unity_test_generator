import os

from dotenv import load_dotenv
from openai import OpenAI

############
# API KEYS #
############

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

############
# API URLS #
############

groq_url = "https://api.groq.com/openai/v1"

#####################
# CLIENT INSTANCES  #
#####################

# Client instances
openai_client = OpenAI(api_key=openai_api_key)
groq_client = OpenAI(api_key=groq_api_key, base_url=groq_url)

# Clients dictionary with models
clients = {
    "gpt-4o-mini": openai_client,  # OpenAI small model
    "llama-3.1-8b-instant": groq_client,  # Groq cheap model for testing
    "gpt-oss-20b": groq_client,  # Groq GPT OSS 20B medium
    "openai/gpt-oss-120b": groq_client,  # Groq GPT OSS 120B powerful
}


################################
# SYSTEM_PROMT AND BASE PROMPT #
################################

# System prompt
SYSTEM_PROMPT = """
You are a Python expert. Generate Python docstrings following best practices updated in 2025:
- Use triple double quotes (\"\"\") for the docstring.
- Include a brief description of what the function does.
- Include Args with type annotations and descriptions.
- Include Returns with type and description if applicable.
- Include Raises if the function can raise exceptions.
- Keep lines <= 79 characters.
- ONLY return the docstring text using triple double quotes, do NOT add explanations, 
  comments, code, or anything else.
- Do NOT include Markdown syntax (e.g., ```python) or any code formatting.
"""


# Prompt base template
PROMPT_TEMPLATE = """Write or improve the Python docstring for the following function.
- If the function already has a docstring, improve it following best practices.
- If it has no docstring, generate a new one. 
- Include description of what it does and its arguments.
- Return ONLY the docstring using triple double quotes (\"\"\").
- Do NOT add explanations, comments, or code blocks.
"""