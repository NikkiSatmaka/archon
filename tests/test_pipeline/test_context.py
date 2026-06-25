import pytest

from archon.config import LLMConfig
from archon.models import ProjectScope
from archon.pipeline.context import PipelineContext


def test_pipeline_context_defaults():
    project = ProjectScope(name='Test', description='Test')
    ctx = PipelineContext(project=project)
    assert ctx.requirements is None
    assert ctx.clarifications is None
    assert ctx.design_drivers is None
    assert ctx.report is None


def test_pipeline_context_with_requirements(sample_requirements):
    project = ProjectScope(name='Test', description='Test')
    ctx = PipelineContext(project=project, requirements=sample_requirements)
    assert ctx.requirements is not None
    assert len(ctx.requirements.functional_requirements) > 0


def test_pipeline_context_validation():
    project = ProjectScope(name='Test', description='Test')
    with pytest.raises(ValueError):
        PipelineContext(project=project, user_answers={'q1': 'answer'})


def test_pipeline_context_validation_with_clarifications(sample_clarifications):
    project = ProjectScope(name='Test', description='Test')
    ctx = PipelineContext(
        project=project,
        user_answers={'q1': '30 days'},
        clarifications=sample_clarifications,
    )
    assert ctx.user_answers == {'q1': '30 days'}


def test_llm_config_defaults():
    config = LLMConfig()
    assert config.base_url == 'https://api.openai.com/v1'
    assert config.model_name == 'gpt-4o'
