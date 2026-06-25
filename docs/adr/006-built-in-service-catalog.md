# ADR-006: Built-In Service Catalog as Pydantic Modules

## Status

Accepted

## Context

The candidate generation (step 4) and tradeoff analysis (step 5) agents need
information about cloud services — pricing tiers, capabilities, limitations.
We need a source for this data.

Options considered:

1. **LLM knowledge only** — rely entirely on the LLM's training data. No upfront
   work, but results are non-deterministic and may be outdated or incorrect.

2. **Live API calls** — query cloud provider APIs for service metadata.
   Deterministic but adds latency, API dependencies, and auth complexity.

3. **Built-in structured catalog** — curated lists of `Service` Pydantic models
   organized by category and provider. Deterministic, no API calls, fully
   testable.

## Decision

Use a built-in service catalog as Pydantic modules because:

- Deterministic — agents get consistent results regardless of LLM knowledge
- No API dependencies or authentication required
- Fully typed and testable — each service is a validated Pydantic model
- Easy to extend — add entries by writing a new file
- Agents access it via an `@agent.tool` that searches the catalog, making the
  interaction explicit and observable

```python
@agent.tool
async def lookup_service(
    ctx: RunContext[PipelineContext],
    query: str,
) -> list[Service]:
    """Search the service catalog for cloud services matching the query."""
    return ctx.deps.search(query)
```

## Consequences

- Positive: Deterministic, fast, no external dependencies
- Positive: Easy to add custom or niche services not in LLM training data
- Positive: Agents can be tested without mocking external APIs
- Negative: Manual maintenance required as cloud providers update offerings
- Negative: Catalog limited to what we curate; won't cover every possible service
