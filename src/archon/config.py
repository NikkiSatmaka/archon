import os

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider


class LLMConfig:
    def __init__(self) -> None:
        self.base_url: str = os.getenv('ARCHON_LLM_BASE_URL', 'https://api.openai.com/v1')
        self.api_key: str = os.getenv('ARCHON_LLM_API_KEY', '')
        self.model_name: str = os.getenv('ARCHON_LLM_MODEL', 'gpt-4o')

    def create_model(self) -> OpenAIChatModel:
        return OpenAIChatModel(
            self.model_name,
            provider=OpenAIProvider(
                base_url=self.base_url,
                api_key=self.api_key,
            ),
        )
