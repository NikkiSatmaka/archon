# Pydantic AI — Archon Skill

When working with Pydantic AI in this project, follow these patterns:

## Agent Declaration (Pydantic AI 2.0)

```python
from pydantic_ai import Agent, RunContext

agent = Agent[PipelineContext, Requirements](
    output_type=Requirements,
    instructions='You are a solutions architect...',
    tools=[web_search, calculator],
)
```

- `deps_type` is always `PipelineContext` (first generic param)
- `output_type` is the step's specific Pydantic model (second generic param)
- **No model string in constructor** — the actual model is passed at `run()` time
- Use `instructions=` (string) instead of `system_prompt=` (deprecated in 2.0)
- Tools are listed in `tools=[]` as plain async functions (not decorators in this project)

## Tool Registration

Two valid patterns in Pydantic AI 2.0:

**Pattern A — Module-level functions (used in this project):**
```python
from pydantic_ai import RunContext

async def my_tool(
    ctx: RunContext[PipelineContext],
    arg: str,
) -> str:
    """Short description — this becomes the tool schema sent to the LLM."""
    ...

# Pass in Agent constructor:
agent = Agent[PipelineContext, Output](..., tools=[my_tool])
```

**Pattern B — `@agent.tool` decorator:**
```python
@agent.tool
async def my_tool(
    ctx: RunContext[PipelineContext],
    arg: str,
) -> str:
    """Short description."""
    ...
```

- The first parameter is always `ctx: RunContext[PipelineContext]`
- Always type-annotate all parameters and return types

## Model Setup (Pydantic AI 2.0)

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

- `OpenAIModel` → **`OpenAIChatModel`** in 2.0
- `OpenAIProvider` is imported from `pydantic_ai.providers.openai` (not `pydantic_ai.models.openai`)

## Running Agents

```python
model = config.create_model()  # via LLMConfig helper
result = await agent.run(user_input, deps=ctx, model=model)
# result.output is a validated Pydantic model instance
```

- Always pass `model=` at `run()` time, never hardcode in the agent definition

## Testing with TestModel (Pydantic AI 2.0)

```python
from pydantic_ai.models.test import TestModel

def test_step():
    model = TestModel(
        call_tools=['my_tool'],         # list of tool name strings (NOT function refs)
        custom_output_args={              # dict of output model field values
            'field1': 'value1',
            'field2': 'value2',
        },
    )
    result = agent.run_sync('test input', deps=ctx, model=model)
    assert isinstance(result.output, MyOutputModel)
    assert result.output.field1 == 'value1'
```

Key changes from 1.x:
- `callable_tools=[my_tool]` → **`call_tools=['my_tool']`** (string names, not function references)
- `static_result=MyModel(...)` → **`custom_output_args={...}`** (dict of field values)
- Output data is validated through the model's Pydantic validators
- Use `call_tools=[]` (empty list) to skip all tool calls
- If tools are listed in `call_tools`, they are **actually executed** — ensure the test input won't break them
