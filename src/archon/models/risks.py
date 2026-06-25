from pydantic import BaseModel, Field


class Risk(BaseModel):
    category: str = Field(
        description='Risk category (technical, cost, security, operational, scaling, dependency)'
    )
    description: str = Field(description='What the risk is')
    severity: str = Field(description='High, Medium, Low')
    likelihood: str = Field(description='High, Medium, Low')
    mitigation: str = Field(description='How to mitigate this risk')
    owner: str | None = Field(default=None, description='Who should own this risk')


class RiskAssessment(BaseModel):
    risks: list[Risk] = Field(description='Identified risks')
    overall_risk_level: str = Field(description='Overall risk assessment')
    risk_recommendations: list[str] = Field(
        default_factory=list, description='Actions to reduce overall risk'
    )
