# Helpers

git-branch := `git rev-parse --abbrev-ref HEAD`
git-branch-clean := replace(git-branch, '/', '-')
git-commit := `git rev-parse --short=8 HEAD`
git-commit-long := `git rev-parse HEAD`

setup:
    uv pip install -e ".[dev]"
    pre-commit install

lint:
    ruff check
    ruff format --check

format:
    ruff check --fix --exit-zero
    ruff format
