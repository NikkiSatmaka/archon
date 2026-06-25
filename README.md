# Archon — AI-Powered Cloud Architecture Assistant

Archon guides users through a 9-step solutions architect workflow to produce
professional cloud architecture recommendations.

## Quick Start

```bash
uv sync
# configure .env (see .env.example)
uv run archon --project "Food delivery platform" --description "..."
```

## Documentation

- `docs/architecture.md` — business logic and workflow design
- `docs/adr/` — architecture decision records
- `AGENTS.md` — conventions for AI agents working on this project

## Tech Stack

Python 3.12+, uv, Pydantic v2, Pydantic AI, Pyrefly, pytest, ruff
