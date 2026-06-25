from typing import Literal

from pydantic import BaseModel, Field


class ProjectScope(BaseModel):
    name: str = Field(description='Project name')
    industry: str | None = Field(default=None, description='Industry vertical')
    description: str = Field(description='High-level project description')
    preferred_provider: Literal['aws', 'gcp', 'azure'] | None = Field(
        default=None, description='Preferred cloud provider if any'
    )
    team_capabilities: list[str] = Field(
        default_factory=list, description='Existing team skills and experience'
    )
    existing_systems: list[str] = Field(
        default_factory=list, description='Existing systems to integrate with'
    )
    budget_range: str | None = Field(default=None, description='Budget constraint if known')
    timeline: str | None = Field(default=None, description='Expected timeline')
