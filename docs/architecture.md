# Architecture — Archon Business Logic

## Overview

Archon is an AI-powered cloud architecture assistant. It implements a 9-step
solutions architect workflow as a sequential pipeline of Pydantic AI agents.
Each agent is responsible for one phase of the architecture process, taking
structured input and producing structured output (Pydantic models).

The pipeline is orchestrated by `Orchestrator`, which:
- Chains agents sequentially
- Passes accumulated state via `PipelineContext`
- Handles the checkpoint/resume flow after step 2 (clarifications)
- Provides the model gateway configuration to all agents

## Workflow

```
┌─────────────┐
│  User Input │  (project scope, description, constraints)
└──────┬──────┘
       ↓
┌──────────────────────────────────────────────────────────────┐
│  Step 1: Requirements Gatherer                               │
│  Agent[PipelineContext, Requirements]                        │
│  Extracts business goals, functional/non-functional reqs,    │
│  scale, availability, security, compliance, budget, timeline │
└──────────────────────────┬───────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│  Step 2: Unknowns Identifier                                 │
│  Agent[PipelineContext, Clarifications]                       │
│  Identifies missing information, generates clarifying        │
│  questions, records assumptions needed to continue           │
└──────────────────────────┬───────────────────────────────────┘
                           ↓
                    ╔══════════════╗
                    ║ CHECKPOINT   ║  ← Return to user for input
                    ╚══════════════╝
                           ↓  (user answers injected)
┌──────────────────────────────────────────────────────────────┐
│  Step 3: Design Drivers                                      │
│  Agent[PipelineContext, DesignDrivers]                        │
│  Determines and ranks key design drivers (cost, reliability, │
│  latency, compliance, simplicity, etc.)                      │
└──────────────────────────┬───────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│  Step 4: Candidate Architectures                             │
│  Agent[PipelineContext, CandidateArchitectures]               │
│  Generates 2-3 architecture options with components, data    │
│  flow, deployment model, operational model                   │
└──────────────────────────┬───────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│  Step 5: Tradeoff Analysis                                   │
│  Agent[PipelineContext, TradeoffAnalysis]                     │
│  Compares each option against design drivers, scores them,   │
│  evaluates cost, complexity, scalability, reliability, etc.  │
└──────────────────────────┬───────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│  Step 6: Recommendation                                      │
│  Agent[PipelineContext, Recommendation]                       │
│  Selects the best architecture, explains why, why others     │
│  were rejected, and key assumptions                          │
└──────────────────────────┬───────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│  Step 7: Risk Assessment                                     │
│  Agent[PipelineContext, RiskAssessment]                       │
│  Identifies technical, cost, security, operational, scaling  │
│  risks with severity, likelihood, and mitigation strategies  │
└──────────────────────────┬───────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│  Step 8: Implementation Roadmap                              │
│  Agent[PipelineContext, ImplementationRoadmap]                │
│  Breaks implementation into phases (MVP → production →       │
│  scale → advanced), each with tasks and timeline             │
└──────────────────────────┬───────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│  Step 9: Final Deliverable                                   │
│  Agent[PipelineContext, ArchitectureReport]                   │
│  Produces the complete structured report combining all       │
│  prior outputs into a cohesive deliverable                   │
└──────────────────────────┬───────────────────────────────────┘
                           ↓
                    ┌──────────────┐
                    │  Report Out  │  (ArchitectureReport model)
                    └──────────────┘
```

## PipelineContext

`PipelineContext` is the shared state object passed through the entire pipeline.
Each step reads its dependencies from context and writes its output to the
corresponding field.

```python
class PipelineContext(BaseModel):
    project: ProjectScope
    requirements: Requirements | None = None
    clarifications: Clarifications | None = None
    design_drivers: DesignDrivers | None = None
    candidates: CandidateArchitectures | None = None
    tradeoffs: TradeoffAnalysis | None = None
    recommendation: Recommendation | None = None
    risks: RiskAssessment | None = None
    roadmap: ImplementationRoadmap | None = None
    report: ArchitectureReport | None = None
```

### Field Dependencies

| Step | Reads | Writes | Validates |
|---|---|---|---|
| Step 1 | `project` | `requirements` | All fields non-null |
| Step 2 | `project`, `requirements` | `clarifications` | Has at least one question or assumption |
| Step 3 | `project`, `requirements`, `clarifications` | `design_drivers` | At least 3 drivers ranked |
| Step 4 | `project`, `requirements`, `design_drivers` | `candidates` | At least 2 options |
| Step 5 | `candidates`, `design_drivers` | `tradeoffs` | All options compared |
| Step 6 | `candidates`, `tradeoffs`, `design_drivers` | `recommendation` | Exactly 1 selected |
| Step 7 | `recommendation`, `candidates` | `risks` | At least 1 risk |
| Step 8 | `recommendation`, `risks` | `roadmap` | At least 1 phase |
| Step 9 | All prior fields | `report` | All sections populated |

