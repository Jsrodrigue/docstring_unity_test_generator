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
models = [
    "gpt-4o-mini",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
]

clients = {
    "gpt-4o-mini": openai_client,  # OpenAI model                $0.15/$0.60
    "meta-llama/llama-4-scout-17b-16e-instruct": groq_client,  # Groq Llama model            $0.11/$0.34
    "openai/gpt-oss-20b": groq_client,  # Groq GPT OSS 20B - cheaper  $0.075/$0.30
    "openai/gpt-oss-120b": groq_client,  # Groq GPT OSS 120B powerful  $0.15/$0.60
}
# Groq GPT OSS 120B powerful  $0.15/$0.60


####################################
# SYSTEM_PROMT AND TEMPLATE PROMPT #
####################################

# System prompt
SYSTEM_PROMPT = """
You are a Python expert. Review Python functions and their docstrings.

Rules:
- Description must explain what the function does.
- Args must list each parameter with type and description.
- Include Returns ONLY if function returns a value.
- Include Raises ONLY if applicable.
- Keep lines <= 79 characters.
- Only generate the docstring text, without triple quotes or formatting.
- Do NOT include Markdown, quotes, comments, or code blocks (e.g., starting with ```json or ```python).
- Always return a single string per docstring using '\n' for line breaks.
- Write in English.
- Only return JSON, nothing else. Do NOT add any extra text, explanations,
  introductions, or comments.

Instructions for output:
1. For each function, check if the docstring meets all best practices.
2. Only include functions whose docstrings are missing or incorrect.
3. If a docstring is fully correct, **do not include that function in the output**.
4. Return a JSON array of objects with:
   - "name": function name
   - "docstring": updated docstring
5. Do not modify functions unnecessarily.
"""


# Prompt base template
PROMPT_TEMPLATE = """
Generate or improve Python docstrings for the following functions.
Return a list of JSON objects, each with keys:
- "name": function name
- "docstring": the improved docstring
Only include functions that need modification; omit in the response those that are already correct.

Functions:

"""
