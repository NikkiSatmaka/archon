import pytest

from archon.models import Assumption, Clarifications, ProjectScope, Question, Requirements
from archon.models.architecture import ArchitectureOption, CandidateArchitectures, Component
from archon.models.design_drivers import DesignDrivers, Driver
from archon.models.recommendation import Recommendation
from archon.models.risks import Risk, RiskAssessment
from archon.models.roadmap import ImplementationRoadmap, Phase
from archon.models.tradeoffs import DriverScore, OptionComparison, TradeoffAnalysis
from archon.pipeline.context import PipelineContext


@pytest.fixture
def sample_project() -> ProjectScope:
    return ProjectScope(
        name='Food Delivery Platform',
        industry='Food & Beverage',
        description='A cloud-native food delivery platform serving 100K daily active users. '
        'Needs real-time order tracking, payment processing, and restaurant management.',
        preferred_provider='aws',
        team_capabilities=['Python', 'Docker', 'PostgreSQL'],
        budget_range='$20K-30K/month',
        timeline='6 months to MVP',
    )


@pytest.fixture
def sample_requirements() -> Requirements:
    return Requirements(
        business_goals=['Launch in 3 markets', '50K orders/day by month 6'],
        functional_requirements=[
            'Real-time order tracking',
            'Payment processing',
            'Restaurant dashboard',
        ],
        non_functional_requirements=['< 2s page load', '99.9% uptime', 'PCI DSS compliance'],
        expected_scale='100K DAU, 50K orders/day',
        availability_requirements='99.9%',
        security_requirements=['PCI DSS', 'Data encryption at rest and in transit'],
        compliance_requirements=['PCI DSS', 'GDPR', 'CCPA'],
        budget_constraints='$20K-30K/month cloud costs',
        team_capabilities=['Python', 'Docker', 'PostgreSQL'],
    )


@pytest.fixture
def sample_clarifications() -> Clarifications:
    return Clarifications(
        questions=[
            Question(
                id='q1',
                question='What is the expected data retention period?',
                context='Compliance requirements mention GDPR',
                impact_if_unanswered='May over-provision storage or violate data retention policies',
            ),
        ],
        assumptions=[
            Assumption(
                assumption='Average order value of $25',
                rationale='Industry average for food delivery',
                impact_if_wrong='Cost estimates may be off by 20-30%',
            ),
        ],
    )


@pytest.fixture
def sample_design_drivers() -> DesignDrivers:
    return DesignDrivers(
        drivers=[
            Driver(
                name='lowest_latency',
                importance=10,
                rationale='Real-time order tracking requirement',
            ),
            Driver(name='highest_reliability', importance=9, rationale='99.9% uptime SLA'),
            Driver(
                name='regulatory_compliance',
                importance=8,
                rationale='PCI DSS and GDPR requirements',
            ),
            Driver(
                name='lowest_cost', importance=6, rationale='Budget constrained at $20-30K/month'
            ),
        ],
    )


@pytest.fixture
def sample_candidates() -> CandidateArchitectures:
    return CandidateArchitectures(
        options=[
            ArchitectureOption(
                name='Serverless-first',
                description='Lambda + API Gateway + DynamoDB',
                components=[
                    Component(
                        name='API',
                        service='API Gateway',
                        provider='aws',
                        purpose='REST API',
                        configuration='Regional',
                    ),
                ],
                data_flow='API Gateway → Lambda → DynamoDB',
                deployment_model='Serverless',
                operational_model='Fully managed',
                estimated_monthly_cost='$15K-20K',
            ),
            ArchitectureOption(
                name='ECS-based',
                description='ECS Fargate + RDS PostgreSQL',
                components=[
                    Component(
                        name='API',
                        service='ECS Fargate',
                        provider='aws',
                        purpose='Container API',
                        configuration='2x task definitions',
                    ),
                ],
                data_flow='ALB → ECS → RDS',
                deployment_model='Container',
                operational_model='Container orchestration via ECS',
                estimated_monthly_cost='$20K-25K',
            ),
        ],
    )


@pytest.fixture
def sample_tradeoffs() -> TradeoffAnalysis:
    return TradeoffAnalysis(
        comparisons=[
            OptionComparison(
                option_name='Serverless-first',
                scores=[
                    DriverScore(
                        driver='lowest_latency', score=4, notes='Low latency for most operations'
                    )
                ],
                total_score=35,
                cost_assessment='Lower cost due to pay-per-use',
                complexity_assessment='Simple operational model',
                risk_assessment='Cold start risk',
            ),
            OptionComparison(
                option_name='ECS-based',
                scores=[
                    DriverScore(driver='lowest_latency', score=5, notes='Consistent low latency')
                ],
                total_score=32,
                cost_assessment='Higher base cost',
                complexity_assessment='More operational overhead',
                risk_assessment='Container management complexity',
            ),
        ],
        summary='Serverless-first wins on cost and simplicity; ECS wins on consistent performance.',
    )


@pytest.fixture
def sample_recommendation() -> Recommendation:
    return Recommendation(
        selected_option='Serverless-first',
        rationale='Best balance of cost, simplicity, and scalability for MVP phase',
        rejected_alternatives=['ECS-based: higher operational overhead for initial launch'],
        key_assumptions=['Order volume grows gradually', 'Cold start latency acceptable'],
    )


@pytest.fixture
def sample_risks() -> RiskAssessment:
    return RiskAssessment(
        risks=[
            Risk(
                category='technical',
                description='Lambda cold starts during peak hours',
                severity='Medium',
                likelihood='Medium',
                mitigation='Use provisioned concurrency for critical functions',
            ),
        ],
        overall_risk_level='Medium',
    )


@pytest.fixture
def sample_roadmap() -> ImplementationRoadmap:
    return ImplementationRoadmap(
        phases=[
            Phase(
                name='MVP',
                description='Core ordering flow',
                tasks=['Set up API Gateway', 'Implement order Lambda', 'Deploy DynamoDB tables'],
                estimated_effort='8 weeks',
            ),
        ],
        total_estimated_timeline='6 months',
    )


@pytest.fixture
def sample_context(
    sample_project: ProjectScope, sample_requirements: Requirements
) -> PipelineContext:
    return PipelineContext(project=sample_project, requirements=sample_requirements)


@pytest.fixture
def full_context(
    sample_project: ProjectScope,
    sample_candidates: CandidateArchitectures,
    sample_tradeoffs: TradeoffAnalysis,
    sample_recommendation: Recommendation,
    sample_risks: RiskAssessment,
    sample_roadmap: ImplementationRoadmap,
) -> PipelineContext:
    return PipelineContext(
        project=sample_project,
        requirements=Requirements(
            business_goals=['Launch in 3 markets'],
            functional_requirements=['Order tracking'],
            non_functional_requirements=['99.9% uptime'],
            expected_scale='100K DAU',
        ),
        clarifications=Clarifications(
            questions=[],
            assumptions=[
                Assumption(
                    assumption='Avg order $25',
                    rationale='Industry avg',
                    impact_if_wrong='Cost off by 20%',
                )
            ],
        ),
        design_drivers=DesignDrivers(
            drivers=[
                Driver(name='lowest_latency', importance=10, rationale='Real-time'),
                Driver(name='highest_reliability', importance=9, rationale='99.9% uptime'),
                Driver(name='security', importance=8, rationale='Customer data protection'),
            ],
        ),
        candidates=sample_candidates,
        tradeoffs=sample_tradeoffs,
        recommendation=sample_recommendation,
        risks=sample_risks,
        roadmap=sample_roadmap,
    )
