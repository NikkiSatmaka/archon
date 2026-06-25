# ADR-003: 9-Step Sequential Agentic Pipeline

## Status

Accepted

## Context

The architecture workflow has 9 distinct phases (requirements → unknowns →
drivers → candidates → tradeoffs → recommendation → risks → roadmap →
deliverable). We need to choose an orchestration model.

Options considered:

1. **Single monolithic agent** — one agent handles all 9 steps in a single
   conversation. Simple but hard to test, debug, or customize per step.

2. **9 independent agents, sequential** — each step is a separate Pydantic AI
   `Agent` with its own system prompt, tools, and output model. The orchestrator
   chains them.

3. **Hierarchical agents** — sub-agents for groups of steps with a supervisor
   agent. More flexible but more complex than needed for phase 1.

## Decision

Use 9 independent sequential agents because:

- Maps 1:1 to the established architecture workflow — clear separation of
  concerns
- Each agent has a specific `output_type`, making tests deterministic
- Independent agents can be developed, tested, and iterated in isolation
- The checkpoint after step 2 enables human-in-the-loop (clarifying questions
  before proceeding to design)
- Pydantic AI's `Agent` pattern makes each step ~30-60 lines of code
- Easy to reorder, skip, or extend steps in future phases

### Pipeline Flow

```
[Input] → Step1 → Step2 → [Checkpoint] → Step3 → ... → Step9 → [Report]
             ↑ outputs  ↑ outputs         ↑ resumed with
             Requirements Clarifications    user answers
```

## Consequences

- Positive: Each step is independently testable with `TestModel`
- Positive: Clear failure isolation — a bug in step 4 doesn't affect step 2
- Positive: Steps can be parallelized in future (e.g., generate multiple
  candidates concurrently)
- Negative: Sequential execution means total latency = sum of all 9 steps
- Negative: Context must be explicitly passed between steps via
  `PipelineContext`
