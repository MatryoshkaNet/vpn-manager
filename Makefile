UV_RUN = uv run

DOCS_SOURCE_DIR = docs/source/
DOCS_BUILD_DIR = docs/build/

.PHONY: install-uv
install-uv: ## Install uv if missing
	@echo "Install uv."
	@which uv > /dev/null || (curl -LsSf https://astral.sh/uv/install.sh | sh)


.PHONY: install-depends
install-depends: install-uv ## Install depends
	@echo "Install depends"
	@uv sync --all-extras


.PHONY: install-pre-commit
install-pre-commit: install-depends ## Install pre-commit
	@echo "Install pre-commit"
	@$(UV_RUN) pre-commit install

.PHONY: install
install: install-uv install-depends install-pre-commit ## Install dependencies and setup env

.PHONY: format
format-code: ## Format code
	@echo "Run formatters"
	@$(UV_RUN) ruff format --preview

.PHONY: lint
lint-code: ## Lint code
	@echo "Run linters"
	@$(UV_RUN) mypy --pretty
	@$(UV_RUN) ruff check --no-fix

.PHONY: tests
tests: ## Run tests
	@echo "Run tests"
	@$(UV_RUN) pytest

.PHONY: coverage
coverage: tests # Run coverage tests
	@echo "Run coverage tests"
	@$(UV_RUN) coverage html

.PHONY: docs-serve
docs-serve: ## Run docs serve
	@echo "Run docs serve"
	@$(UV_RUN) sphinx-autobuild $(DOCS_SOURCE_DIR) $(DOCS_BUILD_DIR)

.PHONY: clean
clean: ## Remove build artifacts
	@echo "Remove build artifacts"

	@echo "Remove ruff cache"
	@rm -rf .ruff_cache/

	@echo "Remove mypy cache"
	@rm -rf .mypy_cache/

	@echo "Remove coverage cache"
	@rm -rf .coverage

	@echo "Remove reports files"
	@rm -rf reports/

	@echo "Delete docs build files"
	@rm -rf $(DOCS_BUILD_DIR)
