# Python Environment
PYTHON=python
PIP=pip

# Paths
VENV_DIR=venv

# Detect OS and set VENV_BIN accordingly
ifeq ($(OS),Windows_NT)
	VENV_BIN=$(VENV_DIR)/Scripts
else
	VENV_BIN=$(VENV_DIR)/bin
endif

# Install dependencies
install:
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_BIN)/$(PYTHON) -m pip install --upgrade pip setuptools wheel
	$(VENV_BIN)/$(PIP) install -r requirements.txt

# Run Fastapi server
run:
	$(VENV_BIN)/uvicorn main:app --host 0.0.0.0 --port 8000

# Clean up pyc files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Show help
help:
	@echo "Makefile for Fastapi service"
	@echo "Usage:"
	@echo "  make install        - Install dependencies"
	@echo "  make run            - Run Fastapi development server"
	@echo "  make clean          - Clean up pyc files"
