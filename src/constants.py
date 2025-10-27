import os

from dotenv import load_dotenv
from openai import OpenAI

#############
# PARAMETER #
#############

MAX_TOKENS = 1000

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

# Clients models and client dictionary
models = ["gpt-4o-mini",
          "meta-llama/llama-4-scout-17b-16e-instruct",
          "openai/gpt-oss-20b",
          "openai/gpt-oss-120b" ]

clients = {
    "gpt-4o-mini": openai_client,                                   # OpenAI model                $0.15/$0.60
    "meta-llama/llama-4-scout-17b-16e-instruct" : groq_client,      # Groq Llama model            $0.11/$0.34
    "openai/gpt-oss-20b": groq_client,                              # Groq GPT OSS 20B - cheaper  $0.075/$0.30
    "openai/gpt-oss-120b": groq_client                              # Groq GPT OSS 120B powerful  $0.15/$0.60
}
                        # Groq GPT OSS 120B powerful  $0.15/$0.60


####################################
# SYSTEM_PROMT AND TEMPLATE PROMPT #
####################################

# System prompt 
SYSTEM_PROMPT = """
You are a Python expert. Generate Python docstrings following best practices 
updated in 2025:
- Include a brief description of what the function does.
- Include Args with type annotations and descriptions.
- Include Returns with type and description only if the function actually 
  returns a value.
- Include Raises if the function can raise exceptions.
- Keep lines <= 79 characters.
- ONLY generate the docstring text, without triple quotes or any additional 
  formatting.
- Correct any formatting errors in existing docstrings.
- Do NOT add explanations, comments, code, or anything else.
- Do NOT include Markdown syntax (e.g., ```python) or any code formatting.
- Write all the docstring in English.
- If there is nothing to improve, return the original docstring unchanged.
- Always return a JSON array of objects, each with keys:
  - "name": function name
  - "docstring": the improved or generated docstring (without triple quotes or any aditional formatation)
 
"""


# Prompt base template
PROMPT_TEMPLATE = """
  Generate or improve Python docstrings for the following functions.
  Return a JSON array of objects, each with keys:
  - "name": function name
  - "docstring": the improved or generated docstring (without triple quotes or any aditional formatation)

  Functions:
  {functions_code}
"""
