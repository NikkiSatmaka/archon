from pydantic_ai import Agent

from archon.models import Recommendation
from archon.pipeline.context import PipelineContext

# pyrefly: ignore
recommendation_agent = Agent[PipelineContext, Recommendation](
    output_type=Recommendation,
    instructions=(
        'You are a solutions architect selecting the best architecture. '
        'Given the tradeoff analysis and design drivers, choose the option that '
        'best satisfies the requirements. '
        'Explain: why it was selected, why alternatives were rejected, '
        'and key assumptions behind the decision. '
        'Include sensitivity analysis: how would the recommendation change '
        'if key assumptions shifted?'
    ),
)
