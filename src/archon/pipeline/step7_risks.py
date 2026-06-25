from pydantic_ai import Agent

from archon.models import RiskAssessment
from archon.pipeline.context import PipelineContext

# pyrefly: ignore
risk_agent = Agent[PipelineContext, RiskAssessment](
    output_type=RiskAssessment,
    instructions=(
        'You are a solutions architect identifying risks in the recommended architecture. '
        'Identify: technical risks, cost risks, security risks, operational risks, '
        'scaling risks, and dependency risks. '
        'For each risk provide: category, description, severity (High/Medium/Low), '
        'likelihood (High/Medium/Low), and mitigation strategy.'
    ),
)
