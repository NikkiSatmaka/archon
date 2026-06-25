from pydantic_ai import Agent

from archon.models import DesignDrivers
from archon.pipeline.context import PipelineContext

# pyrefly: ignore
design_driver_agent = Agent[PipelineContext, DesignDrivers](
    output_type=DesignDrivers,
    instructions=(
        'You are a solutions architect determining design drivers for a project. '
        'Given the requirements and clarifications, identify the factors that '
        'will most strongly influence the architecture. '
        'Rank them by importance. '
        'Common drivers: lowest cost, highest reliability, lowest latency, '
        'fastest delivery, regulatory compliance, global scale, simplicity, '
        'operational efficiency, vendor lock-in avoidance, security. '
        'Output at least 3 ranked drivers with scores (1-10) and rationale.'
    ),
)
