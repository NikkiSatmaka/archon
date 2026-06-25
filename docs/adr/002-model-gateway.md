# ADR-002: OpenAI-Compatible Model Gateway

## Status

Accepted

## Context

Archon needs to work with multiple LLM providers (OpenRouter, LiteLLM proxy,
and future gateways) without code changes. The pipeline agent definitions
should not be coupled to a specific provider.

Options considered:

1. **Custom `LLMClient` abstraction** — define a base class with
   `async def generate()`, implement per-provider subclasses.

2. **Pydantic AI `OpenAIModel` + `OpenAIProvider`** — use OpenAI SDK format
   with configurable `base_url`. Works with any OpenAI-compatible endpoint.

3. **Pydantic AI model string prefixes** — use `'openrouter:...'`,
   `'openai:...'`, `'google:...'` directly in agent definitions.

## Decision

Use `OpenAIModel` with a custom `OpenAIProvider` because:

- Every major gateway (OpenRouter, LiteLLM, Together AI) exposes an
  OpenAI-compatible endpoint
- A single `base_url` + `api_key` + `model_name` config handles all providers
- No custom LLM abstraction layer to write or maintain
- Pydantic AI's `OpenAIModel` handles the OpenAI-compatible format natively
- Environment variables control the provider without code changes
- Avoids provider-specific prefixes in agent definitions (more portable)

```python
model = OpenAIModel(
    config.model_name,
    provider=OpenAIProvider(
        base_url=config.base_url,
        api_key=config.api_key,
    ),
)
```

## Consequences

- Positive: Zero provider-specific code; any OpenAI-compatible endpoint works
- Positive: Simple configuration via 3 environment variables
- Positive: Easy to add provider-specific auth or headers via `OpenAIProvider`
- Negative: Tied to OpenAI API format (though this is the de facto standard)
- Negative: Providers that diverge from OpenAI format require a different model
  class (Pydantic AI supports Anthropic, Gemini, etc. directly as alternatives)
