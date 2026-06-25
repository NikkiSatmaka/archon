import pytest
from pydantic_ai.models.test import TestModel

from archon.models import (
    ArchitectureReport,
    CandidateArchitectures,
    Clarifications,
    DesignDrivers,
    ImplementationRoadmap,
    ProjectScope,
    Recommendation,
    Requirements,
    RiskAssessment,
    TradeoffAnalysis,
)
from archon.pipeline.context import PipelineContext
from archon.pipeline.step1_requirements import requirements_agent
from archon.pipeline.step2_unknowns import clarifier_agent
from archon.pipeline.step3_design_drivers import design_driver_agent
from archon.pipeline.step4_candidates import candidate_agent
from archon.pipeline.step5_tradeoffs import tradeoff_agent
from archon.pipeline.step6_recommendation import recommendation_agent
from archon.pipeline.step7_risks import risk_agent
from archon.pipeline.step8_roadmap import roadmap_agent
from archon.pipeline.step9_deliverable import deliverable_agent


def _make_ctx() -> PipelineContext:
    return PipelineContext(
        project=ProjectScope(name='Test', description='A test project'),
    )


@pytest.mark.asyncio
async def test_requirements_agent_with_test_model():
    model = TestModel(
        call_tools=['web_search', 'lookup_service'],
        custom_output_args={
            'business_goals': ['Launch platform'],
            'functional_requirements': ['User authentication', 'Order management'],
            'non_functional_requirements': ['99.9% uptime', '<2s response time'],
            'expected_scale': '10K users',
            'assumptions': ['Assume AWS as provider'],
        },
    )
    result = await requirements_agent.run(
        'Build a food delivery app',
        deps=_make_ctx(),
        model=model,
    )
    assert isinstance(result.output, Requirements)
    assert 'Launch platform' in result.output.business_goals


@pytest.mark.asyncio
async def test_clarifier_agent_with_test_model():
    ctx = _make_ctx()
    ctx.requirements = Requirements(
        business_goals=['Launch'],
        functional_requirements=['Order tracking'],
        non_functional_requirements=['Fast'],
        expected_scale='Unknown',
    )

    model = TestModel(
        call_tools=[],
        custom_output_args={
            'questions': [],
            'assumptions': [],
        },
    )
    result = await clarifier_agent.run(
        ctx.requirements.model_dump_json(),
        deps=ctx,
        model=model,
    )
    assert isinstance(result.output, Clarifications)


@pytest.mark.asyncio
async def test_design_driver_agent_with_test_model():
    ctx = _make_ctx()
    ctx.requirements = Requirements(
        business_goals=['Launch'],
        functional_requirements=['Order tracking'],
        non_functional_requirements=['Fast'],
        expected_scale='10K users',
    )

    model = TestModel(
        call_tools=[],
        custom_output_args={
            'drivers': [
                {'name': 'lowest_latency', 'importance': 10, 'rationale': 'Real-time tracking'},
                {'name': 'highest_reliability', 'importance': 9, 'rationale': '99.9% uptime'},
                {'name': 'security', 'importance': 8, 'rationale': 'Customer data protection'},
            ],
        },
    )
    result = await design_driver_agent.run('test', deps=ctx, model=model)
    assert isinstance(result.output, DesignDrivers)


@pytest.mark.asyncio
async def test_candidate_agent_with_test_model():
    ctx = _make_ctx()
    ctx.requirements = Requirements(
        business_goals=['Launch'],
        functional_requirements=['Order tracking'],
        non_functional_requirements=['Fast'],
        expected_scale='10K users',
    )

    model = TestModel(
        call_tools=['lookup_service'],
        custom_output_args={
            'options': [
                {
                    'name': 'Serverless',
                    'description': 'Lambda + API Gateway',
                    'components': [],
                    'data_flow': 'API Gateway -> Lambda -> DynamoDB',
                    'deployment_model': 'Serverless',
                    'operational_model': 'Fully managed',
                    'estimated_monthly_cost': '$15K',
                },
                {
                    'name': 'Container',
                    'description': 'ECS Fargate',
                    'components': [],
                    'data_flow': 'ALB -> ECS -> RDS',
                    'deployment_model': 'Container',
                    'operational_model': 'Orchestrated',
                    'estimated_monthly_cost': '$20K',
                },
            ],
        },
    )
    result = await candidate_agent.run('test', deps=ctx, model=model)
    assert isinstance(result.output, CandidateArchitectures)


@pytest.mark.asyncio
async def test_tradeoff_agent_with_test_model():
    ctx = _make_ctx()

    model = TestModel(
        call_tools=[],
        custom_output_args={
            'comparisons': [],
            'summary': 'No comparison available',
        },
    )
    result = await tradeoff_agent.run('test', deps=ctx, model=model)
    assert isinstance(result.output, TradeoffAnalysis)


@pytest.mark.asyncio
async def test_recommendation_agent_with_test_model():
    ctx = _make_ctx()

    model = TestModel(
        call_tools=[],
        custom_output_args={
            'selected_option': 'Option A',
            'rationale': 'Best fit',
            'rejected_alternatives': ['Option B'],
            'key_assumptions': ['Growth is linear'],
        },
    )
    result = await recommendation_agent.run('test', deps=ctx, model=model)
    assert isinstance(result.output, Recommendation)


@pytest.mark.asyncio
async def test_risk_agent_with_test_model():
    ctx = _make_ctx()

    model = TestModel(
        call_tools=[],
        custom_output_args={
            'risks': [],
            'overall_risk_level': 'Low',
        },
    )
    result = await risk_agent.run('test', deps=ctx, model=model)
    assert isinstance(result.output, RiskAssessment)


@pytest.mark.asyncio
async def test_roadmap_agent_with_test_model():
    ctx = _make_ctx()

    model = TestModel(
        call_tools=[],
        custom_output_args={
            'phases': [],
            'total_estimated_timeline': '3 months',
        },
    )
    result = await roadmap_agent.run('test', deps=ctx, model=model)
    assert isinstance(result.output, ImplementationRoadmap)


@pytest.mark.asyncio
async def test_deliverable_agent_with_test_model():
    ctx = _make_ctx()

    model = TestModel(
        call_tools=[],
        custom_output_args={
            'executive_summary': 'Test',
            'architecture_overview': 'Overview',
            'diagram_description': 'Diagram',
            'major_components': [],
            'data_flow': 'Flow',
            'tradeoff_analysis': TradeoffAnalysis(comparisons=[], summary='').model_dump(),
            'recommendation': Recommendation(
                selected_option='A',
                rationale='Best',
                rejected_alternatives=[],
                key_assumptions=[],
            ).model_dump(),
            'risks': RiskAssessment(risks=[], overall_risk_level='Low').model_dump(),
            'roadmap': ImplementationRoadmap(phases=[], total_estimated_timeline='').model_dump(),
        },
    )
    result = await deliverable_agent.run('test', deps=ctx, model=model)
    assert isinstance(result.output, ArchitectureReport)
