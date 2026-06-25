from pydantic import BaseModel, model_validator

from archon.models import (
    ArchitectureReport,
    CandidateArchitectures,
    Clarifications,
    DesignDrivers,
    ImplementationRoadmap,
    ProjectScope,
    Recommendation,
    Requirements,
    RiskAssessment,
    TradeoffAnalysis,
)


class PipelineContext(BaseModel):
    project: ProjectScope
    requirements: Requirements | None = None
    clarifications: Clarifications | None = None
    design_drivers: DesignDrivers | None = None
    candidates: CandidateArchitectures | None = None
    tradeoffs: TradeoffAnalysis | None = None
    recommendation: Recommendation | None = None
    risks: RiskAssessment | None = None
    roadmap: ImplementationRoadmap | None = None
    report: ArchitectureReport | None = None
    user_answers: dict[str, str] | None = None

    @model_validator(mode='after')
    def validate_checkpoint_resume(self) -> 'PipelineContext':
        if self.user_answers and self.clarifications is None:
            raise ValueError('Cannot have user_answers without clarifications')
        return self
