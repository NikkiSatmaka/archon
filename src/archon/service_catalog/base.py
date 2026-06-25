from typing import Literal

from pydantic import BaseModel, Field

ServiceCategory = Literal[
    'compute', 'storage', 'database', 'analytics', 'ai_ml', 'serverless', 'networking', 'security'
]
Provider = Literal['aws', 'gcp', 'azure']


class Service(BaseModel):
    name: str = Field(description='Service name')
    provider: Provider = Field(description='Cloud provider')
    category: ServiceCategory = Field(description='Service category')
    description: str = Field(description='What the service does')
    use_cases: list[str] = Field(description='Typical use cases')
    pricing_model: str = Field(description='How pricing works')
    limitations: list[str] = Field(default_factory=list, description='Known limitations')
    typical_latency: str = Field(default='', description='Performance characteristic')
    compliance: list[str] = Field(default_factory=list, description='Compliance certifications')
