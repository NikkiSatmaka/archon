from pydantic import BaseModel, Field

from archon.models.architecture import Component
from archon.models.recommendation import Recommendation
from archon.models.risks import RiskAssessment
from archon.models.roadmap import ImplementationRoadmap
from archon.models.tradeoffs import TradeoffAnalysis


class ArchitectureReport(BaseModel):
    executive_summary: str = Field(
        description='Executive summary of the recommendation',
        min_length=1,
    )
    architecture_overview: str = Field(
        description='High-level architecture description',
        min_length=1,
    )
    diagram_description: str = Field(
        description='Text description of the architecture diagram',
        min_length=1,
    )
    major_components: list[Component] = Field(
        description='Key components in the architecture',
    )
    data_flow: str = Field(
        description='How data moves through the system',
        min_length=1,
    )
    tradeoff_analysis: TradeoffAnalysis = Field(
        description='Tradeoff analysis',
    )
    recommendation: Recommendation = Field(
        description='Final recommendation',
    )
    risks: RiskAssessment = Field(
        description='Risk assessment',
    )
    roadmap: ImplementationRoadmap = Field(
        description='Implementation plan',
    )
