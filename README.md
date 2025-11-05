
# Docstring & Unit Test Generator

Automate docstring and unit test creation for Python projects using LLMs. Provides both a CLI and a web UI so teams can quickly increase documentation quality and test coverage with minimal manual work.


## Summary
Generates docstrings and pytest tests from your source code using configurable LLMs. Try the web UI or run it from the CLI.

## Why it matters
- Save developer time by auto-creating high-quality docstrings.
- Produce realistic unit tests that mirror your project structure.
- Keep your codebase well-documented and more maintainable, accelerating onboarding and code reviews.

## Quick demo
Run the web UI:
```bash
python app_gradio.py
# Open http://localhost:7860
```

Generate docstrings from the CLI:
```bash
python -m src.cli docstring generate ./src --model gpt-4o-mini
```

Generate unit tests:
```bash
python -m src.cli unit_test generate ./src --project ./ --model gpt-4o
```

## Screenshots



## Demo video


## Features
- Safe docstring insertion (Injects only the docstring)
- Mirrors your project tree into `tests/` and creates pytest-style test files.
- CLI (Typer) + Web UI (Gradio).
- Modular LLM execution layer; swap or add models easily.
- Configurable: select models, specific functions/classes, and style (Google/NumPy).

## Installation

Unix / macOS:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Optional (install editable package from source):
```bash
pip install -e .
```

If you prefer the `pyproject.toml` workflow, you can also use `poetry` or `uv` — but providing `requirements.txt` is recommended for quick testing.

### API Keys & Supported Models

This tool supports multiple LLM providers. You'll need to set up API keys in your environment:
```bash
OPENAI_API_KEY=your-key-here    # For gpt-4o-mini
GROQ_API_KEY=your-key-here      # For Llama and GPT-OSS models
```

Supported models:
- OpenAI: `gpt-4o-mini`
- Groq: 
  - `meta-llama/llama-4-scout-17b-16e-instruct`
  - `openai/gpt-oss-20b`
  - `openai/gpt-oss-120b`

Select models via `--model` flag in CLI or environment variables. 

The selection of models can be easly customizable by modifing the `constants.py` file.

## Minimal example (input → output)

Input file (before):
```python
def add(a, b):
   return a + b
```

Suggested docstring (after):
```python
def add(a, b):
    """
    Return the sum of two numbers.
    
    Args:
      a (int or float): The first number.
      b (int or float): The second number.
    Returns:
      int or float: The sum of the two numbers.
    """
    return a + b
```

Generated pytest (example):
```python
def test_add():
   assert add(1, 2) == 3
```

## How it works (high level)
1. Scanner: parses the codebase and finds functions/classes.
2. LLM agent: generates docstrings or test code using prompts. 
3. Generator: formats outputs (Google/NumPy style) and writes mirrored files under `tests/`.
4. Review: user can preview and accept changes in docstring via the Gradio UI.

## Agents & Pipelines

This project uses a modular agent architecture where agents process Python files one at a time and return structured items (`DocstringOutput` and `UnitTestOutput` objects) containing the generated content and metadata.

### Agent Types & Responsibilities

- **Docstring Agent** (single-agent flow)
  - Processes one file at a time using `CodeExtractorTool`
  - For each function/class found, generates a Google/NumPy-style docstring
  - Returns a list of `DocstringOutput` generated content.

- **Unit Test Pipeline** (two-agent flow: Generator → Reviewer)
  - Generator agent:
    - Processes one source file at a time
    - Returns test `UnitTestOutput` objects with generated pytest functions
    - Includes necessary imports and fixtures in metadata
  - Reviewer agent:
    - Takes the generated file content.
    - Validates tests, imports, and assertions
    - Returns fixed test code or validation report

### Processing Flow

1. IndexScanner finds Python files and extracts `CodeItem` objects
2. Agents process files one by one:
   ```
   module.py → [CodeItem1, CodeItem2, ...] → Generator → Reviewer → Final Items
   ```
3. Review (only for docstring) and write.


### Benefits of File-based Processing

- Granular control: accept/reject changes per function
- Better context: each item includes its imports and dependencies
- Efficient processing: only changed files are reprocessed
- Safe execution: process one file at a time, handle errors gracefully

### Configuration

- Models are configurable via CLI flags or in the gradio app.
- Each agent can use a different model (e.g., faster model for review)
- Processing can be parallelized across files (but serial within each file)

## Run tests
```bash
pytest -q
```

## Project structure (high level)
- `src/` — main implementation modules (CLI, generators, executors, agents).
- `examples/` — sample usage and quick demos.
- `tests/` — unit tests (auto-generated tests appear here).
- `app_gradio.py` — launch Gradio web UI.

## Indexing (ProjectIndexer)

This project includes an incremental project indexer that scans your Python codebase and extracts "code items" (functions, classes, imports, etc.) for fast lookup and context. The indexer is implemented in `src/core_base/indexer/project_indexer.py` and provides an efficient workflow for large repositories.

Key points:

- Storage: index data is stored under the project directory in `.code_index/`:
  - `.code_index/indexes/` — per-file pickles with extracted CodeItems (one `.pkl` per source file).
  - `.code_index/hashes/file_hashes.pkl` — a mapping of file paths to SHA1 hashes used to detect changes.
- Incremental updates: the indexer computes a SHA1 hash for each `.py` file and only reprocesses files that are new or whose hash changed. Deleted files are removed from the index folder.
- Safe scanning: hidden folders and `__pycache__` are skipped when scanning the tree.


## License
This project is licensed under the MIT License — see the `LICENSE` file in this repository for details.

