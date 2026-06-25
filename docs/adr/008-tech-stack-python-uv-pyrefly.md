# ADR-008: Python 3.12+ / uv / Pyrefly / Ruff

## Status

Accepted

## Context

We need to select the core toolchain for the project: Python version, package
manager, type checker, and linter.

## Decision

| Tool | Choice | Rationale |
|---|---|---|
| Language | Python 3.12+ | Modern Python features (type parameter syntax `list[X]`, `type` statement), active ecosystem |
| Package manager | `uv` | Fast, reliable, single binary; native pyproject.toml support; built-in venv management |
| Type checker | Pyrefly strict | Rust-based, checks 1.85M LOC/s, >90% typing spec conformance, built-in Pydantic support, aggressively catches errors in unannotated code |
| Linter + Formatter | Ruff | Zero-config, fast (Rust), replaces flake8 + isort + black |

Pyrefly was chosen over Mypy and Pyright because:
- Significantly faster on large codebases
- Built-in Pydantic model validation awareness
- Strict mode catches errors in unannotated code that Mypy skips
- Active development by Meta, stable 1.0.0 since May 2026
- Good IDE integration (VSCode, Neovim, Zed)

## Consequences

- Positive: Fast type checking enables quick feedback loops
- Positive: Modern Python features improve code ergonomics
- Positive: uv + Ruff reduce configuration overhead
- Negative: Pyrefly is newer — smaller community and fewer resources than Mypy
- Negative: Strict mode may require more annotations than some teams are used to
