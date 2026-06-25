from pydantic import BaseModel, Field


class Phase(BaseModel):
    name: str = Field(description='Phase name (e.g., MVP, Production Readiness)')
    description: str = Field(description='What this phase achieves')
    tasks: list[str] = Field(description='Key tasks')
    estimated_effort: str = Field(description='Time or person-weeks estimate')
    dependencies: list[str] = Field(default_factory=list, description='Prerequisites')


class ImplementationRoadmap(BaseModel):
    phases: list[Phase] = Field(description='Implementation phases in order')
    total_estimated_timeline: str = Field(description='Overall timeline estimate')
