
_list:
  @just --list

# Check the package with Ruff and Ty
check:
  uv run ruff check src
  uv run mypy src

# Run package tests
test:
  uv run pytest tests

# Run Ruff and make safe fixes
fix:
  uv run ruff check --fix src
