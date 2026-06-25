# Pyrefly — Archon Skill

## Configuration

Pyrefly is configured in `pyrefly.toml`:

```toml
strict = true
target-version = "3.12"
```

## Running

```bash
uv run pyrefly check src/    # type check the source
uv run pyrefly check tests/  # type check tests
```

## Common Patterns

### Strict mode catches
- Unannotated function parameters (must annotate everything)
- Implicit `Any` returns
- Unsafe `Optional` usage (use `| None` instead)
- Incorrect `BaseModel` usage

### Suppressing errors
Prefer fixing over suppressing. If suppression is necessary:

```python
# pyrefly: disable-next-line=annotation-missing
result = some_untyped_call()
```

### Pydantic model type checking
Pyrefly has built-in Pydantic support — model fields are type-checked:

```python
class MyModel(BaseModel):
    name: str = Field(description="...")
    # type error if you assign int to name
```

### Protocol over ABC
Prefer `Protocol` for duck typing (Pyrefly handles it well):

```python
from typing import Protocol

class Searchable(Protocol):
    async def search(self, query: str) -> list[str]: ...
```
