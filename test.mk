.PHONY: test-help test test-all test-accuracy

test-help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  test - Run the tests"
	@echo "  test-all - Run all tests"
	@echo "  test-accuracy - Run the accuracy tests"

test:
	python -m pytest tests/ -v -m "not slow"

test-all:
	python -m pytest tests/ -v -s

test-accuracy:
	python -m pytest tests/unit/test_accuracy.py -v -s