## Agent Catalog

### Step 1: Requirements Gatherer

| Aspect | Detail |
|---|---|
| `output_type` | `Requirements` |
| Tools | `web_search`, `service_catalog` |
| Behavior | Given project description, extracts structured requirements. If info is sparse, uses tools to research industry patterns and typical requirements. |
| Edge cases | Minimal input ("build me a platform") — agent uses web search to infer reasonable defaults and flags them as assumptions. |

### Step 2: Unknowns Identifier

| Aspect | Detail |
|---|---|
| `output_type` | `Clarifications` |
| Tools | None (pure reasoning) |
| Behavior | Reviews requirements against known completeness criteria. Generates questions for missing/ambiguous information. Records assumptions where the agent chose a reasonable default. |
| Edge cases | Complete requirements yield few or zero questions. Contradictory requirements (e.g., "lowest cost" + "highest reliability") flagged as ambiguity risks. |

### Step 3: Design Drivers

| Aspect | Detail |
|---|---|
| `output_type` | `DesignDrivers` |
| Tools | None (pure reasoning) |
| Behavior | Determines which design drivers apply to this project and ranks them by importance. Outputs a scored list with rationales. |
| Edge cases | Some drivers may be tied in importance — both ranked equally. |

### Step 4: Candidate Architectures

| Aspect | Detail |
|---|---|
| `output_type` | `CandidateArchitectures` |
| Tools | `service_catalog`, `calculator` |
| Behavior | Generates 2-3 distinct architecture options. Uses service catalog to find appropriate services. Uses calculator for rough cost estimates. Each option describes components, data flow, deployment, and operations. |
| Edge cases | Very low budget constrains options — may generate one cloud-native and one hybrid/multi-cloud alternative. |

### Step 5: Tradeoff Analysis

| Aspect | Detail |
|---|---|
| `output_type` | `TradeoffAnalysis` |
| Tools | `calculator` |
| Behavior | Scores each option against each design driver. Produces a comparison matrix and textual analysis of tradeoffs. |
| Edge cases | If options are very similar, comparative analysis may be brief. |

### Step 6: Recommendation

| Aspect | Detail |
|---|---|
| `output_type` | `Recommendation` |
| Tools | None (pure reasoning) |
| Behavior | Selects the winning architecture, explains why it best satisfies the design drivers, why alternatives were rejected, and documents key assumptions. |
| Edge cases | Close calls are documented with sensitivity analysis ("if requirements change, option B becomes better"). |

### Step 7: Risk Assessment

| Aspect | Detail |
|---|---|
| `output_type` | `RiskAssessment` |
| Tools | None (pure reasoning) |
| Behavior | Identifies risks across technical, cost, security, operational, scaling, and dependency categories. Each risk has severity, likelihood, and mitigation. |
| Edge cases | Risk scores may trigger a recommendation review (if high-risk, the output flags this). |

### Step 8: Implementation Roadmap

| Aspect | Detail |
|---|---|
| `output_type` | `ImplementationRoadmap` |
| Tools | None (pure reasoning) |
| Behavior | Breaks implementation into 3-4 phases: MVP, production readiness, scale optimization, advanced capabilities. Each phase has tasks, dependencies, and estimated effort. |
| Edge cases | Very small projects may have 2 phases; large enterprises may have 5+. |

### Step 9: Final Deliverable

| Aspect | Detail |
|---|---|
| `output_type` | `ArchitectureReport` |
| Tools | None (aggregation + reasoning) |
| Behavior | Takes all prior outputs and synthesizes them into a cohesive architecture report. Adds executive summary and architecture overview. Does not duplicate — references prior step outputs. |
| Edge cases | If any prior step failed or was skipped, the agent should handle gracefully and document gaps. |

## Clarification Flow

The clarification flow is a key interaction pattern:

1. **Step 2 generates questions**: The `Clarifications` model contains a list of
   `Question` objects (each with `question: str`, `context: str`, and
   `impact_if_unanswered: str`).

2. **Checkpoint**: The orchestrator returns `Clarifications` to the caller
   (CLI layer). The caller displays questions to the user and collects answers.

3. **Resume**: The caller provides user answers as a
   `dict[str, str]` mapping question IDs to answers.

4. **Before proceeding**: The orchestrator presents a summary of all
   clarifications + answers and asks for final confirmation.

