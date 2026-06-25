class PipelineError(Exception):
    """Base exception for pipeline errors."""


class StepExecutionError(PipelineError):
    """Agent failed to produce valid output."""


class CheckpointError(PipelineError):
    """Invalid resume after checkpoint."""
