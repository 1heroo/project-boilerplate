COMPOSE := $(shell docker compose version >/dev/null 2>&1 && echo "docker compose" || echo "docker-compose")

help: ## Показать список команд
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
.PHONY: help

install: ## Установить зависимости (poetry, .venv в проекте)
	@poetry install
.PHONY: install

requirements: ## Синхронизировать requirements.txt для Docker
	@poetry show --only main --no-ansi | awk '{print $$1"=="$$2}' > requirements.txt
.PHONY: requirements

config: ## Создать configs/prod.toml из примера
	@test -f configs/prod.toml || cp configs/prod.toml.example configs/prod.toml
.PHONY: config

run: ## Публичный API (:8000)
	@uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
.PHONY: run
{%- if cookiecutter.use_metrics %}

metrics: ## Metrics-апка (:8002, /metrics)
	@uvicorn src.metrics:app --host 0.0.0.0 --port 8002
.PHONY: metrics
{%- endif %}
{%- if cookiecutter.use_kafka %}

broker: ## Kafka consumers (FastStream, health :8004)
	@faststream run src.broker:app --port 8004
.PHONY: broker
{%- endif %}
{%- if cookiecutter.use_taskiq %}

taskiq: ## Taskiq worker (health :8003)
	@taskiq worker src._taskiq:broker
.PHONY: taskiq

taskiq-scheduler: ## Taskiq scheduler (ровно один экземпляр)
	@taskiq scheduler src._scheduler:scheduler
.PHONY: taskiq-scheduler
{%- endif %}

migrate: ## Накатить миграции Postgres
	@alembic upgrade head
.PHONY: migrate

migration: ## Новая миграция: make migration m="add foo"
	@alembic revision --autogenerate -m "$(m)"
.PHONY: migration

infra-up: ## Поднять dev-инфраструктуру
	@$(COMPOSE) -f docker-compose.dev.yml up -d
.PHONY: infra-up

infra-down: ## Остановить dev-инфраструктуру
	@$(COMPOSE) -f docker-compose.dev.yml down
.PHONY: infra-down

infra-ps: ## Статус dev-инфраструктуры
	@$(COMPOSE) -f docker-compose.dev.yml ps
.PHONY: infra-ps

lint: ## ruff check
	@ruff check src tests
.PHONY: lint

format: ## ruff format
	@ruff format src tests
.PHONY: format

test: ## Все тесты
	@pytest
.PHONY: test

test-unit: ## Только юнит-тесты (без инфраструктуры)
	@pytest -m "not integration"
.PHONY: test-unit
