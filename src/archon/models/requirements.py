from pydantic import BaseModel, Field


class Requirements(BaseModel):
    business_goals: list[str] = Field(
        description='Business objectives this architecture must achieve'
    )
    functional_requirements: list[str] = Field(
        description='Functional capabilities the system must provide'
    )
    non_functional_requirements: list[str] = Field(
        description='Performance, scalability, security, etc.'
    )
    expected_scale: str = Field(description='Expected usage volume (users, requests, data size)')
    availability_requirements: str | None = Field(
        default=None, description='Uptime/SLA requirements'
    )
    security_requirements: list[str] = Field(
        default_factory=list, description='Security constraints and requirements'
    )
    compliance_requirements: list[str] = Field(
        default_factory=list, description='Regulatory compliance needs'
    )
    budget_constraints: str | None = Field(default=None, description='Budget limitations')
    existing_systems: list[str] = Field(
        default_factory=list, description='Systems to integrate with'
    )
    team_capabilities: list[str] = Field(default_factory=list, description='Operations team skills')
    assumptions: list[str] = Field(
        default_factory=list, description='Assumptions made during requirements gathering'
    )
