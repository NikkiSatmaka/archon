import pytest

from archon.config import LLMConfig
from archon.models import ProjectScope
from archon.pipeline.context import PipelineContext
from archon.pipeline.orchestrator import Orchestrator


@pytest.mark.asyncio
async def test_orchestrator_initialization():
    config = LLMConfig()
    orchestrator = Orchestrator(config)
    assert orchestrator.config is config


@pytest.mark.asyncio
async def test_orchestrator_default_config():
    orchestrator = Orchestrator()
    assert orchestrator.config is not None
    assert orchestrator.config.base_url == 'https://api.openai.com/v1'


@pytest.mark.asyncio
async def test_context_summary_empty(sample_project: ProjectScope):
    from archon.pipeline.orchestrator import _context_summary

    ctx = PipelineContext(project=sample_project)
    result = _context_summary(ctx)
    assert result == ''


@pytest.mark.asyncio
async def test_context_summary_with_requirements(sample_project: ProjectScope, sample_requirements):
    from archon.pipeline.orchestrator import _context_summary

    ctx = PipelineContext(project=sample_project, requirements=sample_requirements)
    result = _context_summary(ctx)
    assert 'Requirements' in result
    assert 'Functional' in result or 'functional' in result


@pytest.mark.asyncio
async def test_resume_without_clarifications_raises_error(sample_project: ProjectScope):
    orchestrator = Orchestrator()
    ctx = PipelineContext(project=sample_project)
    with pytest.raises(Exception) as exc_info:
        await orchestrator.resume(ctx, {'q1': 'answer'})
    assert 'clarifications' in str(exc_info.value).lower()
