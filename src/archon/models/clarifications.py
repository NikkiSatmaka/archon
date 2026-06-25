from pydantic import BaseModel, Field


class Question(BaseModel):
    id: str = Field(description='Unique identifier for this question')
    question: str = Field(description='The clarifying question')
    context: str = Field(description='What prompted this question')
    impact_if_unanswered: str = Field(description='Risk of proceeding without this information')


class Assumption(BaseModel):
    assumption: str = Field(description='The assumption being made')
    rationale: str = Field(description='Why this assumption is reasonable')
    impact_if_wrong: str = Field(description='Consequence if assumption is incorrect')


class Clarifications(BaseModel):
    questions: list[Question] = Field(description='Questions for the user')
    assumptions: list[Assumption] = Field(description='Assumptions made to proceed')
    ambiguity_risks: list[str] = Field(
        default_factory=list, description='Risks from ambiguous requirements'
    )
