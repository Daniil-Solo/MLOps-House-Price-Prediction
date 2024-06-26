#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = mlops-course
PYTHON_INTERPRETER = poetry run python

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies
poetry:
	pip install poetry

prod-requirements: poetry
	poetry install --only main

dev-requirements: poetry
	poetry install --with main --with dev

docs-requirements: poetry
	poetry install --with main --with docs

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using ruff
ruff-lint:
	$(PYTHON_INTERPRETER) -m ruff check src

ruff-format:
	$(PYTHON_INTERPRETER) -m ruff format src

black-codestyle:
	$(PYTHON_INTERPRETER) -m black --check src

mypy-type-checking:
	$(PYTHON_INTERPRETER) -m mypy src

## Data
raw-data:
	$(PYTHON_INTERPRETER) src/data/download_data.py data/raw/data.csv

clean-data:
	$(PYTHON_INTERPRETER) src/features/clean_raw_data.py data/raw/data.csv data/interim/cleaned_data.csv

amenities:
	$(PYTHON_INTERPRETER) src/features/download_amenities.py -a pub -a cafe -a fast_food -a restaurant data/external/eat.json
	$(PYTHON_INTERPRETER) src/features/download_amenities.py -a college -a kindergarten -a library -a school -a university data/external/edu.json
	$(PYTHON_INTERPRETER) src/features/download_amenities.py -a cinema -a fountain -a theatre data/external/culture.json
	$(PYTHON_INTERPRETER) src/features/download_amenities.py -a clinic -a hospital data/external/health.json

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################
