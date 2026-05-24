SHELL := /bin/bash

PYTHON ?= python3
VENV ?= .venv
VENV_BIN := $(VENV)/bin
PYTHON_PATHS := scripts plugins/rubric-maker-skill/scripts plugins/rubric-maker-skill/skills
MARKDOWN_FIND := find . \( -path ./.git -o -path ./.copilot-tracking -o -path ./.ruff_cache -o -path ./.venv -o -path ./venv -o -path ./build -o -path ./dist \) -prune -o -type f -name '*.md' -print0

RUFF ?= $(shell if [ -x "$(VENV_BIN)/ruff" ]; then printf "$(VENV_BIN)/ruff"; else command -v ruff 2>/dev/null || printf ruff; fi)
TY ?= $(shell if [ -x "$(VENV_BIN)/ty" ]; then printf "$(VENV_BIN)/ty"; else command -v ty 2>/dev/null || printf ty; fi)
FLOWMARK ?= $(shell if [ -x "$(VENV_BIN)/flowmark" ]; then printf "$(VENV_BIN)/flowmark"; else command -v flowmark 2>/dev/null || printf flowmark; fi)
FLOWMARK_ARGS ?= --semantic --cleanups --width 88 --list-spacing preserve
FLOWMARK_WRITE_ARGS ?= --inplace --nobackup $(FLOWMARK_ARGS)

.PHONY: dev-install check format format-check lint ruff-lint ruff-format ruff-format-check typecheck ty-check flowmark-lint flowmark-format smoke

dev-install:
	$(PYTHON) -m venv $(VENV)
	$(VENV_BIN)/python -m pip install --upgrade pip
	$(VENV_BIN)/python -m pip install --group dev

check: lint format-check typecheck smoke

lint: ruff-lint flowmark-lint

format: ruff-format flowmark-format

format-check: ruff-format-check flowmark-lint

ruff-lint:
	$(RUFF) check $(RUFF_CHECK_ARGS) $(PYTHON_PATHS)

ruff-format:
	$(RUFF) format $(RUFF_FORMAT_ARGS) $(PYTHON_PATHS)

ruff-format-check:
	$(RUFF) format --check $(RUFF_FORMAT_ARGS) $(PYTHON_PATHS)

typecheck: ty-check

ty-check:
	$(TY) check $(TY_ARGS)

flowmark-lint:
	@set -euo pipefail; \
	status=0; \
	while IFS= read -r -d '' file; do \
		tmp=$$(mktemp); \
		$(FLOWMARK) $(FLOWMARK_ARGS) "$$file" > "$$tmp"; \
		if ! cmp -s "$$file" "$$tmp"; then \
			echo "flowmark would reformat $$file"; \
			status=1; \
		fi; \
		rm -f "$$tmp"; \
	done < <($(MARKDOWN_FIND)); \
	exit $$status

flowmark-format:
	@set -euo pipefail; \
	while IFS= read -r -d '' file; do \
		$(FLOWMARK) $(FLOWMARK_WRITE_ARGS) "$$file"; \
	done < <($(MARKDOWN_FIND))

smoke:
	python3 scripts/verify_plugin_compat.py
	python3 scripts/verify_schema_sync.py
	python3 scripts/verify_grade_sheet_schema_sync.py
	python3 scripts/smoke_test.py
