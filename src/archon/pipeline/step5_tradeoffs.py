from pydantic_ai import Agent

from archon.models import TradeoffAnalysis
from archon.pipeline.context import PipelineContext
from archon.tools import calculate

# pyrefly: ignore
tradeoff_agent = Agent[PipelineContext, TradeoffAnalysis](
    output_type=TradeoffAnalysis,
    instructions=(
        'You are a solutions architect analyzing tradeoffs between architecture options. '
        'Compare each option against the design drivers. '
        'Evaluate: cost, complexity, scalability, reliability, security, '
        'maintainability, time to implement, vendor lock-in, operational burden. '
        'Score each option per driver (1-5). '
        'Provide a clear comparison matrix and summary.'
    ),
    tools=[calculate],
)
