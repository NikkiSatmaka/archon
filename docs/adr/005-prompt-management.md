# ADR-005: Jinja2 Prompt Templates (Phase 1)

## Status

Accepted

## Context

Each of the 9 agents requires a system prompt that describes its role,
output format, and behavioral guidelines. We need a prompt management strategy.

Options considered:

1. **Hardcoded strings** — prompts embedded in Python code. Simple but
   impossible to review or iterate without code changes.

2. **Jinja2 template files** — separate `.j2` files in `prompts/` directory,
   loaded at runtime and rendered with context variables. Version-controlled.

3. **Prompt management system** — LangChain Hub, Agenta, or similar. Adds
   infrastructure dependencies and operational complexity.

## Decision

Use Jinja2 template files in `prompts/` because:

- Version-controlled alongside code — prompts evolve with their agents
- Reviewable in PRs — prompt changes are visible diffs
- Zero infrastructure — no database, no API, no deployment pipeline
- Jinja2 supports conditionals and loops for dynamic prompt content
- Easy to migrate to a dedicated prompt manager later if needed

```
prompts/
├── step1_requirements.j2
├── step2_unknowns.j2
├── ...
└── step9_deliverable.j2
```

Each agent loads its template at module level and renders it with the current
`PipelineContext` as the template context.

## Consequences

- Positive: Prompts are easy to find, edit, and review
- Positive: No prompt manager lock-in; easy to migrate later
- Positive: Templates can use Jinja2 control flow for conditional sections
- Negative: No prompt versioning beyond git history
- Negative: No A/B testing or prompt evaluation infrastructure
