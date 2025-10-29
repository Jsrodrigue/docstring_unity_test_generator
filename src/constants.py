import os

from dotenv import load_dotenv
from openai import AsyncOpenAI
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

###########
# CLIENTS #
###########

GROQ_BASE_URL = "https://api.groq.ai"

groq_client     = AsyncOpenAI(base_url=GROQ_BASE_URL, api_key="GROQ_API_KEY")
openai_client   = AsyncOpenAI()


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
You are a Python expert specializing in writing clear, standardized docstrings 
following PEP 257 and the best practices for 2025.

Your task is to review the provided Python functions and classes, and 
generate or improve their docstrings only when necessary.

Rules:
- If a function or class already has a complete, well-written docstring, skip it (do not include it in the output).
- If it lacks a docstring, or the existing one can be improved for clarity, completeness, or consistency, include it.
- Clearly describe what the function or class does.
- Include Args with types and concise descriptions.
- Add Returns, Raises, or Attributes if relevant.
- Keep lines readable and concise (<= 79 characters ideally).
- Do NOT include code, markdown, triple quotes, or comments.
- The output must only contain updated or newly generated docstrings.
"""



# Prompt base template
PROMPT_TEMPLATE = """
Analyze the following Python functions and classes.
Generate improved docstrings only for those that need changes.

Functions and classes:
"""
