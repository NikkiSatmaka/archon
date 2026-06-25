import pydantic
import pytest

from archon.models import (
    ArchitectureReport,
    CandidateArchitectures,
    Clarifications,
    DesignDrivers,
    DriverScore,
    Phase,
    ProjectScope,
    Question,
    Requirements,
    Risk,
)
from archon.pipeline.context import PipelineContext


def test_project_scope_creation():
    project = ProjectScope(
        name='Test',
        description='A test project',
    )
    assert project.name == 'Test'
    assert project.preferred_provider is None


def test_requirements_defaults():
    reqs = Requirements(
        business_goals=['Goal'],
        functional_requirements=['Func'],
        non_functional_requirements=['NFR'],
        expected_scale='100 users',
    )
    assert reqs.security_requirements == []
    assert reqs.compliance_requirements == []
    assert reqs.existing_systems == []


def test_clarifications_with_questions():
    q = Question(
        id='q1',
        question='What data retention?',
        context='GDPR requirement',
        impact_if_unanswered='Compliance risk',
    )
    c = Clarifications(questions=[q], assumptions=[])
    assert len(c.questions) == 1
    assert c.questions[0].id == 'q1'


def test_design_drivers_validation():
    with pytest.raises(pydantic.ValidationError):
        DesignDrivers(drivers=[])


def test_candidate_architectures_min_options():
    with pytest.raises(pydantic.ValidationError):
        CandidateArchitectures(options=[])


def test_tradeoff_analysis_scoring():
    score = DriverScore(driver='cost', score=3, notes='Moderate')
    assert score.score >= 1 and score.score <= 5


def test_risk_severity():
    risk = Risk(
        category='technical',
        description='Cold starts',
        severity='High',
        likelihood='Medium',
        mitigation='Provisioned concurrency',
    )
    assert risk.severity == 'High'


def test_roadmap_phases():
    phase = Phase(
        name='MVP',
        description='Core features',
        tasks=['Setup', 'Build', 'Deploy'],
        estimated_effort='8 weeks',
    )
    assert len(phase.tasks) == 3


def test_full_report_creation(full_context: PipelineContext):
    report = ArchitectureReport(
        executive_summary='Summary',
        architecture_overview='Overview',
        diagram_description='Diagram',
        major_components=full_context.candidates.options[0].components,
        data_flow='Data flow',
        tradeoff_analysis=full_context.tradeoffs,
        recommendation=full_context.recommendation,
        risks=full_context.risks,
        roadmap=full_context.roadmap,
    )
    assert report.executive_summary == 'Summary'
    assert len(report.major_components) > 0


@pytest.mark.parametrize('field', ['executive_summary', 'architecture_overview', 'data_flow'])
def test_report_required_fields(field: str, full_context: PipelineContext):
    data = {
        'executive_summary': 'Summary',
        'architecture_overview': 'Overview',
        'diagram_description': 'Diagram',
        'major_components': full_context.candidates.options[0].components,
        'data_flow': 'Data flow',
        'tradeoff_analysis': full_context.tradeoffs,
        'recommendation': full_context.recommendation,
        'risks': full_context.risks,
        'roadmap': full_context.roadmap,
    }
    data[field] = ''
    with pytest.raises(pydantic.ValidationError):
        ArchitectureReport(**data)
