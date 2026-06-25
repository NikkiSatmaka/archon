from pydantic import BaseModel, Field


class Recommendation(BaseModel):
    selected_option: str = Field(description='Name of the recommended architecture')
    rationale: str = Field(description='Why this option was selected')
    rejected_alternatives: list[str] = Field(description='Why other options were not chosen')
    key_assumptions: list[str] = Field(
        description='Assumptions that this recommendation depends on'
    )
    sensitivity: str | None = Field(
        default=None, description='How the recommendation would change if key assumptions shift'
    )
