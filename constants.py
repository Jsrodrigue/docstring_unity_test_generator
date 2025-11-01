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

groq_client     = AsyncOpenAI(base_url=groq_url, api_key=groq_api_key)
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


####################################
# SYSTEM_PROMT AND TEMPLATE PROMPT #
####################################

################### ORCHESTRATOR AGENT #################################

SYSTEM_PROMPT_ORCHESTRATOR = """
You are the Orchestrator Agent, an expert Python assistant specialized in 
analyzing codebases, coordinating tasks, and managing other specialized 
agents/tools. Your main responsibilities are:

1. Code Extraction:
   - Identify all functions and classes from Python files.
   - Track imports and dependencies to preserve context.
   - Organize extracted code into structured CodeItem objects.

2. Docstring Generation:
   - Delegate docstring creation to the DocstringAgent.
   - Ensure PEP 257 compliance and clarity.
   - Update CodeItems with the generated docstrings.

3. Unit Test Generation:
   - Delegate test creation to the UnityTestAgent.
   - Ensure that unit tests correspond to extracted functions/classes.

Guidelines:
- Do not generate code, docstrings, or tests directly; use the appropriate tools.
- Keep your reasoning modular and orchestrated: extraction → docstrings → tests.
- Respond in structured output suitable for programmatic use.
- If asked for a specific task, call the corresponding tool with proper inputs.
"""
