from pydantic_ai import Agent

from archon.models import Clarifications
from archon.pipeline.context import PipelineContext

# pyrefly: ignore
clarifier_agent = Agent[PipelineContext, Clarifications](
    output_type=Clarifications,
    instructions=(
        'You are a solutions architect reviewing requirements. '
        'Given the project scope and requirements, identify missing or ambiguous '
        'information that could affect architecture decisions. '
        'Generate clarifying questions for the user. '
        'Also record assumptions you must make to proceed without that information, '
        'and flag risks caused by missing information.'
    ),
)
