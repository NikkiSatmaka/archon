# uv — Archon Skill

## Commands

```bash
uv sync                  # Install all dependencies from lockfile
uv sync --group dev      # Include dev dependencies
uv add <package>         # Add a dependency
uv add --group dev <pkg> # Add a dev dependency
uv remove <package>      # Remove a dependency
uv run <command>         # Run a command in the venv
uv lock                  # Regenerate lockfile
uv build                 # Build the package
```

## Project Structure

Dependencies are declared in `pyproject.toml` under `[project.dependencies]`
and `[project.optional-dependencies]`.

## Running Project Commands

```bash
uv run pyrefly check src/
uv run pytest
uv run ruff check src/
uv run ruff format src/
```

Never use `pip`, `python -m`, or `uv pip install` — they bypass `pyproject.toml`,
skip lockfile updates, and risk installing to system or user Python.
Use `uv add <package>` then `uv sync` instead.
