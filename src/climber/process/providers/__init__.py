"""LLM provider implementations."""

from .base import BaseLLMProvider
from .openai import OpenAIProvider
from .anthropic import AnthropicProvider
from ...config import Config


def create_provider(config: Config) -> BaseLLMProvider:
    """Create LLM provider based on configuration."""
    if config.provider == "openai":
        return OpenAIProvider(config.api_key)
    elif config.provider == "anthropic":
        return AnthropicProvider(config.api_key)
    else:
        raise ValueError(f"Unsupported provider: {config.provider}")


__all__ = ["BaseLLMProvider", "OpenAIProvider", "AnthropicProvider", "create_provider"]