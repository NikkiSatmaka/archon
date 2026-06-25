import logging

from pydantic_ai.models.openai import OpenAIChatModel

from archon.config import LLMConfig
from archon.exceptions import CheckpointError, StepExecutionError
from archon.models import (
    ArchitectureReport,
    ProjectScope,
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

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, llm_config: LLMConfig | None = None) -> None:
        self.config = llm_config or LLMConfig()

    def _model(self) -> OpenAIChatModel:
        return self.config.create_model()

    async def run_until_checkpoint(self, project: ProjectScope) -> PipelineContext:
        model = self._model()
        ctx = PipelineContext(project=project)

        logger.info('Step 1: Gathering requirements')
        try:
            result = await requirements_agent.run(
                project.description, deps=ctx, model=model,
            )
            ctx.requirements = result.output
        except Exception as e:
            raise StepExecutionError(f'Step 1 failed: {e}') from e

        logger.info('Step 2: Identifying unknowns')
        try:
            input_text = ctx.requirements.model_dump_json()
            result = await clarifier_agent.run(
                input_text, deps=ctx, model=model,
            )
            ctx.clarifications = result.output
        except Exception as e:
            raise StepExecutionError(f'Step 2 failed: {e}') from e

        return ctx

    async def resume(
        self, ctx: PipelineContext, user_answers: dict[str, str],
    ) -> ArchitectureReport:
        if ctx.clarifications is None:
            raise CheckpointError('Cannot resume without clarifications')

        ctx.user_answers = user_answers
        model = self._model()

        logger.info('Step 3: Determining design drivers')
        try:
            result = await design_driver_agent.run(
                _context_summary(ctx), deps=ctx, model=model,
            )
            ctx.design_drivers = result.output
        except Exception as e:
            raise StepExecutionError(f'Step 3 failed: {e}') from e

        logger.info('Step 4: Generating candidate architectures')
        try:
            result = await candidate_agent.run(
                _context_summary(ctx), deps=ctx, model=model,
            )
            ctx.candidates = result.output
        except Exception as e:
            raise StepExecutionError(f'Step 4 failed: {e}') from e

        logger.info('Step 5: Analyzing tradeoffs')
        try:
            result = await tradeoff_agent.run(
                _context_summary(ctx), deps=ctx, model=model,
            )
            ctx.tradeoffs = result.output
        except Exception as e:
            raise StepExecutionError(f'Step 5 failed: {e}') from e

        logger.info('Step 6: Selecting recommendation')
        try:
            result = await recommendation_agent.run(
                _context_summary(ctx), deps=ctx, model=model,
            )
            ctx.recommendation = result.output
        except Exception as e:
            raise StepExecutionError(f'Step 6 failed: {e}') from e

        logger.info('Step 7: Identifying risks')
        try:
            result = await risk_agent.run(
                _context_summary(ctx), deps=ctx, model=model,
            )
            ctx.risks = result.output
        except Exception as e:
            raise StepExecutionError(f'Step 7 failed: {e}') from e

        logger.info('Step 8: Creating implementation roadmap')
        try:
            result = await roadmap_agent.run(
                _context_summary(ctx), deps=ctx, model=model,
            )
            ctx.roadmap = result.output
        except Exception as e:
            raise StepExecutionError(f'Step 8 failed: {e}') from e

        logger.info('Step 9: Producing final deliverable')
        try:
            result = await deliverable_agent.run(
                _context_summary(ctx), deps=ctx, model=model,
            )
            ctx.report = result.output
        except Exception as e:
            raise StepExecutionError(f'Step 9 failed: {e}') from e

        return ctx.report


def _context_summary(ctx: PipelineContext) -> str:
    parts: list[str] = []
    if ctx.requirements:
        parts.append(f'Requirements: {ctx.requirements.model_dump_json()}')
    if ctx.clarifications:
        parts.append(f'Clarifications: {ctx.clarifications.model_dump_json()}')
    if ctx.user_answers:
        parts.append(f'User answers: {ctx.user_answers}')
    if ctx.design_drivers:
        parts.append(f'Design drivers: {ctx.design_drivers.model_dump_json()}')
    if ctx.candidates:
        parts.append(f'Candidates: {ctx.candidates.model_dump_json()}')
    if ctx.tradeoffs:
        parts.append(f'Tradeoffs: {ctx.tradeoffs.model_dump_json()}')
    if ctx.recommendation:
        parts.append(f'Recommendation: {ctx.recommendation.model_dump_json()}')
    if ctx.risks:
        parts.append(f'Risks: {ctx.risks.model_dump_json()}')
    if ctx.roadmap:
        parts.append(f'Roadmap: {ctx.roadmap.model_dump_json()}')
    return '\n\n'.join(parts)
