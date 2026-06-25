# ADR-007: Pydantic Model Output Only (Phase 1)

## Status

Accepted

## Context

The final deliverable of the pipeline (step 9) is an architecture report. We
need to decide what format it takes.

Options considered:

1. **Pydantic model only** — the pipeline produces a structured
   `ArchitectureReport` Pydantic model. Rendering to markdown/HTML is handled
   by a separate agent or process in a later phase.

2. **Pydantic model + rendering** — the pipeline also generates markdown/HTML
   output directly.

3. **Rendering agent** — a 10th agent or separate tool takes the Pydantic model
   and produces formatted output.

## Decision

Phase 1 produces only the Pydantic model for these reasons:

- Clean separation of data from presentation
- The model is testable, queryable, and can be validated programmatically
- Rendering decisions (format, style, template) don't affect pipeline logic
- The rendering can be handled by a dedicated agent in phase 2, keeping
  concerns separated
- Easier to evolve — the report schema can change without touching presentation

```python
class ArchitectureReport(BaseModel):
    executive_summary: str
    architecture_overview: str
    major_components: list[Component]
    data_flow: str
    tradeoff_analysis: TradeoffAnalysis
    recommendation: Recommendation
    risks: RiskAssessment
    roadmap: ImplementationRoadmap
```

## Consequences

- Positive: Pipeline logic is independent of output formatting
- Positive: Report model can be used programmatically (API responses, CI
  pipelines, integrations)
- Positive: Simpler tests — no markdown parsing or HTML validation
- Negative: No human-readable output in phase 1 without manual inspection of
  the model
