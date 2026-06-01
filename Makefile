help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

dev: ## Run dev server
	uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

test: ## Run tests
	pytest tests/ -v --cov=src

lint: ## Lint code
	black src/ tests/
	isort src/ tests/
	ruff check src/ tests/

docker-up: ## Start Docker
	docker-compose up -d

docker-down: ## Stop Docker
	docker-compose down

clean: ## Clean artifacts
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache htmlcov .coverage
