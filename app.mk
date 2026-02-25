VENV_DIR = virtual-env

.PHONY: app-help activate install start

app-help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  activate - Activate the virtual environment"
	@echo "  install - Install the dependencies"
	@echo "  start - Start the application"

activate:
	source $(VENV_DIR)/bin/activate

install:
	poetry install

start:
	python src/main.py