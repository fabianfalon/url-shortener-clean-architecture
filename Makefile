run-compose = docker compose -f docker-compose.yaml

up:
	@echo "Starting/attaching to stack. Use CTRL+C to stop."
	$(run-compose) up

build:
	$(run-compose) build