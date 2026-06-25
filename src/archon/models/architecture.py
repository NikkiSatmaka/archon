from pydantic import BaseModel, Field


class Component(BaseModel):
    name: str = Field(description='Component name')
    service: str = Field(description='Cloud service used')
    provider: str = Field(description='Cloud provider')
    purpose: str = Field(description='What this component does')
    configuration: str = Field(description='Key configuration details')


class ArchitectureOption(BaseModel):
    name: str = Field(description='Name for this option')
    description: str = Field(description='Brief overview')
    components: list[Component] = Field(description='Major components')
    data_flow: str = Field(description='How data flows between components')
    deployment_model: str = Field(description='Deployment approach')
    operational_model: str = Field(description='How the system is managed')
    estimated_monthly_cost: str = Field(description='Rough cost estimate')
    pros: list[str] = Field(default_factory=list, description='Strengths of this option')
    cons: list[str] = Field(default_factory=list, description='Weaknesses of this option')


class CandidateArchitectures(BaseModel):
    options: list[ArchitectureOption] = Field(description='Architecture options', min_length=2)
