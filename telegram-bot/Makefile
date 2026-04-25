install:
	pip install -r requirements.txt
	pip install ruff mypy pytest pre-commit

lint:
	ruff check .
	ruff format --check .

typecheck:
	mypy .

check: lint typecheck

ci: install check