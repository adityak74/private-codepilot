"""Engine"""

from private_codepilot.core.config import Config
from private_codepilot.core.llm_client import LLMClient
from private_codepilot.core.embeddings_client import EmbeddingsClient


class PrivateCodepilot:
    """Private Code pilot"""

    def __init__(self):
        """Initialize PrivateCodepilot"""
        self.app_config = Config().app_config
        self.embeddings_client = EmbeddingsClient()

    def setup(self):
        """Setup"""
        self.embeddings_client.generate_embeddings()

    def get_qa_chain(self):
        """Get QA chain"""
        ollama_client = LLMClient().ollama
        return self.embeddings_client.get_qa_chain_interface(
            llm_interface=ollama_client
        )

    def get_active_repo(self):
        """Get Active Repo"""
        return self.app_config.REPO_DIR


if __name__ == "__main__":
    private_codepilot = PrivateCodepilot()
    print(private_codepilot.app_config)
