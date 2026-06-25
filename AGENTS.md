# AGENTS.md — Archon

## Project

Archon is an AI-powered cloud architecture assistant. It guides a user through a
9-step solutions architect workflow to produce a professional architecture
recommendation report, output as a structured Pydantic model.

## Tech Stack

- Python 3.12+, `uv` for package management
- **`src/` layout** — `archon` lives under `src/`; tests import it via
  `pythonpath = ["src"]` in `pyproject.toml` (no editable install needed)
- Pydantic v2 for all data models
- **Pydantic AI** for the agent framework (built by the Pydantic team)
- Pyrefly (strict mode) for static type checking
- `pytest` + `pytest-asyncio` for testing
- `ruff` for linting
- `Jinja2` for prompt templates

## Code Conventions

- **Type hints** — every function, method, and attribute must be annotated.
- **Pydantic everywhere** — never pass raw dicts between agents. All pipeline
  state is typed via `PipelineContext`.
- **Async first** — all LLM calls and tool invocations are `async def`.
- **No comments** unless the code cannot be made self-documenting.
- **Import order**: stdlib → third-party → local, separated by blank lines.
- **Naming**: `snake_case` for functions/vars, `PascalCase` for classes/models,
  `UPPER_CASE` for constants.
- **Line length**: 100 characters.
- **Error handling**: use explicit custom exceptions (not bare `except`).

### Pydantic Model Conventions

- Use `str` for IDs and enum-like fields (not `int` or `Enum` unless strictly
  needed for exhaustiveness checking).
- Use `Field(description=...)` on every field for LLM context.
- Use `model_validator` for cross-field validation, not `@validator` (deprecated).
- Use `Literal` types for constrained string fields (e.g., provider names).
- Keep models flat — prefer composition over deep nesting.
- Mark optional fields with `| None` and `= None`, never use `Optional[]`.

## Git Workflow

**Trunk-based with feature branches** — branches off `main`, squash-merged back.

- `main` is always deployable and must pass `pyrefly check` + `pytest`.
- Branch naming: `feat/<short-description>`, `fix/<short-description>`,
  `chore/<short-description>`, `docs/<short-description>`.
- Commits must be **atomic**:
  - One logical change per commit.
  - Each commit passes `pyrefly check` (where applicable).
  - Never mix `feat`, `fix`, `chore`, `test`, `docs` in a single commit.
  - Use `git add -p` to stage only relevant hunks.
- Commit messages follow **Conventional Commits**:
  ```
  feat: add requirements gathering agent
  fix: correct cost estimate for multi-region deployments
  test: add edge case coverage for tradeoff analyzer
  chore: configure pyrefly with strict mode
  docs: update pipeline workflow in AGENTS.md
  ```
- Squash-merge feature branches to keep `main` history clean; write the squash
  message as a single well-formed conventional commit.

## LLM Provider (Model Gateway with Pydantic AI)

Pydantic AI provides built-in multi-provider support. We use
`OpenAIChatModel` with a custom `OpenAIProvider` to route through any
OpenAI-compatible gateway (OpenRouter, LiteLLM proxy, custom gateway):

```python
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIChatModel(
    'anthropic/claude-sonnet-4',
    provider=OpenAIProvider(
        base_url='https://openrouter.ai/api/v1',
        api_key='sk-...',
    ),
)
```

Configuration via environment variables:

| Variable | Example | Required |
|---|---|---|
| `ARCHON_LLM_BASE_URL` | `https://openrouter.ai/api/v1` | Yes |
| `ARCHON_LLM_API_KEY` | `sk-...` | Yes |
| `ARCHON_LLM_MODEL` | `anthropic/claude-sonnet-4` | No (uses provider default) |

## Pydantic AI Agent Pattern

Each pipeline step is a module-level Pydantic AI `Agent` instance:

```python
from pydantic_ai import Agent, RunContext
from archon.pipeline.context import PipelineContext
from archon.models.requirements import Requirements

agent = Agent[PipelineContext, Requirements](
    output_type=Requirements,
    instructions='You are a solutions architect...',
    tools=[web_search, calculator],
)
```

### Agent rules

1. `deps_type` (first generic param) is always `PipelineContext`.
2. `output_type` (second generic param) is the step's specific Pydantic model.
3. Tools are module-level async functions passed via `tools=[]` (or `@agent.tool` decorators).
4. **No model string in constructor** — the model is passed at `run()` time.
5. Use `instructions=` (string) instead of deprecated `system_prompt=`.
6. Never interactively prompt the user — all I/O is routed through the
   orchestrator.

