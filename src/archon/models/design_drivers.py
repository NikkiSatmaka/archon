from typing import Literal

from pydantic import BaseModel, Field

DriverName = Literal[
    'lowest_cost',
    'highest_reliability',
    'lowest_latency',
    'fastest_delivery',
    'regulatory_compliance',
    'global_scale',
    'simplicity',
    'operational_efficiency',
    'vendor_lock_in_avoidance',
    'security',
]


class Driver(BaseModel):
    name: DriverName = Field(description='The design driver')
    importance: int = Field(ge=1, le=10, description='Importance score (1=low, 10=critical)')
    rationale: str = Field(description='Why this driver matters for this project')


class DesignDrivers(BaseModel):
    drivers: list[Driver] = Field(description='Ranked design drivers', min_length=3)
