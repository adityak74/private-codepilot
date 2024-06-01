"""LLM Client"""

from langchain_community.llms import Ollama
from private_codepilot.core.config import Config


class LLMClient:
    """LLM Client"""

    def __init__(self):
        config = Config()
        self.ollama = Ollama(
            base_url=config.app_config.OLLAMA_URL,
            model=config.app_config.OLLAMA_LLM_MODEL,
        )
