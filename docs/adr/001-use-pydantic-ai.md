# ADR-001: Use Pydantic AI as the Agent Framework

## Status

Accepted

## Context

Archon requires an LLM integration layer to power its 9-step architecture
pipeline. Each step must:
- Accept structured input and return structured output (Pydantic models)
- Call tools (web search, calculator, service catalog lookup)
- Handle retries and validation errors gracefully
- Support multiple LLM providers without code changes

Options considered:

1. **Raw OpenAI SDK** — provides chat completions only. Requires building
   tool-call loops, structured output parsing, retry logic, and provider
   abstraction from scratch.

2. **Pydantic AI** — agent framework from the Pydantic team with built-in
   structured output, tool calling, validation reflection, and multi-provider
   support.

3. **LiteLLM SDK** — provider router (100+ LLMs) but no agent/tool/structured
   output support. Would still require building the agent infrastructure.

## Decision

Use Pydantic AI because:

- Already committed to Pydantic v2 — same team, zero compatibility risk
- `output_type=MyModel` eliminates structured output parsing glue code
- `@agent.tool` decorator + `RunContext` provides type-safe tool calling
- Built-in reflection loop auto-retries on validation failure
- Multi-provider via `'openrouter:...'` prefix or `OpenAIModel` with custom
  `OpenAIProvider`
- `TestModel` enables deterministic testing without real LLM calls
- Capabilities (web search, thinking, MCP) are available for future expansion
- Saves approximately 500+ lines of boilerplate vs. raw OpenAI SDK

## Consequences

- Positive: Less code to write and maintain; focus on architecture logic
- Positive: Type-safe agent definitions work well with Pyrefly strict mode
- Positive: Easy to swap models at runtime (pass `model` at `run()` time)
- Negative: Additional dependency (~50KB)
- Negative: Team members must learn Pydantic AI patterns
