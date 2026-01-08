
_list:
  @just --list

# Check the package with Ruff and Ty
check:
  uv run ruff check src
  uv run ty check src

# Run package tests
test:
  uv run pytest tests
