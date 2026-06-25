from pydantic_ai import Agent

from archon.models import Requirements
from archon.pipeline.context import PipelineContext
from archon.tools import lookup_service, web_search

# pyrefly: ignore
requirements_agent = Agent[PipelineContext, Requirements](
    output_type=Requirements,
    instructions=(
        'You are a solutions architect gathering requirements for a cloud project. '
        'Given a project description, extract structured requirements covering: '
        'business goals, functional requirements, non-functional requirements, '
        'expected scale, availability, security, compliance, budget, existing '
        'systems, and team capabilities. '
        'If information is missing, use web_search to research typical requirements '
        'for the given industry, and use lookup_service to identify relevant services. '
        'Flag any assumptions you make.'
    ),
    tools=[web_search, lookup_service],
)
