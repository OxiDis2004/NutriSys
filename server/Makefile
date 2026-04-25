install:
	pip install -r requirements.txt
	pip install ruff mypy pytest pre-commit

lint:
	ruff check .
	ruff format --check .

typecheck:
	mypy .

test:
	pytest

check: lint typecheck test

ci: install check