
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

# GPT: Fail if the working tree isn't clean
_git-clean:
    git diff --quiet
    git diff --cached --quiet

# Bump to the next dev version
dev-next: _git-clean
    uv version --bump patch --bump dev=0
    git commit -am "Start next development cycle"
