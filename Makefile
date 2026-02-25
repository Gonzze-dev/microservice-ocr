VENV_DIR = virtual-env

activate:
	source $(VENV_DIR)/bin/activate

install: activate
	poetry install

start:
	python src/main.py

test:
	python -m pytest tests/ -v -m "not slow"

test-all:
	python -m pytest tests/ -v -s

test-accuracy:
	python -m pytest tests/unit/test_accuracy.py -v -s

