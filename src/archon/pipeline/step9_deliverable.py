from pydantic_ai import Agent

from archon.models import ArchitectureReport
from archon.pipeline.context import PipelineContext

# pyrefly: ignore
deliverable_agent = Agent[PipelineContext, ArchitectureReport](
    output_type=ArchitectureReport,
    instructions=(
        'You are a solutions architect producing a final architecture report. '
        'Synthesize all prior outputs (requirements, drivers, candidates, '
        'tradeoffs, recommendation, risks, roadmap) into a professional '
        'architecture recommendation report. '
        'Include: executive summary, architecture overview, diagram description, '
        'major components, data flow, tradeoff analysis, recommendation, '
        'risks and mitigations, and implementation roadmap.'
    ),
)
