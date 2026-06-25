from typing import Literal

from pydantic import BaseModel, Field

Score = Literal[1, 2, 3, 4, 5]


class DriverScore(BaseModel):
    driver: str = Field(description='Design driver name')
    score: Score = Field(description='How well this option satisfies this driver')
    notes: str = Field(description='Justification for the score')


class OptionComparison(BaseModel):
    option_name: str = Field(description='Architecture option name')
    scores: list[DriverScore] = Field(description='Scores across all design drivers')
    total_score: int = Field(description='Sum of all driver scores')
    cost_assessment: str = Field(description='Cost evaluation')
    complexity_assessment: str = Field(description='Complexity evaluation')
    risk_assessment: str = Field(description='Risk evaluation')


class TradeoffAnalysis(BaseModel):
    comparisons: list[OptionComparison] = Field(description='Comparison of all options')
    summary: str = Field(description='Overall tradeoff summary')