### Tool pattern

Module-level functions passed via `tools=[]`:

```python
async def my_tool(
    ctx: RunContext[PipelineContext],
    arg: str,
) -> str:
    """Description — this becomes the LLM's tool schema."""
    ...
```

## Pipeline Architecture

The orchestrator chains 9 agents sequentially. Each step populates one field of
`PipelineContext`:

```
[Input] → Step1 → Step2 → [Checkpoint] → Step3 → Step4 → Step5 → Step6 → Step7 → Step8 → Step9 → [Report]
```

- **Step 1** (Requirements): Gather requirements from project description.
- **Step 2** (Unknowns): Identify missing info, generate clarifying questions.
- **[Checkpoint]**: Orchestrator returns questions to CLI layer; user answers
  injected before resume.
- **Step 3** (Design Drivers): Determine and rank the key design drivers.
- **Step 4** (Candidates): Generate multiple architecture options.
- **Step 5** (Tradeoffs): Compare options against design drivers.
- **Step 6** (Recommendation): Select the best architecture.
- **Step 7** (Risks): Identify risks and mitigations.
- **Step 8** (Roadmap): Create phased implementation plan.
- **Step 9** (Deliverable): Produce final structured report.

## Service Catalog

A built-in structured catalog of cloud services under
`src/archon/service_catalog/`. Each module exports a list of `Service` objects
(Pydantic models) describing common cloud services across AWS, GCP, and Azure.

Agents access the catalog via a `@agent.tool` that injects the catalog as a
dependency (`deps=ServiceCatalog`), allowing search and filtering.

## Prompt Management

Prompts are Jinja2 template files in `prompts/`. Each agent loads its template
and passes it as `instructions=` to the Pydantic AI `Agent` constructor.

```
prompts/
├── step1_requirements.j2
├── step2_unknowns.j2
├── ...
└── step9_deliverable.j2
```

Templates are rendered with the current `PipelineContext` as the template
context: `Template(source).render(context=ctx)`.

## Testing

- Every module in `src/archon/` must have a corresponding test module.
- Use `pytest-asyncio` (auto mode enabled in pyproject.toml).
- Use **Pydantic AI's `TestModel`** for deterministic agent testing (2.0 API):
  ```python
  from pydantic_ai.models.test import TestModel

  def test_step():
      model = TestModel(
          call_tools=['my_tool'],        # string names, not function refs
          custom_output_args={            # dict of output model field values
              'field1': 'value1',
              'field2': 'value2',
          },
      )
      result = agent.run_sync('input', deps=ctx, model=model)
      assert isinstance(result.output, MyOutputModel)
      assert result.output.field1 == 'value1'
  ```
  - `callable_tools=` → `call_tools=` (list of string tool names)
  - `static_result=` → `custom_output_args=` (dict of field values)
- Fixtures in `conftest.py`:
  - `sample_project`: complete `ProjectScope` with realistic data
  - `test_model`: `TestModel` configured per test case
  - `pipeline_context`: fully populated context for end-to-end tests
- Mock the LLM at the boundary; test agent logic, not the model.

## Skills

This project uses opencode skill files at `.opencode/skills/` to guide AI agents
on technology-specific patterns. Load the relevant skill when working with:
- `pydantic-ai` — agent/tool/dependency patterns
- `pyrefly` — type checker configuration and strict mode practices
- `uv` — package management commands

## Configuration (environment variables)

| Variable | Default | Description |
|---|---|---|
| `ARCHON_LLM_BASE_URL` | `https://api.openai.com/v1` | OpenAI-compatible endpoint |
| `ARCHON_LLM_API_KEY` | — | API key for the provider |
| `ARCHON_LLM_MODEL` | (provider default) | Model override |

## Commands

```bash
# Dependency management (always uv add + uv sync, never uv pip install)
uv add <package>                 # add a runtime dependency
uv add --group dev <package>     # add a dev dependency
uv sync                          # refresh venv from lockfile
uv sync --group dev              # include dev deps

# Running
uv run pyrefly check src/        # type check
uv run pytest                    # run tests
uv run pytest -v                 # verbose tests
uv run ruff check src/           # lint
uv run ruff check src/ --fix     # auto-fix lint issues
uv run ruff format src/          # format code
```

> **Never use `uv pip install`** (including `uv pip install -e .`) — it bypasses
> `pyproject.toml`, skips the lockfile, and can silently install into the wrong
> environment (system or user site-packages). If the package is not importable,
> check `pythonpath` in `[tool.pytest.ini_options]` or run `uv sync`.
