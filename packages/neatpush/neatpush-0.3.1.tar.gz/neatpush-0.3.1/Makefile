.DEFAULT_GOAL := all
black = black neatpush tests
ruff = ruff neatpush tests

.PHONY: install
install:
	pip install -U pip
	pip install -e .[all]
	pre-commit install -t pre-push

.PHONY: format
format:
	$(ruff) --fix
	$(black)

.PHONY: lint
lint:
	ruff neatpush/ tests/
	$(black) --check

.PHONY: mypy
mypy:
	mypy --cache-fine-grained neatpush

.PHONY: test
test:
	pytest

.PHONY: all
all: lint mypy test

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '.*DS_Store'`
	rm -rf .cache
	rm -rf .*_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -rf .eggs
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	rm -rf public
	rm -rf .hypothesis
	rm -rf .profiling
