# ============================================================
# 🧠 Docstring Auto-Generator CLI
#
# Usage examples:
#   make docstring-generate path=examples/
#   make docstring-generate path=examples/ names=greet
#   make docstring-generate path=examples/ project=. model=gpt-4o
#   make docstring-generate path=src model=gpt-4o-mini names=main,App
#   make docstrings path=examples/
#
# Notes:
# - All arguments are optional except 'path'.
# - 'project' is optional (used for indexing a root project).
# - 'model' defaults to gpt-4o-mini if not provided.
# ============================================================

# Default values
path ?= examples/
project ?=
names ?=
model ?= gpt-4o-mini

# Absolute path to uv (change if needed)
UV := /c/Users/Juan/.local/bin/uv

.PHONY: docstring-generate
docstring-generate:
	@echo "[INFO]Generating docstrings..."
	@args=""; \
	if [ -n "$(path)" ]; then args="$$args $(path)"; fi; \
	if [ -n "$(project)" ]; then args="$$args --project $(project)"; fi; \
	if [ -n "$(names)" ]; then args="$$args --names $(names)"; fi; \
	if [ -n "$(model)" ]; then args="$$args --model $(model)"; fi; \
	echo "[INFO] Running: $(UV) run python -m src.cli docstring scan-and-generate $$args"; \
	$(UV) run python -m src.cli docstring scan-and-generate $$args

# Alias corto
.PHONY: docstrings
docstrings: docstring-generate
