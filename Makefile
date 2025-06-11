run-compose = docker compose -f docker-compose.yaml

up:
	@echo "Starting/attaching to stack. Use CTRL+C to stop."
	$(run-compose) up

build:
	$(run-compose) build

# Run ruff linter on the backend directory and automatically fix issues
shell/lint:
	ruff check src/ --fix

# Format the backend code using ruff
shell/format:
	ruff check --config=pyproject.toml backend --fix --select I --exclude "migrations"
	ruff format src --exclude "migrations"