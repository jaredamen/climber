"""Base LLM provider interface."""

from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """Base class for LLM providers."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate response from the LLM."""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Get the model name being used."""
        pass
