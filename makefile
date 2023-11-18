# Variables
PYTHON = python3
PIP = $(PYTHON) -m pip
PYTEST = $(PYTHON) -m pytest

SERVICE_PATH = src
TESTS_PATH = tests
LOG_PATH = log

VENV_PATH = _venv
REQUIREMENTS_PATH = requirements.txt
# DEV_REQUIREMENTS_PATH = requirements/dev.txt

.PHONY: install help black isort autoflake speedtest cleanup flake8 test

autoflake:
	autoflake --in-place --remove-all-unused-imports --ignore-init-module-imports -r $(SERVICE_PATH)

black:
	black $(SERVICE_PATH)
	black $(TESTS_PATH)

cleanup: isort black autoflake


help:
	@echo "Available targets:"
	@echo "  install       - Install required dependencies"
	@echo "  prod      	   - Run the FastAPI application in production mode"
	@echo "  dev           - Run the FastAPI application in development mode with hot-reloading"
	@echo "  black         - Format code using black"
	@echo "  isort         - Sort imports using isort"
	@echo "  autoflake     - Remove unused imports and variables"

isort:
	isort $(SERVICE_PATH)
	isort $(TESTS_PATH)

install:
	$(PIP) install -r $(REQUIREMENTS_PATH)

flake8:
	flake8 --tee . > _flake8Report.txt

# speedtest:
# 	if [ ! -f example/http_request.so ]; then gcc -shared -o example/http_request.so example/http_request.c -lcurl -fPIC; fi
# 	python3 example/loop_c.py

test:
	pre-commit run -a
	pytest
# sed -i 's|<source>/workspaces/DevSetGo_Toolkit</source>|<source>/github/workspace/DevSetGo_Toolkit</source>|' /workspaces/DevSetGo_Toolkit/coverage.xml
# coverage-badge -o coverage.svg -f

run:
	python3 src/main.py