5. **Step 3+**: Continue with the enriched context.

```python
# Pseudocode for the checkpoint flow
result = await orchestrator.run_until_checkpoint(project)
# result has PipelineContext with requirements + clarifications
# CLI layer:
for q in result.clarifications.questions:
    answer = input(f"{q.question} ")
    user_answers[q.id] = answer
confirmed = input("Proceed with architecture design? (y/n) ")
if confirmed:
    report = await orchestrator.resume(user_answers)
```

## Service Catalog

The service catalog is a structured set of Pydantic models organized by
category. Each service has:

| Field | Type | Description |
|---|---|---|
| `name` | `str` | Service name (e.g., "Amazon S3") |
| `provider` | `Literal['aws', 'gcp', 'azure']` | Cloud provider |
| `category` | `ServiceCategory` | Compute, storage, database, analytics, ai_ml, serverless |
| `description` | `str` | What the service does |
| `use_cases` | `list[str]` | Typical use cases |
| `pricing_model` | `str` | How pricing works (per-hour, per-GB, per-request) |
| `limitations` | `list[str]` | Known limitations |
| `typical_latency` | `str` | Performance characteristic |
| `compliance` | `list[str]` | Compliance certifications |

The catalog is accessed via a tool:

```python
@agent.tool
async def lookup_service(
    ctx: RunContext[PipelineContext],
    query: str,
) -> list[Service]:
    """Search the service catalog for cloud services matching the query."""
    return ctx.deps.search(query)
```

## Tools

### `web_search`
- Interface: `async def web_search(query: str) -> str`
- Purpose: Search for current cloud service pricing, documentation, or best
  practices
- Implementation: Wraps a search API (DuckDuckGo, Tavily, or similar)
- Error handling: Returns "Search unavailable" on failure (non-blocking)

### `calculator`
- Interface: `async def calculate(expression: str) -> float`
- Purpose: Safely evaluate mathematical expressions for cost estimation
- Implementation: Uses a safe expression evaluator (not `eval`)
- Error handling: Returns `NaN` on invalid expressions

### `lookup_service` (service catalog tool)
- Interface: `async def lookup_service(query: str) -> list[Service]`
- Purpose: Search the built-in service catalog
- Implementation: Keyword matching across service names, descriptions, and
  use cases
- Error handling: Returns empty list on no match

## Error Handling

The pipeline defines a custom exception hierarchy:

```
PipelineError
├── StepExecutionError   # Agent failed to produce valid output
├── ValidationError      # Pydantic validation failed on agent output
└── CheckpointError      # Invalid resume after checkpoint
```

### Per-step failure modes

| Failure | Handling |
|---|---|
| LLM returns invalid JSON (not Pydantic-valid) | Pydantic AI's reflection loop auto-retries with validation error message |
| Tool call fails (web search down) | Tool returns graceful error string, agent continues without it |
| Step produces None for required field | `PipelineContext` validator catches missing fields, raises `StepExecutionError` |
| Orchestrator receives invalid resume data | `CheckpointError` with details |

## Edge Cases

| Scenario | Handling |
|---|---|
| **Empty/minimal requirements** | Step 1 uses web search to infer typical requirements for the given industry/use case. Flags all inferred values as assumptions. |
| **Contradictory constraints** ("cheap + high availability") | Step 2 flags as ambiguity risk. Step 3 ranks drivers with tradeoff explanation. |
| **Budget below minimum viable** | Step 7 flags as cost risk. Recommendation includes phased approach or alternative providers. |
| **No preferred provider** | Agents consider all 3 providers equally. Step 7 includes vendor lock-in analysis. |
| **Unsupported provider** | Agent uses web search to research the provider. Falls back to closest comparable services with warning. |
| **Very large/small scale** | Agents adjust recommendations accordingly. Microservices for large scale, serverless for small. |
| **Compliance requirements** | Agents filter services by compliance certifications. If no catalog services match, web search is used. |

## Phase 2 Considerations

- **Markdown/HTML rendering**: A dedicated rendering agent or tool that takes
  `ArchitectureReport` and produces formatted documents.
- **CLI layer**: Interactive CLI with rich input, progress indicators, session
  persistence, and output file generation.
- **Prompt versioning**: A prompt registry with versioned templates, A/B testing
  capability.
- **Multi-turn conversations**: Allow users to revise requirements mid-pipeline
  and re-run affected steps.
- **Parallel candidate generation**: Step 4 could generate candidates in
  parallel for faster throughput.
- **Architecture diagrams**: Generate Mermaid or PlantUML diagrams from the
  report model.
