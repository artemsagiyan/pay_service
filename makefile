format:
	@echo "formatting..."
	poetry run ruff format app

types:
	@echo "checking types..."
	poetry run mypy app


migration:
	@echo "running migrations..."
	alembic revision --autogenerate -m "inittial migration1"

