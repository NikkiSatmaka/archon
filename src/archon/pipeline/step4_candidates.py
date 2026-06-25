from pydantic_ai import Agent

from archon.models import CandidateArchitectures
from archon.pipeline.context import PipelineContext
from archon.tools import calculate, lookup_service

# pyrefly: ignore
candidate_agent = Agent[PipelineContext, CandidateArchitectures](
    output_type=CandidateArchitectures,
    instructions=(
        'You are a solutions architect generating candidate architectures. '
        'Given the requirements, clarifications, and design drivers, create '
        '2-3 distinct architecture options. '
        'For each option describe: major components, data flow, deployment model, '
        'and operational model. '
        'Use lookup_service to find appropriate cloud services. '
        'Use calculate for rough cost estimates. '
        'Avoid selecting a winner at this stage.'
    ),
    tools=[lookup_service, calculate],
)
