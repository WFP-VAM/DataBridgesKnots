#* Variables
SHELL := /usr/bin/env bash
PYTHON := python
PYTHONPATH := `pwd`/src

#* INSTALL

#* Install tools into isolated environment
#* Not needed if you have these already installed globally
.PHONY: install-tools
install-tools:
	uv tool install black
	uv tool install isort
	uv tool install ruff
	uv tool install mypy
	uv tool install bandit


#* Install dependencies and package
.PHONY: install
install:
	uv sync --all-extras --dev --frozen

#* LINTING

#* Check formatting
.PHONY: check-codestyle
check-codestyle:
	uv run isort --diff --check-only --settings-path pyproject.toml ./
	uv run black --diff --check --config pyproject.toml ./
	uv run ruff check .

#* Fix formatting
.PHONY: codestyle
codestyle:
	uv run isort --settings-path pyproject.toml ./
	uv run black --config pyproject.toml ./
	uv run ruff check . --fix

#* Tests
.PHONY: test
test:
	uv run pytest -c pyproject.toml --cov-report=html --cov=src/wfp_survey_toolbox tests/
	uv run coverage-badge -o assets/images/coverage.svg -f

#* Typing
.PHONY: mypy
mypy:
	uv run mypy --config-file pyproject.toml ./

.PHONY: check-safety
check-safety:
	uv run bandit -r src

#* All in one
.PHONY: lint
lint: test check-codestyle mypy

#* DOCS

#* Documentation
# Build documentation files into site folder
.PHONY: docs
docs:
	poetry run mkdocs build

# Render documentation on localhost
.PHONY: docs-serve
docs-serve:
	poetry run mkdocs serve

#* DOCKER

# Example: make docker-build VERSION=latest
# Example: make docker-build IMAGE=some_name VERSION=0.1.0
.PHONY: docker-build
docker-build:
	@echo Building docker $(IMAGE):$(VERSION) ...
	docker build \
		-t $(IMAGE):$(VERSION) . \
		-f ./docker/Dockerfile --no-cache

# Example: make docker-remove VERSION=latest
# Example: make docker-remove IMAGE=some_name VERSION=0.1.0
.PHONY: docker-remove
docker-remove:
	@echo Removing docker $(IMAGE):$(VERSION) ...
	docker rmi -f $(IMAGE):$(VERSION)


#* CLEANING

.PHONY: pycache-remove
pycache-remove:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

.PHONY: dsstore-remove
dsstore-remove:
	find . | grep -E ".DS_Store" | xargs rm -rf

.PHONY: mypycache-remove
mypycache-remove:
	find . | grep -E ".mypy_cache" | xargs rm -rf

.PHONY: ipynbcheckpoints-remove
ipynbcheckpoints-remove:
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf

.PHONY: pytestcache-remove
pytestcache-remove:
	find . | grep -E ".pytest_cache" | xargs rm -rf

.PHONY: build-remove
build-remove:
	rm -rf build/

.PHONY: cleanup
cleanup: pycache-remove dsstore-remove mypycache-remove ipynbcheckpoints-remove pytestcache-remove
