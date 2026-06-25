from pydantic_ai import Agent

from archon.models import ImplementationRoadmap
from archon.pipeline.context import PipelineContext

# pyrefly: ignore
roadmap_agent = Agent[PipelineContext, ImplementationRoadmap](
    output_type=ImplementationRoadmap,
    instructions=(
        'You are a solutions architect creating an implementation roadmap. '
        'Given the recommended architecture and risks, break the implementation '
        'into phases. '
        'Typical phases: Phase 1 (MVP), Phase 2 (Production Readiness), '
        'Phase 3 (Scale Optimization), Phase 4 (Advanced Capabilities). '
        'For each phase provide: name, description, key tasks, estimated effort, '
        'and dependencies.'
    ),
)
