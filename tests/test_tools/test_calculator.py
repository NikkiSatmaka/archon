import pytest
from pydantic_ai import RunContext

from archon.models import ProjectScope
from archon.pipeline.context import PipelineContext
from archon.tools import calculate


@pytest.fixture
def ctx() -> RunContext[PipelineContext]:
    project = ProjectScope(name='Test', description='Test')
    return RunContext[PipelineContext](
        deps=PipelineContext(project=project),
        tool_name='test',
        retry=0,
        run_step=0,
        model='test',
        usage=[],
    )


@pytest.mark.asyncio
async def test_calculate_simple(ctx: RunContext[PipelineContext]):
    result = await calculate(ctx, '2 + 3')
    assert result == 5.0


@pytest.mark.asyncio
async def test_calculate_complex(ctx: RunContext[PipelineContext]):
    result = await calculate(ctx, '10 * 1000 / 720 * 2')
    assert result == pytest.approx(27.777, rel=1e-3)


@pytest.mark.asyncio
async def test_calculate_power(ctx: RunContext[PipelineContext]):
    result = await calculate(ctx, '2 ** 10')
    assert result == 1024.0


@pytest.mark.asyncio
async def test_calculate_negative(ctx: RunContext[PipelineContext]):
    result = await calculate(ctx, '-5 + 3')
    assert result == -2.0


@pytest.mark.asyncio
async def test_calculate_invalid_expression(ctx: RunContext[PipelineContext]):
    with pytest.raises((ValueError, SyntaxError)):
        await calculate(ctx, 'invalid expression')
