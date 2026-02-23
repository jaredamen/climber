"""Pytest configuration and fixtures."""

import pytest
from unittest.mock import Mock
from climber.config import Config
from climber.ingest.base import ContentItem


@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    config = Mock(spec=Config)
    config.api_key = "test-api-key"
    config.provider = "openai"
    return config


@pytest.fixture
def sample_content():
    """Sample content item for testing."""
    return ContentItem(
        text="This is sample content for testing. It contains multiple sentences. Some are longer than others. This helps test chunking and processing.",
        title="Test Document",
        source="test://example.com",
        content_type="test"
    )


@pytest.fixture
def mock_llm_response():
    """Mock LLM response."""
    return "This is a mock response from the LLM provider."